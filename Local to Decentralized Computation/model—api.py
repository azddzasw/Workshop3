import pickle
from flask import Flask, request, jsonify
import json
from sklearn.datasets import load_breast_cancer

# upload mode
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
data = load_breast_cancer()
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    # get parameters
    radius_mean = float(request.args.get('radius_mean'))
    texture_mean = float(request.args.get('texture_mean'))
    perimeter_mean = float(request.args.get('perimeter_mean'))
    area_mean = float(request.args.get('area_mean'))
    smoothness_mean = float(request.args.get('smoothness_mean'))

    features = [[radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean]]
    prediction = model.predict(features)

    response = {
        'prediction': int(prediction[0]),
        'class_name': data.target_names[prediction[0]]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)