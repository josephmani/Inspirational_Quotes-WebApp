import psycopg2
from flask import Flask	
from flask import render_template,jsonify

app = Flask("Inpirational Quotes")

dbconn = psycopg2.connect("dbname=quotes")	  

@app.route("/")
def index(): 
    cursor = dbconn.cursor()   
    cursor.execute("select quote,author,source from openings order by random() limit 1")	#query
    data= cursor.fetchall()	#get data
    return render_template("main.html", data=data)	#render
    

if __name__=="__main__":
	app.run(debug=True)
