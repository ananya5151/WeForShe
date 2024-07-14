from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS  # type: ignore
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
import joblib
from sklearn.preprocessing import LabelEncoder # type: ignore
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
    recommendations =  {
        'Brown': [
    {'name': 'Olive Green', 'hex': '#808000'},
    {'name': 'Rust', 'hex': '#B7410E'},
    {'name': 'Terracotta', 'hex': '#E76E54'},
    {'name': 'Beige', 'hex': '#F5F5DC'},
    {'name': 'Emerald Green', 'hex': '#50C878'},
    {'name': 'Royal Blue', 'hex': '#4169E1'},
    {'name': 'Rich Purple', 'hex': '#6A0DAD'},
    {'name': 'Deep Red', 'hex': '#8B0000'}
],
        'Dark': [
    {'name': 'Bright Yellow', 'hex': '#FFD700'},
    {'name': 'Turquoise', 'hex': '#40E0D0'},
    {'name': 'Cobalt Blue', 'hex': '#0047AB'},
    {'name': 'Fuchsia', 'hex': '#FF00FF'},
    {'name': 'Crimson Red', 'hex': '#DC143C'},
    {'name': 'Emerald Green', 'hex': '#50C878'},
    {'name': 'White', 'hex': '#FFFFFF'},
    {'name': 'Coral', 'hex': '#FF7F50'}
],

       'Olive': [
    {'name': 'Earthy Tones', 'hex': '#8B4513'},
    {'name': 'Dusty Pink', 'hex': '#DDA0DD'},   
    {'name': 'Teal', 'hex': '#008080'},         
    {'name': 'Mustard Yellow', 'hex': '#FFD700'}, 
    {'name': 'Soft Lavender', 'hex': '#E6E6FA'}, 
    {'name': 'Warm Beige', 'hex': '#F5F5DC'},  
    {'name': 'Burnt Orange', 'hex': '#CC5500'}, 
    {'name': 'Deep Purple', 'hex': '#6A0DAD'}   
],
        'Dusky': [
    {'name': 'Peach', 'hex': '#FFDAB9'},
    {'name': 'Lavender', 'hex': '#E6E6FA'},
    {'name': 'Teal', 'hex': '#008080'},
    {'name': 'Deep Purple', 'hex': '#6A0DAD'},
    {'name': 'Coral', 'hex': '#FF7F50'},
    {'name': 'Emerald Green', 'hex': '#50C878'},
    {'name': 'Burgundy', 'hex': '#800020'},
    {'name': 'Copper', 'hex': '#B87333'}
],
        'Wheatish': [
    {'name': 'Soft Peach', 'hex': '#FFDAB9'},
    {'name': 'Pastel Yellow', 'hex': '#FFFACD'},
    {'name': 'Turquoise', 'hex': '#40E0D0'},
    {'name': 'Dusty Rose', 'hex': '#D3A6B0'},
    {'name': 'Lavender', 'hex': '#E6E6FA'},
    {'name': 'Olive Green', 'hex': '#808000'},
    {'name': 'Rust Orange', 'hex': '#B7410E'},
    {'name': 'Warm Gray', 'hex': '#A89F91'}
],
       'Fair': [
    {'name': 'Pastel Pink', 'hex': '#FFB6C1'},
    {'name': 'Light Blue', 'hex': '#ADD8E6'},
    {'name': 'Lavender', 'hex': '#E6E6FA'},
    {'name': 'Soft Mint', 'hex': '#98FF98'},
    {'name': 'Coral', 'hex': '#FF7F50'},
    {'name': 'Cream', 'hex': '#FFFDD0'},
    {'name': 'Light Gray', 'hex': '#D3D3D3'},
    {'name': 'Peach', 'hex': '#FFDAB9'}
],
    }

    recommended_colors = recommendations.get(skin_tone, [])
    return jsonify(recommended_colors)

if __name__ == '__main__':
    app.run(debug=True)