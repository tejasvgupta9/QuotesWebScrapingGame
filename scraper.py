
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from termcolor import colored
import pyfiglet
import csv


base_url="http://quotes.toscrape.com"
def scrape_quotes():
	all_quotes=[]
	url="/page/1"
	while url:

		res=requests.get(f"{base_url}{url}")
		#print(f"Now Scraping {base_url}{url}")
		soup=BeautifulSoup(res.text,"html.parser")
		quotes=soup.find_all(class_="quote")
		for quote in quotes:
			all_quotes.append({
				"text":quote.find(class_="text").get_text(),
				"author":quote.find(class_="author").get_text(),
				"bio-link":quote.find("a")["href"]
				})

		next_btn=soup.find(class_="next")
		url=next_btn.find("a")["href"] if next_btn else None
		#sleep(1)
	return all_quotes
#sleep(2)
#print(all_quotes)
#print(all_quotes)
def start_game(quotes):
	quote=choice(quotes)
	remaining_guesses=4
	print("Here's a quote")
	print(quote["text"])
	print(quote["author"])
	guess=''

	while guess.lower() != quote["author"].lower() and remaining_guesses>0 :
			guess=input(f"Who said this quote? Guesses remaing: {remaining_guesses}\n ")
			if guess.lower()==quote["author"].lower():
				print("Congrats,you got it right")
				print(colored(pyfiglet.figlet_format("Congrats"),"blue"))
				break
			remaining_guesses-=1
			if remaining_guesses == 3:
				res=requests.get(f"{base_url}{quote['bio-link']}")
				soup=BeautifulSoup(res.text,"html.parser")
				birth_date=soup.find(class_="author-born-date").get_text()
				birth_place=soup.find(class_="author-born-location").get_text()
				print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
			elif remaining_guesses==2:
				print(f"Here's a hint: The author's first name starts with {quote['author'][0]}")
			elif remaining_guesses==1:
				last_initial=quote["author"].split(" ")[1][0]
				print(f"Here's a hint: The author's first name starts with {last_initial}")
			else:
				print(f"Sorry you ran out of guesses. The answer was {quote['author']}")


	again=''
	while again.lower() not in ('y','yes','no','n'):
		again=input("Would you like to play again (Y/N)? ")
	if again.lower() in ('y','yes'):
		return start_game(quotes)
	else:
		print("OKAY,GOODBYE!")
		print(pyfiglet.figlet_format("BYE"))

quotes=scrape_quotes()
start_game(quotes)








