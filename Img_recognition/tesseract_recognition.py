import glob
import os

import cv2
import imutils
import pytesseract

INPUT_IMG_ADDRESS = '../Img_processed/Mix_char'
# OUTPUT_IMG_ADDRESS = '../Img_processed/Mix_char/first_result'

# INPUT_IMG_ADDRESS = '../Img_processed/Single_char'
OUTPUT_IMG_ADDRESS = '../Img_processed/Single_char'

CONFIG = ('-l eng --oem 1 --psm 10')
DOT_INPUT_IMG_ADDRESS = '../Img_processed/Single_char'
DOT_OUTPUT_IMG_ADDRESS = '../Img_processed/Single_char/Dot'
DEBUG = False


class Counter(object):
    def __init__(self, start=0):
        self.num = start

    def count(self):
        self.num += 1
        return self.num


def resize_to_fit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """

    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]
    if DEBUG:
        cv2.imshow('raw image', image)
        cv2.waitKey()
    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)
    if DEBUG:
        cv2.imshow('scaling image', image)
        cv2.waitKey()
    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int(abs(width - image.shape[1]) / 2.0)
    padH = int(abs(height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    pad_color = [255, 255, 255]
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
                               cv2.BORDER_CONSTANT, value=pad_color)
    if DEBUG:
        cv2.imshow('add the border', image)
        cv2.waitKey()

    image = cv2.resize(image, (width, height))

    if DEBUG:
        cv2.imshow('the final output image', image)
        cv2.waitKey()
        cv2.destroyAllWindows()
    # return the pre-processed image
    return image


def clf_single_char():
    counts = {}
    for img_index in range(1, 4180):
        input_image_name = str(img_index) + ".jpg"
        try:
            input_image = os.path.join(INPUT_IMG_ADDRESS, input_image_name)
            raw_img = cv2.imread(input_image)
        except FileNotFoundError:
            continue
        scaled_img = resize_to_fit(raw_img, 13, 20)
        letter_text = pytesseract.image_to_string(scaled_img, config=CONFIG)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        output_address = os.path.join(OUTPUT_IMG_ADDRESS, '{}'.format(letter_text))
        try:
            if not os.path.exists(output_address):
                os.makedirs(output_address)
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            continue

        p = os.path.join(output_address, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, raw_img)

        # increment the count for the current key
        counts[letter_text] = count + 1


def file_move_dir(mv_input_img_address, mv_output_img_address):
    """
    Move the input_address images into output_img_address
    :param mv_input_img_address:
    :param mv_output_img_address:
    :return:
    """
    single_char_list = glob.glob(os.path.join(mv_input_img_address, "*"))
    last_name_of_output_file = int(((os.listdir(mv_output_img_address))[-1]).split(sep='.')[0])

    for img_index in single_char_list:
        # input_image = DOT_IMG_ADDRESS + str(img_index) + ".jpg"
        # mv_input_image = os.path.join(DOT_INPUT_IMG_ADDRESS, "{}.png".format(str(img_index).zfill(6)))
        mv_raw_img = cv2.imread(img_index)
        DEBUG = False
        if DEBUG:
            cv2.imshow('mv_raw_img', mv_raw_img)
            cv2.waitKey()
        img_output_address = os.path.join(mv_output_img_address,
                                          "{}.png".format(str(last_name_of_output_file + 1).zfill(6)))
        cv2.imwrite(img_output_address, mv_raw_img)
        last_name_of_output_file += 1
    for img_index in single_char_list:
        # input_image = DOT_IMG_ADDRESS + str(img_index) + ".jpg"
        # mv_input_image = os.path.join(DOT_INPUT_IMG_ADDRESS, "{}.png".format(str(img_index).zfill(6)))
        # if os.path.exists(mv_input_image):
        os.remove(img_index)
        # print(os.path.split(img_index)[:-1])
    os.removedirs(mv_input_img_address)


def move_all_file():
    """
    依照A-Z，1-9的顺序将文件进行汇总整理
    :return:
    """
    to_change_file = {}
    for index in range(10):
        to_change_file[str(index)] = str(index)
    for index in range(26):
        to_change_file[str(chr(index + ord('A')))] = str(chr(index + ord('A')))
    to_change_file['Dot'] = 'Dot'
    to_change_file['-'] = '-'
    to_change_file['+'] = '+'
    print(to_change_file)

    for key, value in to_change_file.items():
        mv_input_img_address = os.path.join(INPUT_IMG_ADDRESS, key)
        mv_output_img_address = os.path.join(OUTPUT_IMG_ADDRESS, value)
        print("mv_input_img_address: {}".format(mv_input_img_address))
        print('mv_output_img_address: {}'.format(mv_output_img_address))
        try:
            file_move_dir(mv_input_img_address, mv_output_img_address)
        except FileNotFoundError:
            print("FileNotFoundError:{}:{}".format(key, value))
            continue
        except IndexError:
            print("IndexError:{}:{}".format(key, value))
            continue


def file_order_naming(input_file_address):
    """
    re-order image index
    :param input_file_address:
    :return:
    """
    to_order_file = glob.glob(os.path.join(input_file_address, "*"))
    new_order = Counter()
    for file_index in to_order_file:
        basefile_pwd, basefile_index = os.path.split(file_index)
        if DEBUG:
            print("basefile_pwd:{}".format(basefile_pwd))
            print("basefile_index:{}".format(basefile_index))
        new_order_index = os.path.join(basefile_pwd, "{}.png".format(str(new_order.count()).zfill(6)))
        os.rename(file_index, new_order_index)


def reorder_all_file_index():
    file_order_suffix = []
    for i in range(10):
        file_order_suffix.append(str(i))
    for i in range(26):
        file_order_suffix.append((str(chr(i + ord('A')))))
    file_order_suffix.append('+')
    file_order_suffix.append('-')
    file_order_suffix.append('Dot')

    # print(file_order_suffix)
    for index in file_order_suffix:
        file_order_img_addres = os.path.join(INPUT_IMG_ADDRESS, index)
        # print(file_order_img_addres)
        try:
            file_order_naming(file_order_img_addres)
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    # to_change_file = {')': 'O', '$': 'S', 'BD': 'D', 'Cc': 'C', 'fe': 'G',
    #                   'IN': 'N', 'Ww': 'W', 'oO': 'O', 'xX': 'X', 'Ss': 'S',
    #                   'Pp': 'P', 'cD': 'D', 'IA': 'A'}
    # to_change_file = {'GC': 'O', 'QO': 'O', 'I)': 'D', 'Vv': 'V', 'UJ': 'U',
    #                   '8': 'B', '9': 'D', '0': 'O'}

    # to_change_file = {'—': '-', '$': 'S', '~': '-', '8': 'B', 'BD': 'D',
    #                   'Cc': 'C', 'Ic': 'C', 'IE': 'E', 'IL': 'L', 'IN': 'N',
    #                   'le': 'E', 'Of': 'O', 'oO': 'O', 'P,': 'P', 'P;': 'P',
    #                   'Pp': 'P', 'q': 'O', 'QO': 'O', 'S$': 'S', 'Ss': 'S',
    #                   'Tt': 'T', 'uU': 'U', 'Vv': 'V', 'Ww': 'W', 'xX': 'X'}

    # to_change_file = {'@': '0', '_': '-', '~': '-',
    #                   '~-': '-', '-~': '-', '=': '-', '4d': '4', '8g': '8',
    #                   'dc': '0', 'e': 'O', 'e@': 'O', 'f': 'I', 'iw': 'W',
    #                   'j': '1', 'P': '2', 'Q': '0', 'Q@': '0', 'Sg': '9',
    #                   'Ss': '0', 'Ww': 'W'}
    # to_change_file = {'hhb': 'b', 'hh1': '1', 'hhd': 'd', 'hhe': 'e', 'hhh': 'h',
    #                   'hhhh0': '0', 'hhx': 'x', 'hhy': 'y', 'hhw': 'w', 'hht': 't',
    #                   'hhs': 's', 'hho': 'o', 'hhl': 'l', 'hhho': 'O', 'hhi': 'I'}
    # to_change_file = {'-': '-', '0': '0', '1': '1', '2': '2', '3': '8',
    #                   'hh9': '9', 'hhh0': '0'}

    move_all_file()
