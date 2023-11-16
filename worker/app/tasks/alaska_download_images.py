from os import listdir, makedirs
import getpass
import asf_search as asf
from app import app

from download_images import ImageDownloader

class AlaskaImageDownloader(ImageDownloader):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @app.task(name='download_images', queue='download_images')
    def download_images(self):
        session = asf.ASFSession().auth_with_creds(username=self._username, password=self._password)

        results = asf.geo_search(
            intersectsWith=self._polygon or 'POLYGON((-91.97 28.78,-88.85 28.78,-88.85 30.31,-91.97 30.31,-91.97 28.78))',
            platform=asf.PLATFORM.UAVSAR,
            start=self._start_date or '2010-01-01',
            end=self._end_date or '2010-02-01',
            processingLevel=asf.PRODUCT_TYPE.METADATA,
            maxResults=20,
        )

        makedirs('./satellite_images', exist_ok=True)
        results.download(
            path='./satellite_images',
            session=session,
            processes=10
        )

        listdir('./satellite_images')


if __name__ == '__main__':
    print('Downloader satellite images from web resource search.asf.alaska.edu')
    username = input('Username:')
    password = getpass.getpass('Password:')
    start_date = input('Start date [sample: 2020-12-31 leave it blank for default]:')
    end_date = input('End date [sample: 2021-01-31 leave it blank for default]:')
    polygon = input('Enter polygin [sample: POLYGON((-91.97 28.78,-88.85 28.78,-88.85 30.31,-91.97 30.31,-91.97 28.78)) leave it blank for default]:')
    AlaskaImageDownloader(username, password, start_date, end_date, polygon).download_images()
