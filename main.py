import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.bestchange.ru/visa-mastercard-rub-to-tron.html")

soup = BeautifulSoup(response.text, "lxml")
table_data = soup.find("table", id="content_table")

data = soup.find('tbody')

name = data.find('td', class_="bj").find("div", class_="ca").text
link = data.find('td', class_="bj").find("a", href=True)['href']
rate = data.find('td', class_="bi").find("div", class_="fs").text
deposit = data.find('td', class_="bi").find("div", class_="fm1").text
reserve = data.find("td", class_="ar arp").text
feedback = data.find("td", class_="rw").find("td", class_="rwr pos").text
feedback_link = data.find("a", class_="rwa", href=True)['href']


print(link)
print(name)
print(rate)
print(deposit)
print(reserve)
print(feedback)
print(feedback_link)