import os
import cv2
import numpy as np
from colour import Color
from protopost import ProtoPost

from utils import b64_to_img, img_to_b64

PORT = int(os.getenv("PORT", 80))

#TODO: make configurable
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.6
DEFAULT_COLOR = "#0000ff"

def get_luminance(r, g, b):
  return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_text_color(r, g, b):
  if get_luminance(r, g, b) > 0.5:
    return (0, 0, 0)
  return (1, 1, 1)

def annotate(img, annotations):
  for anno in annotations:
    x, y, w, h = np.array(anno["bounds"]).astype("int").tolist()
    x1, y1, x2, y2 = [x, y, x+w, y+h]

    color = anno["color"] if "color" in anno else DEFAULT_COLOR
    text = anno["text"] if "text" in anno else ""

    try:
      color = Color(color)
    except:
      color = Color(rgb=iter(color))

    text_color = get_text_color(*color.rgb)
    text_color = (np.array(text_color) * 255).astype("int").tolist()
    color = (np.array(color.rgb) * 255).astype("int").tolist()

    #...reverse color
    color = color[::-1]

    #draw bounding box
    img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    if text.strip() != "":
      #determine text size
      (rw, rh), _ = cv2.getTextSize(text, FONT, FONT_SCALE, 1)
      #draw bg rectangle
      img = cv2.rectangle(img, (x1-1, y1 - 22), (x1 + rw+1, y1), color, -1)
      #draw text
      img = cv2.putText(img, text, (x1, y1 - 5), FONT, FONT_SCALE, text_color, 1, cv2.LINE_AA)

  return img

def handler(data):
  img = data["image"]
  annos = data["annotations"] if "annotations" in data else [] #literally why would you ever do this
  img = b64_to_img(img)
  img = annotate(img, annos)
  img = img_to_b64(img)
  return img

routes = {
  "": handler,
}

ProtoPost(routes).start(PORT)
