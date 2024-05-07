#Equipe: Alexandre Bezerra de Lima, Ryann Carlos de Arruda Quintino, Victor Henrique Felix Brasil 
import socket
from bitarray import bitarray
from request_generator import create_request
from text_formatter import format_received_message

if __name__ == '__main__':

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
                client_socket.sendto(create_request(bitarray('0000')),('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = client_socket.recvfrom(2048)
                print(format_received_message(message))
                
            if option == 2:
                client_socket.sendto(create_request(bitarray('0001')), ('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = client_socket.recvfrom(2048)
                print(format_received_message(message))

            if option == 3:
                client_socket.sendto(create_request(bitarray('0010')), ('15.228.191.109', 50000))

                print("Resposta do servidor: ", end='')
                message, _ = client_socket.recvfrom(2048)
                print(format_received_message(message, False))

        except ConnectionError:
            print("Conexão com o servidor foi perdida!")
            break
        except socket.timeout:
            print("Tempo máximo espera atingido, tente novamente!")
    
    client_socket.close()