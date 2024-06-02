#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from fabric.api import env, local, put, run
import os
from datetime import datetime

# Define the hosts
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your server IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = '~/.ssh/id_rsa'  # Replace with your SSH key path if necessary

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    Returns:
        str: The path of the created archive, or None if the archive was not created.
    """
    try:
        if not os.path.exists('versions'):
            os.makedirs('versions')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(timestamp)
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        print("Error during packing:", e)
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    
    Args:
        archive_path (str): The path to the archive to be deployed.
        
    Returns:
        bool: True if all operations were successful, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the filename and the folder name from the archive_path
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/<folder_name> on the server
        run('mkdir -p /data/web_static/releases/{}'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(file_name, folder_name))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(file_name))

        # Move the contents out of the uncompressed folder
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(folder_name))

        return True
    except Exception as e:
        print("Error during deployment:", e)
        return False

def deploy():
    """
    Creates and distributes an archive to web servers.
    
    Returns:
        bool: True if all operations were successful, otherwise False.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

