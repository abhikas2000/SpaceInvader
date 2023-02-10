from random import randint
import pygame

pygame.init()

#window
screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("Space Invader")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
bgimg=pygame.image.load("img.png")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
enemy_interval=1000
enemy_time_counter=0
bullet_interval=500
bullet_time_counter=0


#Spaceship
player_img=pygame.image.load("spaceship.png")
playerX=600
playerY=600
playerX_change=0
playerY_change=0
def player(x,y):
    #player boundry
    if x<=0:
        x=0
    if x>=1216:
        x=1216

    if y<=550:
        y=550
    if y>=656:
        y=656
    #Drawing Player
    screen.blit(player_img,(x,y))


#Enemy
class enemy:
    enemy_img=pygame.image.load("enemy.png")
    def __init__(self):
        self.enemyX=randint(0,1216)
        self.enemyY= -64 

    #drawing Enemy
    def enemy_draw(self):
        screen.blit(self.enemy_img,(self.enemyX,self.enemyY))
enemy_list=[]


#Bullet
class bullet:
    bullet_img=pygame.image.load("bullet.png")
    def __init__(self):
        self.bulletX=playerX+20
        self.bulletY=playerY+16

    #Drawing Bullet
    def bullet_draw(self):
        screen.blit(self.bullet_img,(self.bulletX,self.bulletY))
bullet_list=[]

#Score
score_value=0
font=pygame.font.Font("freesansbold.ttf",40)
def show_score(x,y):
    score=font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#Game Over
def game_over():
    font_over=pygame.font.Font("freesansbold.ttf",96)
    over_text=font_over.render("GAME OVER",True,(255,100,100))
    screen.blit(over_text,(336,186))
        

blast=pygame.image.load("blast.png")
running=True
game_loop=True
#Main
while running:
    screen.blit(bgimg,(0,0))

    current_time=pygame.time.get_ticks()

    credit=pygame.font.Font("freesansbold.ttf",30)
    credit_text=credit.render(":MADE BY:",True,(255,16,240))
    screen.blit(credit_text,(550,675))

    creditA_text=credit.render("ABHINAV KASHYAP",True,(245,240,31))
    screen.blit(creditA_text,(30,675))

    creditS_text=credit.render("SPANDAN DAS",True,(245,240,31))
    screen.blit(creditS_text,(1030,675))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #key binding for spaceship
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change= -3
            if event.key==pygame.K_RIGHT:
                playerX_change= 3
            if event.key==pygame.K_UP:
                playerY_change= -3
            if event.key==pygame.K_DOWN:
                playerY_change= 3
            if event.key==pygame.K_ESCAPE:
                running=False
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                playerY_change= 0
    if game_loop:
        #Bullet spawn and movement
        if current_time>bullet_time_counter:
            bullet_time_counter+=bullet_interval
            bullet_list.append(bullet())
            bullet_sound=pygame.mixer.Sound("laser.wav")
            bullet_sound.set_volume(0.2)
            bullet_sound.play()
        for i in bullet_list:
            if i.bulletY<=2:
                bullet_list.remove(i)
            else:
                i.bullet_draw()
                i.bulletY-=2.5

        #Enemy spawn and movement
        if current_time>enemy_time_counter:
            enemy_time_counter+=enemy_interval
            enemy_list.append(enemy())
        for i in enemy_list:
            i.enemy_draw()
            i.enemyY+=0.5

        #Bullet and enemy collision
        for i in bullet_list:
            for j in enemy_list:
                if ((i.bulletX>=j.enemyX-24 and i.bulletX<=j.enemyX+64) and (i.bulletY>=j.enemyY and i.bulletY<=j.enemyY+64)):
                    bullet_list.remove(i)
                    enemy_list.remove(j)
                    screen.blit(blast,(i.bulletX,i.bulletY))
                    score_value+=1
                    blast_sound=pygame.mixer.Sound("explosion.wav")
                    blast_sound.set_volume(0.2)
                    blast_sound.play()
        
        #Spaceship spawn and position update
        playerX+=playerX_change
        playerY+=playerY_change
        player(playerX,playerY)

        show_score(10,10)
        for i in enemy_list:
            if i.enemyY>=playerY:
                game_loop=False
                del enemy_list
                del bullet_list

    else:
        game_over()
        show_score(540,300)
        esc_font=pygame.font.Font("freesansbold.ttf",46)
        esc_text=esc_font.render("Press Esc To Exit",True,(255,255,255))
        screen.blit(esc_text,(420,380))        

    pygame.display.update()