# export.py
import os
import requests

def download_album(service, album_id, album_title, disk_mount_point: str, user_email):
    file_path = os.path.join(disk_mount_point, user_email, album_title)
    os.makedirs(file_path, exist_ok=True)
    next_page_token = None

    total_photos = 0
    exported_photos = 0
    while True:
        response = service.mediaItems().search(body={
            'albumId': album_id,
            'pageSize': 100,
            'pageToken': next_page_token
        }).execute()

        media_items = response.get('mediaItems', [])
        if not media_items:
            print(f"No se encontraron fotos en el álbum: {album_title}")
            break
        total_photos += len(media_items)
        for item in media_items:
            try:
                filename = item['filename']
                photo_url = item['baseUrl'] + '=d'  # URL para descargar a tamaño completo
                print(f"Descargando {filename}...")
                img_data = requests.get(photo_url).content
                with open(os.path.join(file_path, filename), 'wb') as f:
                    f.write(img_data)
                    f.close()
                exported_photos += 1
            except Exception as e:
                print(f"Error descargando foto: {e}")

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    print(f"Descargadas {exported_photos} fotos en {file_path} de {total_photos}")
    return exported_photos == total_photos
