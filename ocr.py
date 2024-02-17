# import asrtoolkit
# from asrtoolkit import wer, cer
import cv2
import io
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
from PIL import Image
import pytesseract
from skimage import io as ioski
from skimage.color import rgb2gray
from skimage.transform import rotate,resize
import os
from google.cloud import vision_v1
from dotenv import load_dotenv, find_dotenv
from deskew import determine_skew
load_dotenv()
def convert_rgba_to_rgb(image_path):
    img = Image.open(image_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
        img.save(image_path)



#Here is where the input photo will be placed
sample_img = r'C:\Users\Vikrant\OneDrive\Desktop\desktop_folder\web_development\pythonOCR\express\uploads\image.png'

convert_rgba_to_rgb(sample_img)
output_img=Image.open(sample_img)
#the path to the cred json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\Vikrant\OneDrive\Desktop\desktop_folder\web_development\pythonOCR\ocrhackanova-fb80f40474e1.json"

client = vision_v1.ImageAnnotatorClient()


image = ioski.imread(sample_img)
grayscale = rgb2gray(image)
angle = determine_skew(grayscale)
rotated = rotate(image, angle, resize=True) * 255
ioski.imsave("output_deskewed.png", rotated.astype(np.uint8))

def pre_process_image(image):
    img = cv2.imread(image)
    img = cv2.resize(img, None, fx=.3, fy=.3) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11) #to remove background
    return img
def img_process(image):
    cv2output = io.imread(image)
    angle = determine_skew(cv2output)
    rotated = rotate(cv2output, angle, resize=True) * 255
    return rotated
processed_img = pre_process_image("output_deskewed.png")
cv2.imwrite("output_processed.png",processed_img)
processed_img = pre_process_image(sample_img)
cv2.imwrite("output_no_deskewing.png",processed_img)

with io.open("output_processed.png",'rb') as image_file:
    content = image_file.read()

image_v=vision_v1.Image(content=content)
response = client.document_text_detection(image=image_v)
docText = response.full_text_annotation.text
hypothesis5 = docText
print(hypothesis5)
