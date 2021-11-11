
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

previousWristZValue = 0.00
previousElbowZValue = 0.00
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
  results = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5).process(image)

  if results.pose_landmarks:
      if(previousWristZValue<results.pose_landmarks.landmark[15].z):
          #print("Am I being Beckoned?")
          constantBeckoned += 1
      elif(previousElbowZValue>results.pose_landmarks.landmark[13].z):
          #print("Am I being Shooed?")
          constantShooed += 1
      if(totalSamples%10 == 0):
        if(constantBeckoned>=constantShooed): print("I am being Beckoned")
        else: print("I am being Shooed")
        constantBeckoned = 0
        constantShooed = 0

      previousIndexZValue = results.pose_landmarks.landmark[8].z
      previousWristZValue = results.pose_landmarks.landmark[0].z
      totalSamples += 1

  # Draw the pose annotation on the image.
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  #image.flags.writeable = True
  #mp_drawing.draw_landmarks(
  #    image,
  #    results.pose_landmarks,
  #    mp_pose.POSE_CONNECTIONS,
  #    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
  # Flip the image horizontally for a selfie-view display.
  cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
  if cv2.waitKey(5) & 0xFF == 27:
    break
cap.release()