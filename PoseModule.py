import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles


MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red

def visualize(image, detection_result) -> np.ndarray:
    for detection in detection_result.detections:
        category = detection.categories[0]
        category_name = category.category_name

        if category_name not in ['person', 'car']:
            continue

        bbox = detection.bounding_box
        start_point = (bbox.origin_x, bbox.origin_y)
        end_point = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)

        probability = round(category.score, 2)

        cv2.rectangle(image, start_point, end_point, (0,255,0), 3)
  
        result_text = f"{category_name} ({probability})"
        text_location = (bbox.origin_x, bbox.origin_y - 10)

        cv2.putText(image, result_text, text_location,
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0,255,0), 2)

    return image


class humanDetector():
    def __init__(self,cap):
        self.cap = cap
        self.base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
        self.options = vision.ObjectDetectorOptions(base_options=self.base_options,
                                            score_threshold=0.5)
        self.detector = vision.ObjectDetector.create_from_options(self.options)

    def findObjets(self):
        success, img = self.cap.read()
        if success:   
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

            detection_result = self.detector.detect(image)
            image_copy = np.copy(image.numpy_view())
            annotated_image = visualize(image_copy, detection_result)
            
            return annotated_image



