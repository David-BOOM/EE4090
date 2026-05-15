import os
files = ['object_detection_ncnn_fps.py', 'object_detection_pt_fps.py', 'object_detection.py', 'object_detection_onnx_fps.py']

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Check if picamera2 is already in there
    if 'from picamera2 import Picamera2' in content:
        continue
        
    # Replace imports
    content = content.replace('import cv2', 'import cv2\nfrom picamera2 import Picamera2')
    
    # Replace cap = cv2.VideoCapture(0, cv2.CAP_V4L2) and related camera configs
    # We will use Regex for a robust replacement
    import re
    
    camera_init_patt = r'''    # Initialize.*?
    cap = cv2\.VideoCapture.*?
    cap\.set.*?
    cap\.set.*?
    cap\.set.*?

    if not cap\.isOpened\(\):
        print\("Error: Could not open the camera\."\)
        return'''
        
    picam_init = '''    # Initialize the Raspberry Pi Camera using picamera2
    try:
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        picam2.configure(config)
        picam2.start()
    except Exception as e:
        print(f"Error: Could not initialize picamera2. {e}")
        return'''
        
    content = re.sub(camera_init_patt, picam_init, content, flags=re.DOTALL)
    
    read_patt = r'''        # Read a frame from the camera
        ret, frame = cap\.read\(\)
        if not ret:
            print\("Failed to grab frame\."\)
            break'''
            
    picam_read = '''        # Read a frame from the camera using picamera2
        try:
            image_rgb = picam2.capture_array()
            # OpenCV display expects BGR
            frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Failed to grab frame: {e}")
            break'''
            
    content = re.sub(read_patt, picam_read, content)
    
    release_patt = r'''    cap\.release\(\)'''
    picam_release = '''    picam2.stop()'''
    content = re.sub(release_patt, picam_release, content)
    
    with open(f, 'w') as file:
        file.write(content)
