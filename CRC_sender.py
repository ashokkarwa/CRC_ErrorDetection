# -*- coding: utf-8 -*-
""" CRC SENDER """

import socket
import random

s=socket.socket()

s.bind(('localhost',9999))

print('waiting for connection')

s.listen()

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

def encodeData(data, poly):
   
    l_key = len(poly)
   
    appended_data = data + '0'*(l_key-1)
    remainder = div(appended_data, poly)
   
    crc_data = data + remainder
    return crc_data

def add_error(msg):
    ran=random.randint(0,1000)
    ind=ran%(len(msg))

    error=[]
    
    for i in range (0,len(msg)):
        error.append(msg[i])
        
    if(ind%2==0):
        
        if error[ind]=='1':
            error[ind]='0'
        else:
            error[ind]='1'
    return ''.join(error)
   

file=open('CRC-send.txt','r')

message=[]

line='a'
while(line):
    line=file.read(5)
    message.append(line)

while(True):
    c,addr=s.accept()
    print('Got connection from ',addr)
    
    #we decided to use CRC-8 (x^8+x^2+x+1)
    poly='100000111'
    
    
    for i in message:
        
        s_data=i
    
        data =(''.join(format(ord(i), '07b') for i in s_data))
        
        crc_code=encodeData(data,poly)
        dummy=crc_code
        
        print('CRC code is '+crc_code)
        
       
        #crc_code=add_error(dummy) #remove this statement for error free transfer
        
        c.sendall(bytes(crc_code,'utf-8'))
    
        print(c.recv(10240).decode())
    
    file.close()   
