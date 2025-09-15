from utils import compute_checksum, get_crc
from error_injector import inject_errors

def mac_to_binary(mac: str) -> str:
    return "".join(f"{int(h,16):08b}" for h in mac.split("-"))

def create_frames(input_file, sender_mac, receiver_mac, LEN="0010111000101110"):
    frames=[]
    with open(input_file,"r",encoding="utf-8") as f:
        while True:
            payload=f.read(46)
            if not payload: break
            payload_bits=""
            for ch in payload:
                payload_bits += f"{ord(ch):08b}"
            if len(payload)<46:
                payload_bits += "0"*(8*(46-len(payload)))
            frame_bits=mac_to_binary(sender_mac)+mac_to_binary(receiver_mac)+LEN+payload_bits
            if len(frame_bits)!=480:
                raise ValueError("Frame not 480 bits")
            frames.append(frame_bits)
    frame_list=[]
    for frame in frames:
        frame_list.append([
            compute_checksum(frame),
            get_crc(frame,8),
            get_crc(frame,10),
            get_crc(frame,16),
            get_crc(frame,32)
        ])
    return inject_errors(frame_list)
