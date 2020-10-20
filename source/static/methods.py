from io import BytesIO
from os import path, mkdir
import requests
from core import config
from base64 import encodebytes, decodebytes
from uuid import uuid4


def webp_to_png(img: BytesIO) -> str:
    if not path.exists('tmp'):
        mkdir('tmp')
    img = encodebytes(img.read()).decode('UTF-8')
    r = requests.post(config['w2j_url'], json={
        'key': config['w2j_key'],
        'image': img
    })

    filename = f'temp{uuid4().hex}.jpeg'  # I will optimize it later. Probably.

    open(path.join('tmp', filename), 'wb').write(decodebytes(r.text.encode()))
    return path.join('tmp', filename)
