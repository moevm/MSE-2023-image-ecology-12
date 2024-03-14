from rasterio.io import MemoryFile
from rasterio.enums import Compression

def compress(input_bytes: bytes) -> bytes:
    with MemoryFile(input_bytes) as memfile:
        with memfile.open() as src:
            profile = src.profile
            profile.update(compression=Compression.lzw)
            
            with MemoryFile() as mem_dst:
                with mem_dst.open(**profile) as dst:
                    for i in range(1, src.count + 1):
                        data = src.read(i)
                        dst.write(data, i)
                
                # Получаем сжатые данные обратно в байтах
                return mem_dst.read()