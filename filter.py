import csv
import io
import json
import os

from flask import render_template, request, redirect, flash, send_file
from werkzeug.utils import secure_filename

from database import read_data, read_specific_data
from test_new import app

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

l1 = []
l2 = []
s = []


def perform(key, num, filename):
    dct = []
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


@app.route('/filter_csv', methods=['GET', 'POST'])
def filter_csv():
    if request.method == 'POST':
        mycheckbox = request.form.get('mycheckbox')
        file = request.files['file']
        filename = secure_filename(file.filename)
        content = {'row': read_specific_data(mycheckbox)}
        key = (content['row'][0][0])
        num = request.form.get('num')
        perform(key, num, filename)
        context = {'row': read_data()}
        return render_template('filter_csv.html', context=context, activate_download=True)
    context = {'row': read_data()}
    return render_template('filter_csv.html', context=context, activate_download=False)


@app.route('/download', methods=['GET'])
def download():
    header = ["Test case", "No", "Source IP", "Destination IP", "Protocol", "Message Info", "Message Contents",
              "Path Mgmt Check", "Transmit Timer", "Periodic Timer"]
    csv_content = list()
    csv_content.append(','.join(header))
    for item in s:
        csv_content.append('"' + '","'.join(item.values()) + '"')
    response = app.response_class(
        response=os.linesep.join(csv_content),
        status=200,
        mimetype='text/csv'
    )
    response.headers.set('Content-disposition', "attachment", filename='sample_merge_csv.csv')
    return response


@app.route('/ladder', methods=['GET', 'POST'])
def ladder():
    if request.method == 'POST':
        f = request.files['fileupload']
        if not f:
            flash('No files chosen')
            return redirect(request.url)

        reader = csv.reader(open(r'Interfaces\Interfaces.csv', 'r'))
        Dictionary = {}
        data = []
        Message = []
        View = [[]]

        for row in reader:
            k, v = row
            Dictionary[k] = v

        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        Valid_List = ['Message', 'Interface', 'In / Out', 'Input Overwrite', 'Validation Overwrite', 'Timeout (ms)',
                      'Policy/Platform Changes', 'Comments']
        Valid_List = [x.lower() for x in Valid_List]
        FColumn = next(csv_input)
        FColumn = [x.lower() for x in FColumn]
        status = all(x in FColumn for x in Valid_List)
        if len(FColumn) != 12 or not status:
            flash('Choose Appropriate File Format', 'error')
            return render_template('ladder.html')
        else:
            for row in csv_input:
                if row[7] == '' and row[8] == '':
                    Message.append('No Message')
                else:
                    Message.append(row[7] + row[8])
                key = row[5][0].upper() + row[5][1].lower()
                list = Dictionary[key].split('->')
                if row[6] == 'IN':
                    data.append(list[0] + "->" + list[1] + ":" + "  " + row[4])
                else:
                    data.append(list[1] + "->" + list[0] + ":" + "  " + row[4])
        return render_template('result.html', result=data, result2=Message)
    return render_template('ladder.html')


@app.route('/download_sample_file')
def download_sample_file():
    path = "File_Format.csv"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
