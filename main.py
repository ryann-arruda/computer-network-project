import socket
from bitarray import bitarray
from request_generator import create_request

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

                data_received = b''

                data_received += client_socket.recv(1024)
                print(str(data_received))
                print(data_received.decode(errors='replace'))
                
            if option == 2:
                print("opção 2")
            if option == 3:
                print("opção 3")  
        finally:
            print("Erro ao enviar a mensagem! Tente novamente.")
    
    client_socket.close()