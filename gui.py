import pygame
import pygame_textinput
import pygame.freetype
import sys
import login
import sqlite3

pygame.init()

#Create display window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366 

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("UNO")
icon = pygame.image.load('Assets/uno_icon.ico')
pygame.display.set_icon(icon)
pygame.key.set_repeat()
GAME_FONT = pygame.freetype.Font("Assets/Fonts/cambria.ttf",22)
WELCOME_FONT = pygame.freetype.Font("Assets/Fonts/cambria.ttf",48)
PLAYER_FONT = pygame.freetype.Font("Assets/Fonts/YeastyFlavorsRegular-yweyd.ttf",37)
TEXT_FONT = pygame.freetype.Font("Assets/Fonts/YeastyFlavorsRegular-yweyd.ttf",17)
END_FONT = pygame.freetype.Font("Assets/Fonts/YeastyFlavorsRegular-yweyd.ttf",1)


back = pygame.image.load("Assets/Cards/back.png").convert_alpha()
back_hi = pygame.image.load("Assets/Cards/back_hi.png").convert_alpha()
signup_img = pygame.image.load('Assets/sign_up.png').convert_alpha()
signup_img_hi = pygame.image.load('Assets/sign_up_hi.png').convert_alpha()
card_button = pygame.image.load('Assets/more_cards.png').convert_alpha()
card_button_hi = pygame.image.load('Assets/more_cards_hi.png').convert_alpha()

signin_img = pygame.image.load('Assets/sign_in.png').convert_alpha()
signin_img_hi = pygame.image.load('Assets/sign_in_hi.png').convert_alpha()

uno_logo = pygame.image.load('Assets/uno_logo.png').convert_alpha()
play_img = pygame.image.load('Assets/play.png').convert_alpha()
play_hi_img = pygame.image.load('Assets/play_hi.png').convert_alpha()
leaderboard_img = pygame.image.load('Assets/leaderboard.png').convert_alpha()
leaderboard_hi_img = pygame.image.load('Assets/leaderboard_hi.png').convert_alpha()

setting_img = pygame.image.load('Assets/settings.png').convert_alpha()
setting_hi_img = pygame.image.load('Assets/settings_hi.png').convert_alpha()

quit_img = pygame.image.load('Assets/quit.png').convert_alpha()
quit_hi_img = pygame.image.load('Assets/quit_hi.png').convert_alpha()

temp_uno = pygame.image.load('Assets/Cards/green 1.png').convert_alpha()
temp_uno2 = pygame.image.load('Assets/Cards/green 0.png').convert_alpha()

pu_img = pygame.image.load('Assets/pickup.png').convert_alpha()
pu_img_hi = pygame.image.load('Assets/pickup_hi.png').convert_alpha()

separte = pygame.image.load('Assets/separate.png').convert_alpha()
separte_hi = pygame.image.load('Assets/separate_hi.png').convert_alpha()

compare = pygame.image.load('Assets/compare.png').convert_alpha()
compare_hi = pygame.image.load('Assets/compare_hi.png').convert_alpha()

redimg= pygame.image.load('Assets/red_button.png').convert_alpha()
redimghi= pygame.image.load('Assets/red_button_hi.png').convert_alpha()

blueimg= pygame.image.load('Assets/blue_button.png').convert_alpha()
blueimghi= pygame.image.load('Assets/blue_button_hi.png').convert_alpha()

yellowimg= pygame.image.load('Assets/yellow_button.png').convert_alpha()
yellowimghi= pygame.image.load('Assets/yellow_button_hi.png').convert_alpha()

greenimg= pygame.image.load('Assets/green_button.png').convert_alpha()
greenimghi= pygame.image.load('Assets/green_button_hi.png').convert_alpha()


games_img = pygame.image.load('Assets/gamesplayed.png').convert_alpha()
games_hi_img = pygame.image.load('Assets/gamesplayed_hi.png').convert_alpha()

