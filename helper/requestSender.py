import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

class RequestSender:
    def __init__(self, server_url):
        self.server_url = server_url

    def _make_request(self, endpoint, data, method='POST'):    # make this private
        headers = {'content-Type': 'application/json'}
        try:
            if method == 'POST':
                response = requests.post(f'{self.server_url}/{endpoint}', json=data, headers=headers)
                print(response)
            elif method == 'GET':
                response = requests.get(f'{self.server_url}/{endpoint}', json=data, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method: Use 'POST' or 'GET'.")
            
            # Raise exception for bad status codes (4xx, 5xx)
            response.raise_for_status()
            data = response.json()
            print("Response JSON:", data)
            return data
        
        except HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except ConnectionError as conn_err:
            return {"error": f"Connection error occurred: {conn_err}"}
        except Timeout as timeout_err:
            return {"error": f"Timeout error occurred: {timeout_err}"}
        except RequestException as req_err:
            return {"error": f"An error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"Unexpected error: {err}"}

    def check_user(self, email):
        email_data = {'email': email}
        return self._make_request('check-user', email_data)

    def registration(self, email, password):
        register_data = {'email': email, 'password': password}
        print(register_data)
        return self._make_request('register', register_data)

    def login(self, email, password):
        login_data = {'email': email, 'password': password}
        return self._make_request('login', login_data)
    
    def getKey(self):
        return self._make_request('get-key', {})
