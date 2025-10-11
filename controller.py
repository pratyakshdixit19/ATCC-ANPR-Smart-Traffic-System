def compute_green_times(counts, total_cycle=90):
    """
    counts: dict of direction -> vehicle_count
    total_cycle: total cycle length (seconds)
    """
    total = sum(counts.values())
    if total == 0:
        # no vehicles, equal distribution
        return {d: total_cycle // len(counts) for d in counts}
    
    # proportional allocation
    times = {}
    for d, c in counts.items():
        times[d] = int((c / total) * total_cycle)
        if times[d] < 10:
            times[d] = 10  # minimum 10s green

    return times


# Example usage
if __name__ == "__main__":
    traffic_counts = {'North': 10, 'South': 20, 'East': 5, 'West': 15}
    result = compute_green_times(traffic_counts)
    print("Green Light Allocation (in seconds):")
    for direction, sec in result.items():
        print(f"{direction}: {sec}s")


# import cv2
# import easyocr
# from ultralytics import YOLO

# # Initialize models
# reader = easyocr.Reader(['en'])
# yolo_model = YOLO("yolov8n.pt")

# vehicle_classes = ['car', 'bus', 'truck', 'motorbike']
# cap = cv2.VideoCapture(0)  # Single webcam

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # --- ANPR ---
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     plate_results = reader.readtext(gray)
#     for bbox, text, prob in plate_results:
#         if prob > 0.5:
#             top_left = tuple(bbox[0])
#             bottom_right = tuple(bbox[2])
#             cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 2)
#             cv2.putText(frame, text, (int(top_left[0]), int(top_left[1]-10)), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

#     # --- ATCC ---
#     results = yolo_model(frame)
#     counts = {cls:0 for cls in vehicle_classes}
#     for result in results:
#         for box in result.boxes:
#             cls_id = int(box.cls[0])
#             cls_name = yolo_model.names[cls_id]
#             if cls_name in vehicle_classes:
#                 counts[cls_name] += 1
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
#                 cv2.putText(frame, cls_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

#     total = sum(counts.values())
#     if total > 20:
#         signal = "RED - Heavy Traffic"
#     elif 10 <= total <= 20:
#         signal = "YELLOW - Moderate Traffic"
#     else:
#         signal = "GREEN - Light Traffic"

#     cv2.putText(frame, f"Signal: {signal}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
#     cv2.imshow("Smart Traffic Management", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
