from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def classify_body_type(bust, waist, hips):
    k = 5  # Small threshold for rectangle type
    
    if abs(bust - hips) < k and waist < (bust + hips) / 2:
        return "Hourglass"
    elif abs(bust - hips) < k and abs(waist - (bust + hips) / 2) < k:
        return "Rectangle"
    elif bust > hips and waist < hips:
        return "Apple"
    elif hips > bust and waist < bust:
        return "Pear"
    elif bust > hips and waist < hips:
        return "Inverted Triangle"
    
    return "Unknown"

@app.route('/recommend', methods=['POST'])
def recommend_clothing():
    data = request.json
    bust = data.get('bust')
    waist = data.get('waist')
    hips = data.get('hips')
    body_type = data.get('body_type')

    if body_type is None:
        body_type = classify_body_type(bust, waist, hips)

    recommendations = {
        'Hourglass': [
            'Fitted dresses', 'Wrap tops', 'High-waisted skirts',
            'Belted coats', 'Structured blazers', 'Peplum tops',
            'V-neck dresses', 'A-line skirts'
        ],
        'Pear': [
            'A-line skirts', 'Empire waist dresses', 'Structured tops',
            'Dark-colored pants', 'Embellished tops', 'Tailored jackets',
            'Off-shoulder blouses', 'Flared jeans'
        ],
        'Apple': [
            'Straight-leg pants', 'V-neck tops', 'Draped dresses',
            'Empire waist tops', 'Wrap dresses', 'Layered outfits',
            'Long cardigans', 'Structured blazers'
        ],
        'Rectangle': [
            'Belted dresses', 'Peplum tops', 'Layered outfits',
            'Fit and flare dresses', 'A-line skirts', 'Belted tops',
            'Structured coats', 'Printed pants'
        ],
        'Inverted Triangle': [
            'Wide-leg pants', 'A-line skirts', 'Soft, flowy tops',
            'V-neck dresses', 'Belted waist tops', 'Layered outfits',
            'Culottes', 'Printed tops'
        ],
    }

    recommended_clothing = recommendations.get(body_type, [])

    return jsonify({'body_type': body_type, 'recommendations': recommended_clothing})

if __name__ == "__main__":
    app.run(port=5001)

