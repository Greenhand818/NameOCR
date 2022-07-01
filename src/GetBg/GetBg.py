import glob
import cv2 as cv
import os
import utility
import numpy as np


def GetBackground(source, result):
    imgs = glob.glob(os.path.join(source, "*.jpg"))
    for img in imgs:
        image = cv.imread(img)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        roi = cv.selectROI("select an area to remove words", image, False)
        print(roi)
        # 方法二：使用opencv的inpaint图像修复方法，收集周边像素信息，来得到结果。
        h, w = image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]].shape[:2]
        mask[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = np.ones((h, w), dtype=np.uint8)
        dst = cv.inpaint(image, mask, 3, cv.INPAINT_NS)
        # 方法一：将区域中图像像素全部设为其投影到x或y轴上的点的像素
        # image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = np.repeat(np.expand_dims(image[roi[1] - 1, roi[0]:roi[0] + roi[2]], 0), h, axis=0)
        # image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = np.repeat(np.expand_dims(image[roi[1]:roi[1] + roi[3], roi[0]-1], 1), w, axis=1)
        # dst[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = np.repeat(np.expand_dims(dst[roi[1] - 1, roi[0]:roi[0] + roi[2]], 0), h, axis=0)

        cv.imwrite(os.path.join(result, img.replace(os.path.join(source, ''), '')), dst)
    # 直接Canny
    # canny_image = cv.Canny(image, 200, 200)
    # cv.imwrite('canny_img.png', canny_image)

if __name__ == '__main__':
    args = utility.parse_args()
    GetBackground(args.source, args.result)