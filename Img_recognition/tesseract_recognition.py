import os

import cv2
import pytesseract

INPUT_IMG_ADDRESS = '../Img_processed/Single_char/'
OUTPUT_IMG_ADDRESS = '../Img_processed/Single_char'
CONFIG = ('-l eng --oem 1 --psm 10')


class Counter(object):
    def __init__(self, start=0):
        self.num = start

    def count(self):
        self.num += 1
        return self.num


if __name__ == '__main__':

    counts = {}
    for img_index in range(1, 9108):
        input_image = INPUT_IMG_ADDRESS + str(img_index) + ".jpg"
        raw_img = cv2.imread(input_image)
        letter_text = pytesseract.image_to_string(raw_img, config=CONFIG)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        output_address = os.path.join(OUTPUT_IMG_ADDRESS, '{}'.format(letter_text))
        if not os.path.exists(output_address):
            os.makedirs(output_address)

        p = os.path.join(output_address, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, raw_img)

        # increment the count for the current key
        counts[letter_text] = count + 1
