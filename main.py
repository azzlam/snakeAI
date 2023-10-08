import pygame
import random

WIDTH, HEIGHT = 630, 630
ROW, COL = 40, 40
FPS = 10

# Snake and Apple Variables
snakeDirection = ""
snakeList = []
applePos = []
appleEaten = False
snakeDead = False
score = 0


# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (70, 70, 70)

pygame.init()
pygame.display.set_caption("Snake AI")
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial_bold", 380)
running = True


def generateSnake(snakeList, snakeDirection):
    if len(snakeList) == 0:
        #head
        x = random.randrange(5, COL-4)
        y = random.randrange(5, ROW-4)
        snakeList.append([x, y])

        #body
        snakeList.append(random.choice([[x, y+1], [x, y-1], [x+1, y], [x-1, y]]))


        if snakeList[0][0] > snakeList[1][0]:
            snakeDirection = "RIGHT"
        elif snakeList[0][0] < snakeList[1][0]:
            snakeDirection = "LEFT"
        elif snakeList[0][1] > snakeList[1][1]:
            snakeDirection = "DOWN"
        elif snakeList[0][1] < snakeList[1][1]:
            snakeDirection = "UP"
        #tail
        if snakeDirection == "RIGHT":
            snakeList.append([snakeList[1][0]-1, snakeList[1][1]])
        elif snakeDirection == "LEFT":
            snakeList.append([snakeList[1][0]+1, snakeList[1][1]])
        elif snakeDirection == "DOWN":
            snakeList.append([snakeList[1][0], snakeList[1][1]-1])
        elif snakeDirection == "UP":
            snakeList.append([snakeList[1][0], snakeList[1][1]+1])
    return snakeList, snakeDirection
        
def generateApples(snakeList, applePos):
    if len(applePos) == 0:
        while True:
            x = random.randrange(1, COL)
            y = random.randrange(1, ROW)
            if [x, y] not in snakeList:
                applePos = [x, y]
                break 
    return applePos

def updateSnake(snakeList, snakeDirection, snakeDead, appleEaten):
    if not snakeDead:
        if not appleEaten:
            snakeList.pop()
        else:
            appleEaten = False
        if snakeDirection == "RIGHT":
            snakeList.insert(0, [snakeList[0][0]+1, snakeList[0][1]])
        elif snakeDirection == "LEFT":
            snakeList.insert(0, [snakeList[0][0]-1, snakeList[0][1]])
        elif snakeDirection == "DOWN":
            snakeList.insert(0, [snakeList[0][0], snakeList[0][1]+1])
        elif snakeDirection == "UP":
            snakeList.insert(0, [snakeList[0][0], snakeList[0][1]-1])
    return snakeList, appleEaten

def collision(snakeList, snakeDead, applePos, snakeDirection, score, appleEaten):
    #check if snake eats apple
    if snakeList[0] == applePos:
        appleEaten = True
        score += 1
        applePos = []
    #check if snake hits wall
    if snakeList[0][0] < 1 or snakeList[0][0] > COL or snakeList[0][1] < 1 or snakeList[0][1] > ROW:
        snakeDead = True

    #check if snake hits itself
    if snakeList[0] in snakeList[1:]:
        snakeDead = True
    return snakeDead, applePos, score, appleEaten
while running:
    snakeList, snakeDirection = generateSnake(snakeList, snakeDirection)
    snakeList, appleEaten = updateSnake(snakeList, snakeDirection, snakeDead, appleEaten)
    snakeDead, applePos, score, appleEaten = collision(snakeList, snakeDead, applePos, snakeDirection, score, appleEaten)
    applePos = generateApples(snakeList, applePos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            if event.key == pygame.K_UP and snakeDirection != "DOWN":
                snakeDirection = "UP"
            if event.key == pygame.K_DOWN and snakeDirection != "UP": 
                snakeDirection = "DOWN"
            if event.key == pygame.K_LEFT and snakeDirection != "RIGHT":
                snakeDirection = "LEFT"
            if event.key == pygame.K_RIGHT and snakeDirection != "LEFT":
                snakeDirection = "RIGHT"



    #draw background
    display.fill(GREY)

    #draw score
    img = font.render(str(score), True, (57, 60, 65))
    display.blit(img, img.get_rect(center = (20*15+15, 20*15+15)).topleft) 

    if snakeDead:
        continue

    #draw apple
    if len(applePos) > 0:
        pygame.draw.rect(display, 'RED', (applePos[0]*15, applePos[1]*15, 13, 13))


    #draw snake
    for part in snakeList[1:]:
        pygame.draw.rect(display, (180,180,180), (part[0]*15, part[1]*15, 13, 13))
    pygame.draw.rect(display, 'WHITE', (snakeList[0][0]*15, snakeList[0][1]*15, 13, 13))
    #draw borders
    pygame.draw.rect(display, WHITE, (10, 10, WIDTH-20, HEIGHT-20), 3) 
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
