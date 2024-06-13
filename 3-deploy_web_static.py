#!/usr/bin/python3
"""
 creates and distributes an archive to your web servers
"""
from fabric.operations import local, run, env
from datetime import datetime
import os
from datetime import datetime
from fabric.api import run, put, env

env.hosts = ['18.207.112.206', '54.89.195.83']
env.user = 'ubuntu'


dt = datetime.now()
dt = datetime.strftime(dt, "%Y%m%d%H%M%S")
archive = "versions/web_static_" + dt + ".tgz"


def do_pack():
    """packs directory files to .tgz"""
    try:
        if not os.path.exists("./versions"):
            os.makedirs("./versions")

        local("tar -cvzf {} web_static".format(archive))
        return archive
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False

    try:

        put(archive_path, "/tmp/")

        archive_name = os.path.basename(archive_path)
        unpack = archive_path.split("/")[-1]
        folder = ("/data/web_static/releases/" + unpack.split(".")[0])

        pre_a = archive_name[:-4]

        re = "/data/web_static/releases"
        tar = "sudo tar -xzf /tmp"
        cu = "/data/web_static/current"

        run("sudo mkdir -p {}/{}/".format(re, pre_a))
        run("{}/{} -C {}/{}".format(tar, archive_name, re, pre_a))
        run("sudo rm /tmp/{:s}".format(archive_name))
        run("sudo mv {}/{}/web_static/* {}/{}/".format(re, pre_a, re, pre_a))
        run("sudo rm -rf {}/{}/web_static".format(re, pre_a))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}/{}/ {}".format(re, pre_a, cu))

        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """creates and distributes an archive to your web server"""
    try:
        archive_path = do_pack()
        status = do_deploy(archive_path)
        return status
    except:
        return False
