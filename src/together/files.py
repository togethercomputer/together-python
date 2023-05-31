import requests
import urllib.parse
import posixpath


class Files:
    def __init__(self, together_api_key) -> None:
        self.together_api_key = together_api_key
        self.endpoint_url = (
            "http://localhost:8895/v1/files/"  # TODO Assign correct endpoint
        )

    def list_files(self):
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(self.endpoint_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def upload_file(self, file):
        files = {"file": open(file, "rb")}

        data = {"purpose": "fine-tune"}
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url, headers=headers, files=files, data=data
            ).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def delete_file(self, file_id):
        delete_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file(self, file_id):
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file_content(self, file_id, output_file):
        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        # write to file
        open(output_file, "wb").write(response.content)

        return response  # this should be null
