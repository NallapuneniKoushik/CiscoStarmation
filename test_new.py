import csv
import io

from flask import *

from Server_Connection import *
from database import add_data

app = Flask(__name__)
app.secret_key = 'secret_key'
app.debug = True
wsgi_app = app.wsgi_app


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if request.form['action'] == 'add':
            return redirect('/add_record', code=307)
        elif request.form['action'] == 'delete':
            return redirect('/delete_record', code=307)
        elif request.form['action'] == 'submit':
            return redirect('/submit_records', code=307)
    data = read_records()
    return render_template("index.html", data=data)


@app.route('/add_record', methods=['POST'])
def add_record():
    values = dict()
    values['hostname'] = request.form['hostname']
    values['username'] = request.form['username']
    values['password'] = request.form['password']
    values['arguments'] = request.form['arguments']
    values['status'] = "Not Connected"

    msg = '{}@{} add: '.format(values['username'], values['hostname'])
    msg += insert_record(values)
    flash(msg)

    return redirect('/')


@app.route('/delete_record', methods=['POST'])
def delete_record():
    for rowid_checked, delete in request.form.items():
        if delete == 'on' and rowid_checked.count('-') > 0:
            data = read_records()
            rowid, checked = rowid_checked.split('-')
            rowid = int(rowid)
            username = data[rowid]['username']
            hostname = data[rowid]['hostname']
            msg = '{}@{} delete: '.format(username, hostname)
            msg += delete_record_db(rowid)
            flash(msg)

    return redirect('/')


@app.route('/submit_records', methods=['POST'])
def submit_records():
    records_read = read_records()
    data = dict()
    for rowid_checked, submit in request.form.items():
        if submit == 'on' and rowid_checked.count('-') > 0:
            rowid, checked = rowid_checked.split('-')
            rowid = int(rowid)
            data[rowid] = records_read[rowid]
    msg = '{} records submitted'.format(len(data))
    flash(msg)
    server_connection(data)
    return redirect('/')


@app.route('/get_data')
def get_data():
    data = read_records()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/get_pcap_file/<slug>')
def get_pcap_file(slug):
    slug = int(slug)
    data = read_records()
    values = data[slug]
    hostname = values['hostname']
    username = values['username']
    arguments = values['arguments']
    #
    # named_tuple = tm.localtime()
    # time_string = tm.strftime("%d_%m_%Y", named_tuple)

    pcap_filename = '_'.join((username, hostname.replace('.', '_'), arguments)) + '.pcap'
    cwd = os.getcwd()
    file_path = os.sep.join((cwd, "TcpOutputs", pcap_filename))
    pcap_data = read_file(file_path)
    response = app.response_class(
        response=pcap_data,
        status=200,
        mimetype='text/*'
    )
    response.headers.set('Content-disposition', "attachment", filename=pcap_filename)
    return response


# adding


@app.route('/fonct', methods=['POST', 'GET'])
def fonct():
    if request.method == 'POST':
        Protocol = request.form['Protocol']
        key = request.form['key']
        add_data(Protocol, key)
    return render_template('ex.html')


if __name__ == '__main__':
    app.run()
