from ..util.parse_util import hex_readable


# Check "4.1 EPC C1 G2（ISO18000-6C）COMMAND"
CMD_INVENTORY_ALL = 0x01
CMD_READ = 0x02
CMD_WRITE = 0x03
CMD_READER_INFORMATION = 0x21
CMD_SET_READER_POWER = 0x2F


class Command:
    def __init__(self, command: int, reader_address: int = 0xFF, data=None):
        self.command = command
        self.reader_address = reader_address
        self.data = data
        if isinstance(data, int):
            self.data = bytearray([data])
        if data is None:
            self.data = bytearray([])
        self.frame_length = 4 + len(self.data)
        self.base_data = bytearray([self.frame_length, self.reader_address, self.command])
        self.base_data.extend(bytearray(self.data))

    def __str__(self) -> str:
        return_value = ''
        serialize = self.serialize()
        value = '>>> START COMMAND  ================================'
        return_value = f'{return_value}\n{value}'
        value = f'COMMAND        >> {hex_readable(self.command)}'  # Command
        return_value = f'{return_value}\n{value}'
        value = f'READER ADDRESS >> {hex_readable(self.reader_address)}'  # Reader address
        return_value = f'{return_value}\n{value}'
        if self.data:  # Data
            value = f'DATA           >> {hex_readable(self.data)}'
            return_value = f'{return_value}\n{value}'
        value = f'SERIALIZE      >> {hex_readable(serialize)}'  # Serialize
        return_value = f'{return_value}\n{value}'
        value = '>>> END COMMAND    ================================'
        return_value = f'{return_value}\n{value}'
        return return_value.strip()

    def serialize(self) -> bytearray:
        serialize = self.base_data
        ui_crc_value = 0xFFFF
        for x in range((len(serialize))):
            ui_crc_value = ui_crc_value ^ serialize[x]
            for y in range(8):
                if ui_crc_value & 0x0001:
                    ui_crc_value = (ui_crc_value >> 1) ^ 0x8408  # POLYNOMIAL
                else:
                    ui_crc_value = ui_crc_value >> 1
        crc_h = (ui_crc_value >> 8) & 0xFF
        crc_l = ui_crc_value & 0xFF
        serialize = serialize + bytes([crc_l])
        serialize = serialize + bytes([crc_h])
        return serialize


