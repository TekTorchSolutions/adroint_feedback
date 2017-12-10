from flask import Flask,render_template,request
from pymongo import MongoClient
import requests
import json
app=Flask(__name__)

@app.route('/adroint',methods=["GET","POST"])
def index():
    if request.method=='POST':
        if request.form["feedback_area"]!="" and request.form["response_area"]!="":
            send_to_db(feedback=True,request_text=request.form["request_area"],response_text=request.form["response_area"],feedback_text=request.form["feedback_area"])
            return render_template("adroint_app.html",resp="")
        data={
            "text":request.form['request_area']
        }
        url='https://thawing-waters-94320.herokuapp.com/webhook'
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        #return str(json.loads(r.text))
        resp={
            "response":str(json.loads(r.text)),
            "request":data["text"]
        }
        print(resp)
        print("Lets send")
        if request.form["feedback_area"]=="" and request.form["response_area"]=="" and request.form["request_area"]!="":
            print("Nearly sending")
            send_to_db(feedback=False,request_text=request.form["request_area"],response_text=str(json.loads(r.text)))


        return  render_template('adroint_app.html',resp=resp)

    return render_template("adroint_app.html",resp="")


def send_to_db(feedback=False,request_text="",response_text="",feedback_text=""):
    print("Connecting")
    client = MongoClient("mongodb://jas1994:biology12@ds133476.mlab.com:33476/adroint_logs")
    print("Connected")

    db = client['adroint_logs']
    print("Sending")

    if feedback:
        collection = db["logs_with_feedback"]
        db_dict={
            "req":request_text,
            "resp":response_text,
            "feed":feedback_text


        }
        collection.insert(db_dict)
        print("Sent")

    else:
        collection=db["plain_logs"]
        db_dict = {
            "req": request_text,
            "resp": response_text,


        }
        collection.insert(db_dict)
        print("Sent")



if __name__=='__main__':
    app.run(debug=True)