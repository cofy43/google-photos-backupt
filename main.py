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

from tabulate import tabulate
from tqdm import tqdm

def get_user_input(prompt: str, valid_options: list) -> int:
    while True:
        try:
            user_input = int(input(prompt))
            if user_input not in valid_options and len(valid_options) > 0:
                raise ValueError
            return user_input
        except ValueError:
            print("Invalid input. Try again.")

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

    albumns_headers = ["Id", "Name", "Items"]
    albums_photos = [[x, get_photos_in_album(service, x['id'])] for x in tqdm(albums, desc="Procesando álbumes")]
    print("Albums finded:")
    albums_data = [[i, x[0]['title'], len(x[1])] for i, x in enumerate(albums_photos)]
    print(tabulate(albums_data, headers=albumns_headers, tablefmt="grid"))

    album_index = get_user_input("Enter the number of the album to export: ", list(range(1, len(albums))))
    
    list_photos = get_photos_in_album(service, albums[album_index-1]['id'])
    if not list_photos:
        print('No photos found in the album.')
        return

    print("Number of photos found in the album:", len(list_photos))

    internal_disks, external_disks = get_disk_partitions()

    print("Do you whant internal or external disk?")
    disk_type = ""
    while disk_type not in ['internal', 'external']:
        disk_type = input("Enter 'internal' or 'external': ")

    disk_mount_point = os.path.expanduser("~/Documents")

    if disk_type == 'internal':
        if not internal_disks:
            print("No internal disks found.")
            return
        print("Internal Disks:")
        disks_headers = ["Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        internal_disks_data = [[disk['device'], disk['mountpoint'], disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for disk in internal_disks]
        print(tabulate(internal_disks_data, headers=disks_headers, tablefmt="grid"))
        print("Internal disk selected.")
    else:
        print("External disk selected.")
        print("Select the external disk number:")
        external_disks_data = [[i+1, disk['device'], disk['mountpoint'], disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for i, disk in enumerate(external_disks)]
        external_disk_header = ["Number", "Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        print(tabulate(external_disks_data, headers=external_disk_header, tablefmt="grid"))
        
        external_disk_index = get_user_input("Enter the number of the external disk: ", list(range(1, len(external_disks))))

        disk_mount_point = external_disks[external_disk_index-1]['mountpoint']
    
    download_album(
        list_photos,
        albums[album_index-1]['title'], 
        disk_mount_point,
        user_email)

if __name__ == '__main__':
    main()
