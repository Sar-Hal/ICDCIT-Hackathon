import time
import requests

def make_request_with_rate_limit(url, headers, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get("Retry-After", 1))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                retries += 1
            else:
                return response
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            retries += 1
            time.sleep(2 ** retries)

    print("Max retries exceeded.")
    return None

url = "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"
headers = {"Authorization": "Bearer url"}

response = make_request_with_rate_limit(url, headers)
if response:
    print(response.json())
else:
    print("Failed to get a response from the API.")