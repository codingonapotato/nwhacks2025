import cv2
import mediapipe as mp

class detector():
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,  
            max_num_hands=1,         
            min_detection_confidence=0.7,  
            min_tracking_confidence=0.5   
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def getWristX(self, handNo=0):
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            wrist_base = myHand.landmark[0]
            return wrist_base.x
        return None

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)    # mediapipe hand can only process RGB image
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLandmarks, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def checkHandedness(self, handNo=0):
        if self.results.multi_handedness:
            handedness = self.results.multi_handedness[handNo]
            return handedness.classification[0].label
        return None

    def checkPalmOrBack(self, handNo=0):
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            thumb_tip = myHand.landmark[2]
            pinky_tip = myHand.landmark[20]    # compare base of thumb to tip of pinky
            
            hand_type = self.checkHandedness(handNo)
            if hand_type == "Left":
                # For left hand, palm is facing the camera if thumb.x < pinky.x
                if thumb_tip.x > pinky_tip.x:
                    return "Palm"
                else:
                    return "Back"
            elif hand_type == "Right":
                # For right hand, palm is facing the camera if thumb.x > pinky.x
                if thumb_tip.x < pinky_tip.x:
                    return "Palm"
                else:
                    return "Back"
        return None

    def checkFingersCurled(self, handNo=0):
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            hand_type = self.checkHandedness(handNo)
            palm_back_facing = self.checkPalmOrBack(handNo)
            finger_curls = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

            if hand_type == "Right":
                if palm_back_facing == "Palm":
                    finger_curls = [
                        1 if myHand.landmark[4].x > myHand.landmark[2].x else 0,  # Thumb
                        1 if myHand.landmark[8].y > myHand.landmark[6].y else 0,  # Index
                        1 if myHand.landmark[12].y > myHand.landmark[10].y else 0,  # Middle
                        1 if myHand.landmark[16].y > myHand.landmark[14].y else 0,  # Ring
                        1 if myHand.landmark[20].y > myHand.landmark[18].y else 0   # Pinky
                    ]
                elif palm_back_facing == "Back":
                    finger_curls = [
                        1 if myHand.landmark[4].x < myHand.landmark[2].x else 0,  # Thumb
                        1 if myHand.landmark[8].y > myHand.landmark[6].y else 0,  # Index
                        1 if myHand.landmark[12].y > myHand.landmark[10].y else 0,  # Middle
                        1 if myHand.landmark[16].y > myHand.landmark[14].y else 0,  # Ring
                        1 if myHand.landmark[20].y > myHand.landmark[18].y else 0   # Pinky
                    ]

            elif hand_type == "Left":
                if palm_back_facing == "Palm":
                    finger_curls = [
                        1 if myHand.landmark[4].x < myHand.landmark[2].x else 0,  # Thumb
                        1 if myHand.landmark[8].y > myHand.landmark[6].y else 0,  # Index
                        1 if myHand.landmark[12].y > myHand.landmark[10].y else 0,  # Middle
                        1 if myHand.landmark[16].y > myHand.landmark[14].y else 0,  # Ring
                        1 if myHand.landmark[20].y > myHand.landmark[18].y else 0   # Pinky
                    ]
                elif palm_back_facing == "Back":
                    finger_curls = [
                        1 if myHand.landmark[4].x > myHand.landmark[2].x else 0,  # Thumb
                        1 if myHand.landmark[8].y > myHand.landmark[6].y else 0,  # Index
                        1 if myHand.landmark[12].y > myHand.landmark[10].y else 0,  # Middle
                        1 if myHand.landmark[16].y > myHand.landmark[14].y else 0,  # Ring
                        1 if myHand.landmark[20].y > myHand.landmark[18].y else 0   # Pinky
                    ]

            return finger_curls
        return None


    def checkFingersCrossed(self, handNo=0, finger1=8, finger2=12):
        # default check index and middle fingure crossed for infinity sign
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            palm_back_facing = self.checkPalmOrBack(handNo)
            hand_type = self.checkHandedness(handNo)
            
            x1 = myHand.landmark[finger1].x
            x2 = myHand.landmark[finger2].x
            
            # adjust for Palm/Back orientation
            if hand_type == "Left":
                if palm_back_facing == "Palm":
                    if x1 < x2:
                        return True
                    else:
                        return False
                elif palm_back_facing == "Back":
                    if x1 > x2:
                        return True
                    else:
                        return False
            elif hand_type == "Right":
                if palm_back_facing == "Palm":
                    if x1 > x2:
                        return True
                    else:
                        return False
                elif palm_back_facing == "Back":
                    if x1 < x2:
                        return True
                    else:
                        return False
        return False


# def main():
#     cap = cv2.VideoCapture(1)
#     detector = detector()
    
#     while True:
#         success, img = cap.read()
#         img = detector.findHands(img)

#         finger_curls= detector.checkFingersCurled()
#         handedness = detector.checkHandedness()
#         palm_back_facing = detector.checkPalmOrBack()
#         crossed = detector.checkFingersCrossed(finger1=8, finger2=12)  # Thumb and index
#         # print(f"Handedness: {handedness}")
#         # print(f"Palm/Back: {palm_back_facing}")
#         # print(f"Fingers Curl: {finger_curls}")
#         # print(f"Fingers crossed: {crossed}")
            
#         # Detect specific signs
#         if finger_curls == [0, 0, 1, 1, 0] and not crossed:
#             print("Spider sign detected")
#         elif finger_curls == [1, 0, 0, 1, 1] and not crossed:
#             print("Peace sign detected")
#         elif finger_curls == [1, 0, 0, 1, 1] and crossed:
#             print("Infinity sign detected")
#         elif finger_curls == [0, 1, 1, 1, 0] and not crossed:
#             print("Six sign detected")
        
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()

