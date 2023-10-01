import requests
import re
from lxml import etree

class Base_Api:
    def __init__(self, baseURL = "", postFix = ""):
        self._baseURL = baseURL
        self._postFix = postFix

    def make_get_request(self, endpoint):
        response = ""
        try:
            response = requests.get(f"{self._baseURL}/{endpoint}/{self._postFix}")
        except e:
            print(e)
        
        return response
    
    def find_tables(responseText):
        tables = []
        tables = re.findall("(<table.*?>.*?</table>)", responseText)
        parsed_tables = []
        for table in tables:
            parsed_tables.append(etree.HTML(table).find("body/table"))
        return parsed_tables

    def parse_table(table, filterHeaders = []):
        finalTable = []

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
                        finalRow[columns[itemCount]] = item.text
                itemCount += 1
            finalTable.append(finalRow)

        return finalTable
                
