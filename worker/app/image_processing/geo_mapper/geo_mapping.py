from dataclasses import dataclass
import rasterio


@dataclass(kw_only=True, frozen=True)
class LatLon:
    lon: float
    lan: float


def geo_mapping(input_geotiff_file: str, pixel_x: int, pixel_y: int) -> LatLon:
    with rasterio.open(input_geotiff_file) as src:
        geo_transform = src.transform
        geo_coordinates = geo_transform * (pixel_x, pixel_y)
        
        print(f"Географические координаты для пикселя ({pixel_x}, {pixel_y}):")
        print(f"Долгота (Longitude): {geo_coordinates[0]}")
        print(f"Широта (Latitude): {geo_coordinates[1]}")
    return LatLon(lon=geo_transform[0], lan=geo_coordinates[1])
