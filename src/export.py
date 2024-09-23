# export.py
import os
import requests
from tqdm import tqdm

def download_album(photos_list, album_title, disk_mount_point: str, user_email):
    file_path = os.path.join(disk_mount_point, user_email, album_title)
    os.makedirs(file_path, exist_ok=True)

    total_photos = len(photos_list)
    exported_photos = 0
    for photo in tqdm(photos_list, desc="Exportando fotos"):
        try:
            filename = photo['filename']
            if os.path.exists(os.path.join(file_path, filename)):
                continue
            is_video = filename.lower().endswith('.mov')
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
            exported_photos += 1
        except Exception as e:
            print(f"Error descargando foto: {e}")
    
    print(f"Descargadas {exported_photos} fotos en {file_path} de {total_photos}")
    return exported_photos == total_photos
