#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import select
from game import roboc

from contextlib import redirect_stdout
import io


HOST = ''
PORT = 12800
END_MSG = "exit"

MSG_SRV_INTRO = '\nBienvenue dans cette partie,\nun joueur doit entrer \'c\' pour commencer'


def startgame():
    """server for multi-clients"""
    print('Server is starting')
    main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Fix [Errno 98] Address already in use at restart
    # but pipes with players are still broken
    main_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    main_connection.bind((HOST, PORT))
    main_connection.listen(5)

    print("Listening on port {}".format(PORT))

    server_up = True
    game_started = False

    # Starting the labyrinth game
    maptoplay = roboc.server_selectmap()
    game = roboc.init_game(maptoplay)

    connected_clients = []
    while server_up:
        # listening for clients on main connection (max. waiting 50ms)
        requestconnectionlist, wlist, xlist = select.select([main_connection], [], [], 0.05)

        for connexion in requestconnectionlist:
            connection_cli, connection_info = connexion.accept()
            # every connected socket is a client (clients list)
            connected_clients.append(connection_cli)

        # Listening for connected clients (select, max. waiting 50ms)
        # exception if no client (try to else if no exception)
        try:
            clients_to_read, wlist, xlist = select.select(connected_clients, [], [], 0.05)
        except select.error:
            pass
        else:
            # read what each client has to say (recv)
            for client in clients_to_read:
                # Client is a socket
                msg_received = client.recv(1024)
                msg_received = msg_received.decode() # Can crash on special chars
                client_id = get_remote_port(client)
                print("Received '{}' from port {}".format(msg_received, client_id))

                # manage game start
                # if started, no new player accepted
                if 'c' == msg_received :
                    game_started = True

                if not game_started:
                    # manage players init in game
                    roboc.manage_players_addition(game, client_id)
                    send_client(client, MSG_SRV_INTRO)
                elif 'new player connected' in msg_received:
                    send_client(client,'Too late, game is already started\nTry again next time')
                    client.close()
                    connected_clients.remove(client)
                    break
                else:
                    # 'exit' quitter la partie en cours
                    if msg_received == END_MSG:
                        print('Joueur {} a stoppé la partie'.format(current_player_sign, roboc.MSG_MOVE))
                        server_up = False
                    else:
                        # manage client movements
                        f = io.StringIO()
                        with redirect_stdout(f):
                            try:
                                game.move_robot(msg_received, client_id)
                            except UserWarning as warning:
                                print(warning)
                                game.status = '{}'.format(warning)
                                server_up = False
                                break

                        # display game and question to players
                        current_player_sign = game.players[client_id].sign
                        question_game = 'Joueur {} : {}'.format(current_player_sign, roboc.MSG_MOVE)
                        game_msg = '{} \n {}'.format(repr(game), question_game)
                        # display_to_all(connected_clients, game_msg)
                        send_client(client, '\n'+game_msg+'\n'+ f.getvalue())

                # Return the socket’s file descriptor
                # print(client.fileno())
    close_connections (main_connection, connected_clients, game.status)


# def display_to_all(clients, msg):
#     for client in clients:
#         send_client(client, '\n'+msg)


def close_connections (main_connection, connected_clients, msg):
    """
    To close all connections
    :param main_connection:
    :param connected_clients:
    """
    print("Fermeture des connexions")

    for client in connected_clients:
        the_end_msg = "{}\n\nAll connections are now closed\nThank you".format(msg)
        client.send(the_end_msg.encode())
        client.close()

    main_connection.close()


def get_remote_port(socket):
    """
    Return the port to which a socket is bound.
    :param socket:
    :return: port:
    """
    addr, port = socket.getpeername()
    return port


def send_client(client, msg):
    """
    Encode msg to send
    :param client:
    :param msg:
    :return:
    """
    client.send(msg.encode())

if __name__ == '__main__':
    startgame()


# static method list
send_client = staticmethod(send_client)