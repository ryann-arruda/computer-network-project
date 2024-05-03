def format_received_message(data_received, is_text):
    processed_message = b''
    processed_message += data_received
    processed_message = processed_message[4:]
    
    if is_text:
        processed_message = processed_message.decode(errors='replace')
    else:
        processed_message = int.from_bytes(processed_message, 'big')

    return processed_message