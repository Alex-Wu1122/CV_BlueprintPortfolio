# -*- coding: utf-8 -*-
import os
import pickle
import socket
import sys
import threading
import time
import globals
import rsa
from flask import Flask, redirect, render_template, request, url_for

import blockchain_server
import newserver
import sqlite3 as lite
import sqlite3



class Transaction:
    def __init__(self, sender, receiver, amounts, fee, message):
        self.sender = sender
        self.receiver = receiver
        self.amounts = amounts
        self.fee = fee
        self.message = message

def generate_address():
    public, private = rsa.newkeys(512)
    public_key = public.save_pkcs1()
    private_key = private.save_pkcs1()
    return get_address_from_public(public_key), extract_from_private(private_key)

def get_address_from_public(public):
    address = str(public).replace('\\n','')
    address = address.replace("b'-----BEGIN RSA PUBLIC KEY-----", '')
    address = address.replace("-----END RSA PUBLIC KEY-----'", '')
    address = address.replace(' ', '')
    return address

def extract_from_private(private):
    private_key = str(private).replace('\\n','')
    private_key = private_key.replace("b'-----BEGIN RSA PRIVATE KEY-----", '')
    private_key = private_key.replace("-----END RSA PRIVATE KEY-----'", '')
    private_key = private_key.replace(' ', '')
    return private_key

def transaction_to_string(transaction):
    transaction_dict = {
        'sender': str(transaction.sender),
        'receiver': str(transaction.receiver),
        'amounts': transaction.amounts,
        'fee': transaction.fee,
        'message': transaction.message
    }
    return str(transaction_dict)

def initialize_transaction(sender, receiver, amount, fee, message):
    # No need to check balance
    new_transaction = Transaction(sender, receiver, amount, fee, message)
    return new_transaction

def sign_transaction(transaction, private):
    private_key = '-----BEGIN RSA PRIVATE KEY-----\n'
    private_key += private
    private_key += '\n-----END RSA PRIVATE KEY-----\n'
    private_key_pkcs = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    transaction_str = transaction_to_string(transaction)
    signature = rsa.sign(transaction_str.encode('utf-8'), private_key_pkcs, 'SHA-1')
    return signature
app = Flask(__name__)
@app.route('/transaction', methods=['GET', 'POST'])
def tran():
    if request.method == 'POST':
        with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=3) as con:
            cur1 = con.cursor()
            cur1.execute("SELECT password, balance from userdata where username =?",[request.form.get('sender')])  
            send=cur1.fetchone()
        con.commit()
        if send[0]==request.form.get('password') and send[1]>=int(request.form.get('amount')):
            with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=3) as con:
                cur1 = con.cursor()
                cur1.execute("Insert into usertransaction Values(?,?,?,?,?)",
                [request.form.get('sender'),request.form.get('receiver'),int(request.form.get('amount')),0,0])
            con.commit()
            amou=send[1]-int(request.form.get('amount'))
            return render_template('receipt.html',sender=request.form.get('sender'),receiver=request.form.get('receiver'),amount=request.form.get('amount'),balance=amou)
        elif send[0]!=request.form.get('password'):
            result = "密碼錯誤!"
            return render_template('transaction.html',交易結果=result)
        elif send[1]<request.form.get('amount'):
            result = "餘額不足!"
            return render_template('transaction.html',交易結果=result)
            
        
    
    return render_template('transaction.html',交易結果="")
@app.route('/loginspace', methods=['GET', 'POST'])
def loginspace():
    if request.method == 'POST':
        with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=3) as con:
            cur1 = con.cursor()
            cur1.execute("SELECT password, balance from userdata where username=?",[request.form.get('username')])
            user = cur1.fetchone()
            con.commit()
            if user[0]==request.form.get('password'):
                return render_template('welcome.html',username=request.form.get('username'),balance=user[1])
    return render_template('loginspace.html')

