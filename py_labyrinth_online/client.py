#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import os
import time

HOST = "localhost"
PORT = 12800
END_MSG = b"exit"


def startplayer():
    """Connect client"""
    print ('start cli')

    try:
        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.connect((HOST, PORT))
    except ConnectionError as e:
        print('Connection error : {}\nPlease contact technical support'.format(e))
        sys.exit(0)

    print(server_connection.getsockname())
    print("Connected on port {}".format(PORT))

    # Unique intro to server
    msg_intro_serveur = "port {} : new player connected".format(get_local_port(server_connection))
    server_connection.send(msg_intro_serveur.encode())

    msg_input = b""
    while msg_input != END_MSG:
        # Clean view
        os.system("cls" if os.name == "nt" else "clear")

        msg_recu = server_connection.recv(1024)
        print(msg_recu.decode())  # Can crash on special chars

        # game already started or finished, client quit
        if 'Too late' in msg_recu.decode() or 'connections are now closed' in msg_recu.decode():
            time.sleep(1)
            sys.exit(0)

        msg_input = input("> ")  # Can crash on special chars
        msg_input = str(msg_input)
        msg_input = msg_input.encode()
        server_connection.send(msg_input)

    print("Fermeture de la connexion")
    server_connection.close()


def get_local_port(socket):
    """Return the port to which a socket is bound."""
    addr, port = socket.getsockname()
    return port


if __name__ == '__main__':
    startplayer()