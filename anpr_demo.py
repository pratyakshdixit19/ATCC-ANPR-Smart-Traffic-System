import cv2
import easyocr

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Start webcam (change 0 to video file path if needed)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect edges (to find plates)
    edges = cv2.Canny(gray, 100, 200)

    # Find contours (possible plates)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = w / float(h)
        if 2 < aspect_ratio < 6 and w > 100 and h > 20:
            plate = frame[y:y+h, x:x+w]
            # OCR - read text
            results = reader.readtext(plate)
            for (bbox, text, prob) in results:
                if prob > 0.4:  # confidence threshold
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                    print("Detected Plate:", text)

    cv2.imshow("ANPR Demo", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# import cv2
# import easyocr

# # Initialize OCR reader
# reader = easyocr.Reader(['en'])

# # Open webcam
# cap = cv2.VideoCapture(0)  # 0 = default webcam

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert to gray (optional)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect text
#     results = reader.readtext(gray)
    
#     for bbox, text, prob in results:
#         if prob > 0.5:
#             # Draw rectangle and text
#             top_left = tuple(bbox[0])
#             bottom_right = tuple(bbox[2])
#             cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 2)
#             cv2.putText(frame, text, (int(top_left[0]), int(top_left[1]-10)), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

#     # Display the video
#     cv2.imshow("ANPR Live", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
