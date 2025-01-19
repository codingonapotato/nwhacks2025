import cv2
import time
from detector import detector
import json

file_name = "gesture.txt"

# Read JSON from file
with open(file_name, "r") as file:
    gesture_mapping = json.load(file)

# print("JSON data loaded:")
# print(gesture_mapping)

def check_result(handedness, gesture, gesture_mapping):
    key = f"{handedness}_{gesture}"
    print(key)
    return gesture_mapping.get(key, gesture_mapping["invalid"])

def main():
    cap = cv2.VideoCapture(1)
    hdetector = detector()

    result = []
    start = time.time()
    while True:
        captured = False
        gesture = ""
        
        success, img = cap.read()
        img = hdetector.findHands(img)

        finger_curls= hdetector.checkFingersCurled()
        handedness = hdetector.checkHandedness()
        palm_back_facing = hdetector.checkPalmOrBack()
        crossed = hdetector.checkFingersCrossed(finger1=8, finger2=12)  # Thumb and index
        # print(f"Handedness: {handedness}")
        # print(f"Palm/Back: {palm_back_facing}")
        # print(f"Fingers Curl: {finger_curls}")
        # print(f"Fingers crossed: {crossed}")
            
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
        if duration > 5:
            if not captured:
                result.append(str(5))
            else:
                # print(handedness)
                # print(gesture)
                digit = check_result(handedness, gesture, gesture_mapping)
                result.append(str(digit))
                captured = False
            
            start = time.time()
        print(result)
        cv2.putText(img, str(int(duration)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()