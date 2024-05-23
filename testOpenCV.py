import cv2

# Initialize the camera
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
# Capture a single frame
ret, frame = cap.read()

if ret:
    # Save the image if a frame was successfully captured
    cv2.imwrite('captured_image.jpg', frame)
else:
    print("Failed to capture frame")

# Release the camera
cap.release()