import psycopg2
from flask import Flask	
from flask import render_template,jsonify
import os
import urllib.parse as up


from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(os.path.dirname(os.path.realpath(__file__)), '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

up.uses_netloc.append("postgres")
url = up.urlparse(DATABASE_URL)
dbconn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)


app = Flask(__name__)

app.config.from_mapping(
	DATABASE='quotedb'
)

@app.route('/')
def index(): 
	cursor = dbconn.cursor()   
	cursor.execute("SELECT quote,author,source from openings order by random() limit 1")
	data= cursor.fetchall()	
	dbconn.commit()
	return render_template("main.html", data=data)	#render
	 
if __name__=='__main__':
	app.run()


