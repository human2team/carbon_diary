from flask import Flask, render_template, request, redirect, url_for
from db import insert_entry, get_latest_entry, get_all_entries

app = Flask(__name__)

def calculate_emissions(meal, transport, computer_hours):
    meal_emission = 2 if "고기" in meal else 1
    transport_emission = 5 if "자동차" in transport else 1
    computer_emission = float(computer_hours) * 0.5
    total = meal_emission + transport_emission + computer_emission
    return meal_emission, transport_emission, computer_emission, total

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        meal = request.form["meal"]
        transport = request.form["transport"]
        computer = request.form["computer"]

        # 숫자만 안전하게 추출
        try:
            computer_val = float(computer.split()[0])
        except:
            computer_val = 0.0

        _, _, _, total = calculate_emissions(meal, transport, computer_val)
        insert_entry(meal, transport, computer_val, total)

        return redirect(url_for("index"))

    latest = get_latest_entry()
    diary = get_all_entries()
    return render_template("index.html", latest=latest, diary=diary)

@app.route("/diary")
def diary_page():
    diary = get_all_entries()
    return render_template("diary.html", diary=diary)

if __name__ == "__main__":
    app.run(debug=True)
