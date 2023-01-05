import login
import pygame
from pygame.locals import *
import os
import uno_cards
import sqlite3
import sys
from random import shuffle
import gui


def menu(u):
    """A Function that gives the user options on what they want to do next"""
    while True:
        option = gui.main_menu_loop()
        if option == "play":
            main_game_uno(u)
        if option == "leaderboard":
            leaderboard(user)
        if option == "quit":
                quit()
        

def settings():
    """Allows The User To Open And Read The Read Me File"""
    while True:
        option = input("\nMenu Option: | Rules | Menu |\n\nEnter A Option: ").lower()
        if option == "rules":
            f = open("Rules\ReadMe.txt")
            print(f"..........\n{f.read()}\n..........")
            f.seek(0)
        elif option == "menu": break

def leaderboard(user):
    gui.lead_menu(user)
    


def main_game_uno(user):
    print(f"\nWelcome {user}")
    uno_deck = uno_cards.deck()
    uno_deck.shuffle_cards()
    game = uno_cards.UNO(uno_deck,uno_deck.deal_hand(7),uno_deck.deal_hand(7),uno_deck.deal_hand(7),uno_deck.deal_hand(7))

    first_card = uno_deck.deal_card()
    first_card_check = str(first_card).split(" ")
    while first_card_check[0] == "wild":
        first_card = uno_deck.deal_card()
        first_card_check = str(first_card).split(" ")

    game.game_setter(first_card)
    pick_up = uno_deck.deal_card()
    while game.end_check(user) != True:
        try:
            if True:
                if game.pick_up_card_used() == True:
                    pick_up = uno_deck.deal_card()
                    if pick_up == "end":
                        raise IndexError
                    game.player_move(pick_up,user)
                else:
                    game.player_move(pick_up,user)
            
            if game.plus_4_check() == True:
                add_card = []
                for i in range(4):
                    add_card.append(uno_deck.deal_card())
                game.append_cards(add_card)

            if game.plus_2_check() == True:
                add_card = []
                for i in range(2):
                    add_card.append(uno_deck.deal_card())
                game.append_cards(add_card)
        except TypeError and IndexError:
            
            print("DRAW!!!!!")
            gui.drawloop()
            con = sqlite3.connect("uno_database.db")
            c = con.cursor()

            games_played = c.execute(f"""SELECT Games
                        FROM Leaderboard
                        WHERE UserName = '{user}'
                        """)
            games_played = [int(i) for i in c.fetchone()]
            games_played[0] += 1

            user_draws = c.execute(f"""SELECT Draws
                        FROM Leaderboard
                        WHERE UserName = '{user}'
                        """)
            user_draws = [int(i) for i in c.fetchone()]

            user_draws[0] += 1

            print(f"{games_played},{user_draws}")

            c.execute(f"""UPDATE Leaderboard
            SET Games = {games_played[0]}, Draws = {user_draws[0]}
            WHERE UserName = '{user}'""")   
            con.commit()
            con.close()
            break





if __name__ == "__main__":
    if os.path.exists("uno_database.db"): print("database already created")
    else: login.create()
    
    user = gui.startloop()
    gui.welcomeloop(user)
    menu(user)
        




    