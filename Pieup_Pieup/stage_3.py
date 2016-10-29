import math
import random
import time
import datetime
import os

from pico2d import *


#***************************************
# 스테이지 3
#***************************************
# 기본 인자 초기화
#***************************************
running     = None
character   = None
obstacle    = None
clear_time  = None
game_stop   = None

#***************************************
# Background
# 게임의 배경을 담당하는 클래스
#***************************************
class Background:
    def __init__(self):
        self.image = load_image('stage_3.png')

    def draw(self):
        self.image.draw(250, 200)

#***************************************
# Obstacle
# 게임내 장애물을 담당하는 클래스
#***************************************
class Obstacle:
    #***************************************
    # 장애물 시작 방향 값
    #***************************************
    LEFT_START, RIGHT_START, UP_START, DOWN_START = 0, 1, 2, 3

    image = None

    def __init__(self):
        self.make()

        if Obstacle.image == None:
            Obstacle.image = load_image('stage_3_meteor.png')

    #***************************************
    # make
    # 장애물 재생성 함수
    # x, y 값은 정해진 위치에 따라 생성, 속도 7~12
    #***************************************
    def make(self):
        self.select_pos = random.randint(0, 3)

        if(self.select_pos == self.LEFT_START):
            self.x, self.y  = -20, random.randint(-20, 420)
        elif(self.select_pos == self.RIGHT_START):
            self.x, self.y = 520, random.randint(-20, 420)
        elif(self.select_pos == self.UP_START):
            self.x, self.y = random.randint(-20, 520), -20
        elif(self.select_pos == self.DOWN_START):
            self.x, self.y = random.randint(-20, 520), 420

        self.speed      = random.randint(7, 12)
        #***************************************
        # 장애물의 방향 값 설정
        # x: ↑[0],↓[1] // y: →[0],←[1]
        #***************************************
        self.dir        = random.randint(0, 1)

    #***************************************
    # setpos
    # 속도 값에 따라 장애물 이동
    #***************************************
    def setpos(self, x_speed, y_speed):
        self.x += x_speed
        self.y += y_speed

    # ***************************************
    # calspeed
    # 장애물 방향값에 따라 속도 값 리턴
    # ↑[0],→[0] return +
    # ↓[1],←[1] return -
    # ***************************************
    def calspeed(self, speed):
        if(self.dir == 0):
            return speed
        elif(self.dir == 1):
            return -speed

    def update(self):
        #***************************************
        # 시작 위치에 따라 장애물을 이동
        #***************************************
        if (self.select_pos == self.LEFT_START):
            self.setpos(self.speed, self.calspeed(self.speed))
        elif (self.select_pos == self.RIGHT_START):
            self.setpos(-self.speed, self.calspeed(self.speed))
        elif (self.select_pos == self.UP_START):
            self.setpos(self.calspeed(self.speed), self.speed)
        elif (self.select_pos == self.DOWN_START):
            self.setpos(self.calspeed(self.speed), -self.speed)

        if(self.x < - 30 or self.x > 530 or self.y < - 30 or self.y > 430):
            self.make()

    def getcollisionbox(self):
        return self.x - 20, self.y - 8, self.x + 5, self.y + 18

    def draw(self):
        self.image.draw(self.x, self.y)

    #########################################
    # 충돌 박스 테스트 코드
    ########################################
    def drawcollision(self):
        draw_rectangle(*self.getcollisionbox())

