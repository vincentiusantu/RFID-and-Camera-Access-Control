from socket import socket
from serial import Serial


def get_response_serial(serial: Serial) -> bytearray:
    length_bytes = serial.read(1)
    if length_bytes:
        frame_length = ord(chr(length_bytes[0]))
        data = length_bytes + serial.read(frame_length)
        return bytearray(data)


def get_response_tcp(soc: socket) -> bytearray:
    length_bytes = soc.recv(1)
    if length_bytes:
        frame_length = ord(chr(length_bytes[0]))
        data = length_bytes + soc.recv(frame_length)
        return bytearray(data)

