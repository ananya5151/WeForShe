from flask import Flask, request, jsonify
from flask_cors import CORS 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.preprocessing import LabelEncoder
import os

# Load or train the model
model_path = 'skin_tone_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    # Load your dataset
    df = pd.read_csv('C:/Users/anany/OneDrive/Desktop/WeForShe/colour-theroy/skin_tone_colors_dataset.csv')

    # Check for missing values
    print("Missing values:\n", df.isnull().sum())

    # Ensure the 'Skin Tone' column exists
    if 'Skin Tone' in df.columns:
        df.dropna(subset=['Skin Tone'], inplace=True)

        # Map skin tones to categories
        df['Skin Tone Category'] = df['Skin Tone']

        # Prepare features and labels
        features = df[['Color 1', 'Color 2', 'Color 3', 'Color 4', 'Color 5']]
        labels = df['Skin Tone Category']

        le = LabelEncoder()
        for column in features.columns:
            features.loc[:, column] = le.fit_transform(features[column])  # Use .loc to avoid warnings

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Train the model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Save the model
        joblib.dump(model, model_path)
    else:
        raise KeyError("The required column 'Skin Tone' is missing from the dataset.")

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend_colors():
    data = request.json
    skin_tone = data.get('skin_tone')

    # Example mapping (this should be adjusted based on your dataset)
    recommendations = {
        'Brown': ['#A52A2A', '#DEB887', '#D2691E'],
        'Dark': ['#4B0082', '#000000', '#800000'],
        'Olive': ['#808000', '#F0E68C', '#ADFF2F'],
        'Dusky': ['#A0522D', '#CD853F', '#D2691E'],
        'Wheatish': ['#F5DEB3', '#FFD700', '#FFDAB9'],
        'Fair': ['#FFFACD', '#FFE4B5', '#FFEFD5']
    }

    recommended_colors = recommendations.get(skin_tone, [])
    return jsonify(recommended_colors)

if __name__ == '__main__':
    app.run(debug=True)