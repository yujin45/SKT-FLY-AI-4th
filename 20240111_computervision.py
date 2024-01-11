# -*- coding: utf-8 -*-
"""20240111_ComputerVision.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wmWJRd5Oe8XAbRl-ITEjhwrw52OqURM-

# 이미지 분석
- 유명한 브랜드, 랜드마크 있는가
- 이미지 캡션(설명)
- 이미지 칼라맵

## 개와 고양이 실습1 - params 문제 있음
"""

image_url = "https://health.chosun.com/site/data/img_dir/2023/04/21/2023042102030_0.jpg"
#image_url = "https://image.newdaily.co.kr/site/data/img/2012/11/28/2012112800100_0.jpg"

from PIL import Image
from io import BytesIO
import requests

requests.get(image_url).content # 이미지와 같은 바이너리 파일은 conent로 가져옴 text가 아니라

BytesIO(requests.get(image_url).content) # 변경해주기

Image.open(BytesIO(requests.get(image_url).content))

key = '914cb258620445fdb10e17806d004ea7'
# e747e421639b4b85afd39e6d50114208
endpoint = 'https://labuser59computervision.cognitiveservices.azure.com/'
# 클라우드가 분석 후 결과를 json 형식으로 return해
endpoint += 'vision/v2.0/'
# 버전을 업하면 더 정확하게 나옴. 품종까지!

analyze_endpoint = endpoint + 'analyze'
detect_endpoint = endpoint + 'detect'
ocr_endpoint = endpoint + 'ocr'

headers = {'Ocp-Apim-Subscription-Key' : key}
params = {'visualFeatures' : 'Categories, Description, Color'}
data = {'url': image_url}

response = requests.post(analyze_endpoint, headers=headers,json=data)
response

result = response.json()
result

"""## 개 고양이 분석 실습2"""



image_url = 'https://st3.depositphotos.com/1004199/12631/i/950/depositphotos_126310760-stock-photo-cat-and-dog-together.jpg'

from PIL import Image
from io import BytesIO
import requests

Image.open(BytesIO(requests.get(image_url).content))

key = '819850b090964eddae67fd705e9ef2aa'
endpoint = 'https://labuser51computervision.cognitiveservices.azure.com/'
endpoint = endpoint + 'vision/v2.0/'

analyze_endpoint = endpoint + 'analyze'
detect_endpoint = endpoint + 'detect'
ocr_endpoint = endpoint + 'ocr'

headers = {'Ocp-Apim-Subscription-Key': key}
params = {'visualFeatures':'Categories,Description,Color'}
data = {'url': image_url}

response = requests.post(analyze_endpoint,
                         headers=headers,
                         params=params,
                         json=data)
result = response.json()
result

"""## json의 description만 가져와서 확인하기"""

result['description']['captions'][0]['text']

"""# Object Detection
- 객체 탐지
"""

response = requests.post(detect_endpoint,
                         headers =headers,
                         json = data)
result = response.json()
result

from PIL import Image, ImageDraw, ImageFont

image = Image.open(BytesIO(requests.get(image_url).content))
draw = ImageDraw.Draw(image) #그릴 수 있는 형식으로 바꿔

# 이미지 안의 박스 여러개 칠 것이니까 함수 만들어서 돌리자
def CreateRectangle(objectInfo):
  objects = objectInfo['objects']

  for obj in objects:
    rect = obj['rectangle']
    x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
    # Draw rectangle on the image
    draw.rectangle(((x, y), (x + w, y + h)), outline='red', width=2)

CreateRectangle(result)

image

"""# OCR"""

# 다음에