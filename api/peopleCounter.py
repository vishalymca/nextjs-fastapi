import cv2
from ultralytics import YOLO
import os

model = YOLO('yolov8n.pt')
UPLOAD_DIRECTORY = "./annotated"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def PeopleCounter(filepath):
    # Read the image
    frame = cv2.imread(filepath)
    
    # Get the dimensions of the image
    height, width, channels = frame.shape

    # Run YOLOv8 inference on the frame
    results = model(frame, stream=True)

    # Specify your confidence threshold
    confidence_threshold = 0.6  # Adjust this value as needed

    # Filter out low-confidence results
    filtered_results = []
    for result in results:
        for box in result.boxes:
            print('bojhukshksfkwax', box.conf)
            if box.conf >= confidence_threshold:
                filtered_results.append(result)
                break

    person_count = 0
    for result in filtered_results:
        # Count the number of persons detected
        for box in result.boxes:
            if box.cls == 0:  # Class ID for 'person' in YOLO models
                person_count += 1
        
        # Visualize the results on the frame
        annotated_frame = result.plot()
    
    file_name = filepath.split('/')[-1]
    # Save the annotated frame
    annotated_filepath = os.path.join(UPLOAD_DIRECTORY, file_name)
    cv2.imwrite(annotated_filepath, annotated_frame)

    return person_count, annotated_filepath