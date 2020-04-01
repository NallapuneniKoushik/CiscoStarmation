from flask import Flask, render_template, request
app = Flask(__name__)
import csv, json
def perform(num):
    

    csvFilePath = 'sample_merge_csv.csv'
    jsonFilePath = 'json.json'
    data = {}
    dct=[]
    mdct=[]
    a = []
    l=[]
    l1=[]
    l2=[]
    l3=[]
    b= ""
    c=""
    o={}
    #num=input("Enter IMSI")
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            #print(rows)
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
                    text += '"' + thisline.lstrip() + ' }'*int((spcount1-spcount2)/4) +',\n'
                    bracketcount -= int((spcount1-spcount2)/4)

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
            mdct.append(dct)
            #print(dct)
            #print(dct[0].keys())
       

    
            #CREATE REQUEST
       
            for i in dct:
                counter=0
                td={"f_teid_gre_key":""}
                if ("International_Mobile_Subscriber_Identity_(IMSI)" in i) :
                    #print(i["International_Mobile_Subscriber_Identity_(IMSI)"])
                    if(num==(i["International_Mobile_Subscriber_Identity_(IMSI)"]["imsi"])):
                        if ("seq" in i):
                
                            if("Bearer_Context" in i):
                                #print("1st",i)
                                a=(i["Bearer_Context"])
                                if ("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in a):
                                    b=(i["Bearer_Context"]["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                                    td["f_teid_gre_key"]=b
                                    #print(td)
                                    l1.append(td)
                                
                                elif ("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in i):
                                    b=(i["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                                    td["f_teid_gre_key"]=b
                                    #print(td)
                                
                                    l1.append(td)
                            elif("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in i):
                                b=(i["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                                td["f_teid_gre_key"]=b
                                #print(td)
                            
                                l1.append(td)
         

        
                           
               
            for i in dct:
                td={"f_teid_gre_key":""}
                if ("seq" in i):
                
                        if("Bearer_Context" in i):
                            #print("2nd",i)
                            a=(i["Bearer_Context"])
                            if ("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in a):
                                c=(i["Bearer_Context"]["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                                td["f_teid_gre_key"]=c
                                    #print(td)
                            
                                l.append(td)
                            elif ("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in i):
                                c=(i["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                                td["f_teid_gre_key"]=c
                                    #print(td)
                                
                                l.append(td)
                            
                        elif("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in i):
                            c=(i["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"])
                            td["f_teid_gre_key"]=c
                            #print(c)
                            
                            l.append(td)
         
                        
    x=l
        #print(l)


    y=l1
        #print(y)
    fin=[]
    fr=[]
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for i in y:
            #print("y-->",i)
            if i not in fin:
                fin.append(i)

        for i in x:
            if i not in fin:
                fin.append(i)
        #print(fin)
        #print(len(fin))
        #print(dct)
        flag=1           
        for row in csvReader:
            for i in mdct:
                for j in i:
                    for k in fin:
                        if ("Bearer_Context" in j):
                        
                            if("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in j["Bearer_Context"]):
                                #print("true bc")
                                if j["Bearer_Context"]["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"]==k["f_teid_gre_key"] and "Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in row['Message Contents']['Bearer_Context']:
                                    fr.append(row)
                                    
                                    #print(row)
                                    flag=0
                                    break

                            elif ("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in j) and j["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"]==k["f_teid_gre_key"] and "Bearer_Context" in row['Message Contents'] and 'Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)' in row['Message Contents']:
                                fr.append(row)
                                #print(row)
                                flag=0
                                break
                            
                        if("Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in j):
                            #print(j["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"])
                            if j["Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)"]["f_teid_gre_key"]==k["f_teid_gre_key"] and "Fully_Qualified_Tunnel_Endpoint_Identifier_(F-TEID)" in row['Message Contents']:
                                #print(row)
                                fr.append(row)
                                flag=0
                                break
                        if(flag==0):
                            break
                    if(flag==0):
                        break
                if(flag==0):
                    break
    
    return fr


@app.route("/")
def index():
    return render_template("index_r.html")
wsgi_app=app.wsgi_app


@app.route('/index1',methods = ["GET","POST"])
def hello():
    if request.method=="POST":
        file=request.files["file"]
        file.save(os.path.join("uploads",file.filename))
        num=request.form.get('number')
        op=perform(num)
        f=open("output.csv","w")
        header=["Test case","No","Source IP","Destination IP","Protocol","Message Info","Message Contents","Path Mgmt Check","Transmit Timer","Periodic Timer"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for data in op:
            writer.writerow(data)
        return render_template("index2.html",message='upload')
    return render_template("index1.html",message='upload')



if __name__=='__main__':
    import os
    HOST=os.environ.get('SERVER_HOST','localhost')
    try:
        PORT=int(os.environ.get('SERVER_PORT','5555'))
    except ValueError:
        PORT=5555
    app.run(HOST,PORT)