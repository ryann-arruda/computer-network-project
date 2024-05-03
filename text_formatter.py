def format_received_message(data_received):
    processed_message = b''
    processed_message += data_received
    processed_message = processed_message[4:]
    processed_message = processed_message.decode(errors='replace')

    return processed_message