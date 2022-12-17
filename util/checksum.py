def checksum(message: str, binary_sum: int = 0):
    for i in range(0, len(message), 2):
        if i + 1 >= len(message):
            binary_sum += ord(message[i]) & 0xFF
        else:
            binary_sum += ((ord(message[i]) << 8) & 0xFF00) + (ord(message[i+1]) & 0xFF)

    while (binary_sum >> 16) > 0:
        binary_sum = (binary_sum & 0xFFFF) + (binary_sum >> 16)

    binary_sum = ~binary_sum

    return binary_sum & 0xFFFF
