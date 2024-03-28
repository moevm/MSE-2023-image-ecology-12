from os import listdir, makedirs
import getpass
import asf_search as asf


def downloader(username: str, password: str, start_date: str, end_date: str, polygon: str):
    session = asf.ASFSession().auth_with_creds(username=username, password=password)

    results = asf.geo_search(
        intersectsWith=polygon or 'POLYGON((29.9569 59.9958,30.1349 59.9958,30.1349 60.0508,29.9569 60.0508,29.9569 59.9958))',
        platform=asf.PLATFORM.SENTINEL1,
        start=start_date or '2024-01-01',
        end=end_date or '2024-01-31',
        maxResults=2,
    )

    print(results)
    makedirs('./satellite_images', exist_ok=True)

    results.download(
        path='./satellite_images',
        session=session,
    )
    print(listdir('./satellite_images'))


if __name__ == '__main__':
    print('Downloader satellite images from web resource search.asf.alaska.edu')
    username = "etu_alaska_downloader"
    password = "=;E46x?-X~kcr!%"

    # username = input('Username:')
    # password = getpass.getpass('Password:')
    # start_date = input('Start date [sample: 2024-01-01 leave it blank for default]:')
    # end_date = input('End date [sample: 2024-01-31 leave it blank for default]:')
    # polygon = input('Enter polygin [sample: POLYGON((29.9569 59.9958,30.1349 59.9958,30.1349 60.0508,29.9569 60.0508,29.9569 59.9958)) leave it blank for default]:')
    downloader(username, password, None, None, None, )
