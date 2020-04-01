import os
import sys
import time as tm
from threading import Thread

import paramiko

from db_util import *
from file_utils import *


def send_files_to_client(file_names, username, ftp_client):
    for file in file_names:
        folder = "/home/{}/".format(username)
        dst = '{}/{}'.format(folder, file)
        ftp_client.put(file, dst)
        print("Sent {} to client".format(file))


def connect(values, count=30):
    hostname = values['hostname']
    username = values['username']
    password = values['password']
    arguments = values['arguments']
    pcap_filename = '_'.join((username, hostname.replace('.', '_'), arguments)) + '.pcap'
    values['pcap_filename'] = pcap_filename
    values['count'] = count
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Connection to Server IP address: ' + hostname)
    try:
        ssh_client.connect(hostname=hostname, username=username, password=password)
    except paramiko.ssh_exception:
        sys.exit("Connection Issue, check 1. is the ip ping, 2. check the username and passwords")

    ftp_client = ssh_client.open_sftp()
    dump_json_to_file(values, "properties.json")
    file_names = ['agent.py', 'properties.json']
    send_files_to_client(file_names, username, ftp_client)

    home_dir = "/home/{}/".format(username)
    values['status'] = 'Generating PCAP'
    update_status(values)
    ssh_client.exec_command("sudo -S <<< {} python3 {}agent.py".format(password, home_dir, pcap_filename, password))
    Thread(target=listen, args=(ssh_client, ftp_client, home_dir, values)).start()


def listen(ssh_client, ftp_client, home_dir, values):
    time_elapsed = 0
    while True:
        tm.sleep(5)
        time_elapsed += 1
        password = values['password']
        stdin, stdout, stderr = ssh_client.exec_command(
            "sudo -S <<< {} ls {}properties.json".format(password, home_dir))
        output = stdout.readlines()
        if len(output) == 0 or time_elapsed > 6:
            pcap_filename = values['pcap_filename']
            src = home_dir + pcap_filename
            dst = "C:\\Users\\nakoushi\\Desktop\\TcpOutputs\\{}".format(pcap_filename)
            ftp_client.get(src, dst)
            print("Got Pcap file into local host")
            if len(output) == 0:
                values['status'] = 'Get PCAP : successful'
                merge_pcap()
            else:
                values['status'] = 'Get PCAP : 30 secs timeout'
            update_status(values)
            ftp_client.close()
            ssh_client.close()
            break


def try_connect(values):
    hostname = values['hostname']
    username = values['username']
    password = values['password']
    values['status'] = 'Connected'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=hostname, username=username, password=password)
    except Exception:
        values['status'] = 'Connection failed!'
    finally:
        ssh_client.close()
        update_status(values)
    if values['status'] == 'Connected':
        Thread(target=connect, args=(values,)).start()


def server_connection(data):
    try:
        for rowid, values in data.items():
            Thread(target=try_connect, args=(values,)).start()
    except Exception as e:
        print("Exception occurred: " + e.args[0])


def merge_pcap():
    wire_shark_dir = "C:\\Program Files\\Wireshark"
    src = "C:\\Users\\nakoushi\\Desktop\\TcpOutputs\\"
    dst = "C:\\Users\\nakoushi\\Desktop\\TcpOutput\\merged.pcap"
    src_pcap_s = [src + '\\' + _ for _ in os.listdir(src) if _.endswith('.pcap')]
    pcap_files = ' '.join(src_pcap_s)
    cwd = os.getcwd()
    os.chdir(wire_shark_dir)
    os.system(f"mergecap -w {dst} {pcap_files}")
    os.chdir(cwd)
