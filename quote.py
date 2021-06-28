import requests
import bs4
import sys
import psycopg2

def load_quotes():
	dbconn = psycopg2.connect("dbname=quotes")
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
	dbconn = psycopg2.connect("dbname=quotes")
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
	 
