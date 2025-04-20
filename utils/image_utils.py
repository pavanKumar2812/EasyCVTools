import cv2
import numpy as np

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_roi_from_image(image_bytes: bytes, points: list):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if len(points) != 4:
        raise ValueError("Exactly 4 points are required.")
    
    src_pts = np.array(points, dtype="float32")
    print(f"Points: {points}")
    print(f"src+pts: {src_pts}")
    width = max(int(euclidean(points[0], points[1])), int(euclidean(points[2], points[3])))
    height = max(int(euclidean(points[0], points[3])), int(euclidean(points[1], points[2])))

    dst_pts = np.array([[0,0], [width, 0], [width, height], [0, height]], dtype="float32")

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    roi = cv2.warpPerspective(img, matrix, (width, height))

    _, buffer = cv2.imencode(".jpg", roi)

    return buffer.tobytes()
