import pygame
import pygame_textinput
import pygame.freetype
import time
import sys
import login

pygame.init()

#Create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Button Demo")
pygame.key.set_repeat(400, 50)
GAME_FONT = pygame.freetype.Font("Assets/Fonts/cambria.ttf",20)

signup_img = pygame.image.load('Assets/sign_up.png').convert_alpha()
signup_img_hi = pygame.image.load('Assets/sign_up_hi.png').convert_alpha()

signin_img = pygame.image.load('Assets/sign_in.png').convert_alpha()
signin_img_hi = pygame.image.load('Assets/sign_in_hi.png').convert_alpha()
user_name_img = pygame.image.load('Assets/enter_username.png')
class Button():
    def __init__(self,x,y,image,image_hi,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = pygame.transform.scale(image_hi,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw_login(self):
        action = False
        #ger mouse postion
        pos = pygame.mouse.get_pos()

        #check mouse and clicked condtions
        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0]== 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        #draw button
        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))
        return action

class Enter_Text:
    def __init__(self,x,y,font,font_size,anti,text_manger):
        self.font = pygame.font.SysFont(font,font_size)
        self.anti = anti
        self.cords = x,y
        self.textinput = pygame_textinput.TextInputVisualizer(manager=text_manger,font_object=self.font)
        self.name = ""

    def create(self):
        self.textinput.antialias = self.anti

    def draw(self,events,rect_x,rect_y,rect_w,rect_h):
        self.textinput.update(events)
        inputs_rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        colour = pygame.Color("ghostwhite")
        pygame.draw.rect(screen,colour,inputs_rect)
        screen.blit(self.textinput.surface, (self.cords))

    def enter(self,events):
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            print(f"User pressed enter! Input so far: {self.textinput.value}")
            self.name = str(self.textinput.value)

    def access(self):
        return self.name 
        


class Image():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def display(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))

        

#create buttonm
def gameloop():
    in_button= Button(100, 160, signin_img,signin_img_hi,1)
    up_button = Button(550, 160, signup_img,signup_img_hi,1)
    username = Image(100,210,user_name_img,1)
    
    manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 10)
    text1 = Enter_Text(305,206,"Cambria",20,True,manager)
    text1.create()


    menu =""
    #event handler
    while True:
        events = pygame.event.get()

        screen.fill((198,226,255))
        if menu != "clicked":
            if in_button.draw_login() == True:
                option = "sign in"
                menu = "clicked"
            elif up_button.draw_login() == True:
                option = "sign up"
                print("also clicked")
                menu ="clicked"

        if text1.access() != "":
            user = login.login_or_sign(option,text1.access())
            return user
        if menu == "clicked":
            text1.draw(events,300,201,140,32)
            text_surface, rect = GAME_FONT.render("Enter Username: ", (0, 0, 0))
            screen.blit(text_surface, (145, 212))
            


        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                exit()

            text1.enter(events)

        pygame.display.update()
        clock.tick(60)




#gameloop()
