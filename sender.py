import socket,sys
from frame_builder import create_frames

ERROR_TYPES=["none","single","two","odd","burst"]

def main():
    if len(sys.argv)<6:
        print("Usage: python sender.py <host> <port> <inputfile> <senderMAC> <receiverMAC>")
        return
    host,port,inp,senderMAC,recvMAC=sys.argv[1:6]
    port=int(port)
    frames=create_frames(inp,senderMAC,recvMAC)
    with socket.create_connection((host,port)) as s, s.makefile("r") as r, s.makefile("w") as w:
        w.write(f"{len(frames)}\n"); w.flush()
        for i,frame in enumerate(frames):
            etype=frame[0]
            w.write(f"FRAME:{i}\n")
            w.write(f"ERROR_TYPE:{etype}\n")
            w.write("CHECKSUM:"+frame[1]+"\n")
            w.write("CRC8:"+frame[2]+"\n")
            w.write("CRC10:"+frame[3]+"\n")
            w.write("CRC16:"+frame[4]+"\n")
            w.write("CRC32:"+frame[5]+"\n")
            w.write("END_FRAME\n"); w.flush()
            ack=r.readline().strip()
            print("Frame",i,"sent, error",ERROR_TYPES[etype],"ack:",ack)

if __name__=="__main__": main()
