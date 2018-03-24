import cv2
import numpy as np
import os.path

fileName = ['9','8','7','6','5','4','3','2','1','0']
for i in range(4,109):
    if i < 10:
        img = cv2.imread('img/Urdu WordNet 1.0 Wordlist-00' + str(i) +'.png')
        img_name = 'Urdu WordNet 1.0 Wordlist-00' + str(i)
    elif (i > 9) and (i < 100):
        img = cv2.imread('img/Urdu WordNet 1.0 Wordlist-0' + str(i) + '.png')
        img_name = 'Urdu WordNet 1.0 Wordlist-0' + str(i)
    else:
        img = cv2.imread('img/Urdu WordNet 1.0 Wordlist-' + str(i) + '.png')
        img_name = 'Urdu WordNet 1.0 Wordlist-' + str(i)

    print('Image Name: ' + img_name)

    dir = 'cropped/' + img_name

    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            print('Directory Created: ' + dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise



    #Some House keeping Stuff
    '''

    if os.path.isfile(img):
        print(img + ' - OK')
    else:
        print(img + 'No')
    '''


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(gray,kernel,iterations = 2)
    kernel = np.ones((4,4),np.uint8)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)

    edged = cv2.Canny(dilation, 30, 200)

    _, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.boundingRect(cnt) for cnt in contours]
    rects = sorted(rects,key=lambda  x:x[1],reverse=True)



    i = -1
    j = 1
    y_old = 5000
    x_old = 5000
    for rect in rects:

        x,y,w,h = rect
        area = w * h

        if (w > 180) and (w < 240) and (h > 30):
            out = img[y+10:y+h-10,x+10:x+w-10]
            cv2.imwrite(dir + '/' + fileName[i] + '_' + str(j) + '.png', out)
            #print()

        j+=1
