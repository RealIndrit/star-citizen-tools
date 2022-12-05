import cv2
import sys
import os
from optparse import OptionParser
# read the QRCODE image


def decode(file) -> str:
    try:
        img = cv2.imread(file)
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        # if there is a QR code
        if bbox is not None:
            data: list = data.split(" ")
            data.append(file)
            return data
    except Exception as e:
        print(f'Could not decode QR data for {file} - {e}')


def starcitizen(data):
    starcitizen_data = [
        "Session",
        "ShardId",
        "Time (Unix)",
        "Build",
        "File"
    ]

    for qr_data in data:
        print("-------------------------------------")
        try:
            for i, val in enumerate(qr_data):
                print(f'{starcitizen_data[i]}: {val}')
        except Exception as e:
            print(f'{qr_data} - {e}')


if __name__ == "__main__":
    parser = OptionParser(
        usage='%prog --target=test.png')
    parser.add_option('--target', dest='path',
                      help='target file with the path')
    options, args = parser.parse_args()
    QR_data = []
    if not options.path:
        parser.print_help()
        sys.exit(0)

    if os.path.isfile(options.path):
        QR_data.append(decode(options.path))

    elif os.path.isdir(options.path):
        for file in os.listdir(options.path):
            extension = os.path.splitext(file)[1].upper()
            if extension == ".JPG" or extension == ".PNG" or extension == ".JPEG":
                QR_data.append(decode(os.path.join(options.path, file)))

    starcitizen(QR_data)
