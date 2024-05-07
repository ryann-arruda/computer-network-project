import socket
from bitarray import bitarray
from request_generator import create_request
from text_formatter import format_received_message, format_received_message_from_socket_raw
from raw_utility import generate_udp_header, get_free_port

if __name__ == '__main__':
    dest_ip = '15.228.191.109'
    dest_port = 50000

    raw_client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    option = -1

    while option != 4:
        print("Escolha o tipo de Requisição que deseja realizar")
        print("1 - Data e hora atual")
        print("2 - Uma mensagem motivacional para o fim do semestre")
        print("3 - A quantidade de respostas emitidas pelo servidor até o momento")
        print("4 - Sair")

        option = int(input("Digite a opção desejada: "))
        source_port = get_free_port()

        try:
            if option == 1:
                payload = create_request(bitarray('0000'))
                udp_header = generate_udp_header(source_port, dest_port, dest_ip, payload)
                raw_client_socket.sendto(udp_header + payload,('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = raw_client_socket.recvfrom(2048)
                print(format_received_message_from_socket_raw(message))
                
            if option == 2:
                payload = create_request(bitarray('0001'))
                udp_header = generate_udp_header(source_port, dest_port, dest_ip, payload)
                raw_client_socket.sendto(udp_header + payload,('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = raw_client_socket.recvfrom(2048)
                print(format_received_message_from_socket_raw(message))

            if option == 3:
                payload = create_request(bitarray('0010'))
                udp_header = generate_udp_header(source_port, dest_port, dest_ip, payload)
                raw_client_socket.sendto(udp_header + payload,('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = raw_client_socket.recvfrom(2048)
                print(format_received_message_from_socket_raw(message, False))

        except ConnectionError:
            print("Conexão com o servidor foi perdida!")
            break
        except socket.timeout:
            print("Tempo máximo espera atingido, tente noamente!")
    
    raw_client_socket.close()