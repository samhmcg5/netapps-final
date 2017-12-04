# import face_recognition
import cv2
import face_recognition

def save_image(frame):
    cv2.imwrite("saved_image.jpg", frame)

video_capture = cv2.VideoCapture(1)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)

    # for (top, right, bottom, left) in face_locations:
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # elif cv2.waitKey(2) & 0xFF == ord('s'):
    #     print("Saving current frame")
    #     # save_image(frame)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
