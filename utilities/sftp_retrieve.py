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


def download_file_object(sftp_client: SFTPClient, remote_directory: str,
                         remote_filename: str) -> bytes | None:
    """
    Download the newest yield file from the remote directory to the local directory,
    if it doesn't already exist locally.
    :param sftp_client: SFTPClient object
    :param remote_directory: remote directory to download files from
    :param remote_filename: remote filename to download
    :return: bytes of the file content
    """
    remote_filepath = os.path.join(remote_directory, remote_filename)
    try:
        with sftp_client.open(remote_filepath, "rb") as remote_file:
            file_content = remote_file.read()
            print(f"Downloaded {remote_filename} successfully.")
            return file_content
    except Exception as e:
        print(f"Failed to download {remote_filename}: {e}")
