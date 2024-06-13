#!/usr/bin/python3
"""do_clean module"""
import os
from fabric import run, local, env

env.hosts = ['18.207.112.206', '54.89.195.83']
env.user = 'ubuntu'

def clean_foreign():
    """deletes out-of-date archives"""
def clean_local(number=0):
    """deletes out-of-date archives"""
    if not os.path.exists("./versions"):
        return False
    else:

        files = os.listdir("./versions")
        dates = [int(file[11: -4]) for file in files]
        recent = dates[0]

        for date in dates:
            if date > recent:
                recent = date

        recent2 = dates[0]
        for date in dates:
            if date > recent2 and date != recent:
                recent2 = date

    recent = "web_static_" + str(recent) + ".tgz"
    recent2 = "web_static_" + str(recent2) + ".tgz"

    for file in files:
        file_path = f"./versions/{file}"
        if number == 0 or number == 1:
            if file != recent:
                os.remove(file_path)
        else:
            if file != recent or file != recent2:
                os.remove(file_path)

do_clean()
