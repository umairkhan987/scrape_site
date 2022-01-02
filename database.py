import os
from datetime import datetime
from urllib import request

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()
engine = create_engine("mysql+pymysql://root:Khan1234@localhost/spypoint_images")
Base.prepare(engine, reflect=True)
session = Session(engine)

# Model Name
Images = Base.classes.images


def get_image():
    images = session.query(Images).all()
    if images:
        for image in images:
            print(f"{image.id}, {image.path}, {image.location}, {image.image_date}")


def insert_into_db(images_obj):
    if images_obj:
        session.add_all(images_obj)
        session.commit()


def most_recent_date():
    pass


def download_image(url, folder_id, image_id):
    current_dir = os.path.join(os.getcwd(), "images")
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)
    image_name = f"{folder_id}_{image_id}.jpg"
    image_path = os.path.join(current_dir, image_name)
    request.urlretrieve(url, image_path)
    return image_path


def convert_string_into_datetime(date_str):
    return datetime.strptime(date_str, '%A, %B %d, %Y')


def process_data(data):
    images_obj = []
    if data:
        for li in data:
            download_image_url = download_image(li[4], li[0], li[3])
            images_obj.append(
                Images(path=download_image_url, location=li[1], image_date=convert_string_into_datetime(li[2]))
            )

    if images_obj:
        insert_into_db(images_obj)


if __name__ == "__main__":
    data = [
        ['603e89924b85000015901db5', 'Frank’s Feeder LINK-MICRO-S-LTE-YGEP', 'Saturday, January 1, 2022', '61d11af64cbdec001415101f', 'https://s3.amazonaws.com/spypoint-production-account-failover/5ff9caaa6ce1c40014c50231/603e89924b85000015901db5/20220102/PICT4501_202201020324Df2NA.jpg?X-Amz-Expires=86400&X-Amz-Date=20220102T033810Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIATVANQEDJ5KPEZXK2%2F20220102%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=a356ea8964f9700164487af95ca64094613c4621f1403df6287da75e6100f066'],
        ['603e89924b85000015901db5', 'Frank’s Feeder LINK-MICRO-S-LTE-YGEP', 'Saturday, January 1, 2022', '61d11af64cbdec0014151020', 'https://s3.amazonaws.com/spypoint-production-account-failover/5ff9caaa6ce1c40014c50231/603e89924b85000015901db5/20220102/PICT4500_202201020324Km96F.jpg?X-Amz-Expires=86400&X-Amz-Date=20220102T033832Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIATVANQEDJ5KPEZXK2%2F20220102%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=a7f337e17a451ea9704c1960d15c3135e95375f0c25798433e52af505f358486']]
    process_data(data)