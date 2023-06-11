import cv2
import numpy as np
import datetime
from flask import Flask, request, jsonify, send_file
import random
import string

app = Flask(__name__)

def detectImage(img_path):
    img_original = cv2.imread(f'original/{img_path}')
    img = cv2.imread(f'original/{img_path}',0)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(5,5),0)
    edges = cv2.Canny(blur, 50, 150)
    dilated = cv2.dilate(edges, (1,1), iterations = 2)

    # FONT TEXT
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 100)
    fontScale = 1.5
    color = (0, 0, 0)
    thickness = 3

    # FIND CONTOUR
    # CIRCLE
    # (cnt,_) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # HEXAGONAL
    (cnt,_) = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # TEXT IN IMAGE
    # print("Terdapat {} sarang dalam gambar".format(len(cnt)))
    cv2.putText(img_original, "Terdapat {} sarang dalam gambar".format(len(cnt)), org, font, fontScale, color, thickness)

    x = datetime.datetime.now()
    cv2.putText(img_original, x.strftime("%A, %b %S, %Y %H:%M"), (50, 200), font, fontScale, color, thickness)
    alpha = 0.5 # Transparency factor

    # DRAW CONTOUR
    for c in cnt:
        area = cv2.contourArea(c)
        if area < 1000:
            continue
        else:
            cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

    # REZIZE IMAGE
    img_original_resize = cv2.resize(img_original, (600, 600))
    img_resize = cv2.resize(img, (600, 600))
    dilated_resize = cv2.resize(dilated, (600, 600))

    # SHOW IMAGE
    # original = cv2.imshow('Original', img_original_resize)
    # original = cv2.imshow('Find Object Contur', img_resize)
    # sarang = cv2.imshow("Sarang", dilated_resize)

    # SAVE IMAGE
    print("Upload Successfully")
    cv2.imwrite(f'result/{img_path}', img_original_resize)
    cv2.imwrite(f'filter/{img_path}', img_resize)
    cv2.imwrite(f'contour/{img_path}', dilated_resize)
    print("Save Image Processing Successfully")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    many_nests = round(len(cnt) / 2)

    return {'filename': img_path,
            'status': 'success',
            'many_nests': many_nests,
            'original': f'preview/original/{img_path}',
            'contour': f'preview/contour/{img_path}',
            'filter': f'preview/filter/{img_path}',
            'result': f'preview/result/{img_path}',
            'message': 'File uploaded successfully',
            'time': x.strftime("%A, %b %S, %Y %H:%M")}

def random_string(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@app.route('/api/upload', methods=['POST'])
def upload_file():
    f = request.files['file']

    if not f:
        return 'No file part'

    files = f.filename
    extension = files.split('.')[1]
    name = random_string(10)
    filename = f'{name}.{extension}'

    f.save(f'original/{filename}')

    data = detectImage(filename)

    return jsonify(data)

@app.route('/preview/<path:filename>')
def preview(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()