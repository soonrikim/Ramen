from tabelog_scraper import Tabelog
import json

# Tabelog 클래스의 인스턴스 생성
tokyo_food_review = Tabelog(base_url="https://tabelog.com/rstLst/?Srt=D&SrtT=rvcn&svd=20231105&svt=1900&svps=2", test_mode=False, p_ward='日本全体')

# 별점에 따라 그룹화하여 출력
tokyo_food_review.group_by_score()

# 데이터가 DataFrame에 제대로 로드되었는지 확인하고, JSON 파일로 저장할 수 있습니다.
if not tokyo_food_review.df.empty:
    print("데이터가 올바르게 DataFrame에 로드되었습니다.")
    print("DataFrame 내용:")
    print(tokyo_food_review.df.head())  # 데이터 확인

    # JSON 파일로 저장
    try:
        tokyo_food_review.save_to_json('tabelog_data.json')  # 'tabelog_data.json' 파일에 데이터 저장
    except Exception as e:
        print(f"JSON 파일로 데이터를 저장하는 중에 오류가 발생했습니다: {e}")
else:
    print("데이터를 로드하지 못했거나 DataFrame이 비어 있습니다.")
