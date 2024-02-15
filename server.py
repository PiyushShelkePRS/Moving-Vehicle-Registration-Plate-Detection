import os
os.environ["KMP_DUPLICATE_LIB_OK"]= 'TRUE'
from flask import Flask, jsonify, request, render_template, send_from_directory
import json
import cv2
import easyocr
from datetime import datetime
import random
import mailgun
# print('ca')

static_path = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


threshold = 0.25
reader = easyocr.Reader(['en'], gpu=False)


def deleteItem(vehicleNo):
    items = []

    with open('data.json', 'r') as f:
        items = json.load(f)

    for i in range(len(items)):
        if items[i]['vehicleNo'] == vehicleNo:
            print('deleting', items[i])
            del items[i]
            break

    with open('data.json', 'w') as f:
        json.dump(items, f)


def payTheChallan(vehicleNo):
    items = []

    with open('data.json', 'r') as f:
        items = json.load(f)

    for i in range(len(items)):
        if items[i]['vehicleNo'] == vehicleNo:
            items[i]['paid'] = True
            break

    with open('data.json', 'w') as f:
        json.dump(items, f)


def getItemsList():
    items = []

    with open('data.json', 'r') as f:
        items = json.load(f)

    return items


def getRandomCharge():
    charges = [100, 200, 300, 400, 500]
    return charges[random.randint(0, len(charges) - 1)]


def check(vehicleNo, score):
    if vehicleNo.startswith('MH','MP') and len(vehicleNo) >= 8:
        # check if vehicleNo is valid

        myFile = open('data.json')
        data = json.load(myFile)
        myFile.close()

        if not any(d['vehicleNo'] == vehicleNo for d in data):
            print("New vehicleNo Adding to file", vehicleNo, score)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            charge = getRandomCharge()
            data.append({'vehicleNo': vehicleNo, 'time': now,
                        'charge': charge, 'paid': False})

            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)

            print("Sending Email to user..")
            mailgun.mail("New challan generated", "Hello, Your vehicleNo " + vehicleNo +
                         " has been detected by our system at " + now + ". Please pay the challan of Rs. " + str(charge) + " to avoid any legal action.")

        else:
            print("vehicleNo Already in file")


def getSwitchValue():
    myFile = open('switch.txt')
    data = myFile.read()
    myFile.close()
    return int(data)


def readVideo(filepath):

    cam = cv2.VideoCapture(filepath)
    print(filepath)
    cv2.namedWindow("video")

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (350, 300))

        text_ = reader.readtext(frame)

        for t_, t in enumerate(text_):
            # print(t)

            bbox, text, score = t

            if score > threshold:

                try:
                    cv2.putText(
                        frame, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
                except:
                    pass

                if getSwitchValue() == 1:
                    check(text, score)
                else:
                    print("Switch is off")

        cv2.imshow("video", frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            print("q pressed, quitting...")
            break

    cam.release()

    cv2.destroyAllWindows()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def index2():
    return render_template('index.html')


@app.route('/upload_video.html')
def uploadvideo():
    return render_template('upload_video.html')


@app.route('/about_project.html')
def aboutproject():
    return render_template('about_project.html')


@app.route('/guided_by.html')
def guidedetails():
    return render_template('guided_by.html')


@app.route('/technology_used.html')
def technology():
    return render_template('technology_used.html')


@app.route('/developed_by.html')
def developby():
    return render_template('developed_by.html')


@app.route('/<path:path>')
def serve_static(path):
    if os.path.isdir(os.path.join(static_path, path)):
        path = os.path.join(path, 'index.html')
    return send_from_directory(static_path, path)


@app.route('/getItems')
def getItemsJson():
    return jsonify(getItemsList())


@app.route('/getSwitch')
def getSwitch():
    with open('switch.txt', 'r') as f:
        return jsonify({'switch': int(f.read())})


@app.route('/setSwitch', methods=['POST'])
def setSwitch():
    reqjson = request.get_json()
    val = reqjson['switch']

    with open('switch.txt', 'w') as f:
        f.write(str(val))

    return jsonify({'msg': 'ok'})


@app.route('/deleteItem', methods=['POST'])
def deleteFromJson():
    reqjson = request.get_json()
    vehicleNo = reqjson['vehicleNo']
    deleteItem(vehicleNo)
    return jsonify({'msg': 'ok'})


@app.route('/pay-challan', methods=['POST'])
def payChallan():
    reqjson = request.get_json()
    vehicleNo = reqjson['vehicleNo']
    payTheChallan(vehicleNo)
    return jsonify({'msg': 'ok'})


@app.route('/predict-video', methods=['POST'])
def predictVideo():
    myfile = request.files['vidfile']
    filename = myfile.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    myfile.save(filepath)
    readVideo(filepath)
    os.remove(filepath)

    return jsonify({'msg': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
