from PIL import Image, ImageDraw
import random, argparse
# Settings
parser = argparse.ArgumentParser()
parser.add_argument('input', help='font image source')
parser.add_argument('fontwidth', help='width of the font')
parser.add_argument('fontheight', help='height of the font')
parser.add_argument('-o', help='target image path', default='./authcode.png')
parser.add_argument('-l', help='authcode length', default=4)
parser.add_argument('-s', help='salt counts', default=200)
args = parser.parse_args()
fontImgPath = args.input
fontWidth = int(args.fontwidth)
fontHeight = int(args.fontheight)
targetImgPath = args.o
codeLength = int(args.l)
saltNum = int(args.s)
base = ('0','1','2','3','4','5','6','7','8','9',
      'A','B','C','D','E','F','G','H','I','J',
      'K','L','M','N','O','P','Q','R','S','T',
      'U','V','W','X','Y','Z')
# Generate Authcode Image
def getAuthcode(base, fontImgPath, codeLength, fontWidth, fontHeight):
    code = ''
    fontImg = Image.open(fontImgPath)
    codeImg = Image.new('RGBA', (fontWidth*codeLength, fontHeight+6), (255,255,255,0))
    for k in range(codeLength):
        randInt = random.randint(0,len(base)-1)
        code = ''.join((code, base[randInt]))
        img_s = fontImg.crop((randInt*fontWidth,0,(randInt+1)*fontWidth,fontHeight))
        img_s = img_s.rotate(random.randint(-30,30))
        codeImg.paste(img_s, (k*fontWidth,3))
    return codeImg, code
# Add Salt
def addSalt(image, saltNum):
    width, height = image.size
    count = 0
    while count < saltNum:
        randX = random.randint(0, width-1)
        randY = random.randint(0, height-1)
        if image.getpixel((randX, randY))[-1] == 0:
            image.putpixel((randX, randY), (random.randint(100,255), random.randint(100,255), random.randint(100,255), 255))
            count += 1
        else:
            continue
## Add Lines
def addLines(image):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    for k in range(2):
        randHeight = (height/2)*(k%2)+random.randint(5, (height-1)/2-5)
        startPoint = (0, randHeight)
        if random.random() < 0.5:
            endPoint = (width-1, randHeight+random.randint(0,5))
        else:
            endPoint = (width-1, randHeight-random.randint(0,5))
        draw.line((startPoint, endPoint), fill=(0,0,0,255))
    del draw
# Main
if __name__ == '__main__':
    authcode, code = getAuthcode(base, fontImgPath, codeLength, fontWidth, fontHeight)
    addSalt(authcode, saltNum)
    addLines(authcode)
    authcode.save("../generated_image/", 'PNG')
    print ('Generate Authcode: ',code)