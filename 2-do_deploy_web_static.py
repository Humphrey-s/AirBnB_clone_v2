#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import run, put, env
import os

env.hosts = ['18.207.112.206','54.89.195.83']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers"""

    if not os.path.exists(archive_path):
        return False

    try:

        put(archive_path, "/tmp/")

        archive_name = os.path.basename(archive_path)

        pre_a = archive_name[:-4]

        re = "/data/web_static/releases"
        tar = "sudo tar -xzf /tmp"
        cu = "/data/web_static/current"

        run("sudo mkdir -p {}/{}/".format(re, pre_a))
        run("{}/{} -C {}/{}".format(tar, archive_name, re, pre_a))
        run("sudo mv {}/{}/web_static/* {}/{}/".format(re, pre_a, re, pre_a))
        run("sudo rm /tmp/{}".format(archive_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}/{}/ {}".format(re, pre_a, cu))

        return True
    except Exception as e:
        print(e)
        return False
