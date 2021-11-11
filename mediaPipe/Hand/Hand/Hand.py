
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

previousIndexZValue = 0.00
previousWristZValue = 0.00
constantBeckoned = 0
constantShooed = 0
totalSamples = 0

cap = cv2.VideoCapture(0)
while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  results = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1).process(image)

  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:

      #Drawing landmarks to the image consumes too much memory
      mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

      # If the z of the point on the tip of the index finger is increasing, moving away from the camera
      if(previousIndexZValue<hand_landmarks.landmark[8].z):
          #print("Am I being Beckoned?")
          constantBeckoned += 1
      elif(previousWristZValue>hand_landmarks.landmark[8].z):
          #print("Am I being Shooed?")
          constantShooed += 1
      if(totalSamples%10 == 0):
        if(constantBeckoned>=constantShooed): print("I am being Beckoned")
        else: print("I am being Shooed")
        constantBeckoned = 0
        constantShooed = 0

      previousIndexZValue = hand_landmarks.landmark[8].z
      previousWristZValue = hand_landmarks.landmark[0].z
      totalSamples += 1
  # Flip the image horizontally for a selfie-view display.
  cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
  if cv2.waitKey(5) & 0xFF == 27:
    break
cap.release()