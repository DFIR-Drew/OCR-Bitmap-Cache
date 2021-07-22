# OCR-Bitmap-Cache
RDP Bitmap Cache OCR Script to triage text in bitmap cache images.

* Needs output from ANSSI bmc-tools Python script (https://github.com/ANSSI-FR/bmc-tools)
* Requires Python3

# Installation
1. Install python packages
```
pip install pytesseract
pip install opencv-python
```
2. Download [Tesseract](https://digi.bib.uni-mannheim.de/tesseract/) (version [4.0.0dev-20170510](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-4.0.0dev-20170510.exe) tested and working)
3. Add tesseract to User path

# Usage
```
./ocr.py [-h] [-c MIN_CONF] -s SOURCE -d DEST -o CSV -w WORDLIST
```

# Arguments
```
-h, --help                        show this help message and exit
-c MIN_CONF, --min-conf MIN_CONF  mininum confidence value to filter weak text detection
-s SOURCE, --source SOURCE        path to image folder to be OCR'd
-d DEST, --dest DEST              folder to save OCR'd output images
-o CSV, --csv CSV                 csv output file to contain file db
-w WORDLIST, --wordlist WORDLIST  wordlist to test against OCR text
```

# Outputs
* CSV File with:
  * Path to the original file
  * Name of the highlighted output image
  * Output size and location of the words located in the highlighted image
  * Characters identified by the OCR
  * Confidence of the characters identified
  * Top three closest matches to the characters from the custom wordlist input
* Highlighted Images

![csv](https://user-images.githubusercontent.com/87434084/125654480-5dea216e-090b-41cf-9d34-0e5958cf6cbe.png)
![highlighted collage](https://user-images.githubusercontent.com/87434084/125654494-30210475-af4a-4133-8b0d-2bf16dce2dde.jpg)
![close-up collage](https://user-images.githubusercontent.com/87434084/125654506-44484372-40cc-4023-942a-c1b77055b2a4.jpg)
