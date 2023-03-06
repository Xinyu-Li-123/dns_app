"""
This program sends HTTP PUT request to FS to register the FS to AS under the url /register

The request body is a JSON object with the following fields:
{
    “hostname”: “fibonacci.com”, 
    “ip”: “172.18.0.2”,
    “as_ip”: “10.9.10.2”,
    “as_port”: “30001”
}
"""

import requests

# send HTTP PUT request to FS to register the FS to AS
fs_ip = "localhost"
fs_port = "9090"
url = "http://{}:{}/register".format(
    fs_ip, fs_port 
)

# request body
body = {
    "hostname": "fibonacci.com",
    "ip": "localhost",
    "as_ip": "localhost",
    "as_port": "53533"
}

print("Sending HTTP PUT request to FS at {} to register the FS to AS...".format(
    url 
))
print("Request body: {}".format(body))

# send HTTP PUT request
response = requests.put(url, json=body)

# print response
print(response.status_code)
print(response.text)


