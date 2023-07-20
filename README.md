# MSE-2023-image-ecology-12

## Полезные ссылки:

- [База знаний проекта](https://miro.com/app/board/uXjVPmWfHN0=/?share_link_id=127919305492)

## Требования

- docker
- docker compose v2

## Сборка

```bash
docker compose up --build
```

## Запуск

Клиентское приложение доступно на порту 3001, зайти на него можно из браузера по адресу
`http://localhost` или 'http://127.0.0.1'

## Скринкаст для презентации первой итерации
[Ссылка](https://drive.google.com/file/d/1v7AndMWR2ltUdBlKSv7MFNOtTrWpj7yX/view?usp=share_link)

## Правила работы с репозиторием
Справка по git-flow: [GITFLOW.md](https://github.com/moevm/MSE-2023-image-ecology-12/blob/main/GITFLOW.md)

## Загрузка карт на сайт
Примеры карт находятся в папке *./examples*.

Загрузить карты можно в разделе **Загрузить**, выберите нужные файлы, в предложенных полях введите желаемое имя для карт.

Для проверки нахождения леса можно использовать следующие файлы:
- _forest_1.tif_
- _forest_2.tif_
- _forest_3.tif_
- _forest_4.tif_

Для проверки нахождения дорог можно использовать следующие файлы:
- _park_1.tif_
- _park_2.tif_

Для проверки нахождения полей можно использовать файл _field.tif_.

### Дополнительные данные для тестов

Дополнительно можно воспользоваться набором данных [Amazon and Atlantic Forest image datasets for semantic segmentation](https://zenodo.org/record/4498086#.ZAeK3XZBy3A). 
Этот набор данных предоставляет изображения для задачи семантической сегментации, которые можно использовать 
для различных тестовых сценариев.