from ultralytics import YOLO
import cv2

# Load pre-trained YOLO model (already trained on COCO dataset)
model = YOLO('yolov8n.pt')

# Define vehicle classes (YOLO class IDs)
vehicle_classes = {2: 'car', 3: 'motorbike', 5: 'bus', 7: 'truck'}

# Start webcam or video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO on the frame
    results = model(frame, stream=True, conf=0.4)
    counts = {'car':0, 'motorbike':0, 'bus':0, 'truck':0}

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls in vehicle_classes:
                label = vehicle_classes[cls]
                counts[label] += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Show counts
    text = f"Counts: {counts}"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.imshow("Vehicle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# from ultralytics import YOLO
# import cv2

# # Load YOLO model
# model = YOLO("yolov8n.pt")

# cap = cv2.VideoCapture(0)  # Use same webcam or separate

# vehicle_classes = ['car', 'bus', 'truck', 'motorbike']

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model(frame)

#     counts = {cls:0 for cls in vehicle_classes}
#     for result in results:
#         for box in result.boxes:
#             cls_id = int(box.cls[0])
#             cls_name = model.names[cls_id]
#             if cls_name in vehicle_classes:
#                 counts[cls_name] += 1
#                 # Draw bounding box
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
#                 cv2.putText(frame, cls_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

#     # Traffic signal logic (simple)
#     total = sum(counts.values())
#     if total > 20:
#         signal = "RED - Heavy Traffic"
#     elif 10 <= total <= 20:
#         signal = "YELLOW - Moderate Traffic"
#     else:
#         signal = "GREEN - Light Traffic"

#     cv2.putText(frame, f"Signal: {signal}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
#     cv2.imshow("ATCC Live", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
