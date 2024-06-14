import cv2

from flask import Flask, request, jsonify
from flask_cors import CORS
import generate_test_case_text
import generate_test_case_image
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    if request.is_json:
        data = request.get_json()
        print(data)
        
        testCaseType = data.get('testCaseType')
        language = data.get('language')
        checkboxes = data.get('checkboxes')
        numberOfTestCases = data.get('numberOfTestCases')
        scenario = data.get('scenario')
        
        if testCaseType and language and checkboxes is not None and numberOfTestCases and scenario:
            try:
                result = generate_test_case_text.modify_prompt(
                    testCaseType, language, scenario, checkboxes, numberOfTestCases
                )
                return jsonify({'result': result})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'One or more parameters are missing'}), 400
    else:
        return jsonify({'error': 'Unsupported media type. Expected JSON data.'}), 415

@app.route('/generate_image', methods=['POST'])
def generate_image():
    if 'image' not in request.files:
        print("No image file part")
        return jsonify({'error': 'No image file part'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    try:
        nparr = np.frombuffer(image_file.read(), np.uint8)
        decoded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = Image.fromarray(decoded_image)
        
        # Convert the form data to a dictionary
        data = request.form.to_dict()
        # Convert the checkboxes into a list if they are sent as multiple values
        checkboxes = request.form.getlist('checkboxes')
        
        testCaseType = data.get('testCaseType')
        language = data.get('language')
        numberOfTestCases = data.get('numberOfTestCases')

        if testCaseType and language and checkboxes and numberOfTestCases:
            result = generate_test_case_image.modify_prompt(
                testCaseType, language, checkboxes, numberOfTestCases, image
            )
            print("Result from app.py",result)
            return jsonify({'result': result})
        else:
            print("One or more parameters are missing")
            return jsonify({'error': 'One or more parameters are missing'}), 400
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host='192.168.14.121',port=3001)