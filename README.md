# Gaze-Aware Hand Gesture Recognition for Human-Robot Collaboration
This repo represents the implementation of the article Gaze-Aware Hand Gesture Recognition for Intelligent Construction, including dataset, trained models and code.
<p align="center">
  <img width="854" height="480" src="https://github.com/wxjames/Gaze-Aware-GesRec/blob/main/figures/gaze_aware_gesture_recognition.gif">
</p>

<p align="center">
Figure: A pilot study of gaze-aware hand gresture recognition in the lab environment
</p>

## Hardware Requirements
* [Tobii Pro Glasses 3](https://www.tobii.com/products/eye-trackers/wearables/tobii-pro-glasses-3?gclid=CjwKCAiAl9efBhAkEiwA4TorigYLbk-YPA4WiMAH0K29TGAreGRQvjAaUKKdAXq5VttXLjyO4FqraRoCxHEQAvD_BwE)
* [Tap Strap 2](https://www.tapwithus.com/product/tap-strap-2/)

## Software Requirements
* Python3
* [TapSDK](https://github.com/TapWithUs/tap-python-sdk)
* [ultralytics](https://github.com/ultralytics/yolov5): The yolov5 repo should be downloaded under the current directory and the files in the ultralytics/yolov5/utils need to be copied to the utils folder under the current directory.
* websocket-client
* PyTorch
* Keras

## Dataset
The dataset used for offline training is palced in the folder of [ConGes_data](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/ConGes_data). The framework validation data are provided in the folder of [framework_validation_data](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/framework_validation_data).

## Trained Models
The trained gesture classifier is provided in [models](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/models) folder. The yolov5 detection model could downloaded through the following link: .
