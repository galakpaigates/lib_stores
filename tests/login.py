import requests
from tests import make_request

def main():
    print("\nTesting Login Page: ", make_request("http://localhost:5000/"))

    print("\n\nTrying to Login as a Store with Legitimate Information: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'password': 'louLOU2020@!', 
            'email': 'sales@louisvuitton.com'
        })
    )

    print("\n\nTrying to Login as a Store with wrong password: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'email': 'sales@louisvuitton.com',
            'password': 'louLOU2030@!' 
        })
    )

    print("\n\nTrying to Login as a Store with password that doesn't meet the requirement: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'email': 'sales@louisvuitton.com',
            'password': 'sdfk@!' 
        })
    )
    
    print("\n\nTrying to Login as a Store with email that doesn't exists: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'email': 'sales@louisvuitton.com',
            'password': 'sdASDFDSfk@!2233'
        })
    )

    print("\n\nTrying to Login as a Store without email: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'email': '',
            'password': 'asdASD2023@#!'
        })
    )

    print("\n\nTrying to Login as a Store without password: ", make_request(
        url="http://localhost:5000/login/store/",
        method="POST", 
        data={
            'email': 'sales@louisvuitton.com',
            'password': ''
        })
    )


if __name__ == "__main__":
    main()

