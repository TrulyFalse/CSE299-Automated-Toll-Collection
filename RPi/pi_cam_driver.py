from picamera2 import Picamera2, Preview

# module function
def capture_image(img_name):
    picam = Picamera2()
    config = picam.create_preview_configuration()
    picam.configure(config)
    picam.start_preview(Preview.QTGL)

    picam.start()
    picam.capture_file(img_name)
    picam.close()