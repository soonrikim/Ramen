import requests
from bs4 import BeautifulSoup


#def extract_station_name():
    #station_info = []

url = "https://tabelog.com/tokyo/R9/rstLst/RC21/?popular_spot_id=&sk=%7Bsearch_query%7D"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

station_info = soup.find_all('div', class_='list-rst__area-genre cpy-area-genre')

i = 0
for i in range(20):
    print(station_info[i].text.strip().split(" ")[0])  # 역 이름과 추가 정보 추출
    i += 1
