from tabelog_scraper import Tabelog

# Tabelog 클래스의 인스턴스 생성
tokyo_food_review = Tabelog(base_url="https://tabelog.com/rstLst/?vs=1&sa=&sk=&lid=top_navi1&vac_net=&svd=20231029&svt=1900&svps=2&hfc=1&sw=", test_mode=False, p_ward='日本全国')

# 별점대로 그룹화하여 출력
tokyo_food_review.group_by_score()

# 크롤링 결과를 JSON 파일로 저장
tokyo_food_review.df.to_json("tabelog_data.json")
