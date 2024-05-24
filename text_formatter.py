#Equipe: Alexandre Bezerra de Lima, Ryann Carlos de Arruda Quintino, Victor Henrique Felix Brasil 
def format_received_message(data_received, is_text=True):
    processed_message = b''
    processed_message += data_received
    processed_message = processed_message[4:] #pula o formato da rquisição e pega apenas a mensagem
    
    if is_text: #verifica se é string ou texto que precisa ser decodificado
        processed_message = processed_message.decode(errors='replace')
    else:
        processed_message = int.from_bytes(processed_message, 'big') #converte a string para inteiro(usado somente para retornar o número de requisições)

    return processed_message

def format_received_message_from_socket_raw(data_received, is_text=True):
    processed_message = b''
    processed_message += data_received
    processed_message = processed_message[32:] #pega apenas o conteúdo do payload
    
    if is_text: #verifica se é string ou texto que precisa ser decodificado
        processed_message = processed_message.decode(errors='replace')
    else:
        processed_message = int.from_bytes(processed_message, 'big') #converte a string para inteiro(usado somente para retornar o número de requisições)

    return processed_message