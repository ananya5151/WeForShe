from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('skin_tone_colors_dataset.csv')
df.dropna(inplace=True)

# Encode categorical variables
le_skin_tone = LabelEncoder()
le_color = LabelEncoder()

df['Skin Tone'] = le_skin_tone.fit_transform(df['Skin Tone'])
df['Color 1'] = le_color.fit_transform(df['Color 1'])
df['Color 2'] = le_color.fit_transform(df['Color 2'])
df['Color 3'] = le_color.fit_transform(df['Color 3'])
df['Color 4'] = le_color.fit_transform(df['Color 4'])
df['Color 5'] = le_color.fit_transform(df['Color 5'])

# Function to train and recommend colors based on skin tone
def recommend_colors(skin_tone):
    skin_tone_encoded = le_skin_tone.transform([skin_tone])[0]
    recommended_colors = []

    for color_column in ['Color 1', 'Color 2', 'Color 3', 'Color 4', 'Color 5']:
        X = df[['Skin Tone']]
        y = df[color_column]
        model = RandomForestClassifier()
        model.fit(X, y)
        skin_tone_encoded_arr = [[skin_tone_encoded]]
        color_prob = model.predict_proba(skin_tone_encoded_arr)[0]
        recommended_color_idx = color_prob.argmax()
        recommended_color = le_color.inverse_transform([recommended_color_idx])[0]
        recommended_colors.append(recommended_color)

    return recommended_colors

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    skin_tone = data['skin_tone']
    recommendations = recommend_colors(skin_tone)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
