
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email


def get_max_keys(data: list[dict]):
    return [head for head in max(data, key=lambda x: x.keys()).keys()]