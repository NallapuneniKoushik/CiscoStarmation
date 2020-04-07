import csv
import json
from io import StringIO

from flask import request, render_template, Flask
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response

from database import read_data, read_specific_data

UPLOAD_FOLDER = 'uploads/'
from test_new import app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

l1 = []
l2 = []
s = []


def perform(key, num, filename):
    data = {}
    dct = []
    mdct = []
    a = []
    l = []
    l3 = []
    f = []
    op = []
    x = []
    y = []
    t = []
    o = {}
    fin = []
    x = []
    y = []
    with open(filename) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            data = rows['Message Contents']
            a = data
            text = '[{'
            recursive_key = a
            lst = recursive_key.split('\n')
            flag = False
            bracketcount = 1
            quoteopenflag = False
            for ind in range(len(lst) - 1):
                if flag:
                    flag = False
                    continue
                thisline = lst[ind]
                nextline = lst[ind + 1]
                # print(nextline)
                brpt1 = len(thisline) - len(thisline.lstrip())
                brpt2 = len(nextline) - len(nextline.lstrip())
                spcount1 = thisline[:brpt1].count(' ')
                spcount2 = nextline[:brpt2].count(' ')
                if quoteopenflag:
                    text += thisline.lstrip()
                    if thisline.count("'") % 2 == 1:
                        quoteopenflag = False
                        text += '},\n'
                        bracketcount -= 1
                    continue

                if spcount1 < spcount2:
                    if thisline.endswith(':'):
                        text += '"' + thisline.lstrip() + ' {\n'
                        bracketcount += 1
                    else:
                        if thisline.count("'") % 2 == 0:
                            text += '"' + thisline.lstrip() + nextline.lstrip() + '},\n'
                            bracketcount -= 1
                            flag = True
                        else:
                            quoteopenflag = True
                            text += '"' + thisline.lstrip()
                elif spcount1 == spcount2:
                    text += '"' + thisline.lstrip() + ',\n'
                elif spcount1 > spcount2:
                    text += '"' + thisline.lstrip() + ' }' * int((spcount1 - spcount2) / 4) + ',\n'
                    bracketcount -= int((spcount1 - spcount2) / 4)

                if ind == len(lst) - 2:
                    text += '"' + thisline.lstrip() + '}' * bracketcount + "]"
            text = text.replace("'", '"')
            # print(text)

            newtext = ''
            new_list = text.split('\n')
            for i in new_list:
                if ':' in i:
                    breakpoint = i.index(':')
                    value = i[breakpoint:]

                    if value.count('"') < 2 and not value.endswith('{'):
                        if value.endswith('},'):
                            value = ':"' + value[1:-2].strip() + '"},'
                        else:
                            value = ':"' + value[1:-1].strip() + '",'
                    newtext += i[:breakpoint] + '"' + value + '\n'
                else:
                    newtext += i
            # print(newtext)
            dct = json.loads(newtext)

            def form(key, num):
                global l1
                global l2
                global f1

                for l in dct:

                    if key in l.keys():
                        if (l[key]):
                            f = l[key]
                            if num == f:

                                s.append(rows)
                                return s
                            else:
                                for i in dct:
                                    if "International_Mobile_Subscriber_Identity_(IMSI)" in i:
                                        if num == i["International_Mobile_Subscriber_Identity_(IMSI)"]["imsi"]:
                                            if f:
                                                l2 = f
                                for i in dct:
                                    if f:
                                        l1 = f
                                if l1 == l2 and f1:
                                    s.append(rows)
                                    return s

                    else:
                        key = key.split(",")
                        if key[0] and key[1] in l.keys():

                            if (l[key[0]]) and (l[key[1]]):
                                f = l[key[0]]
                                f1 = l[key[1]]

                                if num == f:
                                    s.append(rows)
                                    return s
                                else:
                                    for i in dct:
                                        if "International_Mobile_Subscriber_Identity_(IMSI)" in i:
                                            if num == i["International_Mobile_Subscriber_Identity_(IMSI)"]["imsi"]:
                                                if f:
                                                    l2 = f
                                    for i in dct:
                                        if f:
                                            l1 = f
                                    if l1 == l2 and f1:
                                        s.append(rows)
                                        return s



                        else:
                            if key[0] in l.keys():
                                if type(l[key[0]][key[1]]) is dict:
                                    if (l[key[0]][key[1]][key[2]]):
                                        f = l[key[0]][key[1]][key[2]]
                                        if num == f:
                                            s.append(rows)
                                            return s
                                        else:
                                            for i in dct:
                                                if "International_Mobile_Subscriber_Identity_(IMSI)" in i:
                                                    if num == i["International_Mobile_Subscriber_Identity_(IMSI)"][
                                                        "imsi"]:
                                                        if f:
                                                            l2 = f
                                            for i in dct:
                                                if f:
                                                    l1 = f
                                            if l1 == l2 and f1:
                                                s.append(rows)
                                                return s


                                else:
                                    if (l[key[0]][key[1]]):
                                        f = l[key[0]][key[1]]
                                        if num == f:

                                            s.append(rows)
                                            return s

                                        else:
                                            for i in dct:
                                                if "International_Mobile_Subscriber_Identity_(IMSI)" in i:
                                                    if num == i["International_Mobile_Subscriber_Identity_(IMSI)"][
                                                        "imsi"]:
                                                        if f:
                                                            l2 = f
                                            for i in dct:
                                                if f:
                                                    l1 = f
                                            if l1 == l2 and f1:
                                                s.append(rows)
                                                return s

            form(key, num)
    return s


@app.route('/filter_csv')
def filter_csv():
    context = {'row': read_data()}
    print(context)
    return render_template('filter_csv.html', context=context)


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        mycheckbox = request.form.get('mycheckbox')
        file = request.files['file']
        filename = secure_filename(file.filename)
        content = {'row': read_specific_data(mycheckbox)}
        key = (content['row'][0][0])
        num = request.form.get('num')
        op = perform(key, num, filename)
        return render_template('download.html')
    context = {'row': read_data()}
    return render_template('filter_csv.html', context=context)


@app.route('/download_file', methods=['GET'])
def download_file():
    def generate():
        data = StringIO()
        header = ["Test case", "No", "Source IP", "Destination IP", "Protocol", "Message Info", "Message Contents",
                  "Path Mgmt Check", "Transmit Timer", "Periodic Timer"]
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        writer = csv.DictWriter(data, fieldnames=header)
        writer.writeheader()
        for item in s:
            writer.writerow(item)
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename='output.csv')
    return response


if __name__ == '__main__':
    app.run()
