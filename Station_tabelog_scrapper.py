# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

raw_data = []


class Tabelog:
    """
    食べログスクレイピングクラス
    test_mode=Trueで動作させると、最初のページの３店舗のデータのみを取得できる
    """

    def __init__(self, base_url, test_mode=False, p_ward='', p_category='', begin_page=1, end_page=3):
        # 変数宣言
        self.raw_data = []
        self.base_url = base_url
        self.p_ward = p_ward  # 역을 지정하는 매개변수
        self.p_category = p_category
        self.store_id = ''
        self.store_id_num = 0
        self.store_name = ''
        self.score = 0
        self.ward = p_ward
        self.review_cnt = 0
        self.review = ''
        self.columns = ['store_id', 'store_name', 'score', 'ward', 'review_cnt', 'review']
        self.df = pd.DataFrame(columns=self.columns)
        self.__regexcomp = re.compile(r'\n|\s')  # \nは改行、\sは空白
        page_num = begin_page  # 店舗一覧ページ番号
        if test_mode:
            list_url = base_url + str(
                page_num) + '/?popular_spot_id=&sk=%7Bsearch_query%7D/?Srt=D&SrtT=rt&sort_mode=1'  # 食べログの点数ランキングでソートする際に必要な処理
            self.scrape_list(list_url, mode=test_mode)
        else:
            while True:
                list_url = base_url + str(
                    page_num) + '/?popular_spot_id=&sk=%7Bsearch_query%7D/?Srt=D&SrtT=rt&sort_mode=1'  # 食べログの点数ランキングでソートする際に必要な処理
                if self.scrape_list(list_url, mode=test_mode) != True:
                    page_num += 1
                    break
                # INパラメータまでのページ数データを取得する
                if page_num >= end_page:
                    break
                page_num += 1
        return

    def extract_station_name(html):
        soup = BeautifulSoup(html, 'html.parser')
        station_info = soup.find('div', class_='list-rst__area-genre cpy-area-genre')
        if station_info:
            return station_info.text.strip()  # 역 이름과 추가 정보 추출
        return "역 정보 없음"

    # 웹 페이지 URL
    url = 'https://tabelog.com/tokyo/R9/rstLst/RC21/?popular_spot_id=&sk=%7Bsearch_query%7D'

    # 웹 페이지에서 HTML 가져오기
    response = requests.get(url)
    html_content = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_content, 'html.parser')

    # 각 식당 정보 추출
    for restaurant in soup.find_all('div', class_='list-rst__rst-name'):  # 식당 이름이 포함된 div 태그
        station_name = extract_station_name(str(restaurant))
        # 나머지 정보 추출 및 출력

        # 웹 페이지 URL
    url = 'https://tabelog.com/tokyo/R9/rstLst/RC21/?popular_spot_id=&sk=%7Bsearch_query%7D'
    # 웹 페이지에서 HTML 가져오기
    response = requests.get(url)
    html_content = response.text
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_content, 'html.parser')
    # 각 식당 정보 추출
    for restaurant in soup.find_all('div', class_='list-rst__rst-name'):  # 식당 이름이 포함된 div 태그
        station_name = extract_station_name(str(restaurant))
        # 나머지 정보 추출 및 출력

    def scrape_list(self, list_url, mode):
        """
        店舗一覧ページのパーシング
        """
        i = 0
        r = requests.get(list_url)
        if r.status_code != requests.codes.ok:
            return False
        soup = BeautifulSoup(r.content, 'html.parser')
        soup_a_list = soup.find_all('a', class_='list-rst__rst-name-target')  # 店名一覧
        if len(soup_a_list) == 0:
            return False
        if mode:
            for soup_a in soup_a_list[:2]:
                if i > 19:
                    i = 0
                item_url = soup_a.get('href')  # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(r, item_url, mode, i)
                i += 1
        else:
            for soup_a in soup_a_list:
                if i > 19:
                    i = 0
                item_url = soup_a.get('href')  # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(r, item_url, mode, i)
                i += 1
        return True


    def scrape_item(self, eli_station, item_url, mode, count):
        """
        個別店舗情報ページのパーシング
        """
        start = time.time()
        r = requests.get(item_url)
        html = r.text
        if r.status_code != requests.codes.ok:
            print(f'error:not found{item_url}')
            return
        soup = BeautifulSoup(html, 'html.parser')
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id_num, store_name.strip()), end='')
        self.store_name = store_name.strip()
        # ラーメン屋、つけ麺屋以外の店舗は除外
        store_head = soup.find('div', class_='rdheader-subinfo')  # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')
        # print('ターゲット：', store_head_list[0].text)
        # if store_head_list[0].text not in {'ラーメン', 'つけ麺'}:
        #     print('ラーメンorつけ麺のお店ではないので処理対象外')
        #     self.store_id_num -= 1
        #     return
        # 評価点数取得
        # <b class="c-rating__val rdheader-rating__score-val" rel="v:rating">
        #    <span class="rdheader-rating__score-val-dtl">3.58</span>
        # </b>
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string
        print('  評価点数：{}点'.format(rating_score), end='')
        rating_score = float(rating_score) if rating_score != '-' else 0.0  # 평가 점수를 숫자로 변환
        self.score = rating_score
        # 評価点数が存在しない店舗は除外
        if rating_score == '-':
            print('  評価がないため処理対象外')
            self.store_id_num -= 1
            return
        # レビュー一覧URL取得
        # <a class="mainnavi" href="https://tabelog.com/tokyo/A1304/A130401/13143442/dtlrvwlst/"><span>口コミ</span><span class="rstdtl-navi__total-count"><em>60</em></span></a>
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')
        # レビュー件数取得
        print('  レビュー件数：{}'.format(review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string),
              end='')
        self.review_cnt = review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string
        # レビュー一覧ページ番号
        page_num = 1  # 1ページ*20 = 20レビュー 。この数字を変えて取得するレビュー数を調整。
        # レビュー一覧ページから個別レビューページを読み込み、パーシング
        # 店舗の全レビューを取得すると、食べログの評価ごとにデータ件数の濃淡が発生してしまうため、
        # 取得するレビュー数は１ページ分としている（件数としては１ページ*20=２0レビュー）
        while True:
            review_url = review_tag + 'COND-0/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            # print('\t口コミ一覧リンク：{}'.format(review_url))
            print(' . ', end='')  # LOG
            if self.scrape_review(review_url) != True:
                break
            if page_num >= 1:
                break
            page_num += 1
        process_time = time.time() - start
        print('  取得時間：{}'.format(process_time))
        s_info = BeautifulSoup(eli_station.text, 'html.parser')
        station_info = s_info.find_all('div', class_='list-rst__area-genre cpy-area-genre')
        print(' Station : {}'.format(station_info[count].text.strip().split(" ")[0]))
        station = station_info[count].text.strip().split(" ")[0]
        raw = [store_name.strip(), self.store_id_num, rating_score, self.ward, self.review_cnt, review_tag, station]
        raw_data.append(raw)
        return

    def scrape_review(self, review_url):
        """
        レビュー一覧ページのパーシング
        """
        r = requests.get(review_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{review_url}')
            return False
        soup = BeautifulSoup(r.content, 'html.parser')
        review_url_list = soup.find_all('div', class_='rvw-item')  # 口コミ詳細ページURL一覧
        if not review_url_list:
            return False
        for url in review_url_list:
            if url and url.has_attr('data-detail-url'):
                review_detail_url = 'https://tabelog.com' + url.get('data-detail-url')
                # print('\t口コミURL：', review_detail_url)
                # 口コミ의 텍스트를 가져옵니다.
                self.get_review_text(review_detail_url)
        return True

    def get_review_text(self, review_detail_url):
        """
        口コミ詳細ページをパーシング
        """
        r = requests.get(review_detail_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{review_detail_url}')
            return

        # ２回以上来訪してコメントしているユーザは最新の1件のみを採用
        # <div class="rvw-item__rvw-comment" property="v:description">
        #  <p>
        #    <br>すごい煮干しラーメン凪 新宿ゴールデン街本館<br>スーパーゴールデン1600円（20食限定）を喰らう<br>大盛り無料です<br>スーパーゴールデンは、新宿ゴールデン街にちなんで、ココ本店だけの特別メニューだそうです<br>相方と歌舞伎町のtohoシネマズの映画館でドラゴンボール超ブロリー を観てきた<br>ブロリー 強すぎるね(^^)面白かったです<br>凪の煮干しラーメンも激ウマ<br>いったん麺ちゅるちゅる感に、レアチャーと大トロチャーシューのトロけ具合もうめえ<br>煮干しスープもさすが！と言うほど完成度が高い<br>さすが食べログラーメン百名店<br>と言うか<br>2日連チャンで、近場の食べログラーメン百名店のうちの2店舗、昨日の中華そば葉山さんと今日の凪<br>静岡では考えられん笑笑<br>ごちそうさまでした
        #  </p>
        # </div>
        soup = BeautifulSoup(r.content, 'html.parser')
        review = soup.find_all('div', class_='rvw-item__rvw-comment')  # reviewが含まれているタグの中身をすべて取得
        if len(review) == 0:
            review = ''
        else:
            review = review[0].p.text.strip()  # strip()は改行コードを除外する関数

        # print('\t\t口コミテキスト：', review)
        self.review = review

        # データフレームの生成
        self.make_df()
        return

    def get_review_text(self, review_detail_url):
        """
        口コミ詳細ページをパーシング
        """
        r = requests.get(review_detail_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{review_detail_url}')
            return
        # ２回以上来訪してコメントしているユーザは最新の1件のみを採用
        # <div class="rvw-item__rvw-comment" property="v:description">
        #  <p>
        #    <br>すごい煮干しラーメン凪 新宿ゴールデン街本館<br>スーパーゴールデン1600円（20食限定）を喰らう<br>大盛り無料です<br>スーパーゴールデンは、新宿ゴールデン街にちなんで、ココ本店だけの特別メニューだそうです<br>相方と歌舞伎町のtohoシネマズの映画館でドラゴンボール超ブロリー を観てきた<br>ブロリー 強すぎるね(^^)面白かったです<br>凪の煮干しラーメンも激ウマ<br>いったん麺ちゅるちゅる感に、レアチャーと大トロチャーシューのトロけ具合もうめえ<br>煮干しスープもさすが！と言うほど完成度が高い<br>さすが食べログラーメン百名店<br>と言うか<br>2日連チャンで、近場の食べログラーメン百名店のうちの2店舗、昨日の中華そば葉山さんと今日の凪<br>静岡では考えられん笑笑<br>ごちそうさまでした
        #  </p>
        # </div>
        soup = BeautifulSoup(r.content, 'html.parser')
        review = soup.find_all('div', class_='rvw-item__rvw-comment')  # reviewが含まれているタグの中身をすべて取得
        if len(review) == 0:
            review = ''
        else:
            review = review[0].p.text.strip()  # strip()は改行コードを除外する関数
        # print('\t\t口コミテキスト：', review)
        self.review = review
        # データフレームの生成
        self.make_df()
        return

    def make_df(self):
        self.store_id = str(self.store_id_num).zfill(8)
        se = pd.Series([self.store_id, self.store_name, self.score, self.ward, self.review_cnt, self.review],
                       index=self.columns)
        self.df = self.df.append(se, ignore_index=True)

    def group_by_score(self):
        # grouped = self.df.groupby(pd.cut(self.df['score'], [1, 2, 3, 4, 5], right=False, include_lowest=True))
        grouped = self.df.groupby(pd.cut(self.df['score'], bins=[1, 2, 3, 4, 5], right=False, include_lowest=True,
                                         labels=['[1, 2)', '[2, 3)', '[3, 4)', '[4, 5)']))
        for name, group in grouped:
            print(f"평점대 {name}:")
            for _, row in group.iterrows():
                print(f"{row['store_name']} - 평점: {row['score']}")

    def save_to_json(self, file_name):
        df = pd.DataFrame(self.raw_data,
                          columns=['store_name', 'store_name_id_num', 'score', 'ward', 'review_count', 'review', 'station'])
        try:
            df.to_json(file_name, orient='records', force_ascii=False)
            print("데이터를 JSON 파일로 저장했습니다.")
        except Exception as e:
            print(f"데이터를 저장하는 중에 오류가 발생했습니다: {e}")


    def filter_by_score(self, min_score):
        filtered_df = self.df[self.df['score'] >= min_score]
        return filtered_df

    def search_by_score(self, min_score):
        filtered_df = self.filter_by_score(min_score)
        return filtered_df

    def scrape_with_retry(self, url, retries=3):
        for _ in range(retries):
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == requests.codes.ok:
                    return r
            except requests.RequestException as e:
                print(f"Request failed: {e}")
            time.sleep(1)
        return None


if __name__ == "__main__":
    # 크롤링할 역 이름 목록
    stations = ['新宿駅', '渋谷駅', '恵比寿駅', '代官山駅']  # 예시 역 이름들
    for station in stations:
        print(f"{station}에 대한 크롤링을 시작합니다.")
        tabelog_scraper = Tabelog(
            base_url="https://tabelog.com/tokyo/R9/rstLst/RC21/",
            test_mode=False, p_ward=station)
        # 데이터가 DataFrame에 제대로 로드되었는지 확인하고, JSON 파일로 저장할 수 있습니다.
        if not raw_data:
            print(f"{station}: Array is empty")
        else:
            print(f"{station}: 데이터가 올바르게 DataFrame에 로드되었습니다.")
            print(f"{station}: DataFrame 내용:")
            print(raw_data)  # 데이터 확인
            # JSON 파일로 저장
            try:
                tabelog_scraper.save_to_json(f'tabelog_data_{station}.json')  # 각 역별로 파일 저장
            except Exception as e:
                print(f"{station}: JSON 파일로 데이터를 저장하는 중에 오류가 발생했습니다: {e}")
