import threading

import requests
from tqdm import tqdm


class DownloaderThread(threading.Thread):
    def __init__(self, url, start_byte, end_byte, output_file, progress_bar):
        super().__init__()
        self.url = url
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.output_file = output_file
        self.progress_bar = progress_bar

    def run(self):
        headers = {"Range": f"bytes={self.start_byte}-{self.end_byte}"}
        response = session.get(self.url, headers=headers, stream=True)
        with open(self.output_file, "r+b") as file:
            file.seek(self.start_byte)
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
                    self.progress_bar.update(len(chunk))


def get_total_size(url):
    response = session.get(url, stream=True)
    return int(response.headers.get("content-length", 0))


def multi_part_download(url, output):
    total_size_in_bytes = get_total_size(url)
    num_threads = 8  # Number of threads to use
    block_size = total_size_in_bytes // num_threads
    threads = []
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    progress_bar.set_description(f"Downloading {output}")
    with open(output, "wb"):
        for i in range(num_threads):
            start_byte = i * block_size
            end_byte = start_byte + block_size - 1 if i < num_threads - 1 else ""
            thread = DownloaderThread(url, start_byte, end_byte, output, progress_bar)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    progress_bar.close()


# Example usage
model_file_path = "your_model_url"
output = "output_file_name"
session = requests.Session()
multi_part_download(model_file_path, output)
