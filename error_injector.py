import random

def flip_bit(s,pos):
    arr=list(s)
    arr[pos]='1' if arr[pos]=='0' else '0'
    return "".join(arr)

def flip_k_bits(s,k):
    pos=random.sample(range(len(s)),k)
    arr=list(s)
    for p in pos: arr[p]='1' if arr[p]=='0' else '0'
    return "".join(arr)

def single_bit_error(frames):
    return [flip_bit(f,random.randrange(len(f))) for f in frames]

def two_bit_error(frames):
    return [flip_k_bits(f,2) for f in frames]

def odd_errors(frames):
    return [flip_k_bits(f,3) for f in frames]

def burst_error(frames):
    out=[]
    for f in frames:
        l=len(f); burst=random.randint(5,20)
        start=random.randint(0,l-burst)
        arr=list(f)
        for i in range(start,start+burst):
            arr[i]='1' if arr[i]=='0' else '0'
        out.append("".join(arr))
    return out

def inject_errors(frame_list):
    out=[]
    for i,schemes in enumerate(frame_list):
        etype=i%5
        if etype==0: out.append([0]+schemes)
        elif etype==1: out.append([1]+single_bit_error(schemes))
        elif etype==2: out.append([2]+two_bit_error(schemes))
        elif etype==3: out.append([3]+odd_errors(schemes))
        elif etype==4: out.append([4]+burst_error(schemes))
    return out
