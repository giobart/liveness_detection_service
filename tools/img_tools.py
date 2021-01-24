import base64
import cv2
import io
from PIL import Image
from facenet_pytorch import MTCNN
import numpy as np
from torchvision import transforms
import torch
from tools.model_tools import *
from config import *


def base64arr_to_tensor(frames):
    model = model_init()
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
        detections, probs = face_detector.detect(img)
        if detections is not None:
            x, y, x2, y2 = int(detections[0][0]), int(detections[0][1]), int(detections[0][2]), int(detections[0][3])
            img = Image.fromarray(img[y:y2, x:x2, :])
        # resize face
        img = resize(img, model.input_size)
        # save sample
        img.save("last_image.jpg")

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((model.input_size, model.input_size))
        ])
        tensor_arr.append(transform(img))
    return torch.stack(tensor_arr)


def resize(img, input_size):
    old_size = img.size
    ratio = float(input_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    img = img.resize(new_size, Image.ANTIALIAS)
    new_im = Image.new("RGB", (input_size, input_size))
    new_im.paste(img, ((input_size - new_size[0]) // 2,
                       (input_size - new_size[1]) // 2))
    return new_im


def check_liveness(tensor):
    model = model_init()
    y_hat = model.infer(tensor)
    open_eye = False
    for elem in y_hat:
        print(elem.item())
        if elem.item() < EYE_TRESHOLD:
            open_eye = True
        if elem.item() >= EYE_TRESHOLD and open_eye is True:
            return True
    return False
