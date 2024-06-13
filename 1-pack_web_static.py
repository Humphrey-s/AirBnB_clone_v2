#!/usr/bin/python3
"""
 Fabric script that generates a .tgz archive
"""
from fabric.operations import local
from datetime import datetime
import os

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
