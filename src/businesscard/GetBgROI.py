import cv2 as cv
import os
import utility
import glob

def BgROI(bg_path):
    text_path = os.path.join(bg_path, "bg.txt")
    info = []
    imgs = glob.glob(os.path.join(bg_path, "*.jpg"))
    for img in imgs:
        image = cv.imread(img)
        rois = cv.selectROIs("select ROIs", image, False)
        if type(rois) != tuple:
            rois = rois.tolist()
        detail = [img, rois]
        info.append(detail)
    with open(text_path, 'w') as text_f:
        text_f.seek(0)
        text_f.truncate()
        for line in info:
            line[1] = list(map(str, line[1]))
            for index, x in enumerate(line[1]):
                line[1][index] = x.replace('[', '')
                line[1][index] = line[1][index].replace(']', '')
                line[1][index] = line[1][index].replace(' ', '')
            text_f.write(line[0] + '\t' + " ".join(line[1]) + '\n')

if __name__ == "__main__":
    args = utility.parse_args()
    BgROI(args.bg_path)