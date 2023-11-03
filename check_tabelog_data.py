import pandas as pd

# JSON 파일에서 데이터를 DataFrame으로 읽어오기
try:
    df = pd.read_json("tabelog_data.json")
    print("JSON 파일을 DataFrame으로 성공적으로 읽었습니다.")
    print("DataFrame 내용:")
    print(df)

    # JSON 파일을 다시 저장하기 (추가 작업 혹은 수정 후)
    # 수정 작업은 여기에 수행합니다.

    # 수정된 DataFrame을 JSON 파일로 다시 저장
    df.to_json("updated_tabelog_data.json")
    print("수정된 데이터를 JSON 파일에 성공적으로 저장했습니다.")

except Exception as e:
    print(f"JSON 파일을 읽는 중에 오류가 발생했습니다: {e}")
