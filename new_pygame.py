import pygame
import images
import random

#초기화
pygame.init()
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

#플레이어 위치 player location
keys = [False, False]
playpos = [220, 310]
#버튼 사전 button dictionary
button = images.button()
#플레이어 이미지 사전 plyaer dictionary
player = images.player()
pshoot = player['shoot']
#환영 이미지 사전 mirror dictionary
mirror = images.mirror()
mshoot = player['shoot']
#현재 이미지 값 current image color
cur_color = 'red'
#화살 생성 주기
arrow_rate = 10
arrow_count = arrow_rate - 1
#카드와 카드 이펙트 cards and cards' effects
Rcard = images.red_card()
#화살과 화살가 만난 적 수
acc = [0,0] 
#화살
arrows = []
#몬스터 등장 시간
badtimer = 100
badtimer1 = 0
#몬스터 리스트
badguys = [[1280, 30]]
#체력
healthvalue = 200
#레벨 0 몬스터
Lv0 = images.Lv0_monster()
#레벨 1 몬스터
Lv1 = images.Lv1_monster()
#레벨 2 몬스터
Lv2 = images.Lv2_monster()
#레벨 3 몬스터
Lv3 = images.Lv3_monster()
#레벨 4 몬스터
Lv4 = images.Lv4_monster()
#레벨 5 몬스터
Lv5 = images.Lv5_monster()
#FPS
clock = pygame.time.Clock()


running = 1
excitcode = 0

#화면 띄우기
while running:
    clock.tick(60)
    badtimer -= 1
    #색깔 관리
    active_player = player[cur_color]
    active_mirror = mirror[cur_color]
    active_button = button[cur_color]

    #화면을 깨끗하게 한다.
    screen.fill((255,255,255)) #RGB
    
    #모든 요소들을 다시 그린다.#blit은 다시 그리기
    for x in range(5):
            screen.blit(images.tent_road,(0,(x+1)*140-110))
            screen.blit(images.tent,(0,(x+1)*140-110))
            screen.blit(images.pave_road,(300,(x+1)*140-110))
    screen.blit(images.castle, (200,30))
    screen.blit(images.ball_room, (0,730))
    screen.blit(images.card_room, (230,730))
    screen.blit(images.score,(0,0))
    screen.blit(images.Ehealth,(0,0))
    screen.blit(Rcard['burning'][0][0], (245,700))
    screen.blit(active_button,(15,750))
   
    #화살 리스트와 플레이어 이미지 관리
    acc[1] = acc[1] + 1
    arrow_count += 1
    if(arrow_count==arrow_rate) :
        arrows.append([[playpos[0], playpos[1]+32], images.arrow()[cur_color]])
        arrow_count = 0
        screen.blit(pshoot, playpos)
    else :
        screen.blit(active_player, playpos)
    #화살 이미지 관리
    for bullet in arrows:
        bullet[0][0] += 30
        if(bullet[0][0]>1280) :
            arrows.pop(0)
        else:
            screen.blit(bullet[1], bullet[0])

    #나쁜 놈들 그리기
    if badtimer == 0:
        badguys.append([1280, 30 + random.randint(0,4)*140])
        badtimer = 100 - (badtimer1*2)
        if badtimer1>=35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        else:
            badguy[0]-=7
        #나쁜 놈들의 공격
        badrect = pygame.Rect(Lv1['zombie'].get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 300:
            healthvalue -= 50
            badguys.pop(index)
        #화살 충돌
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(bullet[1].get_rect())
            bullrect.left = bullet[0][0]
            bullrect.top = bullet[0][1]
            if badrect.colliderect(bullrect) :
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1

        #다음 웨이브
        index+=1
    for badguy in badguys:
        screen.blit(Lv1['zombie'], badguy)

    #시간
    font = pygame.font.Font(None,24)
    survivedtext = font.render(str(int(90000-pygame.time.get_ticks()))+":"\
        +str(int((90000-pygame.time.get_ticks())/1000%60)).zfill(2),True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[1000,0]
    screen.blit(survivedtext, textRect)

    #체력 감소
    for health in range((200-healthvalue)//2):
        screen.blit(images.health0, (200-(health+1)*2,0))
    
    #화면을 다시 그린다.
    pygame.display.flip() 

    #게임 이벤트
    for event in pygame.event.get(): 
        #게임 종료
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
       
        if event.type == pygame.KEYDOWN:
             #이동 moving
            if event.key == pygame.K_w or  event.key == pygame.K_UP:
                keys[0] = True
            elif event.key == pygame.K_s or  event.key == pygame.K_DOWN:
                keys[1] = True
            #색깔 바꾸기 changing color
            if event.key == pygame.K_1:
                cur_color = 'red'
            elif event.key == pygame.K_2:
                cur_color = 'green'
            elif event.key == pygame.K_3:
                cur_color = 'blue'
            elif event.key == pygame.K_4:
                cur_color = 'yellow'
            elif event.key == pygame.K_5:
                cur_color = 'purple'
            elif event.key == pygame.K_6:
                cur_color = 'jade'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or  event.key == pygame.K_UP:
                keys[0] = False
            elif event.key == pygame.K_s or  event.key == pygame.K_DOWN:
                keys[1] = False

     
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     position = pygame.mouse.get_pos()
        #     acc[1] = acc[1] + 1
        #     arrows.append()
    #플레이어 이동 범위 제한 player movement range limits
    if keys[0] and playpos[1]>30:
        playpos[1] = playpos[1] - 140
    elif keys[1] and playpos[1]<590:
        playpos[1] = playpos[1] + 140
    
    #이겼는가?
    if pygame.time.get_ticks()>= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    
#승리와 패배 처리
screen.blit(images.result()[exitcode], (0,0))
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit(0)
    pygame.display.flip()
    

