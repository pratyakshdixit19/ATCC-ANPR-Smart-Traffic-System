from ultralytics import YOLO
import cv2
import time

# Load pre-trained YOLOv8 model (small version for speed)
model = YOLO('yolov8n.pt')  # downloads automatically if not present

# Define the vehicle classes we care about
vehicle_classes = ['car', 'bus', 'truck', 'motorbike']

def analyze_traffic(image_path):
    # Read the image
    frame = cv2.imread(image_path)
    results = model(frame)  # detect objects

    # Count detected vehicles
    counts = {cls: 0 for cls in vehicle_classes}
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            if cls_name in counts:
                counts[cls_name] += 1

    # Simulate traffic control logic
    total_vehicles = sum(counts.values())
    if total_vehicles > 20:
        signal_status = "🔴 Heavy traffic — Increase green light duration!"
    elif 10 <= total_vehicles <= 20:
        signal_status = "🟡 Moderate traffic — Normal signal cycle."
    else:
        signal_status = "🟢 Light traffic — Shorter green light."

    return {
        "counts": counts,
        "total_vehicles": total_vehicles,
        "signal_status": signal_status
    }


if __name__ == "__main__":
    img = "traffic1.webp"  # replace with your traffic image
    result = analyze_traffic(img)
    print(result)
