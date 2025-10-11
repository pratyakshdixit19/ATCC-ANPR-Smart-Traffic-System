# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import cv2
# import easyocr
# import numpy as np
# import os

# app = Flask(__name__)
# CORS(app)

# # Initialize OCR reader
# reader = easyocr.Reader(['en'])

# @app.route('/')
# def home():
#     return jsonify({"message": "ANPR Backend is running!"})

# @app.route('/detect_plate', methods=['POST'])
# def detect_plate():
#     try:
#         # Step 1: Save uploaded image
#         file = request.files['image']
#         file_path = "temp.jpg"
#         file.save(file_path)

#         # Step 2: Read image
#         img = cv2.imread(file_path)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # Step 3: Enhance clarity for detection
#         bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
#         edged = cv2.Canny(bfilter, 30, 200)

#         # Step 4: Find contours
#         keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         contours = keypoints[0] if len(keypoints) == 2 else keypoints[1]
#         contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

#         location = None
#         for contour in contours:
#             approx = cv2.approxPolyDP(contour, 10, True)
#             if len(approx) == 4:
#                 location = approx
#                 break

#         plate_text = "Not detected"
#         if location is not None:
#             mask = np.zeros(gray.shape, np.uint8)
#             new_image = cv2.drawContours(mask, [location], 0, 255, -1)
#             new_image = cv2.bitwise_and(img, img, mask=mask)

#             (x, y) = np.where(mask == 255)
#             (x1, y1) = (np.min(x), np.min(y))
#             (x2, y2) = (np.max(x), np.max(y))
#             cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

#             # Step 5: Preprocess the cropped plate before OCR
#             cropped_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
#             cropped_image = cv2.bilateralFilter(cropped_image, 11, 17, 17)
#             cropped_image = cv2.threshold(cropped_image, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#             # Step 6: OCR with better accuracy
#             results = reader.readtext(cropped_image, detail=0, paragraph=False)

#             if results:
#                 raw_text = " ".join(results)
#                 # Step 7: Clean unwanted symbols and fix spacing
#                 import re
#                 clean_text = re.sub(r'[^A-Z0-9 ]+', '', raw_text.upper())
#                 clean_text = re.sub(r'\s+', ' ', clean_text).strip()
#                 plate_text = clean_text

#         os.remove(file_path)
#         return jsonify({"plate": plate_text})

#     except Exception as e:
#         return jsonify({"error": str(e)})



# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import easyocr
import numpy as np
import os
from atcc import analyze_traffic  # import function

app = Flask(__name__)
CORS(app)

# Initialize OCR reader
reader = easyocr.Reader(['en'])

@app.route('/')
def home():
    return jsonify({"message": "ANPR Backend is running!"})

@app.route('/detect_plate', methods=['POST'])
def detect_plate():
    try:
        # Get uploaded image
        file = request.files['image']
        file_path = "temp.jpg"
        file.save(file_path)

        # Read image
        img = cv2.imread(file_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use EasyOCR to read text from image
        results = reader.readtext(gray)

        # Extract detected texts
        plates = [res[1] for res in results if len(res[1]) >= 4]

        # Cleanup
        os.remove(file_path)

        if plates:
            return jsonify({"plates": plates})
        else:
            return jsonify({"message": "No plate detected!"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/analyze_traffic', methods=['POST'])
def analyze_traffic_route():
    try:
        file = request.files['image']
        file_path = "temp_traffic.jpg"
        file.save(file_path)

        result = analyze_traffic(file_path)
        os.remove(file_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
