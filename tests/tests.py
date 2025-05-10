import requests

def main():
    # try to GET admin page
    print("Try to GET admin page: ", make_request("http://localhost:5000/admin/"))

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


def make_request(url, method="GET", data=None):

    response = None

    if method == "GET":
        response = requests.get(url=url)

        return (True if response.url == url else False, response.status_code, response.url, response.headers)

    elif method == "POST":
        response = requests.post(url=url, data=data)

        return (False if response.url == url else True, response.status_code, response.url, response.headers)

    else:
        raise ValueError("Invalid Request Method")


if __name__ == "__main__":
    main()

