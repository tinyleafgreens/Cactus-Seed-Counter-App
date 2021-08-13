import numpy as np
import cv2
def get_edges(pts):
    pts = pts.reshape((4,2))
    new_pts = np.zeros((4,2), dtype=np.float32)

    add = pts.sum(1)
    new_pts[0] = pts[np.argmin(add)]
    new_pts[2] = pts[np.argmax(add)]

    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]
    new_pts[3] = pts[np.argmax(diff)]

    return new_pts
