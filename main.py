# main.py
import sys
import os
import re

# Add the src directory to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from auth import authenticate
from const import ACCESS_DENIED_MSG, TITLE
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

def show_menu():
    print("1) Export an album")
    print("2) Exit")
    return get_user_input("Enter the number of the option: ", [1, 2])

def export_albums(albums, user_email):
    print("Albums finded:")
    albums_data = [[i+1, x[0]['title'], len(x[1])] for i, x in enumerate(albums)]
    print(tabulate(albums_data, headers=["Id", "Name", "Items"], tablefmt="grid"))

    album_index = get_user_input("Enter the number of the album to export: ", list(range(1, len(albums))))
    
    list_photos = albums[album_index-1][1]
    if not list_photos:
        print('No photos found in the album.')
        return

    print("Number of photos found in the album:", len(list_photos))

    external_disk_search = True
    while external_disk_search:
        internal_disks, external_disks = get_disk_partitions()

        disk_type = ""
        if len(external_disks) > 0:
            print("Do you whant internal or external disk?")
            while disk_type not in ['internal', 'external']:
                disk_type = input("Enter 'internal' or 'external': ")
        else:
            print("No external disks found.")
            external_disk_search = get_user_input("Do you want search for external disk again?\n1) Yes\n2) No\n", [1,2]) == 1
            disk_type = 'internal'

    disk_mount_point = os.path.expanduser("~/Documents")

    if disk_type == 'internal':
        if not internal_disks:
            print("No internal disks found.")
            return
        print("Internal Disks:")
        disks_headers = ["Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        internal_disks_data = [[disk['device'], disk['mountpoint'], disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for disk in internal_disks]
        print(tabulate(internal_disks_data, headers=disks_headers, tablefmt="grid"))
        print("Internal disk selected. The album will be downloaded to the Documents folder.")
    else:
        print("External disk selected.")
        print("Select the external disk number:")
        external_disks_data = [[i+1, disk['device'], f"💽 {disk['mountpoint']}", disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for i, disk in enumerate(external_disks)]
        external_disk_header = ["Number", "Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        print(tabulate(external_disks_data, headers=external_disk_header, tablefmt="grid"))
        
        external_disk_index = get_user_input("Enter the number of the external disk: ", list(range(1, len(external_disks))))

        disk_mount_point = external_disks[external_disk_index-1]['mountpoint']
    
    download_album(
        list_photos,
        albums[album_index-1][0]['title'], 
        disk_mount_point,
        user_email)

def main():
    os.system('clear')
    print(TITLE)
    user_email = ""
    # Ask for the user's email (or any other form of identification)
    while re.match(r"[^@]+@[^@]+\.[^@]+", user_email) is None:
        user_email = input("Enter your Google email 📧: ")
    # Authenticate and get the Google Photos service
    print("Authenticating...")
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

    albums_photos = [[x, get_photos_in_album(service, x['id'])] for x in tqdm(albums, desc="Procesando álbumes")]

    while show_menu() == 1:
        export_albums(albums_photos, user_email)

    service.close()

if __name__ == '__main__':
    main()
