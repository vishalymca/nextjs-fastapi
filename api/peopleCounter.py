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
    height, frame_width, channels = frame.shape

    # Run YOLOv8 inference on the frame
    results = model(frame, stream=False, classes=[0])

    result = results[0]
    person_count = result.__len__()
    
    # Visualize the results on the frame
    annotated_frame = result.plot()

    # cv2.imshow('xyz', annotated_frame)
    # cv2.waitKey(0)

    # Added text to the annotated_frame
    cv2.putText(annotated_frame, f"Detected {person_count} person(s) in the room",(frame_width//2 -60, 30), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)

    file_name = filepath.split('/')[-1]
    # Save the annotated frame
    annotated_filepath = os.path.join(UPLOAD_DIRECTORY, file_name)
    cv2.imwrite(annotated_filepath, annotated_frame)

    return person_count, annotated_filepath

if __name__ == "__main__":
    filePath = 'uploads/_AFS9882.JPG'
    person_count, annotated_filepath = PeopleCounter(filePath);
    print(person_count)
    print(annotated_filepath)