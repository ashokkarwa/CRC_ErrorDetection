# -*- coding: utf-8 -*-
""" CRC- RCIEVER """

import socket
#import binascii


c=socket.socket()

c.connect(('localhost',9999))

print('connected\n')

#we decided to use CRC-8 (x^8+x^2+x+1)
poly='100000111'

l_poly=len(poly)


def xor(a, b):
   
    devided = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            devided.append('0')
        else:
            devided.append('1')
   
    return ''.join(devided)

def div(divident, divisor):
   
    d_len = len(divisor)
   
    tmp = divident[0 : d_len]
   
    while d_len < len(divident):
   
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[d_len]
   
        else:   
            tmp = xor('0'*d_len, tmp) + divident[d_len]
   
        d_len += 1
   
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*d_len, tmp)
   
    rem = tmp
    return rem

def decodeData(data, poly):
   
    l_key = len(poly)
   
    appended_data = data + '0'*(l_key-1)
    remainder = div(appended_data, poly)
   
    return remainder



def bitostr(msg):
    def BinaryToDecimal(binary):
        
        string = int(binary, 2)
        
        return string
    
    b_data=''

    for i in range(0, len(msg),7):
       

        temp_data = msg[i:i + 7]
        decimal_data = BinaryToDecimal(temp_data)
        b_data = b_data + chr(decimal_data)

    return b_data
    

file=open('CRC-recv.txt','a')
file.write('')


while(True):
    
    msg=c.recv(10240).decode()
    if msg == '0000000':
        print('end')
        file.close()
        break
        c.close

    r_data = decodeData(msg, poly)
          
    
    temp = "0" * (len(poly) - 1)
    if r_data == temp:
        de_msg = bitostr(msg[:-(l_poly-1)])
       # print(de_msg)
        file.write(de_msg)
        c.sendall(bytes("Data Recieved ->"+de_msg+ "Received No error FOUND",'utf-8'))
    else:
        c.sendall(bytes("Error in data",'utf-8'))
     
file.close()
c.close()