# ***************************************
# GuidedObstacle
# 캐릭터가 위치해있는 방향으로 날아가는 장애물
# ***************************************
class GuidedObstacle:
    # ***************************************
    # 장애물 시작 방향 값
    # ***************************************
    LEFT_START, RIGHT_START, UP_START, DOWN_START = 0, 1, 2, 3

    image = None

    def __init__(self):
        self.make(250, 200)

        if GuidedObstacle.image == None:
            GuidedObstacle.image = load_image('stage_3_gumeteor.png')

    # ***************************************
    # make
    # 장애물 재생성 함수
    # x, y 값은 정해진 위치에 따라 생성, 속도 10~15
    # ***************************************
    def make(self, chr_x, chr_y):
        self.select_pos = random.randint(0, 3)

        if (self.select_pos == self.LEFT_START):
            self.x, self.y = -20, chr_y
        elif (self.select_pos == self.RIGHT_START):
            self.x, self.y = 520, chr_y
        elif (self.select_pos == self.UP_START):
            self.x, self.y = chr_x, -20
        elif (self.select_pos == self.DOWN_START):
            self.x, self.y = chr_x, 420

        self.chr_x      = chr_x
        self.chr_y      = chr_y
        self.speed      =random.randint(10, 15)
        self.before_pos = 0
        # ***************************************
        # 장애물의 방향 값 설정
        # x: ↑[0],↓[1] // y: →[0],←[1]
        # ***************************************
        self.dir = random.randint(0, 1)

    # ***************************************
    # setpos
    # 속도 값에 따라 장애물 이동
    # ***************************************
    def setpos(self, x_speed, y_speed):
        self.x += x_speed
        self.y += y_speed

    # ***************************************
    # calspeed
    # 장애물 방향값에 따라 속도 값 리턴
    # ↑[0],→[0] return +speed
    # ↓[1],←[1] return -speed
    # ***************************************
    def calcspeed(self, pos, chr_pos, speed):
        # ***************************************
        # 장애물 떨림을 보정하기 위해 before_pos 와 chr_pos 를 비교
        # 같은 좌표라면 속도 값을 0 으로 셋팅
        # ***************************************
        if (self.before_pos == chr_pos):
            return 0

        self.before_pos = chr_pos

        if (pos < chr_pos):
            return speed
        else:
            return -speed

    # ***************************************
    # update
    # 장애물은 캐릭터의 위치 값을 갖고
    # 그 위치를 향해 날아감
    # ***************************************
    def update(self, chr_x, chr_y):
        self.chr_x = chr_x
        self.chr_y = chr_y
        # ***************************************
        # 시작 위치에 따라 장애물을 이동
        # ***************************************
        if (self.select_pos == self.LEFT_START):
            self.setpos(self.speed, (self.calcspeed(self.y, self.chr_y, self.speed)))

        elif (self.select_pos == self.RIGHT_START):
            self.setpos(-self.speed, (self.calcspeed(self.y, self.chr_y, self.speed)))

        elif (self.select_pos == self.UP_START):
            self.setpos((self.calcspeed(self.x, self.chr_x, self.speed)), self.speed)

        elif (self.select_pos == self.DOWN_START):
            self.setpos((self.calcspeed(self.x, self.chr_x, self.speed)), -self.speed)

         # ***************************************
         # 장애물이 화면 밖을 벗어나면 재생성
         # ***************************************
        if (self.x < - 30 or self.x > 530 or self.y < - 30 or self.y > 430):
            self.make(chr_x, chr_y)

    def getcollisionbox(self):
        return self.x - 20, self.y - 8, self.x + 5, self.y + 18

    def draw(self):
        self.image.draw(self.x, self.y)

    #########################################
    # 충돌 박스 테스트 코드
    ########################################
    def drawcollision(self):
        draw_rectangle(*self.getcollisionbox())

