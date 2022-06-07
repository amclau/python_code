import requests #getting content of the TED Talk page

from bs4 import BeautifulSoup #web scraping

import re #Regular Expression pattern matching

import json #json processing

url = 'https://us06web.zoom.us/rec/play/jcaVydlJoMniIpFXPGTBrlluOOzag0us0XCPERJT_PrbFNedwE8l9L5NieR8H_quSgJdn1E_6Fz-nCKZ.ED1sGRsH0udxCiYu?continueMode=true&_x_zm_rtaid=06QFGs4YQGm_aaRFBttvWA.1650612857482.381c353598807aafa882715ef82b3d1a&_x_zm_rhtaid=150'

r = requests.get(url)



soup = BeautifulSoup(r.content, "html.parser")
next_data_script = soup.find("source")
print(next_data_script)

with open("op.txt", "w") as outfile:
        outfile.write(next_data_script.text)
