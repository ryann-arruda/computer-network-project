# Computer Network Project

This project was carried out during the Computer Networks course at UFPB, taught by Professor Dr. Ewerton Salvador.

The main objective of this project was to implement two clients (one using a UDP socket and the other using a RAW socket) of a client/server application that forwards requests to the server running via UDP/IP protocols.

Each client must ask the user to choose one of the request types below:

1. Current date and time;
2. A motivational message for the end of the semester;
3. The number of responses sent by the server so far;
4. Exit.

Once the user has made the choice, the client must send a properly formatted request to the server and wait for the response, displaying it appropriately so that the end user can easily read it.

## Request Message Format

|4 bits | 4 bits | 16 bits |
|:--------:|:--------:|:--------:|
|req    |  type  |identifier|

* **req**: indicates that the message is a request. The bits for this field are 0000;
* **type**: indicates the type of request. Bits 0000 for date request, bits 0001 for motivation sentence and bits 0010 request for the number of requests made to the server;
* **identifier**: non-negative number of 2 bytes determined by the customer. This number should be a value of 1 and 65535 drawn by the customer whenever they send a new request to the server.

> **Example of date request with identifier equal to 14161:** 0000 0000 0011 0111 0101 0001

## Response Message Format

|4 bits | 4 bits | 16 bits | 8 bits | 8 bits | 8 bits | ... |
|:--------:|:--------:|:--------:|:---------:|:--------:|:--------:|:--------:|
|res    |  type  |identifier| response length | byte 1 of the response | byte 2 of the response | ... |

* **res**: indicates that the message is a response. The bits for this field are 0001;
* **type**: indicates the type of response. Bits 0000 for date request, bits 0001 for motivation sentence and bits 0010 request for the number of requests made to the server;
* **identifier**: non-negative number of 2 bytes determined by the customer. This number should be a value of 1 and 65535 drawn by the customer whenever they send a new request to the server;

> **OBS.**: identifier 0 is reserved for the server to inform it of receiving an invalid request.
* **response length**: indicates the length of the response itself in number of bytes (1 to 255);

> **OBS.**: response length 0 indicates that the server received an invalid request.
* **response bytes itself**: sequence of bytes containing the response requested by the client. If the server is reporting receipt of an invalid request, no bytes are forwarded in this field.

> **Example of date response with identifier equal to 14161:** 0001 0000 0011 0111 0101 0001 0001 1010 0100 0110 0111 0010 0110 1001 0010 0000 0100 0001 0111 0000 0111 0010 0010 0000 0011 0010 0011 0110 0010 0000 0011 0000 0011 0010 0011 1010 0011 0010 0011 1000 0011 1010 0011 0011 0011 1001 0010 0000 0011 0010 0011 0000 0011 0010 0011 0100 0000 1010

## General Information about the UDP Header

In order to help implement the UDP header in SOCKET_RAW, the information below should be considered.

### UDP Header

The structure of a UDP segment is demonstrated below.

<table>
    <tr>
        <th colspan="2" style="text-align:center;"><strong>UDP Header</strong></th>
    </tr>
    <tr>
        <td style="text-align:center;">Source Port</td>
        <td style="text-align:center;"><strong>0xE713</strong>(port 59155)</td>
    </tr>
    <tr>
        <td style="text-align:center;">Destination Port</td>
        <td style="text-align:center;"><strong>0xC350</strong>(port 50000)</td>
    </tr>
    <tr>
        <td style="text-align:center;">Segment Length</td>
        <td style="text-align:center;"><strong>0x000B</strong>(length 11, i.e. 8 bytes of header + 3 bytes of payload)</td>
    </tr>
    <tr>
        <td style="text-align:center;">Checksum</td>
        <td style="text-align:center;"><strong>0xE0B3</strong>(final checksum value. At the time the checksum is being calculated, the provisional value of this field should be 0x0000)</td>
    </tr>
    <tr>
        <th colspan="2" style="text-align:center;"><strong>Payload</strong></th>
    </tr>
    <tr>
        <td style="text-align:center;">Payload</td>
        <td style="text-align:center;"><strong>0x025CE1</strong>(request for the number of responses sent by the server, with request identifier 23777)</td>
    </tr>
</table>

To calculate the UDP checksum, RFC 768 states that it is necessary to calculate the 16-bit checksum considering the one's complement of the sum of 2-byte portions of an **IP pseudo header**, the **UDP header** and the **payload**. However, if the last number to be added has only 1 byte, another 0 byte must be added to the right (an operation called padding). The purpose of including the pseudo IP header, according to the RFC, is to provide the protocol with protection against erroneously routed datagrams.

Therefore, the pseudo IP header must be structured before calculating the checksum.

### Pseudo IP Header

The Pseudo IP header has the following structure.

<table>
    <tr>
        <th colspan="2" style="text-align:center;"><strong>Pseudo IP Header</strong></th>
    </tr>
    <tr>
        <td style="text-align:center;">Source IP</td>
        <td style="text-align:center;"><strong>0xC0A8 0169</strong> (IP 192.168.1.105)</td>
    </tr>
    <tr>
        <td style="text-align:center;">Destination IP</td>
        <td style="text-align:center;"><strong>0x0FE4 BF6D</strong> (IP 15.228.191.109)</td>
    </tr>
    <tr>
        <td style="text-align:center;">Byte 0 + Transport protocol number</td>
        <td style="text-align:center;"><strong>0x0011</strong> (byte with decimal value 0 followed by byte with decimal value 17, which is the UDP protocol number according to the Internet Assigned Numbers Authority - IANA)</td>
    </tr>
    <tr>
        <td style="text-align:center;">UDP segment length</td>
        <td style="text-align:center;"><strong>0x000B</strong></td>
    </tr>
</table>

### Checksum

Therefore, considering all the information previously presented, the checksum calculation is given by:

<span style="color:red;">0xC0A8 + 0x0169 + 0x0FE4 + 0xBF6D + 0x0011 + 0x000B + </span><span style="color:green;">0xE713 + 0xC350 + 0x000B + 0x0000 + </span><span style="color:blue;">0x025C + 0xE100</span>

* <span style="color:red;">In red: set of 2 bytes of the Pseudo IP Header</span>
* <span style="color:green;">In green: set of 2 bytes of the UDP header</span>
* <span style="color:blue;">In blue: set of 2 bytes of UDP payload (byte 00 was added to the last payload byte so that all sets in the sum have 2 bytes)</span>

The result of the above summation is 41F48. In order to perform the wraparound in one go to make the result of the sum a 2-byte number, one can consider this result as the 32-bit number 0x00041F48 and sum the most significant 16 bis with the 16 bits least significant, i.e. 0x0004 + 0x1F48, which will produce the result **1F4C**. The checksum will be the 1's complement of **1F4C**, which is E0B3, as can be seen in the binary representation below.

<div style="text-align:center;">
    <strong><span style="padding-right: 28px">1</span> <span style="padding-right: 28px">F</span><span style="padding-right: 28px">4</span>C</strong>
    
    0001 1111 0100 1100

    (1's complement below)

    1110 0000 1011 0011
</div>
<div style="text-align:center;">
    <strong><span style="padding-right: 28px">E</span> <span style="padding-right: 28px">0</span><span style="padding-right: 28px">B</span>3</strong>
</div>

## Authors

* Alexandre Bezerra ([Alexandreprog](https://github.com/Alexandreprog))
* Ryann Carlos ([ryann-arruda](https://github.com/ryann-arruda))
* Victor Brasil ([victorbrasilsilsil](https://github.com/victorbrasilsilsil))