#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Create the versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create the archive name with the current date and time
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(date_time)

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_name))

        # Return the archive path if successfully created
        if os.path.exists(archive_name):
            return archive_name
        else:
            return None
    except Exception as e:
        return None

