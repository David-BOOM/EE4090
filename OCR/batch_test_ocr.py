import os
import cv2
import pytesseract
from pytesseract import Output
import glob
import warnings

# Suppress OpenCV Qt font warnings and PyTorch CPU warnings
os.environ['QT_LOGGING_RULES'] = '*font*=false'
warnings.filterwarnings('ignore', category=UserWarning)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "M2-Images")
    results_base_dir = os.path.join(base_dir, "results")
    tessdata_dir = os.path.join(base_dir, "tessdata")
    
    # Ensure images directory exists
    if not os.path.exists(images_dir):
        print(f"Error: Directory {images_dir} does not exist.")
        return

    # Get all image paths from M2-Images directory (assuming png, jpg, jpeg)
    image_paths = []
    for ext in ('*.png', '*.jpg', '*.jpeg'):
        image_paths.extend(glob.glob(os.path.join(images_dir, ext)))
        # Also check for uppercase extensions
        image_paths.extend(glob.glob(os.path.join(images_dir, ext.upper())))
    
    image_paths = sorted(image_paths)

    if not image_paths:
        print(f"No images found in {images_dir}.")
        return

    print(f"Found {len(image_paths)} images. Starting batch OCR processing at original resolution...")

    # Iterate over all OEM (0-2) and PSM (0-13) values
    for oem in range(3):
        for psm in range(14):
            # Create a specific results folder for this configuration
            folder_name = f"{oem}_{psm}"
            out_dir = os.path.join(results_base_dir, folder_name)
            os.makedirs(out_dir, exist_ok=True)
            
            txt_result_path = os.path.join(out_dir, f"results_oem{oem}_psm{psm}.txt")
            
            # Use original resolution and custom tessdata containing legacy components
            custom_config = f"--tessdata-dir '{tessdata_dir}' --dpi 300 --oem {oem} --psm {psm}"
            
            # Avoid crashing immediately on PSM 0 (OSD) when facing few characters on image  
            if psm == 0:
                custom_config += " -c min_characters_to_try=5"
            
            with open(txt_result_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(f"OCR Results for config: {custom_config}\n")
                txt_file.write("=" * 40 + "\n\n")

                for img_path in image_paths:
                    img_name = os.path.basename(img_path)
                    
                    # Read the full image as per requirements
                    frame = cv2.imread(img_path)
                    if frame is None:
                        continue
                    
                    # Store a copy for drawing
                    output_frame = frame.copy()

                    # Pre-processing: Convert to grayscale and apply Otsu thresholding over the FULL image
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    _, bw_frame = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                    txt_file.write(f"--- File: {img_name} ---\n")
                    recognized_texts = []
                    
                    try:
                        if psm == 0:
                            # PSM 0 requires image_to_osd since it provides orientation data instead of words/bboxes
                            osd_data = pytesseract.image_to_osd(bw_frame, output_type=Output.DICT, config=custom_config)
                            recognized_texts.append(f"Orientation: {osd_data.get('orientation', 'N/A')}, "
                                                    f"Script: {osd_data.get('script', 'N/A')} "
                                                    f"(Conf: {osd_data.get('script_conf', 0)}%)")
                            cv2.putText(output_frame, "PSM 0: OSD Only (No text bounding boxes)", (10, 30), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                        
                        else:
                            # Run OCR on the entire binarized image (No compression/ROI scaling)
                            res = pytesseract.image_to_data(bw_frame, output_type=Output.DICT, config=custom_config)
                            
                            for i in range(len(res['text'])):
                                text = res['text'][i].strip()
                                conf = float(res['conf'][i])
                                
                                # Filter results based on confidence and valid text (same logic as before)
                                if conf > 40 and text:
                                    x = res['left'][i]
                                    y = res['top'][i]
                                    w = res['width'][i]
                                    h = res['height'][i]
                                    
                                    # Draw bounding box (bracket) on the image
                                    cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                    # Put recognized text above the bounding box
                                    cv2.putText(
                                        output_frame, f"{text} ({int(conf)}%)", 
                                        (x, max(0, y - 8)), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                                    )
                                    recognized_texts.append(f"{text} (Conf: {int(conf)}%)")
                                    
                    except pytesseract.TesseractError as e:
                        # Graceful save of specific engine/mode limitations
                        clean_error = str(e).split('\n')[0][:150]
                        txt_file.write(f"Tesseract Engine Notice: {clean_error}\n")
                        cv2.putText(output_frame, "Tesseract mode limited for this image", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    except FileNotFoundError as e:
                        # Catches cases where non-word PSM targets don't emit TSV outputs
                        txt_file.write("This PSM Configuration does not output bounding boxes.\n")
                        cv2.putText(output_frame, "No Text Boxes Output in this Mode", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    except Exception as e:
                        txt_file.write(f"Error processing image: {e}\n")

                    # Output text into result logging
                    if recognized_texts:
                        txt_file.write("\n".join(recognized_texts) + "\n\n")
                    else:
                        txt_file.write("No valid text blocks generated.\n\n")
                            
                    # Save annotated original-resolution image
                    out_img_path = os.path.join(out_dir, img_name)
                    cv2.imwrite(out_img_path, output_frame)
                    
            print(f"Processed configuration folder: {folder_name}")

    print("Batch Processing Complete!")

if __name__ == "__main__":
    main()
