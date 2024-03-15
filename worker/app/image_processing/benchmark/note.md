```console
$ pwd
/MSE-2023-image-ecology-12/worker/app

$ python3 image_processing/benchmark/benchmark.py
```


sample output
```
crop_image для ../map_samples/5.tif заняло 1.3859 секунд
crop_image для ../map_samples/6.tif заняло 1.4098 секунд
/home/kirillkry/.local/lib/python3.10/site-packages/rasterio/mask.py:189: NodataShadowWarning: The dataset's nodata attribute is shadowing the alpha band. All masks will be determined by the nodata attribute
  out_image = dataset.read(
crop_image для ../map_samples/2.tif заняло 0.4402 секунд
crop_image для ../map_samples/8.tif заняло 1.5056 секунд
crop_image для ../map_samples/3.tif заняло 0.0687 секунд
crop_image для ../map_samples/7.tif заняло 0.2955 секунд
/home/kirillkry/.local/lib/python3.10/site-packages/rasterio/mask.py:189: NodataShadowWarning: The dataset's nodata attribute is shadowing the alpha band. All masks will be determined by the nodata attribute
  out_image = dataset.read(
crop_image для ../map_samples/1.tif заняло 0.3919 секунд
Среднее время обрезки: 0.7854 секунд
compress для ../map_samples/5.tif заняло 2.8556 секунд
compress для ../map_samples/6.tif заняло 2.9475 секунд
compress для ../map_samples/2.tif заняло 0.8234 секунд
compress для ../map_samples/8.tif заняло 3.1708 секунд
compress для ../map_samples/3.tif заняло 0.1451 секунд
compress для ../map_samples/7.tif заняло 0.6134 секунд
compress для ../map_samples/1.tif заняло 0.8112 секунд
Среднее время сжатия: 1.6238 секунд
```