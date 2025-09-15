import socket,sys
from utils import validate_checksum, validate_crc, export_detected_frames_csv, pretty_display

def main():
    if len(sys.argv)<2:
        print("Usage: python receiver.py <port>")
        return
    port=int(sys.argv[1])
    detected=[]
    with socket.socket() as srv:
        srv.bind(("0.0.0.0",port)); srv.listen(1)
        print("Receiver listening on",port)
        conn,addr=srv.accept()
        with conn,conn.makefile("r") as r,conn.makefile("w") as w:
            total=int(r.readline())
            for _ in range(total):
                current=[None] # placeholder for errorType
                frameNo=int(r.readline().split(":")[1])
                errorType=int(r.readline().split(":")[1])
                current[0]=errorType
                frames=[]
                for _ in range(5):
                    line=r.readline(); frames.append(line.split(":",1)[1].strip())
                end=r.readline()
                chk=validate_checksum(frames[0])
                c8=validate_crc(frames[1],8)
                c10=validate_crc(frames[2],10)
                c16=validate_crc(frames[3],16)
                c32=validate_crc(frames[4],32)
                detected.append([errorType,chk,c8,c10,c16,c32])
                w.write("ACK\n"); w.flush()
            end=r.readline()
    export_detected_frames_csv(detected)
    pretty_display(detected)

if __name__=="__main__": main()
