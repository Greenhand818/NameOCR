import glob
import os
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw
import random
import pymysql
import utility
from generate_word import build_generate_content
from tqdm import tqdm

sql_info = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Xujiachen@123456',
            'database': 'tryocr1'
}

def generate_pic(content, pic_name, target_path, ttf_path, bg_path, en):  ### 生成图片
    bg_info = os.path.join(bg_path, "bg.txt")
    bg_dict = {}
    with open(bg_info, encoding="utf-8") as bg_f:
        details = bg_f.read().split('\n')
        for detail in details:
            detail_split = detail.split('\t')
            temp = detail_split[1].split(' ')
            for index, x in enumerate(temp):
                temp[index] = list(map(int, x.split(',')))
            bg_dict[detail_split[0]] = temp
    # length = len(content)
    ttf_list = os.listdir(ttf_path)
    ttf = random.sample(ttf_list, 1)
    bgs = glob.glob(os.path.join(bg_path, "*.jpg"))
    bg = random.sample(bgs, 1)
    img = Image.open(bg[0])
    roi = random.sample(bg_dict[bg[0]], 1)[0]

    # 计算区域内颜色深浅
    sum = 0
    hsv_image = cv.imread(bg[0])
    height, width = hsv_image.shape[:2]
    hsv_image = cv.cvtColor(hsv_image, cv.COLOR_BGR2HSV)
    roi_image = hsv_image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2], 2]                ### 高宽
    for x in roi_image:
        for y in x:
            sum += y
    avg = sum // (roi[2] * roi[3])
    if avg > 100:
        color = "#000000"
    else:
        color = "#ffffff"

    image = ImageDraw.Draw(img)
    word_size = random.randint(110, 160)
    if en:
        word_size = word_size // 2
    font = ImageFont.truetype(os.path.join(ttf_path, ttf[0]), word_size)
    textsize = image.textsize(content, font=font, spacing=4)
    # print((roi, textsize))                                                              ### 宽高
    if roi[2] < textsize[0] or roi[3] < textsize[1]:
        word_size = min(int(word_size * roi[2] / textsize[0]) - 2, int(word_size * roi[3] // textsize[1]) - 2)
        font = ImageFont.truetype(os.path.join(ttf_path, ttf[0]), word_size)
        textsize = image.textsize(content, font=font, spacing=4)
    # print(content)
    # print((roi, textsize))
    dw = roi[2] - textsize[0]
    dh = roi[3] - textsize[1]
    # print((dw, dh))
    w_distance = random.randint(0, dw)
    h_distance = random.randint(0, dh)

    area = [roi[0] + w_distance, roi[1] + h_distance]
    # print(area)
    image.text(area, content, font=font, fill=color)

    # 计算适配yolov5输入格式的bbox
    x_center = (area[0] + textsize[0] / 2) / (width+1e-6)
    y_center = (area[1] + textsize[1] / 2) / (height+1e-6)
    w = textsize[0] / (width+1e-6)
    h = textsize[1] / (height+1e-6)
    bbox = [x_center, y_center, w, h]

    # img.show("result")
    ipath = os.path.join(target_path,  pic_name)
    if os.path.exists(ipath):
        os.remove(ipath)
    img.save(ipath)
    return bbox


class BusinessCardGenerator(object):
    def __init__(self, args):
        email_params = {
            'name': 'RandEmail',
            "suffix_path": args.email_suffix
        }
        ch_name_params = {
            'name': 'RandName',
            "last_name_path": args.ch_last_name_path,
            "first_name_path": args.ch_first_name_path
        }
        en_name_params = {
            'name': 'RandName',
            "last_name_path": args.en_first_name_path,
            "first_name_path": args.en_last_name_path
        }
        self.generate_email = build_generate_content(email_params)
        self.ch_generate_name = build_generate_content(ch_name_params)
        self.en_generate_name = build_generate_content(en_name_params)

        self.amount = args.amount
        self.target_path = args.target_path
        self.ttf_path = args.ttf_path
        self.bg_path = args.bg_path

        self.database = args.database

    def __call__(self):
        emails = self.generate_email(self.amount)
        en_names = self.en_generate_name(self.amount // 2, en=True)                   ### 英文名
        ch_names = self.ch_generate_name(self.amount - self.amount // 2)              ### 中文名
        names = en_names + ch_names
        db = pymysql.connect(
            host=sql_info["host"],
            user=sql_info["user"],
            password=sql_info["password"],
            database=sql_info["database"]
        )

        pic_name = []
        print("generate business card:")
        for index in tqdm(range(len(emails)), ncols=100):
            email = emails[index]
            name = names[index]
            if index < self.amount // 2:
                eng = True
            else:
                eng = False
            cursor = db.cursor()
            pic_name.append("%d.jpg" % index)
            bbox = generate_pic(name, pic_name[index], self.target_path, self.ttf_path, self.bg_path, eng)
            bbox = list(map(str, bbox))
            bbox = " ".join(bbox)

            if self.database:
                try:
                    sql = "insert into businesscard (pic_name, email, name, name_bbox) values (%s, %s, %s, %s)"
                    argsql = (pic_name[index], email, name, bbox)
                    cursor.execute(sql, argsql)
                    db.commit()
                except:
                    sql = "update businesscard set email = %s, name = %s, name_bbox = %s where pic_name = %s"
                    argsql = (email, name, bbox, pic_name[index])
                    cursor.execute(sql, argsql)
                    db.commit()
                cursor.close()
        print("success!")


if __name__ == "__main__":
    business_card_generator = BusinessCardGenerator(utility.parse_args())
    business_card_generator()
    # 直接Canny
    # canny_image = cv.Canny(image, 200, 200)
    # cv.imwrite('canny_img.png', canny_image)
