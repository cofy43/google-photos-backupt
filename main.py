# main.py
import sys
import os

# Add the src directory to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from auth import authenticate
from const import ACCESS_DENIED_MSG

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

    if not error:
        print("Authentication successful.")
        print(service)

if __name__ == '__main__':
    main()
