import socket
import struct

# Cria o cabeçalho UDP incluindo portas de origem e destino, além do comprimento do pacote
def create_udp_header(source_port, destination_port, length):
    header = struct.pack('!HHHH', source_port, destination_port, length, 0) # O checksum inicialmente é 0, será calculado abaixo
    return header

# Calculamos o checksum para um pacote UDP, o que é necessário para garantir a integridade dos dados
def udp_checksum(src_addr, dest_addr, udp_length, header, data):
    # Criamos um moidelo de cabeçalho que inclui endereços IP de origem e destino, protocolo e comprimento do UDP
    pseudo_header = struct.pack('!4s4sBBH', 
                                socket.inet_aton(src_addr), 
                                socket.inet_aton(dest_addr), 
                                0, socket.IPPROTO_UDP, udp_length)
    # Combina o modelo de cabeçalho, o cabeçalho UDP e os dados
    full_packet = pseudo_header + header + data
    return calculate_checksum(full_packet)

# Calcula o checksum por meio de uma soma de complemento a um dos bytes do pacote
# Obs: Se o comprimento do pacote não for par, um byte zero é adicionado para deixar certinho
def calculate_checksum(full_packet):    
    if len(full_packet) % 2:
        full_packet += b'\0'
    checksum = 0
    for i in range(0, len(full_packet), 2):
        part = full_packet[i] + (full_packet[i+1] << 8)
        checksum += part
        checksum = (checksum & 0xffff) + (checksum >> 16)
    return ~checksum & 0xffff

# Envia dados utilizando um socket RAW. Primeiro, cria o cabeçalho UDP, calcula o checksum, e então envia o pacote completo para o desitno
def send_data(raw_socket, source_ip, destination_ip, source_port, destination_port, data):
    udp_header = create_udp_header(source_port, destination_port, 8 + len(data))
    print(f"Cabeçalho UDP criado: {udp_header.hex()}")
    udp_length = 8 + len(data)
    checksum = udp_checksum(source_ip, destination_ip, udp_length, udp_header, data)
    # Atualiza o cabeçalho UDP com o checksum calculado
    udp_header = struct.pack('!HHH', source_port, destination_port, udp_length) + struct.pack('H', checksum)
    # Envia o pacote
    raw_socket.sendto(udp_header + data, (destination_ip, 0))


# Busca o endereço IP local da máquina e se conecta a um endereço externo (DNS do próprio Google e retornando o endereço IP usado para essa conexão)
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não ocorre nenhum envio de dados em si auqi, a conexão é feita só para obter o endereço direitinho
        s.connect(("8.8.8.8", 80))  # 8.8.8.8 é o DNS do Google
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

# Encontra uma porta disponível no sistema local, cria um socket temporário, e retorna a porta que o SO atribuiu automaticamente
def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  # O sistema escolhe uma porta disponível
    port = s.getsockname()[1]
    s.close()
    return port

# Inicializa e executa o cliente RAW. Configura o socket, prepara e envia a mensagem.
# TIRAR OS PRINTS DE DEBUGGING ANTES DE CONCLUIR O PROJETO
def run_raw_client():
    print("Script começou")
    try:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        print("Socket RAW criado")
        source_ip = get_local_ip()   # Obtem automaticamente o IP local
        source_port = get_free_port()  # Obtem uma porta disponível
        destination_ip = '15.228.191.109'  # IP do servidor do profesosr
        destination_port = 50000           # Porta do servidor do professor
        message = b"To cansado. MUITO cansado."

        send_data(raw_socket, source_ip, destination_ip, source_port, destination_port, message)
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == '__main__':
    run_raw_client()
