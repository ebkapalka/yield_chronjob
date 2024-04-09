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


def get_newest_file_name(sftp_client: SFTPClient, remote_directory: str) -> str:
    """
    List files in the remote directory
    :param sftp_client: SFTPClient object
    :param remote_directory: directory to list files from
    :return: list of files in the directory
    """
    try:
        files = sftp_client.listdir(remote_directory)
        yield_files = [f for f in files if '_Yield_' in f]
        yield_files_with_dates = [(f, datetime.strptime(
            f.split('_Yield_')[1], '%Y%m%d.csv')) for f in yield_files]
        yield_files_with_dates.sort(key=lambda x: x[1], reverse=True)
        return yield_files_with_dates[0][0] if yield_files_with_dates else ""
    except Exception as e:
        print(f"Failed to list files in {remote_directory}: {e}")
        return ''


def download_file_object(sftp_client: SFTPClient, remote_directory: str, remote_filename: str,
                         chunk_size=65536, use_chunks=False) -> bytes | None:
    """
    Download the file from the remote directory and return its content as bytes.
    This version reads the file in chunks and prints progress.
    :param sftp_client: SFTPClient object
    :param remote_directory: remote directory to download files from
    :param remote_filename: remote filename to download
    :param chunk_size: size of the chunk to read in bytes
    :param use_chunks: manual override to force chunk download
    :return: bytes of the file content
    """
    remote_filepath = os.path.join(remote_directory, remote_filename)
    try:
        with sftp_client.open(remote_filepath, "rb") as remote_file:
            file_size = sftp_client.stat(remote_filepath).st_size
            print(f"File size is {file_size} bytes ({file_size / 1_000_000:.2f} MB)")
            if file_size < 5_000_000 and not use_chunks:
                print(f"Downloading {remote_filename} in one go...")
                file_content = remote_file.read()
            else:
                print(f"Downloading {remote_filename} in chunks...")
                file_content = bytearray()
                while True:
                    chunk = remote_file.read(chunk_size)
                    if not chunk:
                        break
                    file_content.extend(chunk)
            return bytes(file_content)
    except Exception as e:
        print(f"Failed to download {remote_filename}: {e}")
        return None
