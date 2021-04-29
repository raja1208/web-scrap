import these two modules bs4 for selecting HTML tags easily
from bs4 import BeautifulSoup
# requests module is easy to operate some people use urllib but I prefer this one because it is easy to use.
import requests

# I put here my own blog url ,you can change it.
url="https://www.oyorooms.com/"

#Requests module use to data from given url
source=requests.get(url)

# BeautifulSoup is used for getting HTML structure from requests response.(craete your soup)
soup=BeautifulSoup(source.text,'html')

# Find function is used to find a single element if there are more than once it always returns the first element.
title=soup.find('title') # place your html tagg in parentheses that you want to find from html.
print("this is with html tags :",title)

qwery=soup.find('h1') # here i find first h1 tagg in my website using find operation.

#use .text for extract only text without any html tags
print("this is without html tags:",qwery.text) 

inks=soup.find('a') #i extarcted link using "a" tag
print(links)


# ## extarct data from innerhtml 

# here i extarcted href data from anchor tag.
print(links['href']) 

# similarly i got class details from a anchor tag
print(links['class'])


import os, sys, time
import csv
from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from operator import itemgetter

# os.environ['MOZ_HEADLESS'] = '1'
# binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

# two = sys.argv[1]
def clean_data(data):
	try:
		return data[0].text
	except IndexError:
		return 0


def parser_oyo(driver):
	# driver = webdriver.Firefox(firefox_binary=binary)
	# driver.get("https://www.oyorooms.com/oyos-in-kathmandu")

	time.sleep(5)

	hotels_data = []

	hotels_list = driver.find_elements_by_class_name("newHotelCard")
	for hotels in hotels_list:
		hotel_name = hotels.find_elements_by_class_name("newHotelCard__hotelName")
		hotel_location =  hotels.find_elements_by_class_name("newHotelCard__hotelAddress")

		hotel_price_detail = hotels.find_elements_by_class_name("newHotelCard__pricing")
		price = hotel_price_detail[0].text
		hotel_price =  int(price.split(" ")[1])


		hotel_not_discounted_amount = hotels.find_elements_by_class_name("newHotelCard__revisedPricing")
		hotel_discount_percentage = hotels.find_elements_by_class_name("newHotelCard__discount")
		hotel_rating = hotels.find_elements_by_class_name("hotelRating__value")
		hotel_rating_remarks = hotels.find_elements_by_class_name("hotelRating__subtext")

		original_price = clean_data(hotel_not_discounted_amount)
		disc_perc = clean_data(hotel_discount_percentage)
		rating = clean_data(hotel_rating)
		remarks = clean_data(hotel_rating_remarks)

		data = {
			"Name": hotel_name[0].text,
			"Location": hotel_location[0].text,
			"Price after Disc": hotel_price,
			"Original Price": original_price,
			"Disc Percentage": disc_perc,
			"Rating": rating,
			"Remarks": remarks
			}
		print(data)
		hotels_data.append(data)
	# del os.environ['MOZ_HEADLESS'] 
	return hotels_data

def write_data_to_csv(parsed_data, csv_columns, csv_file):
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in parsed_data:
				writer.writerow(data)
	except IOError:
		print("I/O error") 



if __name__ == '__main__':
	url = sys.argv[1]
	driver = webdriver.Chrome()
	driver.get(url)
	parsed_data = parser_oyo(driver)

	#get next pages data
	try:
		nextpageButton = driver.find_elements_by_class_name("btn-next")[0]
		while(nextpageButton != []):
			next_page = nextpageButton.click()
			next_page_data = parser_oyo(driver)
			parsed_data += next_page_data
			nextpageButton = driver.find_elements_by_class_name("btn-next")[0]
	except IndexError:
		pass

	driver.close()

	csv_columns = ['Name','Location','Price after Disc', 'Original Price', 'Disc Percentage', 'Rating', 'Remarks']
	csv_file = "Hotels List.csv"
	write_data_to_csv(parsed_data, csv_columns, csv_file) 

	data_sorted_by_price = sorted(parsed_data, key=itemgetter('Price after Disc'))
	sorted_csv_file = "Hotel List sorted by price.csv"
	write_data_to_csv(data_sorted_by_price, csv_columns, sorted_csv_file)

