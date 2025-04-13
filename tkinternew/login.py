import requests

def make_post_request(url, data, headers=None):
    """
    Makes a POST request to the specified URL with the given data and headers.

    Args:
        url (str): The URL to send the POST request to.
        data (dict or str): The data to send in the request body. Can be a dictionary (for JSON) or a string.
        headers (dict, optional): Optional headers to include in the request. Defaults to None.

    Returns:
        requests.Response or None: The response object if the request is successful, None otherwise.
    """
    try:
        if headers:
            response = requests.post(url, json=data, headers=headers) # Assumes JSON data if data is a dict
        else:
            response = requests.post(url, json=data) # Assumes JSON data if data is a dict
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None

def get_token():
    # Example usage:
    url = "http://localhost:8080/api/auth/login" # Replace with your actual endpoint
    data = {
        "userid": "15800121016",
        "password": "12102003"
    } # Example data. Replace with your actual data.
    headers = {"Content-Type": "application/json"} #Example header.

    response = make_post_request(url, data, headers)

    if response:
        print("POST request successful!")
        print("Response status code:", response.status_code)
        try:
            print("Response JSON:", response.json()) # Try printing the response as JSON
        except requests.exceptions.JSONDecodeError:
            print("Response text:", response.text) # If JSON decoding fails, print the response text.
            return response.text # Return the response text if JSON decoding fails.

    else:
        print("POST request failed.")