@app.route('/home', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=3) as con:
            cur1 = con.cursor()
            cur1.execute("Insert into userdata Values(?,?,?,?,?)",[request.form.get('username'),"n","n",0,0])     
        con.commit()
        return redirect(url_for('usermode',username=request.form.get('username'))) 

    return render_template('home.html')
@app.route('/usermode/<username>', methods=['GET', 'POST'])
def usermode(username):
    #os.system('python blockchain_server.py 1113 127.0.0.1:1111')
    return render_template('usermode.html', username=username)
@app.route('/register')
def register():  
    with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=0.5) as con:
            cur1 = con.cursor()
            cur1.execute("SELECT MAX(cast(number as int)) from userdata")
            port=cur1.fetchone()    
    con.commit()  
    if (port[0]==0):
        os.system('python blockchain_server.py '+"1111")
    else: 
        portb=port[0]+1
        strb=str(portb)      #  利用request取得表單欄位值 
        os.system('python blockchain_server.py '+strb+" 127.0.0.1:1111")
    return render_template('register.html')
@app.route('/packet')
def packet():
    with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=0.5) as con:
            cur1 = con.cursor()
            cur1.execute("SELECT MAX(cast(number as int)) from userdata")
            port=cur1.fetchone()
            cur2 = con.cursor()
            cur2.execute("SELECT username, address, password, balance from userdata where number=?",[port[0]])
            data=cur2.fetchall()   
    con.commit()
    return render_template('register.html',username=data[0][0],address=data[0][1],password=data[0][2],balance=data[0][3])
@app.route('/show/<addd>/<bddd>')
def show():
    return render_template('register.html')
@app.route('/click')
def click():
    blockchain_server.BlockChain.get()
    return redirect(url_for('show'))
    
#@app.route('/application',methods=['GET', 'POST'])
#def application():
#
#    if request.method == 'POST':
#        with sqlite3.connect(r'C:\Users\User\Desktop\blockchain_data.db',timeout=0.5) as con:
#            cur1 = con.cursor()
#            cur1.execute("SELECT address from userdata where username=?",[request.form.get('username')])
#            a=cur1.fetchone()
#            
#
#            
#            print(a[0])  
#        con.commit()
#        
#        
#        return a[0]
#
#    return render_template('application.html')
def handle_receive():
    while True:
        response = client.recv(4096)
        if response:
            print(f"[*] Message from node: {response}")

if __name__ == "__main__":
    app.debug = True
    app.run()  
    target_host = "127.0.0.1"
    target_port = int(1111)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    receive_handler = threading.Thread(target=handle_receive, args=())
    receive_handler.start()
    command_dict = {
        "1": "generate_address",
        "2": "get_balance",
        "3": "transaction"
    }

    while True:
        print("Command list:")
        print("1. generate_address")
        print("2. get_balance")
        print("3. transaction")
        command = input("Command: ")
        if str(command) not in command_dict.keys():
            print("Unknown command.")
            continue
        message = {
            "request": command_dict[str(command)]
        }
        if command_dict[str(command)] == "generate_address":
            address, private_key = generate_address()
            print(f"Address: {address}")
            print(f"Private key: {private_key}")

        elif command_dict[str(command)] == "get_balance":
            address = input("Address: ")
            message['address'] = address
            client.send(pickle.dumps(message))

        elif command_dict[str(command)] == "transaction":
            address = input("Address: ")
            private_key = input("Private_key: ")
            receiver = input("Receiver: ")
            amount = input("Amount: ")
            fee = input("Fee: ")
            comment = input("Comment: ")
            new_transaction = initialize_transaction(
                address, receiver, int(amount), int(fee), comment
            )
            signature = sign_transaction(new_transaction, private_key)
            message["data"] = new_transaction
            message["signature"] = signature

            client.send(pickle.dumps(message))

        else:
            print("Unknown command.")
        time.sleep(1)

    
    
    

 