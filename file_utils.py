import json


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


def clear_file(file_name):
    try:
        with open(file_name, 'w'):
            pass
    except IOError as ioe:
        print(ioe)
        print('Unable to create file {}'.format(file_name))


def read_lines_strip_return(file_name, split=None, index=None, server_type=None):
    try:
        with open(file_name) as readfile:
            lines = readfile.readlines()
            res = list()
            for line in lines:
                line = line.strip()
                if line != '':
                    if split is not None:
                        line = line.split(split)
                        if server_type is not None:
                            if index is None:
                                line.append(server_type)
                                res.append(line)
                            else:
                                res.append(line[index] + ' ' + server_type)
                        else:
                            if index is None:
                                res.append(line)
                            else:
                                res.append(line[index])
                    else:
                        if server_type is not None:
                            res.append(line + ' ' + server_type)
                        else:
                            res.append(line)
        return res
    except FileNotFoundError:
        return "FileNotFoundError: {0}".format(file_name)
    except IOError as ioe:
        print(ioe)
        print('Unable to read file {}'.format(file_name))


def read_file(file_name):
    try:
        with open(file_name) as readfile:
            return readfile.read().strip()
    except FileNotFoundError:
        return "FileNotFoundError: {0}".format(file_name)
    except IOError as ioe:
        print(ioe)
        print('Unable to read file {}'.format(file_name))


def dump_json_to_file(data, file_name):
    touch_file(file_name)
    with open(file_name, 'w') as write_file:
        write_file.write(json.dumps(data, indent=4))
        write_file.write('\n')


def load_json_from_file(file_name):
    touch_file(file_name)
    with open(file_name) as readfile:
        content = readfile.read()
    if content == '':
        content = str(dict())
    content = json.loads(content)
    return content


def append_line_to_file(file_name, content):
    touch_file(file_name)
    with open(file_name, 'a') as append_file:
        append_file.write(content + '\n')


def append_line_to_file_if_doesnt_exist(file_name, content):
    touch_file(file_name)
    lines = read_lines_strip_return(file_name)
    if content not in lines:
        with open(file_name, 'a') as append_file:
            append_file.write(content + '\n')


def check_file_exists(file_name):
    try:
        with open(file_name) as readfile:
            pass
        return True
    except FileNotFoundError as fnfe:
        return False
    except IOError as ioe:
        print(ioe)
        print('Unable to read file {}'.format(file_name))
        return False
