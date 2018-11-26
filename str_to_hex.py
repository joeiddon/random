def string_to_hex(s):
    out = ''
    for i in range(0, len(s), 4):
        part = s[::-1][i:i+4][::-1]
        dig = hex(int(part, 2))[2]
        out = dig + out
    return out

print(string_to_hex('100011110001'))
