# main.py
import sys
import os
import re
import gettext

# Add the src directory to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Configuración de gettext
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')


from auth import authenticate
from const import *
from albums import get_albums, get_photos_in_album
from units import get_disk_partitions
from export import download_album

from tabulate import tabulate
from tqdm import tqdm

def set_language(language):
    print(language)
    lang = gettext.translation('messages', localedir, languages=[language])
    lang.install()
    global _
    _ = lang.gettext

def get_user_input(prompt: str, valid_options: list) -> int:
    while True:
        try:
            user_input = int(input(prompt))
            if user_input not in valid_options and len(valid_options) > 0:
                raise ValueError
            return user_input
        except ValueError:
            print(_(INVALID_INPUT_MSG))

def show_menu():
    print(_(MENU_OPTION_ONE))
    print(_(MENU_OPTION_TWO))
    return get_user_input(_(MENU_CORRECT_OPTIONS), [1, 2])

def export_albums(albums, user_email):
    print(_(ALBUMS_FINDED_MSG))
    albums_data = [[i+1, x[0]['title'], len(x[1])] for i, x in enumerate(albums)]
    print(tabulate(albums_data, headers=["Id", "Name", "Items"], tablefmt="grid"))

    album_index = get_user_input(_(GET_ALBUM_INDEX_PROMPT), list(range(1, len(albums))))
    
    list_photos = albums[album_index-1][1]
    if not list_photos:
        print(_(NOT_PHOTOS_IN_ALBUM_MSG))
        return

    print(_(NUMBER_OF_PHOTOS_MSG), len(list_photos))

    external_disk_search = True
    while external_disk_search:
        internal_disks, external_disks = get_disk_partitions()

        disk_type = ""
        if len(external_disks) > 0:
            print(_(INTERNAL_OR_EXTERNAL_QUESTION))
            while disk_type not in ['internal', 'external']:
                disk_type = input(_(DISK_TYPE_PROMPT))
        else:
            print(_(NO_EXTERNAL_DISKS_MSG))
            external_disk_search = get_user_input(_(RESEARCH_EXTERNAL_DISK_AGAIN), [1,2]) == 1
            disk_type = 'internal'

    disk_mount_point = os.path.expanduser("~/Documents")

    if disk_type == 'internal':
        if not internal_disks:
            print(_(NO_EXTERNAL_DISKS_MSG))
            return

        disks_headers = ["Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        internal_disks_data = [[disk['device'], disk['mountpoint'], disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for disk in internal_disks]
        print(tabulate(internal_disks_data, headers=disks_headers, tablefmt="grid"))
        print(_(INTERNAL_DISK_MSG))
    else:
        print(_(EXTERNAL_DISK_SELECTED_MSG))
        external_disks_data = [[i+1, disk['device'], f"💽 {disk['mountpoint']}", disk['total'], disk['used'], disk['free'], f"{disk['percent']} %"] for i, disk in enumerate(external_disks)]
        external_disk_header = ["Number", "Device", "Mountpoint", "Total", "Used", "Free", "Percent"]
        print(tabulate(external_disks_data, headers=external_disk_header, tablefmt="grid"))
        
        external_disk_index = get_user_input(_(EXTERNAL_DISK_INDEX_PROMPT), list(range(1, len(external_disks))))

        disk_mount_point = external_disks[external_disk_index-1]['mountpoint']
    
    download_album(
        list_photos,
        albums[album_index-1][0]['title'], 
        disk_mount_point,
        user_email)

def main():
    os.system('clear')
    print("Choose your language / Elige tu idioma:")
    print("1) English")
    print("2) Español")
    language_option = get_user_input("Enter the number of the option / Elige el número de la opcion:\n", [1, 2])

    if language_option == 1:
        set_language('en')
    elif language_option == 2:
        set_language('es')

    print(TITLE)
    user_email = ""
    # Ask for the user's email (or any other form of identification)
    while re.match(r"[^@]+@[^@]+\.[^@]+", user_email) is None:
        user_email = input(_(USER_EMAIL_PROMPT))
    # Authenticate and get the Google Photos service
    print(_(AUTENTICATING_MSG))
    service, error = authenticate(user_email)

    if not service:
        print(_(ACCESS_DENIED_MSG))
        print(error)
        return

    print(_(AUTH_COMPLETE_MSG))
    
    print(_(GET_ALBUMS_MSG))
    albums = get_albums(service)
    if not albums:
        print(_(NO_ALBUMS))
        return

    albums_photos = [[x, get_photos_in_album(service, x['id'])] for x in tqdm(albums, desc=_(PROCESSING_ALBUMS_MSG))]

    while show_menu() == 1:
        export_albums(albums_photos, user_email)

    service.close()

if __name__ == '__main__':
    main()
