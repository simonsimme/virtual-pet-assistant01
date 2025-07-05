import cv2
import datetime


class Camera:
        
    def take_selfie(self):
        """Take a selfie using the camera."""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception(f"Camera could not be opened.")
        
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Failed to capture image.")
        self.camera.release()
        save_dir = "selfies"
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir}/selfie_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        return frame