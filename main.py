import socket
from bitarray import bitarray
from request_generator import create_request
from text_formatter import format_received_message

if __name__ == '__main__':

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('15.228.191.109', 50000)
    client_socket.connect(server_address)

    option = -1

    while option != 4:
        print("Escolha o tipo de Requisição que deseja realizar")
        print("1 - Data e hora atual")
        print("2 - Uma mensagem motivacional para o fim do semestre")
        print("3 - A quantidade de respostas emitidas pelo servidor até o momento")
        print("4 - Sair")

        option = int(input("Digite a opção desejada: "))

        try:
            if option == 1:
                client_socket.sendall(create_request(bitarray('0000')))

                print("Resposta do servidor: ", end='')
                print(format_received_message(client_socket.recv(1024)))
                
            if option == 2:
                client_socket.sendall(create_request(bitarray('0001')))

                print("Resposta do servidor: ", end='')
                print(format_received_message(client_socket.recv(1024)))

            if option == 3:
                print("opção 3")  
        except ConnectionError:
            print("Conexão com o servidor foi perdida!")
            break
        except socket.timeout:
            print("Tempo máximo espera atingido, tente noamente!")
    
    client_socket.close()