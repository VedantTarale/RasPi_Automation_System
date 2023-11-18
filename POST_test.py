import requests

# The URL to which you want to send the POST request
url = "http://localhost:8000/add_reading/"

# Data to be sent in the POST request (in this example, a dictionary)
data = {
    "temp": 100.5,
    "pressure": 10500.13,
    "moisture": 178,
    "motor": 0
}

# Make the POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.text)
