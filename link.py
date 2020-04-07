from flask import Flask, request, url_for, redirect, render_template
import csv
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('index.html')


@app.route('/ladder', methods=['GET', 'POST'])
def ladder():
    if request.method == 'POST':
        f = request.files['fileupload']
        if not f:
            print("No files chosen")
            app.logger.info("No File Chosen")
            return redirect(request.url)
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        lines = next(csv_input)
        print(len(lines))

        reader = csv.reader(open(r'Interfaces\Interfaces.csv'))
        Dictionary = {}
        data = []
        Message = []

        for row in reader:
            k, v = row
            Dictionary[k] = v

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
        print('hello')
        return render_template('result.html', result=data, result2=Message)
    return render_template('main1login.html')
