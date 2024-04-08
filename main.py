from utilities.sftp_retrieve import (create_sftp_client, get_newest_yield,
                                     download_file)
from utilities.credentials import retrieve_credentials

import yaml


if __name__ == '__main__':
    remote_directory = "/users/ekapalka/jobsub/Tapeload/"
    local_directory = "C:\\Users\\n18p538\\Documents"
    service = "CopyYieldToKnox"
    creds = {
        "hostname": "jobsub-prod.msu.montana.edu",
        "port": 22,
        "username": "ekapalka",
        "password": None,
    }
    # if need-be: delete_credentials(service, creds["username"])
    _, creds["password"] = retrieve_credentials(
        service, creds["username"])
    sftp = create_sftp_client(**creds)
    newest_file = get_newest_yield(sftp, remote_directory)
    download_file(sftp, remote_directory,
                  newest_file, local_directory)
    sftp.close()
