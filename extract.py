from bs4 import BeautifulSoup

import requests

url = raw_input("Enter a website to extract the URL's from: ")

r  = requests.get("https://www.oyorooms.com//" +url)

data = r.text

soup = BeautifulSoup(data,"html.parser")

for link in soup.find_all('a'):
    print(link.get('href'))
