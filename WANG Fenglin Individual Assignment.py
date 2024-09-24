import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt

url = "https://www.hko.gov.hk/tide/KCTtextPH2024_uc.htm"

response = requests.get(url)

if(response.ok):
    print("Data is ready")
else:
    print(response.status_code)

content = response.text
soup = bs(content, "html.parser")

tideData = []
tides = soup.findAll("td")

for tide in tides:
    tideValue = tide.string
    if tideValue != None and tideValue[0] == " ":
        tideData.append(float(tideValue.strip()))

print(len(tideData))
print(tideData[:100])

# 只要一月份数据
tideData=tideData[:31*24]
tideArr = np.array(tideData).reshape(31,24)

print(tideArr[0])

x = np.arange(24)

y= tideArr[0]

fig,ax = plt.subplots()
ax.plot(x,y)

ax.set_title('Tide Height in Jan 1st')
ax.set_ylabel('Tide Height')
ax.set_xlabel('time')
plt.show()