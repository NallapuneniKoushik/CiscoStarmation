import json
import os


def load_json_from_file(file_name):
    touch_file(file_name)
    with open(file_name) as readfile:
        content = readfile.read()
    if content == '':
        content = str(dict())
    content = json.loads(content)
    return content


def touch_file(file_name):
    try:
        with open(file_name):
            pass
    except FileNotFoundError:
        try:
            with open(file_name, 'w'):
                pass
        except IOError as ioe:
            print(ioe)
            print('Unable to create file {}'.format(file_name))
    except IOError as ioe:
        print(ioe)
        print('Unable to read file {}'.format(file_name))


def create_p_cap():
    properties = load_json_from_file("properties.json")
    arguments = properties['arguments']

    if arguments == 'httpv2':
        arguments = "port 80"
    elif arguments == 'ssh':
        arguments = "port 22"

    command = " echo '{}' | sudo -S tcpdump -n {} -w '{}' -v -c{} ".format(properties['password'],
                                                                           arguments,
                                                                           properties['pcap_filename'],
                                                                           properties['count'])
    os.system(command)
    os.remove("properties.json")
    os.remove("agent.py")


create_p_cap()
