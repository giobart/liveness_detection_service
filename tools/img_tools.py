import base64
import cv2
import io
from PIL import Image
from facenet_pytorch import MTCNN
import numpy as np
from torchvision import transforms
import torch
from tools.model_tools import *


def base64arr_to_tensor(frames):
    face_detector = MTCNN()
    face_detector.select_largest = True
    tensor_arr = []
    for frame in frames:
        # convert to PIL image
        base64img = base64.b64decode(frame)
        buf = io.BytesIO(base64img)
        img = Image.open(buf).convert('RGB')
        img = np.array(img)
        # extract face
        detections, probs, landmarks = face_detector.detect(img)
        if detections is not None:
            x, y, x2, y2 = int(detections[0][0]), int(detections[0][1]), int(detections[0][2]), int(detections[0][3])
            img = Image.fromarray(cv2.cvtColor(img[y:y2, x:x2, :], cv2.COLOR_BGR2RGB))
        # resize face
        img = resize(img, 256)
        # save sample
        img.save("last_image.jpg")

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((256, 256))
        ])
        tensor_arr.append(transform(img))
    return torch.cat(tensor_arr)


def resize(img, input_size):
    old_size = img.size
    ratio = float(input_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)
    new_im = Image.new("RGB", (input_size, input_size))
    new_im.paste(img, ((input_size - new_size[0]) // 2,
                       (input_size - new_size[1]) // 2))
    return img


def check_liveness(tensor):
    model = model_init()
    y_hat = model.infer(tensor).toList()
    for elem in y_hat:
        if int(elem) == 1:
            return True
    return False
