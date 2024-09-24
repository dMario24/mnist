import numpy as np
from PIL import Image
from keras.models import load_model
import os


def get_model_path(file_name="mnist240924.keras"):
    my_path = __file__
    dir_name = os.path.dirname(my_path)
    model_path = os.path.join(dir_name, file_name)
    return model_path

mnist_model = load_model(get_model_path())  # 학습된 모델 파일 경로

def preprocess_image(image_path, invert=False):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    if invert:
        img = 255 - np.array(img)  # 흑백 반전
    else:
        img = np.array(img)

    
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

# 예측
def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = mnist_model.predict(img)
    digit = np.argmax(prediction)
    return digit