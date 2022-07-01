import pymysql
import os
from tqdm import tqdm

sql_info = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Xujiachen@123456',
            'database': 'tryocr1'
}


def GenerateLabel(sql_info, label_path):
    db = pymysql.connect(
        host=sql_info["host"],
        user=sql_info["user"],
        password=sql_info["password"],
        database=sql_info["database"]
    )
    cursor = db.cursor()
    sql = "select pic_name, name_bbox from businesscard"
    cursor.execute(sql)
    all_data = cursor.fetchall()
    print("generate yolo labels:")
    for index in tqdm(range(len(all_data)), ncols=100):
        data = all_data[index]
        file_name = data[0].replace('jpg', 'txt')
        bbox = data[1]
        label = os.path.join(label_path, file_name)
        detail = ['0', bbox]
        detail = '\t'.join(detail)
        with open(label, 'w') as f:
            f.seek(0)
            f.truncate()
            f.write(detail)
    print("success!")


if __name__ == "__main__":
    GenerateLabel(sql_info, "./Labels")