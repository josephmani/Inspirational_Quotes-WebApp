import requests
import bs4
import sys
import psycopg2
import sys
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


def load_quotes():
	cursor = dbconn.cursor()
	for i in range(1,100):
		url= "https://www.goodreads.com/quotes/tag/inspirational?page="
		page= url+ str(i)
		resp=requests.get(page)
		soup =bs4.BeautifulSoup(resp.content,features="html.parser")
		quote_author =soup.find_all("div",attrs={"class":"quoteText"})
		for i in quote_author:
			texts= str(i.text.strip().split('―')[0])
			author_name= str(i.text.strip().split('―')[1])
		
			texts=texts.replace('“','')
			texts=texts.replace('”','')
			if len(texts)>100:
				continue
			
			author_name = author_name.replace('\n','')
			author_name = author_name.replace('   ','')
			
			if ", " in author_name:
				a_list = author_name.split(", ")
				a_list[1]=","+a_list[1]
				cursor.execute("INSERT INTO openings (quote, author, source) VALUES(%s, %s, %s)",(texts, a_list[0], a_list[1]))
			
			else:
				cursor.execute("INSERT INTO openings (quote, author) VALUES(%s, %s)",(texts, author_name))			
			
		dbconn.commit()



def create_db():
	cursor = dbconn.cursor()
	f=open("words.sql")
	sql_code= f.read()
	f.close()
	cursor.execute(sql_code)
	dbconn.commit()
	
	
def main(arg):
	if arg=="create":
		create_db()
	elif arg=="crawl":
		load_quotes()
	else:
		print(f"Unknown command {arg}")		


if __name__=="__main__": #import guard
	main(sys.argv[1])
	 
