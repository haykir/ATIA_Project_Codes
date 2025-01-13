import json
import os
from tqdm import tqdm

# Paths
image_dir = base+'/leftImg8bit/val'  # Adjust to your images path
json_file = base+'/coco/instancesonly_filtered_gtFine_val.json'  # COCO annotations
output_dir = save_dir  # Where to save the YOLO annotations

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load COCO annotations
with open(json_file) as f:
    coco_data = json.load(f)

# Load class names from labels.txt
with open(labels_file) as f:
    class_names = [line.strip() for line in f.readlines()]

# Create a dictionary to map class names to integers
class_dict = {class_name: idx for idx, class_name in enumerate(class_names)}

# Get image information
images = coco_data['images']
annotations = coco_data['annotations']

# Process each image
for image in tqdm(images):
    image_filename = image['file_name']
    image_id = image['id']

    # Get the annotations for the current image
    image_annotations = [anno for anno in annotations if anno['image_id'] == image_id]

    # Prepare YOLO annotations
    yolo_annotations = []
    for anno in image_annotations:
        category_id = anno['category_id']
        class_name = coco_data['categories'][category_id - 1]['name']  # Adjust for category_id starting from 1
        class_idx = class_dict.get(class_name)

        if class_idx is not None:
            # Convert bounding box from COCO [x, y, width, height] to YOLO [class_id, x_center, y_center, width, height]
            x, y, w, h = anno['bbox']
            x_center = (x + w / 2) / image['width']
            y_center = (y + h / 2) / image['height']
            w = w / image['width']
            h = h / image['height']

            # Append to YOLO annotations
            yolo_annotations.append(f"{class_idx} {x_center} {y_center} {w} {h}")

    # Ensure that the directory exists for the current image's annotations
    city_folder = image_filename.split('_')[0]  # Assuming city name is the first part of the filename
    image_output_dir = os.path.join(output_dir, 'train', city_folder)  # Adjust 'train' or 'val' as needed

    # Create directory if it does not exist
    os.makedirs(image_output_dir, exist_ok=True)

    # Save YOLO annotations to a file
    if yolo_annotations:
        label_file_path = os.path.join(image_output_dir, f"{os.path.splitext(image_filename)[0]}.txt")

        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(label_file_path), exist_ok=True)

        with open(label_file_path, 'w') as label_file:
            label_file.write("\n".join(yolo_annotations))

print("Conversion Complete!")
