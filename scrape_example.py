import requests
from bs4 import BeautifulSoup

# 웹페이지에 요청을 보내고 HTML을 가져옵니다
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to retrieve the page")
        return None

# HTML에서 정보 추출하기
def extract_info(html):
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        # 예시: 특정 클래스명을 갖는 요소 추출
        elements = soup.find_all('div', class_='example-class')
        for element in elements:
            # 원하는 정보 추출
            info = element.find('span', class_='info').text
            print(info)
    else:
        print("No HTML content to extract information from")

# 메인 함수
def main():
    url = 'https://tabelog.com/rstLst/?vs=1&sa=&sk=&lid=top_navi1&vac_net=&svd=20231029&svt=1900&svps=2&hfc=1&sw='
    html_content = get_html(url)
    extract_info(html_content)

if __name__ == '__main__':
    main()
