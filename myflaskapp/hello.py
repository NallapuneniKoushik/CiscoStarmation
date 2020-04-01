from flask import Flask, render_template,request,redirect,url_for
import csv
import io

#app.config["IMAGE_UPLOADS"] = 'C:\Users\nirautel\Desktop\myProject\static\Uploads'

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def login():
   if request.method =='POST':
      f= request.files['fileupload']
      if not f:
         print("No files chosen")
         return redirect(request.url)

      # reader = csv.reader(open('C:\\Users\\nirautel\\Desktop\\myProject\\Interfaces.csv', 'r'))
      reader = csv.reader(open(r'C:\Users\nakoushi\FlaskProjects\Interfaces.csv','r'))
      Dictionary = {}
      data = []
      Message=[]

      for row in reader:
         k, v = row
         Dictionary[k] = v

      stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
      csv_input = csv.reader(stream)
      next(csv_input)
      for row in csv_input:
         string = str(row[8] + row[9])
         Message.append(string)
         key = row[5][0].upper() + row[5][1].lower()
         list = Dictionary[key].split('->')
         if row[6]=='IN':
            data.append(list[0] + "->" + list[1] + ":" + "  "+row[4])
         else:
            data.append(list[1] + "->" + list[0] + ":" + "  "+row[4])
      print(data[6])
      return render_template('result.html',result=data,result2=Message)
   return render_template('main1login.html')

if __name__ == '__main__':
   app.run(debug = True)
