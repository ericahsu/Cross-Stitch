import requests
import lxml.html as lh
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "http://www.camelia.sk/dmc_6.htm"
page = requests.get(url)

soup = bs(page.content, 'lxml')
table = soup.select('td[bgcolor]')
table1 = table[1::]

def bgcolorFromString(s):
    s = str(s)
    return s[13:20]

hexValues = []
for item in table1:
    hexValues.append(bgcolorFromString(item))

hex = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9}

def convertHexToRGB(hexValue):
    r = hex[hexValue[1]] * 16 + hex[hexValue[2]]
    g = hex[hexValue[3]] * 16 + hex[hexValue[4]]
    b = hex[hexValue[5]] * 16 + hex[hexValue[6]]
    return (r, g, b)

rgbValues = []
for item in hexValues:
    rgbValues.append(convertHexToRGB(item))

