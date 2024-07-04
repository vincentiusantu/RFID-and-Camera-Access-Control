from ..util import hex_readable


class ReaderInformation:
    def __init__(self, data: bytes):
        self.data = data
        self.version = data[0:2]
        self.reader_type = data[2]
        self.protocol_type = data[3]
        self.freq_max = data[4]
        self.freq_min = data[5]
        self.power = data[6]
        self.scan_time = data[7]

    def __str__(self) -> str:
        return_value = ''
        value = '>>> START READER INFORMATION ======================'
        return_value = f'{return_value}\n{value}'
        value = f'VERSION        >> {hex_readable(self.version)}'  # Version Number
        return_value = f'{return_value}\n{value}'
        value = f'READER TYPE    >> {hex_readable(self.reader_type)}'  # Reader Type
        return_value = f'{return_value}\n{value}'
        value = f'PROTOCOL TYPE  >> {hex_readable(self.protocol_type)}'  # Protocol Type
        return_value = f'{return_value}\n{value}'
        value = f'FREQUENCY MAX  >> {hex_readable(self.freq_max)}'  # Frequency Max
        return_value = f'{return_value}\n{value}'
        value = f'FREQUENCY MIN  >> {hex_readable(self.freq_min)}'  # Frequency Min
        return_value = f'{return_value}\n{value}'
        value = f'POWER          >> {hex_readable(self.power)}'  # Power
        return_value = f'{return_value}\n{value}'
        value = '>>> END READER INFORMATION ======================'
        return_value = f'{return_value}\n{value}'
        return return_value.strip()


