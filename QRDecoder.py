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


def info():
    return """
   Session: Is your session id, it's bound to your current play-session, this session is created when the game is launched from your RSI launcher, and does not change if you switch server/regions in game, to change this sesion, you will have to relaunch the game

   ShardId: The current server you are currently playing on, if this id is the same as your session, it means that no you were either in a loading screen or in a submenu of the main start menu

   Time (Unix): Current unix time, seconds since UTC 1 January 1970, you can easily convert this to more readable date format on the internet

   Build: Current active build being played

   File: You know what this is :)

   EXTRA: Source for this info is from leaked evocati gameplay with debug info active on the screen: https://streamable.com/0woa2q and https://cdn.discordapp.com/attachments/422137614854914048/1048887977025220619/Tavern-Upload-Image-473137-1670072591.png
   """


if __name__ == "__main__":
    parser = OptionParser(
        usage='%prog --target=test.png')
    parser.add_option('--target', dest='path',
                      help='target file with the path')
    parser.add_option('--information', dest='info', action='store_true', default=False,
                      help='Useful information on how to read the data')
    options, args = parser.parse_args()
    QR_data = []

    if options.info:
        print(info())
        sys.exit(0)

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
