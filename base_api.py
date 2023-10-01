import requests
import re
from lxml import etree

class Base_Api:
    def __init__(self, baseURL = "", sealedPostFix = "", completeSetPostfix = ""):
        self._baseURL = baseURL
        self._sealedPostFix = sealedPostFix
        self._completeSetPostfix = completeSetPostfix

    def make_get_request(self, endpoint, getSealedProduct = True):
        response = ""
        try:
            url = f"{self._baseURL}/{endpoint}/"
            if (getSealedProduct):
                url = f"{url}/{self._sealedPostFix}"
            else:
                url = f"{url}/{self._completeSetPostfix}"
            
            response = requests.get(url)
        except e:
            print(e)
        
        return response
    
    def find_tables(self, responseText):
        tables = []
        tables = re.findall("(<table.*?>.*?</table>)", responseText)
        parsed_tables = []
        for table in tables:
            parsed_tables.append(etree.HTML(table).find("body/table"))
        return parsed_tables
    
    def find_complete_set_price(self, responseText):
        rawText = etree.HTML(responseText).find(".//div[@class='price-box paper']").find(".//div[@class='price-box-price']").text
        completeSetPrice = float(rawText.replace('$\xa0', '').replace(',',''))
        return completeSetPrice

    def parse_table(self, table, filterHeaders = []):
        finalTable = {}

        header = table.find("thead/tr")
        headerItems = iter(header)
        columns = []
        for item in headerItems:
            columns.append(item.text)
        
        bodyRows = table.findall("tbody/tr")
        for row in bodyRows:
            finalRow = {}
            itemCount = 0
            for item in row:
                if columns[itemCount] not in filterHeaders:
                    if (columns[itemCount]) == "Card":
                        finalRow[columns[itemCount]] = item.findtext("span/a")
                    else:
                        finalRow[columns[itemCount]] = str(item.text).replace('$\xa0', '')
                itemCount += 1
            finalTable[finalRow['Card']] = finalRow

        return finalTable
                
