import os
from datetime import datetime
from urllib import request

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

db_name = "spypoint_images"
db_username = "root"
db_password = "Khan1234"
db_host = "localhost"

engine = create_engine(f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}")
Base.prepare(engine, reflect=True)
session = Session(engine)

# Model Name
Images = Base.classes.images


def insert_into_db(images_obj):
    if images_obj:
        session.add_all(images_obj)
        session.commit()
        print("All data saved into db...")


def convert_datetime_into_string(date_obj):
    return date_obj.strftime('%A, %B %-d, %Y')


def most_recent_images():
    recent_image_dict = {}
    images = session.query(Images.image_date, Images.location).distinct().order_by(Images.image_date.desc())
    for image in images:
        if image.location not in recent_image_dict:
            recent_image_dict[image.location] = image.image_date
    return recent_image_dict


def download_image(url, folder_id, image_id):
    try:
        current_dir = os.path.join(os.getcwd(), "images")
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        image_name = f"{folder_id}_{image_id}.jpg"
        image_path = os.path.join(current_dir, image_name)
        if not os.path.exists(image_path):
            request.urlretrieve(url, image_path)
        return image_path
    except Exception as e:
        print("Download image Exception\n", str(e))


def convert_string_into_datetime(date_str):
    return datetime.strptime(date_str, '%A, %B %d, %Y')


# Iterate over the provided data and convert into list of images object
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
    most_recent_images()
