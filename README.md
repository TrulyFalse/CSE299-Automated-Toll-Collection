# Automated Toll Collection System Using ML-based VNR for Smart Cities

An automated toll gate that identifies vehicles by reading their license plates with machine-learning-based Optical Character Recognition (OCR). A Raspberry Pi detects an approaching vehicle, photographs the plate, and sends the image to a server. The server checks the plate against a database of registered vehicles and their e-wallets, and the Pi raises or holds the barrier based on the response.

**Links**

- [Project demo website](https://trulyfalse.github.io/CSE299-Automated-Toll-Collection/): demo video, interactive gate simulator, system overview and results
- [Research paper](https://drive.google.com/file/d/1FuKqR-Y52UTDaHCQljByS7zTBa2H5JSC/view?usp=sharing)

## Why this project

Manual toll booths and RFID tags slow down traffic, and basic video tolling struggles with lighting, camera angle and damaged plates. This project replaces them with plate recognition that runs at the gate, so vehicles are charged without stopping for cash or a tag.

## How it works

1. An ultrasonic (sonar) sensor detects a vehicle at 40 cm or closer and moving slower than 0.5 cm/s.
2. The Raspberry Pi camera captures an image of the license plate.
3. The image is uploaded to the server over an HTTP POST request.
4. The server pre-processes the image (grayscale, denoise, binarize), locates the plate, segments the characters and runs OCR.
5. The recognized plate number is matched against the database. The server checks that the vehicle is registered and that its e-wallet has been charged, then returns a boolean response.
6. The Pi raises the barrier with a micro servo if the response is positive, or keeps it closed otherwise. An LCD shows messages and LEDs act as indicator lights.

## Repository structure

| Folder | Contents |
| --- | --- |
| [`RPi`](./RPi) | Sensor and actuator drivers (sonar sensor, servo, LCD, LEDs, camera) and the scripts that run on the Raspberry Pi. |
| [`Website`](./Website) | The full-stack website that lets drivers at the tolling point confirm payment. |

## Hardware

- Raspberry Pi
- Raspberry Pi Camera (PiCamera)
- Ultrasonic (sonar) sensor
- Micro servo (barrier)
- LCD display and indicator LEDs
- Breadboard and wiring

## Tech stack

- **Raspberry Pi:** Python device drivers
- **OCR:** OpenCV-based machine learning model
- **Backend:** Node.js, PHP, Python Flask
- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS, Bootstrap

## Results

The report evaluates the OCR model on accuracy by image type, error categories, comparison with CRNN and Keras-OCR, and execution time on the Raspberry Pi. See the [paper](https://drive.google.com/file/d/1FuKqR-Y52UTDaHCQljByS7zTBa2H5JSC/view?usp=sharing) for the full evaluation.

## Authors

Department of Electrical and Computer Engineering, North South University, Dhaka, Bangladesh.

- Abrar Ur Alam
- Mahbub Mokaddes Akash
- Nafis Raihan
- Md. Fazle Rabby Faysal
