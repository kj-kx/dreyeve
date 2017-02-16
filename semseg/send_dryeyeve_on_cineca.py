import os
import paramiko
from glob import glob
import os
import progressbar
from tqdm import tqdm
from time import sleep
import argparse


if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()

    assert args.host is not None, 'Please provide a correct host'
    assert args.user is not None, 'Please provide a correct username'
    assert args.password is not None, 'Please provide a correct password'

    # set up client
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(args.host, username=args.user, password=args.password)
    sftp = ssh.open_sftp()

    # send sequences
    for i in range(1, 74+1):
        print 'Sending sequence {}...'.format(i)

        local_path = 'Z:/DATA/{:02d}/frames/*.jpg'.format(i)
        remote_path = '/gpfs/work/IscrC_DeepVD/dabati/dreyeve_semantic_seg/data/{:02d}/frames/'.format(i)

        img_list = glob(local_path)

        for im in tqdm(img_list):
            filename = os.path.basename(im)
            sftp.put(im, remote_path+filename)

    sftp.close()
    ssh.close()