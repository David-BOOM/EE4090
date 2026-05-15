import os
import warnings

# Suppress OpenCV Qt font warnings and PyTorch CPU warnings
os.environ['QT_LOGGING_RULES'] = '*font*=false'
warnings.filterwarnings('ignore', category=UserWarning)

import cv2
import pytesseract
from pytesseract import Output
from picamera2 import Picamera2

import threading
import time

# Global variables for multithreading (Optimization 1)
latest_roi_bw = None
cached_results = None
lock = threading.Lock()
running = True

def ocr_worker():
    """Background thread to run Tesseract without blocking the camera feed."""
    global cached_results, running, latest_roi_bw
    
    # Optimization 3: Custom config
    custom_config = r'--oem 1 --psm 11'

    while running:
        with lock:
            if latest_roi_bw is None:
                frame_to_process = None
            else:
                frame_to_process = latest_roi_bw.copy()
        
        if frame_to_process is not None:
            # Run OCR on the binarized frame
            res = pytesseract.image_to_data(frame_to_process, output_type=Output.DICT, config=custom_config)
            
            with lock:
                cached_results = res

def main():
    global latest_roi_bw, cached_results, running
    print("Initializing Asynchronous Tesseract OCR...")

    # Initialize Picamera2
    picam2 = Picamera2()
    # Configure the camera resolution - this avoids the V4L2 overhead
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    # Start the background OCR thread
    ocr_thread = threading.Thread(target=ocr_worker, daemon=True)
    ocr_thread.start()

    print("Starting live text recognition. Press 'q' to quit.")

    prev_time = time.time()

    while True:
        # Calculate FPS
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        # Grab the latest frame directly from the Pi's memory pipeline
        frame = picam2.capture_array()
        
        # Convert RGB (Picamera2 default) to BGR (OpenCV default) to prevent color bugs
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Optimization 4: Turn whole frame into black and white (Otsu threshold) first
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bw_frame = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Define ROI: 55% of width and 55% of height
        h, w = frame.shape[:2]
        roi_w, roi_h = int(w * 0.55), int(h * 0.55)
        x1, y1 = int((w - roi_w) / 2), int((h - roi_h) / 2)
        x2, y2 = x1 + roi_w, y1 + roi_h

        # Extract the region of interest from the B&W frame
        roi_bw = bw_frame[y1:y2, x1:x2]

        # Pass the B&W ROI to the OCR worker thread
        with lock:
            latest_roi_bw = roi_bw
            res_copy = cached_results

        # Draw the ROI box indicating the OCR area on the BGR frame for display
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Draw the cached bounding boxes
        if res_copy is not None:
            for i in range(len(res_copy['text'])):
                text = res_copy['text'][i].strip()
                conf = int(res_copy['conf'][i])
                
                if conf > 40 and text:
                    x = res_copy['left'][i]
                    y = res_copy['top'][i]
                    w_box = res_copy['width'][i]
                    h_box = res_copy['height'][i]
                    
                    tl = (x + x1, y + y1)
                    br = (x + w_box + x1, y + h_box + y1)

                    cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
                    cv2.putText(
                        frame, f"{text} ({conf}%)", (tl[0], tl[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                    )

        # Draw FPS
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the BGR output
        cv2.imshow("Raspberry Pi Live Text Recognition", frame)

        # Check for the 'q' key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    # Release resources
    ocr_thread.join(timeout=1.0)
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
