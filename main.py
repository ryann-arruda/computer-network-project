import socket
from bitarray import bitarray
from request_generator import create_request
from text_formatter import format_received_message

# Criação do socket UDP para comunicação com o servidor
if __name__ == '__main__':

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('15.228.191.109', 50000)
    client_socket.connect(server_address)

    # Inicialização da opção do usuário
    option = -1

    # Loop que mantém o cliente rodando até que o usuário escolha a opção de sair
    while option != 4:
        print("Escolha o tipo de Requisição que deseja realizar")
        print("1 - Data e hora atual")
        print("2 - Uma mensagem motivacional para o fim do semestre")
        print("3 - A quantidade de respostas emitidas pelo servidor até o momento")
        print("4 - Sair")

        option = int(input("Digite a opção desejada: "))

        try:
            if option == 1:
                client_socket.sendall(create_request(bitarray('0000'))) # Envia uma requisição para obter data e hora atual

                print("Resposta do servidor: ", end='')
                print(format_received_message(client_socket.recv(1024), is_text=True)) # Recebe e formata a resposta do servidor
                
            if option == 2:
                client_socket.sendall(create_request(bitarray('0001'))) # Envia uma requisição para obter uma mensagem motivacional (estamos precisando)

                print("Resposta do servidor: ", end='')
                print(format_received_message(client_socket.recv(1024), is_text=True)) # Recebe e formata a resposta do servidor

            if option == 3:
                client_socket.sendall(create_request(bitarray('0010'))) # Envia uma requisição para obter a quantidade de respostas emitidas pelo servidor

                print("Resposta do servidor: ", end='')
                print(format_received_message(client_socket.recv(1024), False)) # Recebe e formata a resposta do servidor, esperando um valor numérico

        # Trata erros de conexão e encerra o loop
        except ConnectionError:
            print("Conexão com o servidor foi perdida!")
            break

        # Trata erros de timeout
        except socket.timeout:
            print("Tempo máximo espera atingido, tente noamente!")

    # Fecha o socket quando escohlemos sair do loop
    client_socket.close()