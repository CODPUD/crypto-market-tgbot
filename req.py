import requests
from config import *
from bs4 import BeautifulSoup


async def getDataKoinal():
    try:
        response = requests.get(linkKoinal)
        soup = BeautifulSoup(response.text, "lxml")
        soup = soup.findAll("span", class_="rate")
        bigdata = {}
        data = {}
        string = ""
        for c in soup:
            try:
                for a in c.text.replace(u'\xa0', u'').lstrip():
                    if a != "\n":
                        string += a
                    else:
                        break

                crypto = string[:3]
                rate = string[3:]

                string = ""

                data[crypto] = rate
                bigdata["rate"] = data
            except:
                pass

        return bigdata
    except:
        return None

async def getDataMercuryo():
    response = requests.get(linkMercuryo).json()
    return response["data"]["buy"]

async def getDataBanxa():
    response = requests.get(linkBanxa).json()
    return response["RateTicker"]["data"]

async def getAllCryptoMercuryo():
    response = requests.get(linkMercuryo).json()
    return response["data"]["buy"]

async def getAllCryptoBanxa():
    response = requests.get(linkBanxa).json()
    for i in response["RateTicker"]["data"]["rates"]:
        response = response["RateTicker"]["data"]["rates"][i]
        break
    return response

async def getAllFiatMercuryo():
    response = requests.get(linkMercuryo).json()
    data = response["data"]["buy"]
    for i in data:
        response = response["data"]["buy"][i]
        break
    return response

async def getAllFiatBanxa():
    response = requests.get(linkBanxa).json()
    return response["RateTicker"]["data"]["rates"]

async def getRateMercuryo(crypto, fiat):
    response = requests.get(linkMercuryo).json()
    return round(float(response["data"]["buy"][crypto][fiat]), 2)

async def getRateBanxa(crypto, fiat):
    response = requests.get(linkBanxa).json()
    return round(float(response["RateTicker"]["data"]["rates"][fiat][crypto]["Value"])*comission, 2)

async def getRateKoinal(crypto):
    data = await getDataKoinal()
    return data['rate'][crypto]

async def getMerCurrentRate(currency):
    msg = f"<b>{currency}</b>\n<code>"
    response = requests.get(linkMercuryo).json()
    data = response["data"]["buy"][currency]
    for rate in data:
        msg += " | " + rate + " | " + str(round(float(data[rate]), 2)) + "\n"
    msg += "</code>"
    return msg

async def getBanxaCurrentRate(currency):
    msg = f"<b>{currency}</b>\n<code>"
    response = requests.get(linkBanxa).json()
    data = response["RateTicker"]["data"]["rates"]
    for i in data:
        msg += " | " + i + " | " + str(round(float(data[i][currency]["Value"])*comission, 2)) + "\n"
    msg += "</code>"
    return msg