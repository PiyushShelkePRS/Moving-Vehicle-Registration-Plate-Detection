import os
os.environ['KMP_DUPLICATE_LIB_OK']= 'TRUE'
import json
import cv2
import easyocr
from datetime import datetime
import random
import mailgun

reader = easyocr.Reader(['en'], gpu=False)

cam = cv2.VideoCapture(0)
cv2.namedWindow("cam")

threshold = 0.25


def getRandomCharge():
    charges = [100, 200, 300, 400, 500]
    return charges[random.randint(0, len(charges) - 1)]


def check(vehicleNo, score):
    if vehicleNo.startswith('MH') and len(vehicleNo) >= 8:
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
                         " has been detected by our system at " + now +". Please pay the challan of Rs. " + str(charge) + " to avoid any legal action.")

        else:
            print("vehicleNo Already in file")


def getSwitchValue():
    myFile = open('switch.txt')
    data = myFile.read()
    myFile.close()
    return int(data)


def start_cam():
    while True:
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

        cv2.imshow("cam", frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            print("q pressed, quitting...")
            break

    cam.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_cam()



