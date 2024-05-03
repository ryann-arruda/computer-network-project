from bitarray import bitarray
from random import randint

def generate_request_identifier():
    request_identifier = randint(1, 65535)
    bytes_request_identifier = request_identifier.to_bytes(2, 'big', signed=False)

    binary_request_identifier = bitarray()
    binary_request_identifier.frombytes(bytes_request_identifier)

    return binary_request_identifier

def create_request(type):
    request_bits = bitarray('0000')

    request_bits += type
    request_bits += generate_request_identifier()

    return request_bits.tobytes()