import sys

def parse(filename="/usr/include/linux/input.h"):
    f = open(filename)
    ord_desc_map = {}
    for l in f:
        l = l.strip()
        s = l.split()
        if len(s) < 3:
            continue
        if s[0] != "#define" or not s[1].startswith("KEY_"):
            continue
        key_val = s[2]
        if key_val.startswith("0x"):
            base = 16
        elif key_val.isdigit():
            base = 10
        else:
            print >> sys.stderr, "invalid", s
            continue
        ord_desc_map[int(key_val, base)] = s[1][4:].lower()
    f.close()
    return ord_desc_map

if __name__ == "__main__":
    print parse()
