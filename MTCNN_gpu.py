from facenet_pytorch import MTCNN
from PIL import Image
import torch
import cv2
import time
import glob


class MTCNNDetectorGPU:
    def __init__(self) -> None:
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.fast_mtcnn = FastMTCNN(
            stride=4,
            resize=0.5,
            margin=14,
            factor=0.6,
            keep_all=True,
            device=self.device
        )
    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.fast_mtcnn(frame)
    def assign_detection(sefl, x, y, frame):
        pass