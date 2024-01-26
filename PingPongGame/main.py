from pygame import *
from random import randint
import sys
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def control_r(self): #To control the right paddle
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < win_height - 155:
            self.rect.y += self.speed

    def control_l(self): # To control the left paddle
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < win_height - 155:
            self.rect.y += self.speed


back = (200, 255, 255)
win_width = 600
win_height = 500

window = display.set_mode((win_width, win_height))
window.fill(back)


racket_1 = Player("racket.png", 30, 200, 4, 50, 150)
racket_2 = Player("racket.png", 520, 200, 4, 50, 150)
ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)

player_1_point = 0
player_2_point = 0 
font.init() 
font2 = font.Font(None, 60)
point_1 = font2.render(str(player_1_point), 1, (255, 0, 0))
point_2 = font2.render(str(player_2_point), 1, (255, 0, 0))

finish = True
game = True
start = False
clock = time.Clock()
FPS = 60
ball_speed_x = 4
ball_speed_y = 4
game_winner = ""
set_point = 0


winner1 = font2.render("PLAYER 1 WIN THE GAME", 1, (255, 0, 0))
winner2 = font2.render("PLAYER 2 WIN THE GAME", 1, (255, 0, 0))
pause_screen_1 = font2.render("THE GAME IS PAUSED!", 1, (0, 255, 0))
pause_screen_2 = font2.render("PRESS C TO CONTINUE!", 1, (0, 255, 0))
start_screen_1 = font2.render("To play to 5 point, press 1",1, (255, 0, 0))
start_screen_2 = font2.render("To play to 15 point, press 2",1, (255, 0, 0))
start_screen_3 = font2.render("To play to 21 point, press 3",1, (255, 0, 0))
ready_screen = font2.render("Get Ready!", 1 , (0, 255, 0))



random_direction = [-1.01,1.01] # direction list

set_point_list = [5,15,21]

countdown_time = 3000
countdown_time_start = 0
countdown_time_end = 3



while game :
    for e in event.get():
        if e.type == QUIT:
            game = False
    key_pressed = key.get_pressed()

    if key_pressed[K_p]:
        finish = True
        window.blit(pause_screen_1, (70, win_height/2))
        window.blit(pause_screen_2, (50, win_height/2 + 50))
    if key_pressed[K_c]:
        finish = False   


    if start != True:
        window.blit(start_screen_1, (60, 200))
        window.blit(start_screen_2, (55, 250))
        window.blit(start_screen_3, (55, 300))
    
    if key_pressed[K_1] or key_pressed[K_2] or key_pressed[K_3]: 
        window.fill(back)
        finish = False
        start = True
        if key_pressed[K_1]: 
            set_point = set_point_list[0]
        if key_pressed[K_2]:
            set_point = set_point_list[1]
        if key_pressed[K_3]:
            set_point = set_point_list[2]
        window.blit(ready_screen, (win_width/2, win_height/2))

    

        

    if finish != True:
        window.fill(back)
        racket_1.control_l()
        racket_2.control_r()
        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y
        

        if sprite.collide_rect(racket_1, ball) or sprite.collide_rect(racket_2, ball):
            ball_speed_x *= -1.01
            direction_choosing = randint(0,1)
            ball_speed_y *=  random_direction[direction_choosing]     # choosing the direction randomly after bouncing off the racket.
            

        if ball.rect.y < 5 or ball.rect.y > win_height - 55:
            ball_speed_x *= 1.01
            ball_speed_y *= -1.01

        if ball.rect.x < 0:
            player_2_point += 1
            ball_speed_x = 4
            ball_speed_y = 4
            ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)

        if ball.rect.x > win_width:
            player_1_point += 1
            ball_speed_x = 4
            ball_speed_y = 4
            ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)

        point_1 = font2.render(str(player_1_point), 1, (255, 0, 0))
        point_2 = font2.render(str(player_2_point), 1, (255, 0, 0))
        window.blit(point_1, (win_width/2 - 60, 5))
        window.blit(point_2, (win_width/2 + 40, 5))
        racket_1.reset()
        racket_2.reset()
        ball.reset()
        if player_1_point == set_point and player_1_point - player_2_point >= 2:
            game_winner = "player 1"
            
        elif player_2_point == set_point and player_2_point - player_1_point >= 2:
            game_winner = "player 2"
            
        if player_1_point - set_point == -1 and player_2_point - set_point == -1:
            set_point += 1
        
    if game_winner != "":
        if game_winner == "player 1":
            window.blit(winner1, (50, win_height/2))
        if game_winner == "player 2":
            window.blit(winner2, (50, win_height/2))
        finish = True
        if key_pressed[K_y]:
            finish = False
            player_1_point = 0
            player_2_point = 0
            game_winner = ""
            ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)
        if key_pressed[K_n]:
            game = False

        
        

    display.update()
    clock.tick(FPS)
        
