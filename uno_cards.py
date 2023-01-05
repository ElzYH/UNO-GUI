from random import shuffle
from random import randint
import time
import sqlite3
import gui

class cards:
    def __init__(self,colour,value):
        self._colour = colour
        self._value = value

    def __repr__(self):
        return f"{self._colour} {self._value}"
    
class deck:
    def __init__(self):
        self.__colour = ["red","green","blue","yellow"]
        self.__special_no_colour = ["plus_4","switch"]
        self.__special = ["block","reverse","plus_2"]
        self.__value = [str(i) for i in (range(0,10))]*2  
        self._card = [
            cards(c,v) for c in self.__colour for v in self.__value
            ]  + [
                cards(c,v) for c in self.__colour for v in self.__special
                ]*2 + [
                    cards("wild",v) for v in self.__special_no_colour
                    ]*4
    
    def get_card(self):
        return self._card
    
    def get_count(self):
        return len(self._card)

    def shuffle_cards(self):
        if self.get_count() == 112:
            shuffle(self._card)
            return self.get_card()

    def _deal(self, num):
        count = self.get_count()
        actual = min([count,num])
        if count == 0:
            print("No more cards")
        cards = self._card[-actual:]
        self._card = self._card[:-actual]
        return cards

    def deal_hand(self,hand_size):
        return self._deal(hand_size)

    def deal_card(self):
        try:
            return self._deal(1)[0]
        except IndexError:
            return "end"



