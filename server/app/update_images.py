import time
import schedule

from download_images import downloader


def updater():
    print('Updateting satellite images')
    is_images_outdated = True # FIXME: заглушка
    if not is_images_outdated:
        return
    username = 'username'
    password = 'password'
    start_date = '2020-12-31'
    end_date = '2021-01-31'
    polygon = 'POLYGON((-91.97 28.78,-88.85 28.78,-88.85 30.31,-91.97 30.31,-91.97 28.78))'
    downloader(username, password, start_date, end_date, polygon)



if __name__ == '__main__':
    schedule.every().day.at("10:00").do(updater)
    while True:
        schedule.run_pending()
        time.sleep(60)
