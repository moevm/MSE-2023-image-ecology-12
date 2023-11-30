from abc import ABC, abstractmethod

class ImageDownloader(ABC):
    def __init__(self, username: str, password: str, start_date: str, end_date: str, polygon: str) -> None:
        self._username = username
        self._password = password
        self._start_date = start_date
        self._end_date = end_date
        self._polygon = polygon

    @abstractmethod
    def download(self):
        pass
