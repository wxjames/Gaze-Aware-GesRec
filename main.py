import copy
import websocket
import base64
import cv2
import json
import globals
import torch
from threading import Thread
from utils.sort import *
import tensorflow.keras as keras
from tapsdk import TapSDK, TapInputMode
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type = str, default = 'online_test')
parser.add_argument('--number', type = int, default = 33)
args = parser.parse_args()
globals.initialize()
model_detection = torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join('models', 'yolov5l-exctru.pt'), source = 'local')
mot_tracker = Sort()

# Data collection for Tobii Glasses 3
def data_uri_to_cv2_img(uri):
    nparr = np.frombuffer(base64.b64decode(uri), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def on_message(wsapp, message):
    mess = json.loads(message)
    body = mess['body'][1]

    if '/9j/' in body:
        globals.camera_view_ori = data_uri_to_cv2_img(body)
    else:
        if body:
            globals.gaze = body['gaze2d']
        else:
            globals.gaze = None

    if mess['body'][0] - globals.time_count > 4:
        wsapp.send('{"path":"rudimentary!keepalive","id":' + str(globals.iter) + ',"method":"POST","body":[]}')
        globals.time_count = mess['body'][0]
        globals.iter += 1

def on_open(wsapp):
    wsapp.send('{"path": "rudimentary:scene","id":10, "method":"POST","body": null}')
    wsapp.send('{"path":"rudimentary:gaze","id":20,"method":"POST","body":null}')
    wsapp.send('{"path":"rudimentary!keepalive","id":28,"method":"POST","body":[]}')

wsapp = websocket.WebSocketApp("ws://192.168.75.51/websocket", subprotocols=["g3api"],
  on_message=on_message, on_open=on_open)

def webrun():
    wsapp.run_forever()

# Data collection for Tap sensor
tap_identifiers = []
model_gesture = keras.models.load_model(os.path.join('models', 'resnet_attention.hdf5'))

def on_connect(identifier, name, fw):
    print(identifier + " Tap: " + str(name), " FW Version: ", fw)
    if identifier not in tap_identifiers:
        tap_identifiers.append(identifier)
    print("Connected taps:")
    for identifier in tap_identifiers:
        print(identifier)
    tap_instance.set_input_mode(TapInputMode("raw", sensitivity=[2, 1, 4]))

def on_disconnect(identifier):
    print("Tap has disconnected")
    if identifier in tap_identifiers:
        tap_identifiers.remove(identifier)
    for identifier in tap_identifiers:
        print(identifier)

def on_raw_sensor_data(identifier, raw_sensor_data):
    if globals.T1 == 0:
        if globals.throw_frame == 0:
            globals.first_timestamp = time.time()
            globals.throw_frame += 1
        elif time.time() - globals.first_timestamp > 2:
            globals.first_timestamp = time.time()
            print('Programs begins at' + str(globals.first_timestamp))
            globals.T1 += 1
    else:
        if time.time() < globals.first_timestamp + (globals.T1 - 1) * globals.time + globals.iter1 * globals.delta_T:
            if raw_sensor_data.type == 1:
                for i in range(2):
                    globals.temp1 = np.append(globals.temp1, [raw_sensor_data.points[i].x, raw_sensor_data.points[i].y,
                                                              raw_sensor_data.points[i].z])
            elif raw_sensor_data.type == 2:
                for i in range(5):
                    globals.temp2 = np.append(globals.temp2, [raw_sensor_data.points[i].x, raw_sensor_data.points[i].y,
                                            raw_sensor_data.points[i].z])
        else:
            globals.iter1 += 1
            globals.temp1 = np.reshape(globals.temp1, (-1, 6))
            globals.temp2 = np.reshape(globals.temp2, (-1, 15))
            ave_temp1 = globals.temp1.mean(axis=0)
            ave_temp2 = globals.temp2.mean(axis=0)
            temp=np.append(ave_temp1, ave_temp2)
            temp = (temp - globals.aver) / globals.std

            globals.Tap_data = np.append(globals.Tap_data, temp)
            if args.mode == 'data_collection':
                globals.interaction_data = np.append(globals.interaction_data, globals.interaction)
            if globals.iter1 == globals.N+1:
                globals.iter1 = 1
                globals.T1 += 1
                print(time.time() - globals.first_timestamp)
                if args.mode == 'online_test' and globals.T1 > 6:
                    globals.Tap_data = np.delete(globals.Tap_data, np.arange(21*globals.N))
            globals.temp1 = np.array([])
            globals.temp2 = np.array([])

def detection_tracking():
    if globals.camera_view_ori is not None:
        globals.camera_view = copy.deepcopy(globals.camera_view_ori)
        if globals.gaze:
            center = (int(960 * globals.gaze[0]), int(540 * globals.gaze[1]))
            cv2.circle(globals.camera_view, center, 10, (0, 0, 255), -1)
        else:
            center = None

        globals.results = model_detection(globals.camera_view)

        # Detection and Tracking
        detections = globals.results.pred[0].cpu().numpy()
        track_bbs_ids = mot_tracker.update(detections)

        for machine in globals.count_interaction:
            globals.count_interaction[machine] = np.delete(globals.count_interaction[machine], 0)
            globals.count_interaction[machine] = np.append(globals.count_interaction[machine], 0)

        for i in range(len(track_bbs_ids)):
            coords = track_bbs_ids[i]
            x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
            if center and center[0] > x1 and center[0] < x2 and center[1] > y1 and center[1] < y2:
                color = (0, 0, 255)
                globals.count_interaction[globals.name[int(coords[-1])]][-1] = 1
            else:
                color = (255, 0, 0)

            cv2.rectangle(globals.camera_view, (x1, y1), (x2, y2), color, 2)
            cv2.putText(globals.camera_view, globals.name[int(coords[-1])] + ' ID:' + str(int(coords[-2])), (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        color, 2)
        cv2.imshow('frame', globals.camera_view)
        cv2.waitKey(1)

def Tapmain():
    global tap_instance
    tap_instance = TapSDK()
    tap_instance.run()
    tap_instance.register_connection_events(on_connect)
    tap_instance.register_disconnection_events(on_disconnect)
    tap_instance.register_raw_data_events(on_raw_sensor_data)

    while True:
        detection_tracking()
        if np.sum(globals.count_interaction['Truck']) > 6:
            globals.interaction = 1
        elif np.sum(globals.count_interaction['Excavator']) > 6:
            globals.interaction = 0
        else:
            globals.interaction = -1

        if globals.T1 - globals.T0 == 1 and args.mode == 'online_test':
            if globals.interaction >= 0:
                globals.Inference_data = np.reshape(globals.Tap_data[-30*21:], (-1,21))
                y_pred = model_gesture.predict([globals.Inference_data.tolist()])
                y_pred[0] = np.multiply(y_pred[0], globals.post_processing[globals.interaction])
                maxindex = np.argmax(y_pred, axis=1)
                if y_pred[0][maxindex[0]] > 0.7 and maxindex[0] != 14:
                    print('Interaction machine: ' + globals.name[globals.interaction] + '; Gesture recognition: ' +
                          globals.gesture_name[globals.interaction][maxindex[0]])
            globals.T0 = globals.T1

if __name__ == "__main__":
    threads = []
    threads.append(Thread(target=webrun))
    for t in threads:
        t.start()
    try:
        Tapmain()
    except KeyboardInterrupt:
        print("\nApplication exit!")
        wsapp.keep_running = False
        if args.mode == 'data_collection':
            with open(os.path.join('framework_validation_data', 'test'+str(args.number)+'-Tap'), "wb") as fp:
                pickle.dump(globals.Tap_data, fp)
            with open(os.path.join('framework_validation_data', 'test'+str(args.number)+'-interaction'), "wb") as fp:
                pickle.dump(globals.interaction_data, fp)
        for t in threads:
            t.join()