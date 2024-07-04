def hex_readable(data) -> str:
    if isinstance(data, bytearray):
        return bytes_to_hex_readable(data)
    if isinstance(data, int):
        return hex_to_hex_readable(data)


def bytes_to_hex_readable(data) -> str:
    response_hex = data.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    return hex_space


def hex_to_hex_readable(data) -> str:
    return hex(data)[2:].upper().zfill(2)


def word_length(data) -> int:
    return int(len(data) / 2)
