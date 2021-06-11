import codecs
import requests
import zipfile
import os
import shutil

async def download_bmdata(url, save_path, chunk_size=128):
    try:
        shutil.rmtree("bmdata")
    except:
        pass

    try:
        os.mkdir("bmdata")
    except:
        pass


    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

    archive = zipfile.ZipFile("bmdata/info.zip")
    archive.extractall("bmdata/")
    archive.close()

async def getExch(exch):
    data = codecs.open("bmdata/bm_exch.dat", 'r', encoding='utf-8',
                       errors='ignore')
    rates = data.read()
    data.close()

    platform = None
    for rate in rates.split('\n'):
        if rate.startswith(exch):
            platform = rate.split(';')[1]
            break

    return platform

async def getBestChange(to_cy, from_cy = "59"):
    info = {}
    await download_bmdata("http://api.bestchange.ru/info.zip", "bmdata/info.zip")
    data = codecs.open("bmdata/bm_rates.dat", 'r', encoding='utf-8',
                     errors='ignore')
    rates = data.read()
    data.close()

    data_rates = []
    for rate in rates.split('\n'):
        if rate.startswith(from_cy+';'+to_cy):
            data_rates.append(rate)

    min_val = float(data_rates[0].split(';')[3])
    min_rate = None
    for rate in data_rates:
        get_val = float(rate.split(';')[3])
        if get_val < min_val:
            min_val = get_val
            min_rate = rate

    platform = await getExch(min_rate.split(';')[2])
    info['name'] = platform
    info['rate'] = min_rate.split(';')[3]
    info['reserve'] = min_rate.split(';')[5]
    info['feedback'] = min_rate.split(';')[6].replace('.','/')
    info['link'] = f"https://www.bestchange.ru/{platform.lower()}-exchanger.html"

    return info