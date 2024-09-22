# main.py
import sys
import os

# Add the src directory to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from auth import authenticate
from const import ACCESS_DENIED_MSG
from albums import get_albums, get_photos_in_album
from units import get_disk_partitions
from export import download_album

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
    print("Select number of album to export:")
    for i, album in enumerate(albums):
        print(f"{i+1}) {album['title']}")
    
    album_index = -1
    while album_index < 0 or album_index >= len(albums):
        album_index = int(input("Enter the number of the album to export: "))
    
    list_photos = get_photos_in_album(service, albums[album_index-1]['id'])
    if not list_photos:
        print('No photos found.')
        return

    print("Number of photos found in the album:", len(list_photos))

    internal_disks, external_disks = get_disk_partitions()

    print("Internal Disks:")
    for disk in internal_disks:
        print(f"Device: {disk['device']}, Mountpoint: {disk['mountpoint']}, Total: {disk['total']}, Used: {disk['used']}, Free: {disk['free']}, Percent: {disk['percent']}%")

    print("\nExternal Disks:")
    for disk in external_disks:
        print(f"Device: {disk['device']}, Mountpoint: {disk['mountpoint']}, Total: {disk['total']}, Used: {disk['used']}, Free: {disk['free']}, Percent: {disk['percent']}%")

    print("Do you whant internal or external disk?")
    disk_type = ""
    while disk_type not in ['internal', 'external']:
        disk_type = input("Enter 'internal' or 'external': ")
    
    disk_mount_point = os.path.expanduser("~/Documents")

    if disk_type == 'internal':
        print("Internal disk selected.")
    else:
        print("External disk selected.")
        print("Select the external disk number:")
        for i, disk in enumerate(external_disks):
            print(f"{i+1}) {disk['mountpoint']}")
        external_disk_index = -1
        while external_disk_index < 0 or external_disk_index >= len(external_disks) + 1:
            external_disk_index = int(input("Enter the number of the external disk: "))
        disk_mount_point = external_disks[external_disk_index-1]['mountpoint']
    
    download_album(
        list_photos,
        albums[album_index-1]['title'], 
        disk_mount_point,
        user_email)

if __name__ == '__main__':
    main()
