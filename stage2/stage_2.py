import random
import time
import datetime
import os

from pico2d import *


#***************************************
# 스테이지 2
#***************************************
# 기본 인자 초기화
#***************************************
running     = None
character   = None
obstacle    = None
clear_time  = None

#***************************************
# Background
# 게임의 배경을 담당하는 클래스
#***************************************
class Background:
    def __init__(self):
        self.image = load_image('stage_2.png')

    def draw(self):
        self.image.draw(250, 200)

#***************************************
# Obstacle
# 게임내 장애물을 담당하는 클래스
#***************************************
class Obstacle:
    image = None

    def __init__(self):
        self.make()

        if Obstacle.image == None:
            Obstacle.image = load_image('stage_2_bubble.png')

    #***************************************
    # make
    # 장애물 재생성 함수
    # x: 20~480, y: -20, 속도: 7~12
    #***************************************
    def make(self):
        self.x, self.y  = random.randint(20, 480), -20
        self.speed      = random.randint(7, 12)

    def update(self):
        #***************************************
        # y 값은 속도 값에 비례하게 상승
        # 지상으로 장애물이 사라지면 make 호출
        #***************************************
        self.y += self.speed

        if(self.y > 500):
            self.make()

    def draw(self):
        self.image.draw(self.x, self.y)

#***************************************
# Character
# 캐릭터를 담당하는 클래스
#***************************************
class Character:
    def __init__(self):
        self.x, self.y  = 250, 200
        self.speed      = 5
        self.frame      = 0
        self.image      = load_image('stage_2_cha.png')

        # ***************************************
        # 최초 생명력은 3
        # ***************************************
        self.life_cnt = 3
        self.life_image = load_image('heart.png')

    def handle_event(self, event):
        # ***************************************
        # ->,<-,↑ 키 입력시 캐릭터 이동
        # 스테이지 2 에서는 x 값을 5 씩 이동
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.x += self.speed
            elif event.key == SDLK_LEFT:
                self.x -= self.speed
            elif event.key == SDLK_UP:
                self.y += self.speed

    def update(self):
        self.frame = (self.frame + 1) % 8
        # ***************************************
        # 화면을 벗어나지 않게 x, y 값을 조정
        # ***************************************
        if self.x > 500:
            self.x = 500
        elif self.x < 0:
            self.x = 0
        elif self.y > 400:
            self.y = 400
        elif self.y < -20:
            self.y = -30

        #***************************************
        # 캐릭터는 밑으로 계속 하강
        #***************************************
        self.y -= 1

        if (self.life_cnt <= 0):
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 70, 0, 70, 70, self.x, self.y)

        # ***************************************
        # life_cnt 에 맞게 생명력 이미지를 draw
        # ***************************************
        for i in range(0, self.life_cnt):
            image_range = 30 * (i + 1)
            self.life_image.draw(image_range, 375)

def handle_events():
    global running
    global character

    events = get_events()

    # ***************************************
    # 종료키를 누르지 않는다면 캐릭터 이벤트 갱신
    # ***************************************
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            character.handle_event(event)

#***************************************
# lifetime
# 클리어 타임을 출력해주고 0 초에 도달하면
# 스테이지 완료를 해주는 함수
#***************************************
def lifetime():
    global running
    global clear_time
    # ***************************************
    # 클리어 시간과 현재 시간과의 차이를 구함
    # ***************************************
    #########################################
    # 현재는 테스트용으로 시간을 5 초만 줌
    #########################################
    life_time   = clear_time - time.time()
    str_time    = datetime.datetime.fromtimestamp(life_time).strftime('%S')

    font        = load_font('HMKMRHD.TTF', 20)
    font.draw(240, 380, str_time)

    # ***************************************
    # 스테이지 1 의 클리어시간을 버티면 게임 종료
    # ***************************************
    if(int(str_time) <= 0 ):
        clear_font = load_font('HMKMRHD.TTF', 50)
        clear_font.draw(70, 200, 'Stage Clear')
        update_canvas()
        delay(3)
        running = False

#***************************************
# stagefail
# 생명력이 0 이 돼 스테이지를 실패한 상태
#***************************************
def stagefail():
    global running

    clear_font = load_font('HMKMRHD.TTF', 50)
    clear_font.draw(90, 200, 'Stage Fail')
    update_canvas()
    delay(3)
    running = False

def main():
    open_canvas(500, 400)

    global running
    global character
    global obstacle
    global clear_time

    back_ground = Background()
    character   = Character()
    #***************************************
    # 스테이지 2 에서 장애물은 15개
    #***************************************
    obstacle    = [Obstacle() for i in range(15)]
    clear_time  = time.time() + 5
    running     = True

    while running:
        handle_events()
        character.update()

        clear_canvas()

        back_ground.draw()
        character.draw()

        for bubble in obstacle:
            bubble.draw()
            bubble.update()

        lifetime()

        if (character.update() == False):
            stagefail()

        update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()



