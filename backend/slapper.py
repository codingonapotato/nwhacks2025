import os
import cv2
import time
from backend.detector import detector
import json


file_name = os.path.join(os.path.dirname(__file__), "gesture.txt")

# Read JSON from file
with open(file_name, "r") as file:
    gesture_mapping = json.load(file)

def convert(result):
    single_string = "".join(result)
    return single_string

def check_result(handedness, gesture, gesture_mapping):
    key = f"{handedness}_{gesture}"
    print(key)
    return gesture_mapping.get(key, gesture_mapping["invalid"])

def main():
    cap = cv2.VideoCapture(1)
    hdetector = detector()

    result = []
    start = time.time()

    # this part for wrist
    wrist_start_time = None
    wrist_start_x = None
    swipe_detected = False

    captured = False
    gesture = ""
    
    while True:
        
        success, img = cap.read()
        img_width = img.shape[1]
        img = hdetector.findHands(img)

        finger_curls= hdetector.checkFingersCurled()
        handedness = hdetector.checkHandedness()
        palm_back_facing = hdetector.checkPalmOrBack()
        crossed = hdetector.checkFingersCrossed(finger1=8, finger2=12)  # Thumb and index
        wrist = hdetector.getWristX()
        # print(f"Handedness: {handedness}")
        # print(f"Palm/Back: {palm_back_facing}")
        # print(f"Fingers Curl: {finger_curls}")
        # print(f"Fingers crossed: {crossed}")

        # handle if exist left swipe is detected
        if wrist is not None:
            if wrist_start_time is None:  # Begin tracking if wrist is detected
                wrist_start_time = time.time()
                wrist_start_x = wrist * img_width
                print(f"Start wrist X: {wrist_start_x}")

            print(f"Current wrist X: {wrist * img_width}")
            elapsed_time = time.time() - wrist_start_time
            wrist_current_x = wrist * img_width

            # Check if the hand moved across 30% of the camera width within 2 seconds
            if elapsed_time <= 3 and wrist_current_x - wrist_start_x >= 0.3 * img_width:
                swipe_detected = True
                print("Swipe detected!")

            # If 3 seconds passed and no swipe detected, reset
            if elapsed_time > 3 and not swipe_detected:
                print("No swipe detected within 3 seconds, resetting...")
                wrist_start_time = None
                wrist_start_x = None

        if swipe_detected:
            # Handle the logic for detected swipe
            print("Swipe successful!")
            break  # Exit the loop after swipe is detected
        else:
            print("Swipe not detected yet or still tracking...")
            
        # Detect specific signs
        if finger_curls == [1, 0, 0, 1, 1] and not crossed:
            # print("Peace sign detected")
            gesture = "peace"
            captured = True
        elif finger_curls == [1, 0, 0, 1, 1] and crossed:
            # print("Infinity sign detected")
            gesture = "infinity"
            captured = True
        elif finger_curls == [0, 1, 1, 1, 0] and not crossed:
            # print("Six sign detected")
            captured = True
            gesture = "six"
        elif finger_curls == [0, 0, 1, 1, 0] and not crossed:
            # print("Spider sign detected")
            captured = True
            gesture = "spider"


        now = time.time()
        duration = now - start
        if duration > 6:
            if not captured:
                result.append(str(5))
            else:
                digit = check_result(handedness, gesture, gesture_mapping)
                result.append(str(digit))
                captured = False
            
            start = time.time()
        remaining_time = 6 - duration
        cv2.putText(img, f"{int(remaining_time)}s left until next digit", (10, 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 6, cv2.LINE_AA)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    password = convert(result)
    print(convert(result))
    cap.release()
    cv2.destroyAllWindows()
    
    return password
    # login_response = request_sender.login("tt@example.com", password)


if __name__ == "__main__":
    main()