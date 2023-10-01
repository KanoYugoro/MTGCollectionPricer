import requests

class Base_Api:
    def __init__(self, baseURL = "", postFix = ""):
        self._baseURL = baseURL
        self._postFix = postFix