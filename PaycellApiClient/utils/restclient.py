import json
import requests


def make_post_request(url, body_dictionary, header_dictionary):
    return requests.post(url, data=json.dumps(body_dictionary), headers=header_dictionary)


def make_get_request(url, header_dictionary):
    return requests.get(url, headers=header_dictionary)