#***************************************
# Character
# 캐릭터를 담당하는 클래스
#***************************************
class Character:

    # ***************************************
    # 캐릭터의 방향 및 시트 값
    # ***************************************
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 5, 4, 1, 0
    # ***************************************
    # 키보드가 눌린 값
    # ***************************************
    K_NONE, K_LEFT_RIGHT, K_UP, K_DOWN = 0, 1, 2, 3

    def __init__(self):
        # ***************************************
        # dirupdown:    현재 KEY_UP,DOWN 상태인가 아닌가
        # dir:          현재 KEY_LEFT, RIGHT 상태인가 아닌가
        #
        # 0[안눌린 상태], 1[UP 상태], 2[DWON 상태]
        # False[안눌린 상태], True[눌린 상태]
        #
        # god:          무적
        # god_time:     무적 시간 [기본 3초]
        # ulti:         궁극기 [화면내 장애물 전부 제거]
        # ***************************************
        self.x, self.y  = 250, 200
        self.speed      = 15
        self.god        = False
        self.god_cnt    = 2
        self.god_time   = 0
        self.ulti       = False
        self.ulti_cnt   = 2
        self.frame      = 0
        self.state      = self.RIGHT_STAND
        self.key        = self.K_NONE
        self.updown     = 0
        self.dir        = False
        self.image      = load_image('stage_3_cha.png')
        self.effect     = load_image('effect.png')
        self.god_image  = load_image('god.png')
        self.ulti_image = load_image('ultimate.png')
        # ***************************************
        # 최초 생명력은 3
        # ***************************************
        self.life_cnt   = 3
        self.life_image = load_image('heart.png')

    def handle_event(self, event):
        # ***************************************
        # ->,<-,↑,↓ 키 입력시 캐릭터 이동
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.state = self.LEFT_RUN
                self.dir = True

            elif event.key == SDLK_RIGHT:
                self.state = self.RIGHT_RUN
                self.dir = True

            elif event.key == SDLK_a:
                self.setgod()
            elif event.key == SDLK_s:
                self.setulti()

            elif event.key == SDLK_UP or event.key == SDLK_DOWN:
                if self.state in (self.LEFT_STAND,):
                    self.state = self.LEFT_RUN
                elif self.state in (self.RIGHT_STAND,):
                    self.state = self.RIGHT_RUN

                if event.key == SDLK_UP:
                    self.updown = 1
                elif event.key == SDLK_DOWN:
                    self.updown = 2

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.state  = self.LEFT_STAND
                self.dir = False

            elif event.key == SDLK_RIGHT:
                self.state  = self.RIGHT_STAND
                self.dir = False

            elif event.key == SDLK_UP or event.key == SDLK_DOWN:
                if self.state in (self.LEFT_STAND,):
                    self.state = self.LEFT_RUN
                elif self.state in (self.RIGHT_STAND,):
                    self.state = self.RIGHT_RUN

                self.updown = 0

    def update(self):
        self.frame = (self.frame + 1) % 8
        # ***************************************
        # 화면을 벗어나지 않게 x, y 값을 조정
        # 스테이지 3 에서는 x, y 값을 12 씩 이동
        # ***************************************
        if self.dir == True:
            if self.state == self.RIGHT_RUN:
                self.x = min(500, self.x + self.speed)
            elif self.state == self.LEFT_RUN:
                self.x = max(0, self.x - self.speed)

        if self.updown != 0:
            if self.updown == 1 and self.y < 400:
                self.y = max(-30, self.y + self.speed)
            elif self.updown == 2 and self.y > 0:
                self.y = min(400, self.y - self.speed)

        if (self.life_cnt <= 0):
            return False

        self.ultiproc()

        self.godproc()

    def ultiproc(self):
        if (self.ulti == True):
            self.ulti = False

    def godproc(self):
       # ***************************************
       # 무적 스킬을 사용했을 경우 시간 처리
       # 시간이 0 이면 무적 스킬을 해제
       # ***************************************
       if self.god == True:
           skill_time = self.god_time - time.time()

           if (skill_time < 0):
               self.god = False
               return

           str_time = datetime.datetime.fromtimestamp(skill_time).strftime('%S')

           font = load_font('HMKMRHD.TTF', 20)
           font.draw(15, 70, str_time)

    # ***************************************
    # damage
    # 장애물과 충돌시 생명력 1 감소
    # ***************************************
    def damage(self):
        # ***************************************
        # god True 면 캐릭터 생명력 변화 없음
        # ***************************************
        if (self.god == True):
            return

        self.life_cnt = self.life_cnt - 1
        self.effect.draw(self.x, self.y)

    def setgod(self):
        if (self.god_cnt > 0 and self.god == False):
            self.god        = True
            self.god_time   = time.time() + 3
            self.god_cnt    -= 1

    def setulti(self):
        if (self.ulti_cnt > 0 and self.ulti == False):
            self.ulti       = True
            self.ulti_cnt   -= 1

    def getcollisionbox(self):
        return self.x - 10, self.y - 22, self.x + 13, self.y + 34

    def getposx(self):
        return self.x

    def getposy(self):
        return self.y

    def getulti(self):
        return self.ulti

    def draw(self):
        self.image.clip_draw(self.frame * 70, self.state * 70, 70, 70, self.x, self.y)
        # ***************************************
        # life_cnt 에 맞게 생명력 이미지를 draw
        # ***************************************
        for i in range(0, self.life_cnt):
            image_range = 30 * (i + 1)
            self.life_image.draw(image_range, 375)

        self.ulti_image.draw(470, 40)
        ulti_font   = load_font('HMKMRHD.TTF', 40)
        ulti_str    = str(self.ulti_cnt)
        ulti_font.draw(455, 40, ulti_str)

        self.god_image.draw(30, 40)
        god_font    = load_font('HMKMRHD.TTF', 40)
        god_str     = str(self.god_cnt)
        god_font.draw(15, 40, god_str)

    #########################################
    # 충돌 박스 테스트 코드
    #########################################
    def drawcollision(self):
        draw_rectangle(*self.getcollisionbox())

