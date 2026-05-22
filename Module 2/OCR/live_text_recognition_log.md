# Development Log: Raspberry Pi Live Text Recognition Application

**Total Logged Effort:** 9 Hours

* Installed EasyOCR and explicitly configured for CPU backend
* Configured V4L2 backend for NoIR Camera Board V2
* Built loop for frame capture and grayscale conversion
* Implemented EasyOCR readtext to extract text and bounding boxes
* Rendered bounding boxes and parsed text onto live frame
* Tested on device; found extreme latency and very low FPS
* Reduced inference frame resolution to 320x240 to improve FPS
* Implemented manual V4L2 queue flush to dump stale frames
* Restored native 640x480 display resolution for the output window
* Decoupled EasyOCR inference resolution from camera display resolution
* Added coordinate scaling logic to correctly align bounding boxes
* Encountered Qt font and PyTorch pin_memory runtime terminal warnings
* Injected QT_LOGGING_RULES environment variable to silence OpenCV UI
* Applied warnings filter to safely mask PyTorch CPU loader flags
* Conducted final testing to ensure real-time >1 FPS processing
* Replaced EasyOCR with Tesseract for higher Pi efficiency
* Switched capture backend from OpenCV V4L2 to Picamera2 to remove buffer lag
* Constrained OCR to center ROI (50% width, 25% height)
* Implemented Otsu binarization on whole frame prior to ROI extraction
* Decoupled OCR processing into background daemon thread
* Applied custom Tesseract parameters (--oem 1 --psm 11) for fast inference
* Added RGB to BGR frame conversion for Picamera2 output

**EasyOCR vs Tesseract Comparison:**
* EasyOCR: deep-learning based, highly accurate, heavy resource usage
* EasyOCR: extreme latency on Raspberry Pi 4 CPU
* Tesseract: lightweight architecture, highly efficient for edge devices
* Tesseract: lower accuracy on complex backgrounds, exceptionally fast inference