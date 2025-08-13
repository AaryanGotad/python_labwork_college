import cv2
import numpy as np
from pyzbar.pyzbar import decode
from matplotlib import pyplot as plt

def preprocess_image(image_path):
    """Load and preprocess the image for better barcode detection"""
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or invalid path")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Apply morphological operations to enhance barcode lines
    kernel = np.ones((3, 3), np.uint8)
    processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return img, processed

def detect_barcode_regions(processed_img):
    """Find potential barcode regions using contour detection"""
    # Find contours
    contours, _ = cv2.findContours(
        processed_img, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    # Filter contours based on aspect ratio (barcode-like shapes)
    barcode_regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        
        # Code 39 typically has aspect ratio > 2
        if aspect_ratio > 2 and w > 100 and h > 20:
            barcode_regions.append((x, y, w, h))
    
    return barcode_regions

def decode_barcode(image, barcode_regions):
    """Decode barcodes in the detected regions"""
    decoded_barcodes = []
    
    for (x, y, w, h) in barcode_regions:
        # Crop the barcode region
        barcode_roi = image[y:y+h, x:x+w]
        
        # Decode using pyzbar
        decoded_objects = decode(barcode_roi)
        
        for obj in decoded_objects:
            if obj.type == 'CODE39':
                decoded_barcodes.append({
                    'data': obj.data.decode('utf-8'),
                    'rect': (x, y, w, h),
                    'polygon': obj.polygon
                })
    
    return decoded_barcodes

def visualize_results(original_img, decoded_barcodes):
    """Draw bounding boxes and display decoded information"""
    output_img = original_img.copy()
    
    for barcode in decoded_barcodes:
        # Draw bounding rectangle
        x, y, w, h = barcode['rect']
        cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Draw polygon (more precise than rectangle)
        points = np.array(barcode['polygon'], np.int32)
        points = points.reshape((-1, 1, 2))
        cv2.polylines(output_img, [points], True, (255, 0, 0), 2)
        
        # Display decoded text
        text = f"CODE39: {barcode['data']}"
        cv2.putText(output_img, text, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Display the result
    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
    plt.title('Detected Code 39 Barcodes')
    plt.axis('off')
    plt.show()

def process_barcode_image(image_path):
    """Complete pipeline for barcode detection and decoding"""
    try:
        # Step 1: Preprocess the image
        original_img, processed_img = preprocess_image(image_path)
        
        # Step 2: Detect barcode regions
        barcode_regions = detect_barcode_regions(processed_img)
        
        # Step 3: Decode barcodes
        decoded_barcodes = decode_barcode(original_img, barcode_regions)
        
        if not decoded_barcodes:
            print("No Code 39 barcodes found in the image.")
            return
        
        # Step 4: Visualize results
        visualize_results(original_img, decoded_barcodes)
        
        # Print decoded data
        print("\nDecoded Barcode Information:")
        for i, barcode in enumerate(decoded_barcodes, 1):
            print(f"Barcode {i}:")
            print(f"  Data: {barcode['data']}")
            print(f"  Position: (x={barcode['rect'][0]}, y={barcode['rect'][1]})")
            print(f"  Dimensions: {barcode['rect'][2]}x{barcode['rect'][3]}")
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")

# Example usage
image_path = 'barcode.jpg'  # Replace with your image path
process_barcode_image(image_path)