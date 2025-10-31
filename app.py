from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['ingredients'].strip().lower()

    if not text:
        return "<h3>Please enter at least one ingredient!</h3><a href='/'>Go Back</a>"

    user_ingredients = [i.strip() for i in text.split(',') if i.strip()]

    try:
        df = pd.read_csv('database/ingredients.csv')
    except Exception as e:
        return f"<h3>Error loading dataset: {e}</h3>"

    results = []
    score = 0

    for ing in user_ingredients:
        match = df[df['Ingredient'].str.lower() == ing]
        if not match.empty:
            impact = match['Impact'].values[0]
            side_effects = match['Side_Effects'].values[0]

            if impact.lower() == 'safe':
                score += 1
            elif impact.lower() == 'harmful':
                score -= 1

            results.append({"ingredient": ing, "impact": impact, "side_effects": side_effects})
        else:
            results.append({"ingredient": ing, "impact": "Unknown", "side_effects": "Not found in dataset"})

    if score > 0:
        status = "✅ Safe Product"
    elif score == 0:
        status = "⚠️ Moderate Product"
    else:
        status = "❌ Harmful Product"

    return render_template('result.html', results=results, status=status)

if __name__ == '__main__':
    app.run(debug=True)
