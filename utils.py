import csv

# --------- Checksum ---------
def compute_checksum(frame_bits: str) -> str:
    FRAME_BITS = 480
    TARGET_BITS = 512
    sum_val = 0
    for i in range(0, FRAME_BITS, 16):
        word = int(frame_bits[i:i+16], 2)
        sum_val += word
        if sum_val > 0xFFFF:  # wraparound carry
            sum_val = (sum_val & 0xFFFF) + 1
    checksum = (~sum_val) & 0xFFFF
    chk = f"{checksum:016b}"
    out = frame_bits + chk
    return out.ljust(TARGET_BITS, "0")

def validate_checksum(frame_bits: str) -> int:
    orig = frame_bits[:480]
    recv_chk = frame_bits[480:496]
    recomputed = compute_checksum(orig)
    return 0 if recv_chk == recomputed[480:496] else 1

# --------- CRC ---------
def compute_crc(data: bytes, width, poly, init, refin, refout, xorout):
    top_bit = 1 << (width-1)
    mask = (1 << width) - 1
    crc = init & mask
    for b in data:
        curr = b
        if refin:
            curr = int(f"{curr:08b}"[::-1], 2)
        crc ^= curr << (width-8)
        for _ in range(8):
            if crc & top_bit:
                crc = ((crc << 1) ^ poly) & mask
            else:
                crc = (crc << 1) & mask
    if refout:
        crc = int(f"{crc:0{width}b}"[::-1], 2)
    return (crc ^ xorout) & mask

def get_crc(frame_bits: str, width: int) -> str:
    if len(frame_bits) != 480:
        raise ValueError("Frame must be 480 bits")
    data = bytearray(int(frame_bits[i:i+8], 2) for i in range(0, 480, 8))
    if width == 8:
        params = (0x07, 0x00, 0x00, False, False)
    elif width == 10:
        params = (0x233, 0x000, 0x000, False, False)
    elif width == 16:
        params = (0x1021, 0xFFFF, 0x0000, False, False)
    elif width == 32:
        params = (0x04C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
    else:
        raise ValueError("Unsupported CRC width")
    poly, init, xorout, refin, refout = params
    crc_val = compute_crc(data, width, poly, init, refin, refout, xorout)
    crc_bits = f"{crc_val:0{width}b}"
    return (frame_bits + crc_bits).ljust(512, "0")

def validate_crc(frame_bits: str, width: int) -> int:
    orig = frame_bits[:480]
    recv_crc = frame_bits[480:480+width]
    recomputed = get_crc(orig, width)
    return 0 if recv_crc == recomputed[480:480+width] else 1

# --------- CSV + Pretty ---------
def export_detected_frames_csv(detected_frames, path="detected_frames.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame","errorType","checksum","crc8","crc10","crc16","crc32"])
        for i, row in enumerate(detected_frames):
            if len(row) >= 6:
                writer.writerow([i] + row)

def pretty_display(detected_frames):
    error_names = ["None","Single","Two","Odd","Burst"]
    print("="*70)
    print(" ERROR DETECTION RESULTS ")
    print("="*70)
    print(f"{'Frame':<6}{'Error':<10}{'Checksum':<10}{'CRC8':<8}{'CRC10':<8}{'CRC16':<8}{'CRC32':<8}")
    for i,row in enumerate(detected_frames):
        if len(row)>=6:
            etype=row[0]
            ename=error_names[etype] if etype<len(error_names) else "?"
            print(f"{i:<6}{ename:<10}" + "".join([("DETECTED" if v else "OK").ljust(10) for v in row[1:]]))
