import os
from sys import path

import requests
from bs4 import BeautifulSoup

url="https://www.ndtv.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")