wins_img = pygame.image.load('Assets/wins.png').convert_alpha()
wins_hi_img = pygame.image.load('Assets/wins_hi.png').convert_alpha()

losses_img = pygame.image.load('Assets/losses.png').convert_alpha()
losses_hi_img = pygame.image.load('Assets/losses_hi.png').convert_alpha()

draws_img = pygame.image.load('Assets/draws.png').convert_alpha()
draws_hi_img = pygame.image.load('Assets/draws_hi.png').convert_alpha()

black_back_img = pygame.image.load('Assets/back.png').convert_alpha()
black_back_hi_img = pygame.image.load('Assets/back_hi.png').convert_alpha()

all_numbers_img = pygame.image.load('Assets/numbers.png')
all_numbers_hi_img = pygame.image.load('Assets/numbers_hi.png')

no_wild_img = pygame.image.load('Assets/no_wilds.png')
no_wild_hi_img = pygame.image.load('Assets/no_wilds_hi.png')

all_cards = pygame.image.load('Assets/all_cards.png')
all_cards_hi = pygame.image.load('Assets/all_cards.png')






bg = pygame.image.load("Assets/uno_background.png")
bg2 = pygame.image.load("Assets/end_screen.png")

#user_name_img = pygame.image.load('Assets/enter_username.png')
class Button():
    """Creates Buttons that change image when the user mouse postion is over the button"""
    def __init__(self,x,y,image,image_hi,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = pygame.transform.scale(image_hi,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.pages = 0

    def draw(self):
        """Returns action and changes self.clicked if the user press the mouse ontop of the image"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0]== 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))
        return action

    


class Enter_Text:
    """Text that the user can type into and can be saved"""
    def __init__(self,x,y,font,font_size,anti,text_manger):
        self.font = pygame.font.SysFont(font,font_size)
        self.anti = anti
        self.cords = x,y
        self.textinput = pygame_textinput.TextInputVisualizer(manager=text_manger,font_object=self.font)
        self.name = ""

    def create(self):
        """Changes antialias to True or False"""
        self.textinput.antialias = self.anti

    def draw(self,events,rect_x,rect_y,rect_w,rect_h):
        """Draws a box for the user to type in and to contrast with the background"""
        self.textinput.update(events)
        inputs_rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        colour = pygame.Color("ghostwhite")
        pygame.draw.rect(screen,colour,inputs_rect)
        screen.blit(self.textinput.surface, (self.cords))

    def enter(self,events):
        """If Enter button is clicked it would save the text input"""
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            self.name = str(self.textinput.value)

    def access(self):
        """Returns the user username"""
        return self.name 

    def clear_text(self):
        """Clears the Current text"""
        self.name = ""
        self.textinput.value = ""


class Text:
    def __init__(self,text,colour,x,y):
        """Creates text"""
        self.text = text
        self.colour = colour
        self.x = x
        self.y = y


    def create(self):
        text_surface, rect = WELCOME_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_2(self):
        text_surface, rect = GAME_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_3(self):
        text_surface, rect = PLAYER_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_4(self):
        text_surface, rect = TEXT_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_5(self):
        text_surface, rect = TEXT_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def clear(self):
        text_surface, rect = END_FONT.render("", (self.colour))
        screen.blit(text_surface, (self.x, self.y))

        

class Image():
    """Displays Images"""
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def display(self):
        """Draws Images"""
        screen.blit(self.image, (self.rect.x,self.rect.y))

class UnoCards():
    """A version of the button class above but with couple of changes for Uno Cards in the game """
    def __init__(self,x,y,image,image_hi,scale,postion):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = pygame.transform.scale(image_hi,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.postion = postion #the current card basically

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0]== 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        elif self.rect.collidepoint(pos) == False:
            screen.blit(self.image, (self.rect.x,self.rect.y))

        return action
        
        

    def get_card(self):
        if self.clicked == True:
            self.clicked = False
            return self.postion


    def clear(self):
        blank = pygame.image.load('Assets/blank.png').convert_alpha()
        screen.blit(blank, (self.rect.x,self.rect.y))




def lead_menu(user): 
    """Menu to display the leaderboard"""
    screen.fill((0,0,0))
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    compare_button = Button(300,340,compare,compare_hi,1)
    separte_button = Button(700,340,separte,separte_hi,1)
    compare_option = False
    separte_option = False
    separte_continue = False
    comsep = True
    compaere_menu = False
    while True:
        while comsep == True:
            screen.fill((0,0,0))
            if compare_button.draw() == True:
                compare_option = True
                comsep = False
            elif separte_button.draw() == True:
                separte_option = True
                comsep = False
            elif back_button.draw() == True:
                comsep = False
                return


            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()
            clock.tick(60)

        
        if separte_option == True:
            screen.fill((0,0,0))
            options = Text("Press 1: Normal | Press 2: NoWilds | Press 3: Number",(240,248,255),20,650)
            options.create()

            while separte_option == True:
                if back_button.draw() == True:
                    separte_option = False
                    comsep = True
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            separte_option = False
                            separte_continue = True
                            gamemode = "Normal"

                        elif event.key == pygame.K_2:
                            separte_option = False
                            separte_continue = True
                            gamemode = "Nowilds"

                        elif event.key == pygame.K_3:
                            separte_continue = True
                            separte_option = False
                            gamemode = "Numbers"

                events = pygame.event.get()
                pygame.display.update()
                clock.tick(60)
            


            if separte_continue == True:
                screen.fill((0,0,0))
                des = Text("Press 1: Games | Press 2: Wins | Press 3: Losses | Press 4: Draws",(240,248,255),20,650)
                choice = ""
                contin = False

                con = sqlite3.connect("uno_database.db")
                c = con.cursor()

                def leaderboard_choice(choice,text,user,gamemode):
                    """To access SQL Table and pull it infomation for it to be displayed"""

                    con = sqlite3.connect("uno_database.db")
                    c = con.cursor()

                    c.execute(f"""SELECT UserName,{choice}
                        From {gamemode}
                        ORDER BY {choice} DESC
                        """)
                    board = []
                    player_postions = [i for i in c.fetchall()]
                    for i in range(0,len(player_postions)):
                            if i < 99:
                                username_length = 10 - len(player_postions[i][0])
                                num_length = 2 - len(str(i+1))
                                leader = (f"{' '*num_length}{i+1}. Name: {player_postions[i][0].capitalize() + ' '*username_length} {text}: {player_postions[i][1]}")
                                board.append(leader)
                                if player_postions[i][0] == user:
                                    user_postion = i + 1
                                    user_games = player_postions[i][1]
                    username_length = 10 - len(user)
                    num_length = 2 - len(str(user_postion))
                    curent_user = f"{' '*num_length}{user_postion}. Name: {user.capitalize() + ' '*username_length}  {text}: {user_games}"
                    return [board,curent_user]

                page = 0
                des.create()
                while separte_continue == True:
                    if page == 1:
                        choice = leaderboard_choice("Games","Games Played",user,gamemode)
                        contin = True

                    elif page == 2:
                        choice = leaderboard_choice("Wins","Ganes Won",user,gamemode)
                        contin = True

                    elif page == 3:
                        choice = leaderboard_choice("Loss","Games Loss",user,gamemode)
                        contin = True

                    elif page == 4:
                        choice = leaderboard_choice("Draws","Games Drawn",user,gamemode)
                        contin = True

                    if back_button.draw() == True:
                        con.close()
                        separte_option = True
                        separte_continue = False
                        #break

                    if contin == True:
                        contin = False
                        screen.fill((0,0,0))
                        if back_button.draw() == True:
                            con.close()
                            separte_option = True
                            separte_continue = False
                            #break
                        #Displays the current user leaderboard preview
                        user_text = Text(choice[1],(240,248,255),100,300)
                        user_text.create_2()
                        y = 10
                        for i in range(len(choice[0])):
                            if i < 25:
                                y += 26
                                board = Text(choice[0][i],(240,248,255),620,y)
                                board.create_2()



                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                page = 1

                            elif event.key == pygame.K_2:
                                page =2 

                            elif event.key == pygame.K_3:
                                page =3

                            elif event.key == pygame.K_4:
                                page =4



                    pygame.display.update()
                    clock.tick(60)

        elif compare_option == True:
            screen.fill((0,0,0))
            optionslist = []
            coptions = Text("PRESS TWO KEYS TO COMPARE OPTIONS: PRESS 1: NORMAL | PRESS 2: NO WILDS | PRESS 3: NORMAL",(240,248,255),20,650)
            coptions.create()

            while compare_option == True:



                if back_button.draw() == True:
                    compare_option = False
                    comsep = True

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if len(optionslist) <= 2:
                        if event.type == pygame.KEYDOWN:
                            if len(optionslist) >= 2:
                                compaere_menu = True
                                compare_option = False
                                break
                            print(optionslist)
                            
                            if event.key == pygame.K_1:
                                if "Normal" not in optionslist:
                                    optionslist.append("Normal")

                            elif event.key == pygame.K_2:
                                if "NoWilds" not in optionslist:
                                    optionslist.append("NoWilds")

                            elif event.key == pygame.K_3:
                                if "Numbers" not in optionslist:
                                    optionslist.append("Numbers")
    

                        
                if compaere_menu == True:
                    screen.fill((0,0,0))
                    contin = False
                    des = Text("Press 1: Games | Press 2: Wins | Press 3: Losses | Press 4: Draws",(240,248,255),20,650)
                    def leaderboard_choice(choice,text,user,gamemode1,gamemode2):
                        """To access SQL Table and pull it infomation for it to be displayed"""

                        con = sqlite3.connect("uno_database.db")
                        c = con.cursor()

                        c.execute(f"""SELECT (UserName,{choice})
                            FROM {gamemode1} INNERJOIN {gamemode2}.UserName
                            {gamemode1}.UserName == {gamemode2}.UserName
                            ORDER BY {choice} DESC
                            """)
                        board = []
                        player_postions = [i for i in c.fetchall()]
                        print(player_postions)
                        for i in range(0,len(player_postions)):
                                if i < 99:
                                    username_length = 10 - len(player_postions[i][0])
                                    num_length = 2 - len(str(i+1))
                                    leader = (f"{' '*num_length}{i+1}. Name: {player_postions[i][0].capitalize() + ' '*username_length} {text}: {player_postions[i][1]}")
                                    board.append(leader)
                                    if player_postions[i][0] == user:
                                        user_postion = i + 1
                                        user_games = player_postions[i][1]
                        username_length = 10 - len(user)
                        num_length = 2 - len(str(user_postion))
                        curent_user = f"{' '*num_length}{user_postion}. Name: {user.capitalize() + ' '*username_length}  {text}: {user_games}"
                        return [board,curent_user]

                    page = 0
                    des.create()
                    print("hello")
                    while compaere_menu == True:
                        if page == 1:
                            print("hihihihihihihihiihih")
                            choice = leaderboard_choice("Games","Games Played",user,optionslist[0],optionslist[1])
                            contin = True

                        elif page == 2:
                            choice = leaderboard_choice("Wins","Ganes Won",user,optionslist[0],optionslist[1])
                            contin = True

                        elif page == 3:
                            choice = leaderboard_choice("Loss","Games Loss",user,optionslist[0],optionslist[1])
                            contin = True

                        elif page == 4:
                            choice = leaderboard_choice("Draws","Games Drawn",user,optionslist[0],optionslist[1])
                            contin = True

                        if back_button.draw() == True:
                            con.close()
                            separte_option = True
                            separte_continue = False
                            #break

                        if contin == True:
                            contin = False
                            screen.fill((0,0,0))
                            if back_button.draw() == True:
                                con.close()
                                separte_option = True
                                separte_continue = False
                                #break
                            #Displays the current user leaderboard preview
                            user_text = Text(choice[1],(240,248,255),100,300)
                            user_text.create_2()
                            y = 10
                            for i in range(len(choice[0])):
                                if i < 25:
                                    y += 26
                                    board = Text(choice[0][i],(240,248,255),620,y)
                                    board.create_2()



                        events = pygame.event.get()
                        for event in events:
                            if event.type == pygame.QUIT:
                                sys.exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                    page = 1

                                elif event.key == pygame.K_2:
                                    page =2 

                                elif event.key == pygame.K_3:
                                    page =3

                                elif event.key == pygame.K_4:
                                    page =4

                        pygame.display.update()
                        clock.tick(60)





                pygame.display.update()
                clock.tick(60)







def displayloop(user,user_deck,len_decks_list,topcard,current_player):
    """Display the same infomation to the user during other players turns"""
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,200)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()
    page = 1
    display_player = Text(f"Player{current_player} Turn...",(205,51,51),535,40)
    display_player.create_3()


    def cards_show(start,end):
        x = 190
        y = 600
        for num in range(len_decks_list[0]):
            if num >= start and num <= end:
                x += 110
                cards = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                if cards.draw() == True:
                        current_card = cards.get_card()
                        for a in user_cards[num][1]: #try to remove the loop i think it pointless
                            a = user_cards[num][1]
                            if current_card == a:
                                current_card = a


    for i in range(80):
        screen.blit(bg, (0,0))
        display_player.create_3()
        display_all_cards.create_4()
        topcard.display()
        user_cards = [[pygame.image.load(f'Assets/Cards/{i}.png').convert_alpha(),str(i)] for i in user_deck]
        user_cards_hi = [pygame.image.load(f'Assets/Cards/{x}_hi.png').convert_alpha() for x in user_deck]

        events = pygame.event.get()
        x = 190
        y = 600

        if page == 1:
            cards_show(0,6)

        elif page == 2:
            cards_show(7,13)

        elif page == 3: 
            cards_show(14,20)


        elif page == 4:
            cards_show(21,27)


        elif page == 5:
            cards_show(28,34)
                               
                        

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    page = 1

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3
                
                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5
        pygame.display.update()
        clock.tick(60)



def winloop(user):
    screen.fill((248,248,255))
    screen.blit(bg2, (0,0))

    for x in range(300):
        screen.blit(bg2, (0,0))
        win = Text(f"{str(user).capitalize()} WIIIIINNNNNSSSSS",("#42e54a"),380,x*1.2)
        win.create()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()


        pygame.display.update()
        clock.tick(60)


def lossloop(player):
    screen.fill((248,248,255))

    for x in range(300):
        screen.blit(bg2, (0,0))
        win = Text(f"Player{str(player + 1).capitalize()} WIIIIINNNNNSSSSS",("#ee2525"),380,x*1.2)
        win.create()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(60)




def drawloop():
    screen.fill((248,248,255))
    screen.blit(bg2, (0,0))
    win = Text(f"DRAW",("#ffffff"),578,360)
    win.create()

    for x in range(180):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def choice_loop():
    screen.fill((255,255,255))
    no_wilds = Button(550,340,no_wild_img,no_wild_hi_img,1)
    number = Button(300, 340, all_numbers_img, all_numbers_hi_img, 1)
    normal = Button(800,340, all_cards,all_cards_hi,1)
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)


    while True:
        events = pygame.event.get()

        if no_wilds.draw() == True:
            return "NoWilds"
        elif number.draw() == True:
            return "Numbers"
        elif normal.draw() == True:
            return "Normal"
        elif back_button.draw() == True:
            return "backtomenu"



        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def playloop(user,user_deck,len_decks_list,topcard,pickup):
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))  
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,200)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()
    page = 1
    pick_up_button = UnoCards(800,330,back,back_hi,1,"pick up")
    play_pu = Button(520,375,pu_img,pu_img_hi,1)

    red_button = Button(100,150,redimg,redimghi,1)
    blue_button = Button(100,250,blueimg,blueimghi,1)
    yellow_button = Button(100,350,yellowimg,yellowimghi,1)
    green_button = Button(100,450,greenimg,greenimghi,1)
    current_card = ""
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    nothing = pygame.image.load('Assets/blank.png').convert_alpha()
    cards1 = UnoCards(0,0,nothing,nothing,1,"")
    cards2 = UnoCards(0,0,nothing,nothing,1,"")
    pu_bool = False
    change_colour = False
    player1_text = Text(f"{str(user).capitalize()} Turn...",("#6d6dba"),30,650)

 

    while True:
        screen.blit(bg, (0,0))
        player1_text.create_3()
        display_all_cards.create_4()
        topcard.display()
        user_cards = [[pygame.image.load(f'Assets/Cards/{i}.png').convert_alpha(),str(i)] for i in user_deck]
        user_cards_hi = [pygame.image.load(f'Assets/Cards/{x}_hi.png').convert_alpha() for x in user_deck]
        pick = UnoCards(400,330,pygame.image.load(f'Assets/Cards/{pickup}.png'),pygame.image.load(f'Assets/Cards/{pickup}_hi.png').convert_alpha(),1,pickup)
        events = pygame.event.get()
        x = 190
        y = 600
      
        
        if page == 1 and pu_bool == False and change_colour == False:
            for num in range(len_decks_list[0]):
                if num <= 6:
                    x += 110
                    cards1 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                    if cards1.draw() == True:
                        current_card = cards1.get_card()
                        for a in user_cards[num][1]:
                            a = user_cards[num][1]
                            if current_card == "wild plus_4" or current_card == "wild switch":
                                change_colour = True

                            elif current_card == a:
                                current_card = a
                                return current_card

        elif page == 2 and pu_bool == False and change_colour == False:
            for num in range(7,len_decks_list[0]):
                if num >= 7 and num <= 13:
                    x += 110
                    cards2 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                    if cards2.draw() == True:
                        current_card = cards2.get_card()
                        for a in user_cards[num][1]:
                            a = user_cards[num][1]
                            if current_card == "wild plus_4" or current_card == "wild switch":
                                change_colour = True

                            elif current_card == a:
                                current_card = a
                                return current_card

        elif page == 3 and pu_bool == False and change_colour == False:
            for num in range(len_decks_list[0]):
                if num >= 14 and num <= 20:
                    x += 110
                    cards2 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                    if cards2.draw() == True:
                        current_card = cards2.get_card()
                        for a in user_cards[num][1]:
                            a = user_cards[num][1]
                            if current_card == "wild plus_4" or current_card == "wild switch":
                                change_colour = True

                            elif current_card == a:
                                current_card = a
                                return current_card

        elif page == 4 and change_colour == False and pu_bool == False:
            for num in range(len_decks_list[0]):
                if num >= 21 and num <= 27:
                    x += 110
                    cards2 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                    if cards2.draw() == True:
                        current_card = cards2.get_card()
                        for a in user_cards[num][1]:
                            a = user_cards[num][1]
                            if current_card == a:
                                current_card = a
                                return current_card


        elif page == 5 and change_colour == False and pu_bool == False:
            for num in range(len_decks_list[0]):
                if num >= 28 and num <= 34:
                    x += 110
                    cards2 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                    if cards2.draw() == True:
                        current_card = cards2.get_card()
                        for a in user_cards[num][1]:
                            a = user_cards[num][1]
                            if current_card == a:
                                current_card = a
                                return current_card

        if pick_up_button.draw() == True:
            pu_bool = True

        if back_button.draw() == True:
            return "endgamerightnow"
        
        if pu_bool == True:
                if pick.draw() == True:
                    pu_bool = False
                    return ["pick up","yes"]

                if play_pu.draw() == True:
                    pu_bool = False
                    return ["pick up","no"]

        if change_colour == True:
            if red_button.draw() == True:
                return [str(current_card),"red"]
            elif green_button.draw() == True:
                return [str(current_card),"green"]
            elif yellow_button.draw() == True:
                return [str(current_card),"yellow"]
            elif blue_button.draw() == True:
                return [str(current_card),"blue"]


        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    page = 1

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3

                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5

            



        pygame.display.update()
        clock.tick(60)




def colour_loop(user,user_deck,len_decks_list,topcard,pickup,current_card):
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))  
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,200)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()


    red_button = Button(100,150,redimg,redimghi,1)
    blue_button = Button(100,250,blueimg,blueimghi,1)
    yellow_button = Button(100,350,yellowimg,yellowimghi,1)
    green_button = Button(100,450,greenimg,greenimghi,1)


    player1_text = Text(f"{str(user).capitalize()} Turn...",("#6d6dba"),30,650)

    player1_text.create_3()
    display_all_cards.create_4()
    topcard.display()

    
    while True:
        events = pygame.event.get()
        if red_button.draw() == True:
            return [str(current_card),"red"]
        elif green_button.draw() == True:
            return [str(current_card),"green"]
        elif yellow_button.draw() == True:
            return [str(current_card),"yellow"]
        elif blue_button.draw() == True:
            return [str(current_card),"blue"]


        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    page = 1

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3

                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5

        pygame.display.update()
        clock.tick(60)


def main_menu_loop():
    logo = Image(510,20,uno_logo,1)
    screen.fill((255,255,255))
    play_button = Button(555, 240, play_img,play_hi_img,1)
    leaderboard_button = Button(555, 360, leaderboard_img,leaderboard_hi_img,1)
    quit_button = Button(555,480,quit_img,quit_hi_img,1)
    option = ""
    while True:
        events = pygame.event.get()
        logo.display()
        if play_button.draw() == True:
            return "play"
        if leaderboard_button.draw() == True:
            return "leaderboard"
        if quit_button.draw() == True:
            sys.exit()


        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        clock.tick(60)


def welcomeloop(user):
    for i in range(120):
        welcome_text = Text(f"Hi {str(user).capitalize()}",(0,0,0),500,325)
        welcome_text2 = Text("Welcome To Uno",(0,0,0),500,375)
        screen.fill((198,226,255))
        welcome_text.create()
        welcome_text2.create()
        events = pygame.event.get()
        for event in events:
                #quit game
                if event.type == pygame.QUIT:
                    sys.exit()
        pygame.display.update()
        clock.tick(60)
    

#create buttonm
def startloop():
    in_button= Button(200, 260, signin_img,signin_img_hi,1)
    up_button = Button(750, 260, signup_img,signup_img_hi,1)
    back_button = Button(50,50,black_back_img,black_back_hi_img,1)
    #username = Image(100,210,user_name_img,1)
    error = ""
    text2 = Text(error,(0,0,0),240,350)

    manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 6)
    text1 = Enter_Text(505,306,"Cambria",22,True,manager)
    text1.create()


    menu =""
    #event handler
    while True:
        events = pygame.event.get()

        screen.fill((198,226,255))
        text2 = Text(error,(255,48,48),200,550)
        if menu != "clicked":
            if in_button.draw() == True:
                option = "sign in"
                menu = "clicked"
            elif up_button.draw() == True:
                option = "sign up"
                menu ="clicked"
                text2.clear()
            else:
                text2.create_2()

        if text1.access() != "":
            list_1 = login.login_or_sign(option,text1.access())
            user = list_1[0]
            error = list_1[1]
            text1.clear_text()
            if user != "":
                return user
            else:
                user = ""
                menu = ""

                
        if menu == "clicked":
            if back_button.draw() == True:
                menu = ""
            text1.draw(events,500,301,140,32)
            text_surface, rect = GAME_FONT.render("Enter Username: ", (0, 0, 0))
            screen.blit(text_surface, (337, 308))
            

        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                sys.exit()

            text1.enter(events)

        pygame.display.update()
        clock.tick(60)





