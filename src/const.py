# src/const.py
from typing import Tuple

ACCESS_DENIED_CODE = 403
ACCESS_DENIED_MSG = "Acceso denegado o credenciales inválidas. Por favor, verifica tus credenciales e inténtalo de nuevo."

TRANSPORT_ERROR_CODE = 501
TRANSPORT_ERROR_MSG = "Error durante la actualización del token"

TIMEOUT_ERROR_CODE = 504
TIMEOUT_ERROR_MSG = "Tiempo de espera agotado durante la actualización del token"

UNEXPECTED_ERROR_CODE = 500
UNEXPECTED_ERROR_MSG = "Ocurrió un error inesperado durante la actualización del token"

AUTORIZATION_PROMPT_MESSAGE = 'Accede a tu cuenta de Google Photos'
AUTORIZATION_CODE_MESSAGE = 'Introduce el código de autorización:'


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