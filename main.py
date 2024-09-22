# main.py
import sys
import os

# Add the src directory to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from auth import authenticate
from const import ACCESS_DENIED_MSG
from albums import get_albums, get_photos_in_album

def main():
    os.system('clear')
    # Ask for the user's email (or any other form of identification)
    user_email = input("Enter your Google email: ")
    service = None

    print("Authenticating...")
    # Authenticate and get the Google Photos service
    service, error = authenticate(user_email)
    if not service:
        print(ACCESS_DENIED_MSG)
        print(error)
        return

    print("Authentication successful.")
    
    print("Getting albums...")
    albums = get_albums(service)
    if not albums:
        print('No albums found.')
        return

    print("Albums finded:")
    print("Select number of album to delete:")
    for i, album in enumerate(albums):
        print(f"{i}) {album['title']}")
    
    album_index = -1
    while album_index < 0 or album_index >= len(albums):
        album_index = int(input("Enter the number of the album to delete: "))
    
    list_photos = get_photos_in_album(service, albums[album_index]['id'])
    if not list_photos:
        print('No photos found.')
        return

    print("Number of photos found in the album:", len(list_photos))

if __name__ == '__main__':
    main()
