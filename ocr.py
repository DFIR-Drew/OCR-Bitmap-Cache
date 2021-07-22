from pytesseract import Output
import pytesseract
import argparse
import cv2
import os
import csv
import difflib
import time
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class ImageData():
    def __init__(self,img):
        self.img = img
        self.image = cv2.imread(img)

    def process_image(self,):
        #rgb = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2RGB)
        denoised_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        results = pytesseract.image_to_data(denoised_img, output_type=Output.DICT, config='--oem 2 --psm 1 -l eng')
        return results


    def process_inverted_image(self,):
        denoised_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        invert_img = cv2.bitwise_not(denoised_img)
        results = pytesseract.image_to_data(invert_img, output_type=Output.DICT, config="--oem 2 --psm 1 -l eng")
        return results


class Result_Iter():
    def __init__(self,writer):
        self.writer = writer

    def update_csv(self,results):
        for i in range(0, len(results["text"])):

            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]

            text = results["text"][i]
            conf = int(results["conf"][i])
            if conf > args["min_conf"] and text != '\ufb01' and text != '':
                print("Confidence: {}".format(conf))
                print("Text: {}".format(text))
                print("")
                row = {}
                row["Path"] = args["source"]
                row["Image"] = im
                row["Left"] = x
                row["Top"] = y
                row["Width"] = w
                row["Height"] = h
                row["Confidence"] = conf
                text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
                row["Raw Words"] = text
                text = ''.join(e for e in text if e.isalnum())
                text = text.lower()
                res = difflib.get_close_matches(text,dictionary_words,n=3)
                if(len(res) == 1):
                    row["Closest Match 1"] = res
                elif(len(res) > 1):
                    row["Closest Match 1"] = res[0]
                if(len(res) > 1):
                    row["Closest Match 2"] = res[1]
                if(len(res) > 2):
                    row["Closest Match 3"] = res[2]
                cv2.rectangle(imgData.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imwrite(os.path.join(args["dest"] ,"output" + str(j) +".jpg"), imgData.image)
                row["OutputImage"] = "output" + str(j) + ".jpg"
                self.writer.writerow(row)

def processImages(j,args, im):
    img = args["source"] + "/" + im
    imgData = ImageData(img)
    results = imgData.process_image()
    results2 = imgData.process_inverted_image()
    writer_class = Result_Iter(writer)
    writer_class.update_csv(results)
    writer_class.update_csv(results2)

if __name__ == '__main__':
    start_time = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--min-conf", type=int, default=0,
        help="mininum confidence value to filter weak text detection")
    ap.add_argument("-s", "--source", required=True, help="path to image folder to be OCR'd")
    ap.add_argument("-d", "--dest", required=True,help="folder to save OCR'd output images")
    ap.add_argument("-o", "--csv", required=True, help="csv output file to contain file db")
    ap.add_argument("-w", "--wordlist", required=True, help="wordlist to test against OCR text")
    args = vars(ap.parse_args())
    if not os.path.isdir(args["dest"]):
        os.mkdir(args["dest"])
    with open(args["csv"],mode='w',newline='') as csv_file:
        f = open(args["wordlist"], "r")
        dictionary_words = f.read().splitlines()
        fieldnames = ['Path', 'Image', 'OutputImage','Left', 'Top', 'Width', 'Height', 'Raw Words', 'Confidence', 'Closest Match 1', 'Closest Match 2', 'Closest Match 3']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        j = 0
        for im in os.listdir(args["source"]):
            print("Processing image ",im, ": ", j + 1, "of ", len(os.listdir(args["source"])))
            j += 1
            #p = multiprocessing.Process(target=processImages, args=(j,args, im))
            #p.start()
            img = args["source"] + "/" + im
            imgData = ImageData(img)
            results = imgData.process_image()
            results2 = imgData.process_inverted_image()
            writer_class = Result_Iter(writer)
            writer_class.update_csv(results)
            writer_class.update_csv(results2)
            logging.info('Image: ' + im + " finished processing.")

    total_time = time.time() - start_time
    total_min = total_time / 60
    total_sec = total_time % 60
    logging.info("--- Execution time: " + str(total_min) + " minutes " + str(total_sec) + " seconds ---")
    print("--- Execution time: %s minutes %s seconds ---" % (str(total_min), str(total_sec)))