def handle_events():
    global running
    global game_stop
    global clear_time
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

        # ***************************************
        # SPACE 누르면 일시정지 상태
        # ***************************************
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if(game_stop == True):
                clear_time = clear_time - time.time()
                game_stop = False
            else:
                clear_time = clear_time + time.time()
                game_stop = True
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
    life_time   = clear_time - time.time()
    str_time    = datetime.datetime.fromtimestamp(life_time).strftime('%S')

    font        = load_font('HMKMRHD.TTF', 20)
    font.draw(240, 380, str_time)

    # ***************************************
    # 스테이지 3 의 클리어시간을 버티면 게임 종료
    # ***************************************
    if(int(str_time) <= 0 ):
        clear_font = load_font('HMKMRHD.TTF', 50)
        clear_font.draw(45, 200, 'STAGE CLEAR')
        update_canvas()
        delay(1)
        running = False

#***************************************
# stagefail
# 생명력이 0 이 돼 스테이지를 실패한 상태
#***************************************
def stagefail():
    global running

    clear_font = load_font('HMKMRHD.TTF', 50)
    clear_font.draw(80, 200, 'STAGE FAIL')
    update_canvas()
    delay(3)
    running = False

def collide(chr, obs):
    left_chr, bottom_chr, right_chr, top_chr = chr.getcollisionbox()
    left_obs, bottom_obs, right_obs, top_obs = obs.getcollisionbox()

    if left_chr < right_obs and right_chr > left_obs and bottom_chr < top_obs and top_chr > bottom_obs:
        return False

    return True

#***************************************
# startstage
# 스테이지 최초 이미지 출력
#***************************************
def startstage():
    back_ground = Background()

    clear_canvas()
    back_ground.draw()

    clear_font = load_font('HMKMRHD.TTF', 50)
    clear_font.draw(125, 200, 'STAGE3')

    update_canvas()
    delay(1)

def main():
    open_canvas(500, 400)

    global running
    global character
    global obstacle
    global game_stop
    global clear_time

    startstage()

    back_ground = Background()
    character   = Character()
    #***************************************
    # 스테이지 3 에서 기본 장애물 10, 유도 장애물 2
    # 클리어 시간은 30초
    #***************************************
    obstacle    = [Obstacle() for i in range(10)]
    guided_obs  = [GuidedObstacle() for i in range(2)]
    #########################################
    # 현재는 테스트용으로 시간을 15 초만 줌
    #########################################
    clear_time  = time.time() + 15

    game_stop   = True
    running     = True

    while running:
        handle_events()

        # ***************************************
        # game_stop 이 True 라면 플레이 상태
        # ***************************************
        if(game_stop == True):
            clear_canvas()

            back_ground.draw()
            character.draw()
            character.drawcollision()

            for meteor in obstacle:
                meteor.draw()
                meteor.drawcollision()
                meteor.update()

            for guided_meteor in guided_obs:
                guided_meteor.draw()
                guided_meteor.drawcollision()
                guided_meteor.update(character.getposx(), character.getposy())

            lifetime()

            # ***************************************
            # 궁극기가 눌렸다면 장애물들 초기화 함수 호출
            # ***************************************
            if (character.getulti() == True):
                for meteor in obstacle:
                    meteor.make()
                for guided_meteor in guided_obs:
                    guided_meteor.make(character.getposx(), character.getposy())

            if (character.update() == False):
                stagefail()

            # ***************************************
            # 장애물이 케릭터와 충돌하면 make 함수를
            # 호출해 다시 재생성 후 케릭터 생명력 1 감소
            # ***************************************
            for meteor in obstacle:
                if collide(character, meteor) == False:
                    meteor.make()
                    character.damage()

            for guided_meteor in guided_obs:
                if collide(character, guided_meteor) == False:
                    guided_meteor.make(character.getposx(), character.getposy())
                    character.damage()

            update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()



