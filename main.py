import cv2
import os
import numpy as np
import glob
import json

print("Urban Parcel Mapping - Final Version")

IMAGE_FOLDER = "images"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PIXELS_PER_FOOT = 2.0
SQFT_PER_PIXEL = 1 / (PIXELS_PER_FOOT ** 2)

image_paths = glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg"))
print(f"Found {len(image_paths)} images")

for IMAGE_PATH in image_paths:
    print(f"\nProcessing {IMAGE_PATH}...")
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((20,20), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = img.copy()
    count = 0
    total_sqft = 0
    parcel_data = []   # <-- digital twin-ku data store pannrom

    for c in contours:
        area = cv2.contourArea(c)
        if area > 8000:
            count += 1
            x, y, w, h = cv2.boundingRect(c)
            area_sqft = area * SQFT_PER_PIXEL
            total_sqft += area_sqft

            cv2.rectangle(result, (x,y), (x+w, y+h), (0, 255, 0), 4)
            cv2.putText(result, f"Plot {count}", (x, y-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(result, f"Area: {area_sqft:.1f} sqft", (x, y+h+25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

            # ---- Digital twin-ku plot details store pannrom ----
            parcel_data.append({
                "plot_id": count,
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "area_sqft": round(area_sqft, 1)
            })

    base_name = os.path.basename(IMAGE_PATH).split('.')[0]
    out_path = os.path.join(OUTPUT_DIR, f"{base_name}_parcel_map.jpg")
    cv2.imwrite(out_path, result)

    # ---- JSON file save pannrom (digital twin data source) ----
    json_path = os.path.join(OUTPUT_DIR, f"{base_name}_data.json")
    with open(json_path, "w") as f:
        json.dump({
            "image": out_path.replace("\\", "/"),
            "total_parcels": count,
            "total_sqft": round(total_sqft, 1),
            "parcels": parcel_data
        }, f, indent=2)

    print(f" -> Saved {out_path} | Found {count} parcels | Total: {total_sqft:.1f} sqft")
    print(f" -> Digital twin data saved: {json_path}")

print("\nAll Done!")