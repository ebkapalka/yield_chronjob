from paramiko.sftp_client import SFTPClient
from datetime import datetime
import paramiko
import os


def create_sftp_client(hostname: str, port: int, username: str,
                       password: str) -> SFTPClient:
    """
    Create an SFTP client
    :param hostname: hostname of the server
    :param port: port number
    :param username: username
    :param password: password
    :return: SFTPClient object
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,
                       port=port,
                       username=username,
                       password=password)
    return ssh_client.open_sftp()


def get_newest_yield(sftp_client: SFTPClient, remote_directory: str) -> str:
    """
    List files in the remote directory
    :param sftp_client: SFTPClient object
    :param remote_directory: directory to list files from
    :return: list of files in the directory
    """
    try:
        files = sftp_client.listdir(remote_directory)
        yield_files = [f for f in files if '_Yield_' in f]
        yield_files_with_dates = [(f, datetime.strptime(f.split('_Yield_')[1], '%Y%m%d.csv')) for f in yield_files]
        yield_files_with_dates.sort(key=lambda x: x[1], reverse=True)
        return yield_files_with_dates[0][0] if yield_files_with_dates else ""
    except Exception as e:
        print(f"Failed to list files in {remote_directory}: {e}")
        return ''


def download_file(sftp_client: SFTPClient, remote_directory: str,
                  remote_filename: str, local_directory: str):
    """
    Download the newest yield file from the remote directory to the local directory,
    if it doesn't already exist locally.
    :param sftp_client: SFTPClient object
    :param remote_directory: remote directory to download files from
    :param remote_filename: remote filename to download
    :param local_directory: local directory to download files to
    :return:
    """
    remote_filepath = os.path.join(remote_directory, remote_filename)
    local_filepath = os.path.join(local_directory, remote_filename)
    if not os.path.exists(local_filepath):
        try:
            sftp_client.get(remote_filepath, local_filepath)
            print(f"Downloaded {remote_filename} to {local_filepath}")
        except Exception as e:
            print(f"Failed to download {remote_filename}: {e}")
    else:
        print(f"File {remote_filename} already exists at "
              f"{local_filepath}. Skipping download.")
