import threading
from datetime import *
from pathlib import Path
from threading import Thread

import paramiko

from db_util import *


def connect(values):
    hostname = values['hostname']
    username = values['username']
    password = values['password']
    arguments =str( values['arguments']).lower()

    today_date = date.today().strftime('%d%m%y')
    time_now = datetime.now().strftime('%H%M%S')
    id = threading.get_ident()
    pcap_filename = '_'.join((username.replace('-', '_'), hostname.replace('.', '_'), today_date, time_now))
    pcap_filename += '_' + str(id) + '.pcap'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Connection to Server IP address: ' + hostname)

    try:
        ssh_client.connect(hostname=hostname, username=username, password=password)
    except paramiko.ssh_exception:
        print("Connection Issue, check 1. is the ip ping, 2. check the username and passwords")

    print('Creating PCAP file.....' + pcap_filename)
    # if arguments=='httpv2':
    #     stdin, stdout, stderr = ssh_client.exec_command("sudo -S <<< \"{}\" tcpdump port 80 -w {} -v -c30".format(password, pcap_filename)) #Verified(Tcp&ssh are coming)
    #
    # elif arguments=='icmp':
    #     stdin, stdout, stderr = ssh_client.exec_command("sudo -S <<< \"{}\" tcpdump -n icmp -w {} -v -c30".format(password, pcap_filename)) #Verified(Tcp&ssh are coming)
    #
    # elif arguments=='tcp':
    #     stdin, stdout, stderr = ssh_client.exec_command("sudo -S <<< \"{}\" tcpdump tcp -w {} -v -c30".format(password, pcap_filename)) #Verified(Tcp&ssh are coming)
    #
    # elif arguments=='ssh':
    #     stdin, stdout, stderr = ssh_client.exec_command("sudo -S <<< \"{}\" tcpdump port 22 -w {} -v -c30".format(password, pcap_filename))  #Verified(Tcp&ssh are coming)

    stdin, stdout, stderr = ssh_client.exec_command("sudo -S <<< \"{}\" tcpdump -n icmp -w {} -v -c30".format(password, pcap_filename))
    output = stdout.read().decode("utf-8")
    print(output)
    print("Creation of PCAP file: {} is done".format(pcap_filename))

    ftp_client = ssh_client.open_sftp()
    src = f'/home/cx-lisa/{pcap_filename}'
    folder = Path(r"C:/Users/nakoushi/Desktop/TcpOutputFiles/")
    namepath = f'{pcap_filename}.pcap'
    dst = folder / namepath
    ftp_client.get(src, dst)
    print("Got Pcap file into local host")
    ftp_client.close()
    ssh_client.close()


def server_connection():
    # data = load_json_from_file('pcapdb.json')
    data = db_util()
    threads = []
    try:
        for hostname_username, values in data.items():
            t = Thread(target=connect, args=(values,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except Exception as e:
        print("Exception occurred: " + e.args[0])


    print("Exiting main Program!!!")


if __name__ == "__main__":
    server_connection()
