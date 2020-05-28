from flask import Blueprint
from flask import render_template
from flask import request
from .static.empty_image import empty_image
import base64
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

scaler = MinMaxScaler(feature_range=(0, 16))
numbers = Blueprint('numbers', __name__, template_folder='templates', static_folder='static')


with open(r'datamodels\static\model\numbers_model', 'rb') as f:
    numbers_model = joblib.load(f)


def preprocess_image(body):
    img = Image.open(BytesIO(body))
    img_resz = img.resize((8, 8), resample=Image.BOX)
    img_array = np.array(img_resz)
    new_img_arr = img_array[:, :, 3]
    new_img_arr_transformed = scaler.fit_transform(new_img_arr)
    value = numbers_model.predict(new_img_arr_transformed.reshape(1, -1))[0]
    return value


@numbers.route('/', methods=['GET'])
def index():
    return render_template('numbers.html')

@numbers.route('/draw', methods=['POST'])
def draw():
    if request.method == 'POST':
        data_url = str(request.data)
        image_encoded = data_url.split(',')[1]
        image_encoded = image_encoded.encode('ascii')
        body = base64.decodebytes(image_encoded)
        if body != empty_image:
            answer = 'Probably you draw ' + str(preprocess_image(body))
        else:
            answer = 'Empty picture'
    return render_template('numbers.html', answer=answer)