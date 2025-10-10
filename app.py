from flask import Flask, render_template, request, redirect, url_for
from db import insert_entry, get_latest_entry, get_all_entries, delete_entry_from_db

app = Flask(__name__)

def calculate_emissions(meal, transport, computer_hours):
    # 탄소 배출량 데이터 (예시)
    emission_data = {
        "소고기": 13,  # 500g CO2e per serving
        "돼지고기": 3.5,
        "닭고기": 3,
        "쌀": 2,
        "채소": 0.5,
        "생선": 2.5
    }

    # 식사 배출량 계산
    meal_emission = 0
    for ingredient in emission_data:
        if ingredient in meal:
            meal_emission += emission_data[ingredient]

    # 교통수단 배출량 계산
    transport_emission = 0
    if "자동차" in transport:
        transport_emission = 0.21 * 10  # 0.21 kg CO2e per km, 가정: 10km 이동
    elif "버스" in transport:
        transport_emission = 0.05 * 10  # 0.05 kg CO2e per km
    elif "기차" in transport:
        transport_emission = 0.04 * 10  # 0.04 kg CO2e per km
    elif "비행기" in transport:
        transport_emission = 0.15 * 10  # 0.15 kg CO2e per km
    else:
        transport_emission = 0.01 * 10  # 기본값

    # 컴퓨터 사용 배출량 계산
    # 평균 전력 소비량 100W, 1kWh 당 0.5 kg CO2e
    computer_emission = (100 / 1000) * computer_hours * 0.5

    # 총 배출량 계산
    total = meal_emission + transport_emission + computer_emission
    return meal_emission, transport_emission, computer_emission, total

# 메인 페이지 (홈)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":                # 사용자가 기록을 입력했을 때
        meal = request.form.getlist("meal[]")   # 여러 개의 식사 내용 리스트로 받기
        transport = request.form["transport"]   # 교통수단
        computer = request.form["computer"]     # 컴퓨터 사용시간 (문자열로 들어옴)

        # 숫자만 안전하게 추출
        try:
            computer_val = float(computer.split()[0])
        except:
            computer_val = 0.0

        # 탄소 배출량 계산
        _, _, _, total = calculate_emissions(meal, transport, computer_val)
        
        # DB에 저장 (음식 리스트를 문자열로 저장)
        insert_entry(", ".join(meal), transport, computer_val, total)

        # 저장 후 새로고침 (중복 입력 방지)
        return redirect(url_for("index"))
    
    # 최근 입력값과 전체 기록 불러오기
    latest_entry = get_latest_entry()
    diary = get_all_entries()
    # 최신 기록이 있으면 계산식 정보 추가
    if latest_entry:
        # DB에 저장된 값에서 필요한 정보 추출 (dict 접근)
        meal = latest_entry['meal'].split(", ") if latest_entry.get('meal') else []
        transport = latest_entry.get('transport', '')
        computer_val = float(latest_entry.get('computer_hours', 0.0)) if latest_entry.get('computer_hours') else 0.0
        meal_emission, transport_emission, computer_emission, total = calculate_emissions(meal, transport, computer_val)
        latest = {
            'emissions': latest_entry.get('emissions', 0.0),
            'meal_emission': round(meal_emission, 2),
            'transport_emission': round(transport_emission, 2),
            'computer_emission': round(computer_emission, 2),
            'meal': latest_entry.get('meal', ''),
            'transport': latest_entry.get('transport', ''),
            'computer': latest_entry.get('computer_hours', 0.0),
            'date': latest_entry.get('entry_date', '')
        }
    else:
        latest = None
    # index.html 템플릿 렌더링
    return render_template("index.html", latest=latest, diary=diary)

# 다이어리 전체 페이지
@app.route("/diary")
def diary_page():
    diary = get_all_entries()
    return render_template("diary.html", diary=diary)

# 데이터베이스에서 특정 기록 삭제
@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    delete_entry_from_db(entry_id)
    return redirect(url_for("index"))

# 개발용 서버 실행
if __name__ == "__main__":
    app.run(debug=True)     

