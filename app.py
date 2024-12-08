from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# נתיב הקובץ JSON
data_file = 'data.json'

# דף הבית
@app.route('/')
def index():
    return render_template('index.html')


# Route לחיפוש
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return "No query provided", 400

    # קריאת המידע מקובץ JSON
    with open(data_file, 'r') as file:
        data = json.load(file)

    # חיפוש לפי שם
    results = [item for item in data if query.lower() in item['name'].lower()]
    return render_template('search.html', results=results, query=query)


# Route להעלאת מתכון
@app.route('/upload', methods=['POST'])
def upload():
    # קבלת נתונים מהטופס
    recipe_name = request.form.get('recipe_name')
    recipe_description = request.form.get('recipe_description')
    recipe_image = request.files['recipe_image']

    # יצירת התיקייה אם היא לא קיימת
    upload_folder = os.path.join('static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)  # יצירת התיקייה
    
    if recipe_image:
        # שמירת התמונה לתיקייה סטטית
        image_path = os.path.join(upload_folder, recipe_image.filename)
        recipe_image.save(image_path)

    # כתיבת המידע ל-json
    with open(data_file, 'r') as file:
        data = json.load(file)

    new_recipe = {
        "name": recipe_name,
        "description": recipe_description,
        "image": f"/static/uploads/{recipe_image.filename}"
    }

    # הוספת המתכון למערך הקיים
    data.append(new_recipe)

    # שמירת המידע חזרה לקובץ JSON
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

    return "Recipe uploaded successfully!"


# הרצת השרת
if __name__ == '__main__':
    # יצירת קובץ JSON בסיסי אם לא קיים
    if not os.path.exists(data_file):
        with open(data_file, 'w') as file:
            json.dump([], file)  # אתחול הקובץ כ-array ריק
    app.run(debug=True)
