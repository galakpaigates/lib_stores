import requests
from tests import make_request

def main():
    # test the home page
    print("Home Page: ", make_request("http://localhost:5000/"))

    # test all stores route
    print("All Stores Page: ", make_request("http://localhost:5000/stores/"))

