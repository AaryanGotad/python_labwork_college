import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    # Load image and ensure it's 512x512
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img.shape != (512, 512):
        img = cv2.resize(img, (512, 512))
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Clean up with morphological operations
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    return img, binary

def find_lines(binary):
    # First detect edges
    edges = cv2.Canny(binary, 50, 150)
    
    # Then find lines
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=15,
        minLineLength=20,
        maxLineGap=10
    )
    
    return edges, lines

def filter_one_pixel_lines(binary, lines):
    one_pixel_lines = []
    line_image = np.zeros_like(binary)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Create points along the line
            length = max(int(np.hypot(x2-x1, y2-y1)), 1)
            x_points = np.linspace(x1, x2, length)
            y_points = np.linspace(y1, y2, length)
            
            # Check thickness
            is_one_pixel = True
            for xi, yi in zip(x_points, y_points):
                xi, yi = int(round(xi)), int(round(yi))
                if xi < 1 or yi < 1 or xi >= 511 or yi >= 511:
                    continue
                
                # More lenient thickness check
                neighborhood = binary[yi-1:yi+2, xi-1:xi+2]
                if np.sum(neighborhood > 0) > 3:  # Allow some neighboring pixels
                    is_one_pixel = False
                    break
            
            if is_one_pixel:
                one_pixel_lines.append(line[0])
                cv2.line(line_image, (x1, y1), (x2, y2), 255, 1)
    
    return one_pixel_lines, line_image

def find_line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    denominator = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denominator == 0:  # Lines are parallel
        return None
    
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denominator
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denominator
    
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = int(x1 + ua*(x2-x1))
        y = int(y1 + ua*(y2-y1))
        return (x, y)
    return None

def detect_intersections(lines, tolerance=5):
    intersections = []
    
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            point = find_line_intersection(lines[i], lines[j])
            if point:
                # Check if this point is too close to existing ones
                duplicate = False
                for existing in intersections:
                    if np.hypot(point[0]-existing[0], point[1]-existing[1]) < tolerance:
                        duplicate = True
                        break
                if not duplicate:
                    intersections.append(point)
    
    return intersections

# Main processing
image_path = input("file path: ")

# 1. Preprocess the image
original, binary = preprocess_image(image_path)

# 2. Find lines
edges, lines = find_lines(binary)
print(f"Initial lines detected: {len(lines) if lines is not None else 0}")

# 3. Filter for one-pixel lines
one_pixel_lines, line_image = filter_one_pixel_lines(binary, lines)
print(f"One-pixel lines found: {len(one_pixel_lines)}")

# 4. Find intersections
intersections = detect_intersections(one_pixel_lines)
print(f"Intersections found: {len(intersections)}")

# Visualization
result_img = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

# Draw lines
for line in one_pixel_lines:
    x1, y1, x2, y2 = line
    cv2.line(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)

# Draw intersections
for point in intersections:
    cv2.circle(result_img, point, 5, (0, 0, 255), -1)

# Display results
plt.figure(figsize=(15, 5))
plt.subplot(131), plt.imshow(binary, cmap='gray'), plt.title('Binary Image')
plt.subplot(132), plt.imshow(edges, cmap='gray'), plt.title('Edge Detection')
plt.subplot(133), plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
plt.title(f'Detected: {len(one_pixel_lines)} lines, {len(intersections)} intersections')
plt.show()

# Print detailed results
print("\nDetected Lines:")
for i, line in enumerate(one_pixel_lines, 1):
    print(f"Line {i}: ({line[0]}, {line[1]}) to ({line[2]}, {line[3]})")

print("\nIntersection Points:")
for i, point in enumerate(intersections, 1):
    print(f"Point {i}: ({point[0]}, {point[1]})")