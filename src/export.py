# export.py
import os
import re
import requests
from tqdm import tqdm

from const import EXPORTING_ALBUMS_CONTENT, EXPORTING_ALBUMS_CONTENT_ERROR
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_photo(photo, file_path):
    try:
        filename = photo['filename']
        if os.path.exists(os.path.join(file_path, filename)):
            return False
        is_video = re.search(r'\.(mov|mp4|avi|mkv|flv|wmv|m4v)$', filename.lower()) is not None
        photo_url = photo['baseUrl'] + '=dv' if is_video else photo['baseUrl'] + '=d'
        img_data = requests.get(photo_url, stream=is_video)
        img_data.raise_for_status()

        with open(os.path.join(file_path, filename), 'wb') as f:
            if is_video:
                for chunk in img_data.iter_content(chunk_size=8192):
                    f.write(chunk)
            else:
                f.write(img_data.content)
            f.close()
        return True
    except Exception as e:
        print(f"{EXPORTING_ALBUMS_CONTENT_ERROR}: {e}")
        return False

def download_album(photos_list, album_title, disk_mount_point: str, user_email):
    file_path = os.path.join(disk_mount_point, user_email, album_title)
    os.makedirs(file_path, exist_ok=True)

    total_photos = len(photos_list)
    exported_photos = 0

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_photo, photo, file_path) for photo in photos_list]
        for future in tqdm(as_completed(futures), total=total_photos, desc=EXPORTING_ALBUMS_CONTENT):
            if future.result():
                exported_photos += 1

    print(f"Descargadas {exported_photos} fotos en {file_path} de {total_photos}")
    return exported_photos == total_photos
