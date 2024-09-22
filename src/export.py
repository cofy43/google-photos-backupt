# export.py
import os
import requests

def download_album(photos_list, album_title, disk_mount_point: str, user_email):
    file_path = os.path.join(disk_mount_point, user_email, album_title)
    os.makedirs(file_path, exist_ok=True)

    total_photos = len(photos_list)
    exported_photos = 0
    for photo in photos_list:
        try:
            filename = photo['filename']
            photo_url = photo['baseUrl'] + '=d'  # URL para descargar a tamaño completo
            print(f"Descargando {filename}...")
            img_data = requests.get(photo_url).content
            with open(os.path.join(file_path, filename), 'wb') as f:
                f.write(img_data)
                f.close()
            exported_photos += 1
        except Exception as e:
            print(f"Error descargando foto: {e}")
    
    print(f"Descargadas {exported_photos} fotos en {file_path} de {total_photos}")
    return exported_photos == total_photos
