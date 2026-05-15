import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

def main():
    # Load the YOLO26 nano model (lightweight, recommended for Raspberry Pi 4)
    # Make sure to export the model first using: yolo export model=yolo26n.pt format=ncnn
    print("Loading YOLO26 NCNN model...")
    model = YOLO('yolo26n_ncnn_model')

    # Initialize the Raspberry Pi Camera using picamera2
    try:
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        picam2.configure(config)
        picam2.start()
    except Exception as e:
        print(f"Error: Could not initialize picamera2. {e}")
        return

    print("Starting object detection. Press 'q' to quit.")

    while True:
        # Read a frame from the camera using picamera2
        try:
            image_rgb = picam2.capture_array()
            # OpenCV display expects BGR
            frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Failed to grab frame: {e}")
            break

        # Run object detection on the frame and disable verbose logging for leaner output
        results = model(frame, stream=True, verbose=False)

        # Ensure we draw the bounding boxes on the frame
        annotated_frame = frame
        for result in results:
            annotated_frame = result.plot()

        # Display the output
        cv2.imshow("Raspberry Pi Object Detection", annotated_frame)

        # Check for the 'q' key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
