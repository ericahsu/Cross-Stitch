import requests
import lxml.html as lh
from bs4 import BeautifulSoup as bs
import pandas as pd

# "http://www.camelia.sk/dmc_5.htm"


class dmcWebscrape(object):
    # Initialize values
    def __init__(self, url):
        self.page = requests.get(url).text
        self.soup = bs(self.page, "lxml")


        self.page2 = requests.get(url)
        self.soup2 = bs(self.page2.content, 'lxml')
        self.bgcolorTableHeader = self.soup2.select('td[bgcolor]')
        self.bgcolorTable = self.bgcolorTableHeader[1::]

        self.initialTable = None
        self.tableOfValues = []
        self.tableNoWhitespace = []
        self.hex = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 
                    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 
                    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9}
        self.dmc = None
        self.colorNames = None
        self.rgbValues = []

    # Create the table of number and names
    def tableOfNumberAndNames(self):
        self.initialTable = self.soup.find_all('font', {'face':"arial, helvetica, sans-serif", 'size':'2'})
        length = len(self.initialTable)
        for index in range(length):
            self.tableOfValues.append(self.initialTable[index].text)

        # Remove any whitespace from elements before appending to a new table
        for item in self.tableOfValues[2:-1]:
            if '\r\n' in item or "  " in item:
                item = item.replace('\r\n', "")
                item = self.removeWhitespace(item)
                self.tableNoWhitespace.append(item)
            else:
                self.tableNoWhitespace.append(item)

        # dmc is the number
        self.dmc = self.tableNoWhitespace[0::2]

        # colorNames are the colors
        self.colorNames = self.tableNoWhitespace[1::2]

    # Remove spaces that are longer than one
    def removeWhitespace(self, s):
        if "  " not in s:
            return s
        else:
            while "  " in s:
                s = s.replace("  ", "")
            return s        

    # Creates the table of rgb values
    def rgbTable(self):
        # Create the table of hex values
        hexValues = []
        for item in self.bgcolorTable:
            item = str(item)
            # Isolates the part of the webscraped data needed
            hexValues.append(item[13:20])

        # Convert the hex value table to rgb values
        for item in hexValues:
            self.rgbValues.append(self.convertHexToRgb(item))

    # Given a hex value, convert it to rgb values
    def convertHexToRgb(self, hexValue):
        r = self.hex[hexValue[1]] * 16 + self.hex[hexValue[2]]
        g = self.hex[hexValue[3]] * 16 + self.hex[hexValue[4]]
        b = self.hex[hexValue[5]] * 16 + self.hex[hexValue[6]]
        return (int(r), int(g), int(b))

    # Returns the complete table of DMC numbers, names, and rgb values
    def getFullTable(self):
        self.tableOfNumberAndNames()
        self.rgbTable()
        df = pd.DataFrame(list(zip(self.dmc, self.colorNames, self.rgbValues)), \
            columns = ['DMC', 'Color', 'RGB'])
        return df

# Loops through the pages of the dmc color chart to create the table of dmc numbers, names, and colors
for pageNumber in range(1, 7):
    url = f"http://www.camelia.sk/dmc_{pageNumber}.htm"
    page = dmcWebscrape(url)
    df = page.getFullTable()
    if pageNumber == 1:
        completeDmcTable = df
    else:
        # Merging learned from: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        completeDmcTable = pd.concat([completeDmcTable, df])

# dataframe to csv documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
completeDmcTable.to_csv('dmctable.csv', index = False)






