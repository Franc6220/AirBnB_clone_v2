#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric.api import env, put, run
import os

# Define the hosts
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your server IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = '~/.ssh/id_rsa'  # Replace with your SSH key path if necessary

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

