import numpy as np

class AccidentDetectionModel(object):

    class_nums = ['Accident', "No Accident"]

    def __init__(self, model_json_file, model_weights_file):
        # We are mocking the AI execution here to bypass tensorflow and missing weights 
        self.frame_count = 0
        print("Mock Model Loaded! Simulating accident after 300 frames.")

    def predict_accident(self, img):
        self.frame_count += 1
        
        # Simulate video playing normally for 300 frames
        if self.frame_count < 300:
            return 'No Accident', [[0.01, 0.99]]
        
        # Trigger the accident alarm
        return 'Accident', [[0.999, 0.001]]