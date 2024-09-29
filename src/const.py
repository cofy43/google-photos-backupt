# src/const.py
from typing import Tuple

TITLE = """
 ▗▄▄▖ ▗▄▖  ▗▄▖  ▗▄▄▖▗▖   ▗▄▄▄▖    ▗▖    ▗▄▖  ▗▄▄▖ ▗▄▖ ▗▖   
▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌       ▐▌   ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌   
▐▌▝▜▌▐▌ ▐▌▐▌ ▐▌▐▌▝▜▌▐▌   ▐▛▀▀▘    ▐▌   ▐▌ ▐▌▐▌   ▐▛▀▜▌▐▌   
▝▚▄▞▘▝▚▄▞▘▝▚▄▞▘▝▚▄▞▘▐▙▄▄▖▐▙▄▄▖    ▐▙▄▄▖▝▚▄▞▘▝▚▄▄▖▐▌ ▐▌▐▙▄▄▖                                                
                                                           
▗▄▄▖  ▗▄▖  ▗▄▄▖▗▖ ▗▖▗▖ ▗▖▗▄▄▖                              
▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌▗▞▘▐▌ ▐▌▐▌ ▐▌                             
▐▛▀▚▖▐▛▀▜▌▐▌   ▐▛▚▖ ▐▌ ▐▌▐▛▀▘                              
▐▙▄▞▘▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌▝▚▄▞▘▐▌                                
                                                           
"""
ACCESS_DENIED_CODE = 403
ACCESS_DENIED_MSG = "Access denied or invalid credentials. Please check your credentials and try again."

TRANSPORT_ERROR_CODE = 501
TRANSPORT_ERROR_MSG = "Error during token update"

TIMEOUT_ERROR_CODE = 504
TIMEOUT_ERROR_MSG = "Timeout during token update"

UNEXPECTED_ERROR_CODE = 500
UNEXPECTED_ERROR_MSG = "An unexpected error occurred during the token update"

AUTHORIZATION_PROMPT_MESSAGE = 'Access your Google Photos account'
AUTHORIZATION_CODE_MESSAGE = 'Enter the authorization code:'

INVALID_INPUT_MSG = "Invalid input. Try again."

MENU_OPTION_ONE = "1) Export an album"
MENU_OPTION_TWO = "2) Exit"
MENU_CORRECT_OPTIONS = "Enter the number of the option: "

ALBUMS_FINDED_MSG = "Albums finded:"

GET_ALBUM_INDEX_PROMPT = "Enter the number of the album to export: "

NOT_PHOTOS_IN_ALBUM_MSG = "No photos found in the album."

NUMBER_OF_PHOTOS_MSG = "Number of photos found in the album:"

INTERNAL_OR_EXTERNAL_QUESTION = "Do you want internal or external disk?"

DISK_TYPE_PROMPT = "1) 'internal'\n2)'external':\n"

NO_EXTERNAL_DISKS_MSG = "No external disks found."

RESEARCH_EXTERNAL_DISK_AGAIN = "Do you want search for external disk again?\n1) Yes\n2) No\n"

INTERNAL_DISK_MSG = "Internal disk selected. The album will be downloaded to the Documents folder."

EXTERNAL_DISK_SELECTED_MSG = "External disk selected."

EXTERNAL_DISK_INDEX_PROMPT = "Enter the number of the external disk: "

USER_EMAIL_PROMPT = "Enter your Google email 📧: "

AUTENTICATING_MSG = "Authenticating..."

AUTH_COMPLETE_MSG = "Authentication complete."

GET_ALBUMS_MSG = "Getting albums..."

NO_ALBUMS = "No albums found."

PROCESSING_ALBUMS_MSG = "Processing albums"
EXPORTING_ALBUMS_CONTENT = "Exportando fotos"
EXPORTING_ALBUMS_CONTENT_ERROR = "Error descargando foto"

def print_error_message(message: str, error: Exception) -> Tuple[None, int]:
    print(f"{message}: {error}")

def access_denied_error(e: Exception) -> Tuple[None, int]:
    print_error_message(ACCESS_DENIED_MSG, e)
    return None, ACCESS_DENIED_CODE

def transport_error(e: Exception) -> Tuple[None, int]:
    print_error_message(TRANSPORT_ERROR_MSG, e)
    return None, TRANSPORT_ERROR_CODE

def timeout_error(e: Exception) -> Tuple[None, int]:
    print_error_message(TIMEOUT_ERROR_CODE, e)
    return None, TIMEOUT_ERROR_CODE

def user_access_token_error(e: Exception) -> Tuple[None, int]:
    print_error_message("Error durante la actualización del token", e)

def unexpected_error(e: Exception) -> Tuple[None, int]:
    print_error_message(UNEXPECTED_ERROR_MSG, e)
    return None, UNEXPECTED_ERROR_CODE