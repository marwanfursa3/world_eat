from flask import Flask, render_template, request
import json

app = Flask(__name__)


# Route to render index.html
@app.route("/")
def index():
    return render_template("index.html")


# Route for search
@app.route("/search")
def search():
    query = request.args.get("query", "").strip().lower()  # מקבל את המחרוזת שהוזנה ומוודא שאין רווחים
    try:
        # קורא את המידע מקובץ JSON
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)  # טוען את המידע
        # מסנן את התוצאות כך שיתאימו לשאילתה שהוזנה
        results = [
            item for item in data if query in item["name"].lower()
        ]
    except Exception as e:
        print("Error loading data:", e)
        results = []

    print("Query:", query)  # הדפסת המחרוזת לשם אבחנה
    print("Results:", results)  # הדפסת התוצאות לשם אבחנה

    return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
