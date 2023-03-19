# Gaze-Aware Hand Gesture Recognition for Human-Robot Collaboration
This repo represents the implementation of the article Gaze-Aware Hand Gesture Recognition for Intelligent Construction, including dataset, trained models and code.
<p align="center">
  <img width="854" height="480" src="https://github.com/wxjames/Gaze-Aware-GesRec/blob/main/figures/gaze_aware_gesture_recognition.gif">
</p>

Figure shows a pilot study of gaze-aware hand gresture recognition in the lab environment. The subject uses gaze information to sepecify the machine he/she intends to interact with and then performs hand gestures to transit commands.

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
The trained gesture classifier is provided in [models](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/models) folder. The yolov5 detection model could be downloaded through the following [link](https://drive.google.com/file/d/12uXY_d24uAGX2LTa0Iz0jbDDoYNRveN9/view?usp=share_link). It should be palced under the [models](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/models) folder.

## Offline Training
The [ConGes_data](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/ConGes_data) dataset is used for offline training. For the traning details, please refer to the work of [dl-4-tsc](https://github.com/hfawaz/dl-4-tsc).

## Framewrok Validation Test
* For the real-time online testing:
```
python main.py --mode online_test
```

* For the data collection:
```
python main.py --mode data_collection --number 33
```

* For the validation test using the collected data:
```
python test_framework.py
```
The test results would be generated in the [results](https://github.com/wxjames/Gaze-Aware-GesRec/tree/main/results) folder.

## Citation
If you find this repo useful in your research, please consider citing:
```

```

## Acknowledgement
We would like to thank the work of [TapSDK](https://github.com/TapWithUs/tap-python-sdk), [ultralytics](https://github.com/ultralytics/yolov5), [SORT](https://github.com/abewley/sort) and [dl-4-tsc](https://github.com/hfawaz/dl-4-tsc) so that we can build our work on top.
