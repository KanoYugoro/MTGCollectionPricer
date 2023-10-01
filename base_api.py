import requests
import re

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
        # If I was doing heavier HTML operations, I'd use a dedicated HTML parser
        tables = []
        tables = re.findall("(<table.*?>.*?</table>)", responseText)
        return tables