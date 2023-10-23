import requests
import together
from together.utils import extract_time

import os
from typing import List, Any

import pytest

def test_upload():
    url = "https://huggingface.co/datasets/laion/OIG/resolve/main/unified_joke_explanations.jsonl"
    save_path = "unified_joke_explanations.jsonl"
    download_response = requests.get(url)

    assert download_response.status_code == 200

    with open(save_path, "wb") as file:
        file.write(download_response.content)

    # upload file
    response = together.Files.upload(save_path)

    assert isinstance(response, dict)
    assert response['filename'] == os.path.basename(save_path)
    assert response['object'] == 'file'

    os.remove(save_path)


def test_list():
    response = together.Files.list()
    assert isinstance(response, dict)
    assert isinstance(response['data'], list)


def test_retrieve():
    # extract file id
    files: List[Any]
    files = together.Files.list()['data']
    files.sort(key=extract_time)
    file_id = files[-1]['id']

    response = together.Files.retrieve(file_id)
    assert isinstance(response, dict)
    assert isinstance(response['filename'], str)
    assert isinstance(response['bytes'], int)
    assert isinstance(response['Processed'], bool)
    assert response['Processed'] == True


def test_retrieve_content():
    # extract file id
    files: List[Any]
    files = together.Files.list()['data']
    files.sort(key=extract_time)
    file_id = files[-1]['id']

    file_path = "retrieved_file.jsonl"

    response = together.Files.retrieve_content(file_id, file_path)
    print(response)
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 0
    os.remove(file_path)


def test_delete():
    # extract file id
    files: List[Any]
    files = together.Files.list()['data']
    files.sort(key=extract_time)
    file_id = files[-1]['id']

    # delete file
    response = together.Files.delete(file_id)

    # tests
    assert isinstance(response, dict)
    assert response['id'] == file_id
    assert response['deleted'] == 'true'


if __name__ == "__main__":
    assert together.api_key, "No API key found, please run `export TOGETHER_API_KEY=<API_KEY>`"
    pytest.main([__file__])