class UNO():
    def __init__(self,uno_deck,player1,player2,player3,player4):
        self._deck = uno_deck
        self._player1 = player1
        self._player2 = player2
        self._player3 = player3
        self._player4 = player4
        self._order = [self._player1,self._player2,self._player3,self._player4]
        self._order_postion = 0
        self._chosen_card = None
        self._topcard = None
        self._cards_weight = {"plus_2":3,"plus_4":5,"block":2,"reverse":2,"switch":4} 
        self._postion_weight = 0
        self._turns = 0
        self._clockwise = True
        self._pickup = False
        self._card_used = {}
        self._colour = ""


    def user_deck(self):
        return [str(i) for i in self._order[0]]

    def players_deck_len(self):
        return [len(self._order[0]),len(self._order[1]),len(self._order[2]),len(self._order[3])]


    def postion_state(self):
        self._postion_weight = 0
        i = 0
        for n in self._order[self._order_postion]:
            i +=1

        if self._clockwise == True:
            if self._order_postion == 3:
                for z in range(len(self._order[0])):
                    z = z + 1
                if i < z:
                    i = 2
                elif i > z:
                    i = -2
                else:
                    i = 0

            else:
                for z in range(len(self._order[self._order_postion + 1])):
                    if i < z:
                        i = 2
                    elif i > z:
                        i = -2
                    else:
                        i = 0

        elif self._clockwise == False:
            if self._order_postion == 0:
                for z in range(len(self._order[3])):
                    if i < z:
                        i = 2
                    elif i > z:
                        i = -2
                    else:
                        i = 0

            else:
                for z in range(len(self._order[self._order_postion - 1])):
                    if i < z:
                        i = 2
                    elif i > z:
                        i = -2
                    else:
                        i = 0
        self._postion_weight = i

            
             


    def card_states(self):
        def ai_choice(postion):
            for z in self._order[self._order_postion]:
                card_check = str(z).split(" ")
                if card_check[0] ==  list_for_cards[postion][0] and card_check[1] == list_for_cards[postion][1]:
                    break
            return str(z)





        top_current_card = str(self._topcard).split(" ")
        list_for_cards = []
        red_count = 0
        green_count = 0
        yellow_count = 0
        blue_count = 0

        for i in self._order[self._order_postion]:
            i = str(i).split()
            g = self._cards_weight.get(i[1])
            list_for_cards.append([i[0],i[1],g])

        list_for_cards = list(filter(lambda x: x[0] == top_current_card[0] or x[1] == top_current_card[1] or x[0] == "wild",list_for_cards)) + [["pick_up",None,0]]
        count = len(list_for_cards)
        for i in range(count):
            if list_for_cards[i][0] == "red":
                red_count += 1
            elif list_for_cards[i][0] == "green":
                green_count += 1
            elif list_for_cards[i][0] == "yellow":
                yellow_count += 1
            elif list_for_cards[i][0] == "blue":
                blue_count += 1
        amount_of_card_weight = {"red":red_count,"green":green_count,"yellow":yellow_count,"blue":blue_count}
        amount_of_card_weight = {k: v for k,v in sorted(amount_of_card_weight.items(), key=lambda item: item[1])}
        for b in range(count):
            if amount_of_card_weight.get(0) == list_for_cards[i][0]:
                list_for_cards[i][2] += 1 

        
        swapped = False
        #print(list_for_cards)
        if count > 1:
            for i in range(count - 1):
                for x in range(0,count-i-1):
                    if list_for_cards[x][2] < list_for_cards[x + 1][2]:
                        swapped = True
                        temp_list = list_for_cards[x + 1]
                        list_for_cards[x + 1] = list_for_cards[x]
                        list_for_cards[x] = temp_list
                
                if not swapped:
                    break
        #print(list_for_cards)

        self.postion_state()
        
        chance = randint(1,100)
        if count >= 4:
            if self._postion_weight == 2:
                if chance > 0 and chance < 10:
                    return ai_choice(0)
                
                elif chance >= 10 and chance < 40:
                    return ai_choice(1)

                else:
                    return ai_choice(2)
            elif self._postion_weight == 0:
                if chance > 0 and chance < 30:
                    return ai_choice(0)
                
                elif chance >= 30 and chance < 70:
                    return ai_choice(1)

                else:
                    return ai_choice(2)
            else:
                if chance > 0 and chance < 50:
                    return ai_choice(0)
                
                elif chance >= 50 and chance < 80:
                    return ai_choice(1)

                else:
                    return ai_choice(2)

        elif count == 3:
            
            if self._postion_weight == 2:
                if chance <= 50:
                    return ai_choice(0)
                else:
                    return ai_choice(1)
            elif self._postion_weight == 0:
                if chance <= 30:
                    return ai_choice(0)
                else:
                    return ai_choice(1)
            else:
                if chance <= 15:
                    return ai_choice(0)
                else:
                    return ai_choice(1)

        

        elif count == 2:
            return ai_choice(0)

        elif count == 1:
            return "pick_up"
            
            
    

        
        
        


    def set_turn(self):
        """Set turns"""
        self._turns = 0

    def set_players_cards(self):
        """Set players hands"""
        self._player1 = self._uno_deck.deal_hand(7)
        self._player2 = self._uno_deck.deal_hand(7)
        self._player3 = self._uno_deck.deal_hand(7)
        self._player4 = self._uno_deck.deal_hand(7)

    def pick_up_card_used(self):
        if self._pickup == True:
            self._pickup = False
            return True
        return False

    def set_order_clockwise(self):
        """Set order postion for the Uno players"""
        self._order_postion = 0


    def set_order_anti_clockwise(self):
        """Set order postion for the Uno players"""
        self._order_postion = 3


    def next_turn(self):
        """Changes who turn it is to play. Check which way the order is going too"""
        if self._clockwise == True:
            if self._order_postion == 3: 
                self.set_order_clockwise()
            else:
                self._order_postion = self._order_postion + 1
        elif self._clockwise == False:
            if self._order_postion == 0:
                self.set_order_anti_clockwise()
            else:
                self._order_postion = self._order_postion - 1

    def card_in_deck(self,pick_up_card):
        """Check if the card trying to be played is in the deck. Returns True if the if it in the deck else it returns False
        and force the user pick up a card without being able to play"""

        for i in self._order[self._order_postion]:
            if str(i) == str(self._player_move):
                return True

        if self._pickup == False:
            self._order[self._order_postion].append(pick_up_card)
        return False
    

    def plus_4_check(self):
        """Returns True if card is == plus_4"""

        current_card = str(self._player_move).split(" ")
        try:
            if current_card[1] == "plus_4":
                return True
            else: 
                return False
        except IndexError:
            None


    def plus_2_check(self):
        """Returns True if card is == plus_2"""

        top_current_card = str(self._topcard).split(" ")
        current_card = str(self._player_move).split(" ")
        try:
            if current_card[0] == top_current_card[0] and current_card[1] == "plus_2":
                return True
            else: 
                return False
        except IndexError:
            None


    def append_cards(self,*args):
        """Appends cards to the next player hand. The amount of cards depends on what function calls it"""
        for i in args:
            if self._clockwise == True:
                self._order[self._order_postion].extend(i)
            else:
                self._order[self._order_postion].extend(i)
        


    
    def colour_check(self,colour):
        """Check if the string (colour), matches the colours. If it does it return TRUE else FAlSE"""

        if colour == "red":
            return True
        elif colour == "green":
            return True
        elif colour == "yellow":
            return True
        elif colour == "blue":
            return True
        else:
            return False


    def update_player_hand(self,current_card):
        """A algorithm that removes a SINGLE card from current player hand after the card was played"""

        count = 0
        card_list = []
        for y in self._order[self._order_postion]:
            if current_card != str(y).split(" "):
                card_list.append(y)
            else:
                if count == 0:
                    count +=1 
                else:
                    card_list.append(y)
        self._order[self._order_postion] = card_list



    def game_setter(self,top_card_setter):
        """Sets the top card, set the turn by calling a function and set the order by calling a function"""

        self._topcard = top_card_setter
        self._cards_weight.update({str(i):1 for i in range(0,10)})
        self.set_turn()
        self.set_order_clockwise()


    def end_check(self,user):
        """This function connects to database, then it does a condtitional check to see if the current player meets the
        condititons. If they do, if it player 1: the user will recive addition to games and wins in. If player 1 loses 
        then player 1 recives additoion to games and loss by 1. ELSE if end check condtion is not TRUE then this code is skipped.
        The databasee is then close after."""

        con = sqlite3.connect("uno_database.db")
        c = con.cursor()
        end = False
        for i in range(4):
            g = 0
            for x in self._order[i]:
                g = g + 1
            if g == 0:
                end = True
                e = i
                break

        if end == True:
            games_played = c.execute(f"""SELECT Games
                        FROM Leaderboard
                        WHERE UserName = '{user}'
                        """)
            games_played = [int(i) for i in c.fetchone()]
            games_played[0] += 1

            if e == 0:
                gui.winloop(user)
                print(f"{user} WINSSS!!!!")
                user_wins = c.execute(f"""SELECT Wins
                FROM Leaderboard
                WHERE UserName = '{user}'
                """)
                user_wins = [int(i) for i in c.fetchone()]
                user_wins[0] += 1
                c.execute(f"""UPDATE Leaderboard
                SET Games = {games_played[0]}, Wins = {user_wins[0]}
                WHERE UserName = '{user}'""") 
            

            else:
                gui.lossloop(e)
                print(f"player{e + 1} wins")
                user_loss = c.execute(f"""SELECT loss
                FROM Leaderboard
                WHERE UserName = '{user}'
                """)
                user_loss = [int(i) for i in c.fetchone()]
                user_loss[0] += 1

                c.execute(f"""UPDATE Leaderboard
                SET Games = {games_played[0]}, Loss = {user_loss[0]}
                WHERE UserName = '{user}'""") 
                
            
            con.commit()
            con.close()
            return True 

        con.close()

    def player_move(self,pick_up_card,user):
        """Displays the top card. Ask the current player what card he wants to play. If the player does not want to play
        the user can pick up card and is given a second chance to play a cards. It then calls function to check the card and
        saves it variable as boolean datatype. Then calls a fucntion to check if player mmets end condtions. After calls a 
        function for the next user turn"""
        self._colour = ""
        print(f"\nPlayer 1: {len(self._order[0])} cards | Player 2: {len(self._order[1])} cards | Player 3: {len(self._order[2])} cards | Player 4: {len(self._order[3])} cards")
        print(f"\nCard On Top: {self._topcard} \n")
        if self._order_postion == 0:
            self._player_move = None
            self._player_move = gui.playloop(user,self.user_deck(),self.players_deck_len(),self._topcard,pick_up_card)
            if self._player_move[0].split()[0] == "wild":
                self._colour = self._player_move[1]
                self._player_move = self._player_move[0]
        
                
                
            if self._player_move[0].replace(" ", "_") == "pick_up" or self._player_move == "":
                self._order[self._order_postion].append(pick_up_card)
                second_chance = self._player_move[1]
                self._pickup = True
                
                if second_chance== "yes":
                    self._player_move = self._order[self._order_postion][-1]
        else:
            self._player_move = self.card_states()
            gui.displayloop(user,self.user_deck(),self.players_deck_len(),self._topcard,self._order_postion+1)
            print(f'Player{self._order_postion + 1} Turn')

        
            if self._player_move.lower().replace(" ", "_") == "pick_up":
                self._order[self._order_postion].append(pick_up_card)
                self._pickup = True
                self._player_move = self._order[self._order_postion][-1]

        is_card_in_deck = self.card_in_deck(pick_up_card)
        if is_card_in_deck == True:
            self.play_card(pick_up_card)
        print(f'Player{self._order_postion + 1} Move: {self._player_move}')
        #time.sleep(1)

        self.next_turn() 
        

    def play_card(self,pick_up_card):
        """This functions replaces the top current card, with the card the user wants to play. It checks for what
        card it is to see if it has any special uses e.g. wild plus_4. Then function calls other functons to excute cards uses"""
        current_card = ""
        top_current_card = ""
        



        current_card = str(self._player_move).split(" ")
        top_current_card = str(self._topcard).split(" ")
        
        if current_card[0] == "wild":
            if self._order_postion == 0:
                colour = self._colour
                if current_card[1] == "switch":
                    while True:
                        if self.colour_check(colour) != True:
                            colour = self._player_move[1]
                        else:
                            break

                elif current_card[1] == "plus_4":
                    if self.plus_4_check() == True:
                        while True:
                            if self.colour_check(colour) != True:
                                colour = self._colour
                            else:
                                break
                self._topcard = cards(colour,"")
                self.update_player_hand(current_card)
            else:
                red_count = 0
                blue_count = 0
                yellow_count = 0
                green_count = 0
                list_for_cards = []
                for i in self._order[self._order_postion]:
                    i = str(i).split()
                    g = self._cards_weight.get(i[1])
                    list_for_cards.append([i[0],i[1],g])

                for i in range(len(self._order[self._order_postion])):
                    if list_for_cards[i][0] == "red":
                        red_count = red_count + 1
                    elif list_for_cards[i][0] == "green":
                        green_count = green_count + 1
                    elif list_for_cards[i][0] == "yellow":
                        yellow_count = yellow_count + 1
                    elif list_for_cards[i][0] == "blue":
                        blue_count = blue_count + 1


                amount_of_card_weight = {"red":red_count,"green":green_count,"yellow":yellow_count,"blue":blue_count}

                amount_of_card_weight = [["red",red_count],["green",green_count],["yellow",yellow_count],["blue",blue_count]]

                swapped = False
                for a in range(len(amount_of_card_weight)-1,0,-1):
                    for o in range(a):
                        if amount_of_card_weight[o][1] < amount_of_card_weight[o + 1][1]:
                            swapped = True
                            temp_list = amount_of_card_weight[o + 1]
                            amount_of_card_weight[o + 1] = amount_of_card_weight[o]
                            amount_of_card_weight[o] = temp_list
                    if not swapped:
                        break
                
                chance = randint(1,20)
                if chance > 9:
                    colour = amount_of_card_weight[0][0]
                else:
                    colour = amount_of_card_weight[1][0]
                
                self._topcard = cards(colour,"")
                self.update_player_hand(current_card)

            
                
        elif current_card[0] == top_current_card[0] and current_card[1] == "reverse":
            if self._clockwise == True:
                self._clockwise = False
            elif self._clockwise == False:
                self._clockwise = True
            self._topcard = cards(current_card[0],current_card[1])
            self.update_player_hand(current_card)
        
        elif current_card[0] == top_current_card[0] and current_card[1]  == "block":
            self.update_player_hand(current_card)
            self._topcard = cards(current_card[0],current_card[1])
            for i in range(1):
                self.next_turn()


        elif current_card[0] == top_current_card[0] and current_card[1] == "plus_2":
            self.plus_2_check()
            self._topcard = cards(current_card[0],current_card[1])
            self.update_player_hand(current_card)

        
        elif current_card[0] == top_current_card[0] or current_card[1] == top_current_card[1]:
            if current_card[1] == "reverse":
                if self._clockwise == True:
                    self._clockwise = False
                elif self._clockwise == False:
                    self._clockwise = True
                self._topcard = cards(current_card[0],current_card[1])
                self.update_player_hand(current_card)
            elif current_card[1]  == "block":
                self.update_player_hand(current_card)
                self._topcard = cards(current_card[0],current_card[1])
                for i in range(1):
                    self.next_turn()
            else:
                self._topcard = cards(current_card[0],current_card[1])
                self.update_player_hand(current_card)
        else:
            if self._order_postion == 0 and self._pickup == False:
                self._pickup = False
                self._order[self._order_postion].append(pick_up_card)

                





        
        
