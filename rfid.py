from serial import Serial
from pathlib import Path
import pickle

from rfdeon import (
    Command, get_response_serial, Response, InventoryAll,
    bytes_to_hex_readable, CMD_INVENTORY_ALL
)
tag1 = "your_tag1"
tag2 = "your_tag2"

names = ['tag1', 'tag2']
encodings = [f"{tag1}", f"{tag2}"]

encodings_location = Path("output/rfid.isiot")

COM_PORT = 'your_COM'
BAUD_RATE = 57600
with encodings_location.open(mode="rb") as f:
    loaded_encodings = pickle.load(f)

idx = 0
ser = Serial(COM_PORT, baudrate=BAUD_RATE)

def encode(encodings_location: Path = encodings_location):
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)

def main():
    try:
        cmd_inventory = Command(CMD_INVENTORY_ALL)
        ser.write(cmd_inventory.serialize())
        response_bytes = get_response_serial(ser)
        response = Response(response_bytes)
        inventory_all = InventoryAll(response.data)
        for tag in inventory_all.tags:
            for i in range(len(loaded_encodings['encodings'])):
                if bytes_to_hex_readable(tag) == loaded_encodings['encodings'][i]:
                    idx = i
                    break
            print('RFID: ', loaded_encodings['names'][idx])
            # time.sleep(1.5)
    except IndexError:
        print("RFID: Not detected.")
    
