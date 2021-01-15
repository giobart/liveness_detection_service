import os

MODEL_URL="https://drive.google.com/uc?id=13y2_hTaWD7SZSJ5QiZfUvnUyozpNTt1l"
MODEL_FOLDER=os.path.join(".", "data", "net")
MODEL_PATH = os.path.join(MODEL_FOLDER, "model.ckpt")
INCEPTION_BN_URL = "https://drive.google.com/uc?id=1iSizx_u8lId4v92yFJVmCyxMLZdvlxTe"
INCEPTION_BN_PATH = os.path.join(MODEL_FOLDER, "bn_inception_weights_pt04.pt")
