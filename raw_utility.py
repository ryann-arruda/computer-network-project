from bitarray import bitarray
import socket

# Obtém o endereço IP da máquina local
def get_local_ip_address():
    host = socket.gethostname()
    return socket.gethostbyname(host)

def ip_string_tobinary(ip_address):
    local_ip_binary = bitarray() # array de bits para armazenar o IP local
    local_ip_binary.setall(False) # inicializa o array com todos os bits 0

    for n in ip_address:
        octet = int(n) # recupera o primeiro octeto do endereço IP
        bytes_octet = octet.to_bytes(1, 'big', signed=False)
        
        bits_octet = bitarray()
        bits_octet.setall(False)
        bits_octet.frombytes(bytes_octet)

        local_ip_binary += bits_octet

    return local_ip_binary

def generate_pseudo_ip_header(dest_ip, udp_segment_length):
    pseudo_ip_header = bitarray() # array de bits para armazenar o Pseudo Cabeçalho IP
    pseudo_ip_header.setall(False) # inicializa o array com todos os bits 0

    local_ip_address = get_local_ip_address() # obtemos o endereço local
    
    # separação dos endereços IP local e do destino em octetos considerando como separador o caractere '.'
    local_ip_address_splited = local_ip_address.split('.')
    dest_ip_address_splited = dest_ip.split('.') 

    # cada octeto separado originalmente estava em string, logo, foram convertidos para binário
    local_ip_binary = ip_string_tobinary(local_ip_address_splited)
    dest_ip_binary = ip_string_tobinary(dest_ip_address_splited)

    # definição do byte0 presente na especificação do Pseudo Cabeçalho IP
    byte0 = bitarray(8)
    byte0.setall(False)

    # O último byte somado, isto é, '00010001', corresponde ao valor decimal 17, que é o número do 
    # protocolo UDP
    pseudo_ip_header += local_ip_binary + dest_ip_binary + byte0 + bitarray('00010001')

    pseudo_ip_header += udp_segment_length # Pseudo Cabeçalho IP completo

    return pseudo_ip_header

def port_tobinary(port):
    # realiza a conversão da porta para bytes, considerando que o tamanho máximo é de 2 bytes e 
    # que está sendo utilizada a ordenção Big Endian
    bytes_port = port.to_bytes(2, 'big', signed=False)

    binary_port = bitarray()
    binary_port.frombytes(bytes_port)

    return binary_port

# função responsável por realizar a soma de 16 bits com 16 bits
def bits_sum(byte1, byte2):
    sum = bitarray(16) # criação de um vetor de bits com 16 bits para armazenar o resultado
    sum.setall(False) # inicialização do vetor com todos os bits 0

    current_carry = -1 # a variável "current_carry" refere-se ao carry que será propagado, ou seja, o "vai um"
    last_carry = -1 # a variável "last_carry" refere-se ao carry que veio da operação anterior
    sum_result = -1
    sum_index = 15

    # o "reversed" aplicado aos bytes faz com que o loop for os percorram de trás para frente,
    # ou seja, se tiver um byte "10011", ele seria percorrido no setindo: 1, 1, 0, 0, 1
    for bit1, bit2 in zip(reversed(byte1), reversed(byte2)):
        last_carry = current_carry
        current_carry = bit1 & bit2 # operação de and bit a bit
        sum_result = bit1 ^ bit2 # operação de xor bit a bit

        if sum_result == 1:
            if last_carry == 1:
                sum_result = 0
                current_carry = 1
        else:
            if last_carry == 1 and current_carry == 1:
                sum_result = 1
            elif last_carry == 1:
                sum_result = 1

        sum[sum_index] = sum_result
        sum_index -= 1

    # wraparound
    if current_carry == 1:
        return bits_sum(sum, bitarray('0000000000000001'))

    return sum

def get_checksum(pseudo_ip_header, udp_header, payload):
    # concatena os bytes que serão utilizados para calcular o checksum
    bytes_to_checksum = pseudo_ip_header + udp_header + payload

    sum = bitarray(16) # criação do array de bits que irá armazenar os 16 bits da soma
    sum.setall(False) # inicialização do array de bits com 0
    checksum = bitarray(16) # criação do array de bits que irá armazenar os 16 bits do checksum
    checksum.setall(False) # inicialização do array de bits com 0

    # extrai os primeiros 16 bits (2 bytes)
    sum = bytes_to_checksum[0:16]

    # itera pelos bits do bitarray de 16 em 16 bits
    for i in range(16, len(bytes_to_checksum), 16):
        # extrai os próximos 16 bits (2 bytes)
        byte = bytes_to_checksum[i:i+16]
        byte.extend('0'* (16 - len(byte))) # caso só tenha 1 byte, preenche com 0 para totalizar 2 bytes

        sum = bits_sum(sum, byte)

    checksum = ~sum # obtém o checksum (inverte os bits)

    return checksum

# tenta encontrar uma porta livre
def get_free_port():
    selected_port = -1

    # enquanto a porta não for encontrar fica na espera
    while selected_port == -1:
        # o intervalo entre [49152,65536[ consiste nas portas dinâmicas que podem ser
        # utilizadas
        for port in range(49152, 65536):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try: # tenta vincular a porta ao socket
                s.bind(('', port))
                selected_port = port
                s.close()
                break
            except OSError:
                s.close()
                continue
    
    return selected_port

def get_udp_segment_length(payload:bytes):
    length = 8 + len(payload)
    bytes_length = length.to_bytes(2, 'big', signed=False) # realiza a conversão da porta para bytes, considerando que o tamanho máximo é de 2 bytes e 
                                                           # que está sendo utilizada a ordenção Big Endian

    udp_segment_length = bitarray()
    udp_segment_length.setall(False)
    udp_segment_length.frombytes(bytes_length)

    return udp_segment_length

def generate_udp_header(source_port, dest_port, dest_ip, payload):
    source_port_binary = port_tobinary(source_port)
    dest_port_binary = port_tobinary(dest_port)

    udp_segment_length = get_udp_segment_length(payload)

    checksum = bitarray(16) # criação de um vetor de 16 bits para o checksum
    checksum.setall(False) # inicialização do vetor de bits com 0
    
    # udp com checksum zerado
    udp_preheader = source_port_binary + dest_port_binary + udp_segment_length + checksum

    bits_payload = bitarray()
    bits_payload.frombytes(payload)
    
    pseudo_ip_header = generate_pseudo_ip_header(dest_ip, udp_segment_length)

    checksum = get_checksum(pseudo_ip_header, udp_preheader, bits_payload)

    udp_header = source_port_binary + dest_port_binary + udp_segment_length + checksum
    
    return udp_header.tobytes()