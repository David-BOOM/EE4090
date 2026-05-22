import cv2
import time
import numpy as np
from picamera2 import Picamera2

# Try importing from TFLite runtime for Raspberry Pi, fallback to standard TensorFlow
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite.python.interpreter import Interpreter

def main():
    # Load the EfficientDet TFLite model
    print("Loading EfficientDet TFLite model...")
    model_path = 'efficientdet_lite0.tflite'
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_shape = input_details[0]['shape']
    input_height, input_width = input_shape[1], input_shape[2]

    # Initialize the Raspberry Pi Camera using picamera2
    try:
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        picam2.configure(config)
        picam2.start()
    except Exception as e:
        print(f"Error: Could not initialize picamera2. {e}")
        return

    print("Starting object detection (EfficientDet). Press 'q' to quit.")

    prev_time = time.time()

    while True:
        # Read a frame from the camera using picamera2 (already in RGB format)
        try:
            image_rgb = picam2.capture_array()
            # OpenCV display expects BGR
            frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Failed to grab frame: {e}")
            break
        
        # Resize to expected input size
        image_resized = cv2.resize(image_rgb, (input_width, input_height))
        
        # EfficientDet-lite usually expects uint8 inputs, expand dimension to [1, height, width, 3]
        input_data = np.expand_dims(image_resized, axis=0)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # The outputs for EfficientDet-Lite are usually:
        # [0]: boxes [1, num_detections, 4]
        # [1]: classes [1, num_detections] 
        # [2]: scores [1, num_detections]
        # [3]: num_detections [1]
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        classes = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]

        h, w, _ = frame.shape
        # Draw bounding boxes
        for i in range(len(scores)):
            if scores[i] > 0.5: # Confidence threshold
                # Boxes are normally normalized [ymin, xmin, ymax, xmax]
                ymin, xmin, ymax, xmax = boxes[i]
                start_point = (int(xmin * w), int(ymin * h))
                end_point = (int(xmax * w), int(ymax * h))
                
                cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                
                label = f"Class {int(classes[i])}: {scores[i]:.2f}"
                cv2.putText(frame, label, (start_point[0], start_point[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the output
        cv2.imshow("Raspberry Pi Object Detection - EfficientDet", frame)

        # Check for the 'q' key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
