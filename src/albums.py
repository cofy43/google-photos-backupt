# albums.py
from googleapiclient.discovery import build

def get_albums(service: build) -> list:
    albums = []
    next_page_token = None

    while True:
        response = service.albums().list(pageSize=50, pageToken=next_page_token).execute()
        albums.extend(response.get('albums', []))
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return albums

def get_photos_in_album(service: build, album_id: str) -> list:
    photos = []
    next_page_token = None

    while True:
        response = service.mediaItems().search(body={'albumId': album_id, 'pageSize': 50, 'pageToken': next_page_token}).execute()
        photos.extend(response.get('mediaItems', []))
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return photos

def delete_album(service, album_id):
    try:
        service.albums().delete(albumId=album_id).execute()
        print(f"Album {album_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting album: {e}")
