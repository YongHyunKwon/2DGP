import random
import time
import datetime
import os
from pico2d import *
import stage_3

#***************************************
# 스테이지 2
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
        self.image = load_image('stage_2.png')

    def draw(self):
        self.image.draw(250, 200)

#***************************************
# Obstacle
# 게임내 장애물을 담당하는 클래스
#***************************************
class Obstacle:
    # ***************************************
    # 장애물 타입 값
    # ***************************************
    NONE, HEART, SPEED_UP, TIME_SUB, MOVE_STOP      = 0, 1, 2, 3, 4
    TIME_ADD, ULTI,GOD                              = 5, 6, 7

    image           = None
    heart_image     = None
    speed_up_image  = None
    time_sub_image  = None
    move_stop_image = None
    time_add_image  = None
    ulti_image      = None
    god_image       = None

    def __init__(self):
        self.obj = self.NONE
        self.make()

        if Obstacle.image == None:
            Obstacle.image              = load_image('stage_2_bubble.png')
        if Obstacle.heart_image == None:
            Obstacle.heart_image        = load_image('heart.png')
        if Obstacle.speed_up_image == None:
            Obstacle.speed_up_image     = load_image('speed_up.png')
        if Obstacle.time_sub_image == None:
            Obstacle.time_sub_image     = load_image('time_sub.png')
        if Obstacle.move_stop_image == None:
            Obstacle.move_stop_image    = load_image('move_stop.png')
        if Obstacle.time_add_image == None:
            Obstacle.time_add_image     = load_image('time_add.png')
        if Obstacle.ulti_image == None:
            Obstacle.ulti_image         = load_image('ultimate.png')
        if Obstacle.god_image == None:
            Obstacle.god_image          = load_image('god.png')

    #***************************************
    # make
    # 장애물 재생성 함수
    # x: 20~480, y: -20, 속도: 7~12
    #***************************************
    def make(self):
        self.randobj()
        self.x, self.y  = random.randint(20, 480), -20
        self.speed      = random.randint(7, 12)

    # ***************************************
    # randobj
    # 장애물의 타입을 결정
    # ***************************************
    def randobj(self):
        rand_val = random.randint(0, 100)
        # ***************************************
        # 0~100 사의 난수값을 가지고 장애물의 타입을 결정
        # ***************************************
        if (rand_val < 5):
            self.obj = self.HEART
        elif (rand_val < 10):
            self.obj = self.SPEED_UP
        elif (rand_val < 15):
            self.obj = self.TIME_SUB
        elif (rand_val < 20):
            self.obj = self.MOVE_STOP
        elif(rand_val < 25):
            self.obj = self.TIME_ADD
        elif (rand_val < 30):
            self.obj = self.ULTI
        elif (rand_val < 35):
            self.obj = self.GOD
        else:
            self.obj = self.NONE

    def getobjtype(self):
        return self.obj

    def update(self):
        #***************************************
        # y 값은 속도 값에 비례하게 상승
        # 지상으로 장애물이 사라지면 make 호출
        #***************************************
        self.y += self.speed

        if(self.y > 500):
            self.make()

    def getcollisionbox(self):
        if (self.obj == self.HEART):
            return self.x - 20, self.y - 10, self.x + 8, self.y + 20
        elif (self.obj == self.SPEED_UP):
            return self.x - 23, self.y - 5, self.x + 8, self.y + 25
        elif (self.obj == self.TIME_SUB):
            return self.x - 20, self.y - 10, self.x + 16, self.y + 13
        elif (self.obj == self.MOVE_STOP):
            return self.x - 19, self.y - 17, self.x + 16, self.y + 17
        elif (self.obj == self.TIME_ADD):
            return self.x - 18, self.y - 17, self.x + 16, self.y + 16
        elif (self.obj == self.ULTI):
            return self.x - 28, self.y - 16, self.x + 24, self.y + 25
        elif (self.obj == self.GOD):
            return self.x - 28, self.y - 22, self.x + 28, self.y + 20
        else:
            return self.x - 20, self.y - 15, self.x + 15, self.y + 20

    def draw(self):
        if (self.obj == self.HEART):
            self.heart_image.draw(self.x, self.y)
        elif (self.obj == self.SPEED_UP):
            self.speed_up_image.draw(self.x, self.y)
        elif (self.obj == self.TIME_SUB):
            self.time_sub_image.draw(self.x, self.y)
        elif (self.obj == self.MOVE_STOP):
            self.move_stop_image.draw(self.x, self.y)
        elif (self.obj == self.TIME_ADD):
            self.time_add_image.draw(self.x, self.y)
        elif (self.obj == self.ULTI):
            self.ulti_image.draw(self.x, self.y)
        elif (self.obj == self.GOD):
            self.god_image.draw(self.x, self.y)
        else:
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
    # 장애물 타입 값
    # ***************************************
    NONE, HEART, SPEED_UP, TIME_SUB, MOVE_STOP  = 0, 1, 2, 3, 4
    TIME_ADD, ULTI, GOD                         = 5, 6, 7

    def __init__(self):
        # ***************************************
        # dirup:            현재 KEY_UP 상태인가 아닌가
        # dir:              현재 KEY_LEFT, RIGHT 상태인가 아닌가
        #
        # False[안눌린 상태], True[눌린 상태]
        #
        # god:              무적
        # god_time:         무적 시간 [기본 3초]
        # ulti:             궁극기 [화면내 장애물 전부 제거]
        # speed_up:         이동속도 증가
        # speed_up_time:    이동속도 증가 시간 [기본 3초]
        # time_sub:         시간 감소
        # move_stop:        이동 금지
        # move_stop_time:   이동 금지 시간[기본 3초]
        # time_add:         시간 증가
        # ***************************************
        self.x, self.y      = 250, 200
        self.x_speed        = 8
        self.y_speed        = 3
        self.cur_x_speed    = 8
        self.cur_y_speed    = 3
        self.god            = False
        self.god_cnt        = 2
        self.god_time       = 0
        self.ulti           = False
        self.ulti_cnt       = 2
        self.speed_up       = False
        self.speed_up_time  = 0
        self.time_sub       = False
        self.move_stop      = False
        self.move_stop_time = 0
        self.time_add       = False
        self.frame          = random.randint(0, 7)
        self.state          = self.RIGHT_STAND
        self.dirup          = False
        self.dir            = False
        self.image          = load_image('stage_2_cha.png')
        self.effect         = load_image('effect.png')
        self.god_image      = load_image('god.png')
        self.ulti_image     = load_image('ultimate.png')
        # ***************************************
        # 최초 생명력은 3
        # ***************************************
        self.life_cnt       = 3
        self.life_image     = load_image('heart.png')

    def handle_event(self, event):
        # ***************************************
        # ->,<-,↑ 키 입력시 캐릭터 이동
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.state  = self.LEFT_RUN
                self.dir    = True

            elif event.key == SDLK_RIGHT:
                self.state  = self.RIGHT_RUN
                self.dir    = True

            elif event.key == SDLK_a:
                self.setgod()
            elif event.key == SDLK_s:
                self.setulti()

            elif event.key == SDLK_UP:
                if self.state in (self.LEFT_STAND,):
                    self.state = self.LEFT_RUN
                elif self.state in (self.RIGHT_STAND,):
                    self.state = self.RIGHT_RUN
                self.dirup = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.state  = self.LEFT_STAND
                self.dir    = False

            elif event.key == SDLK_RIGHT:
                self.state  = self.RIGHT_STAND
                self.dir    = False

            elif event.key == SDLK_UP:
                if self.state in (self.LEFT_RUN,):
                    self.state = self.LEFT_STAND
                elif self.state in (self.RIGHT_RUN,):
                    self.state = self.RIGHT_STAND
                self.dirup = False

    def update(self):
        self.frame = (self.frame + 1) % 8
        # ***************************************
        # 화면을 벗어나지 않게 x, y 값을 조정
        # 스테이지 2 에서는 x 값 5, y 값 3씩 이동
        #
        # dir == True
        # 방향키[→,←] 가 눌렸을 때만 x 이동
        # ***************************************
        if self.dir == True:
            if self.state == self.RIGHT_RUN:
                self.x = min(500, self.x + self.x_speed)
            elif self.state == self.LEFT_RUN:
                self.x = max(0, self.x - self.x_speed)

        # ***************************************
        # dirup == True
        # 방향키[↑] 가 눌렸을 때만 y 이동
        # ***************************************
        if self.dirup == True:
            if self.y < 400:
                self.y = max(-30, self.y + self.y_speed)

        #***************************************
        # 캐릭터는 밑으로 계속 하강
        #***************************************
        self.y -= 1

        if (self.life_cnt <= 0):
            return False

        self.ultiproc()

        self.godproc()

        self.speedupproc()

        self.movestopproc()

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

    def speedupproc(self):
        if (self.speed_up == True):
            skill_time = self.speed_up_time - time.time()

            # ***************************************
            # speed_up 시간이 끝나면 속도 복귀
            # ***************************************
            if (skill_time < 0):
                self.speed_up   = False
                self.x_speed    -= 5
                self.y_speed    -= 3

    def movestopproc(self):
        if (self.move_stop == True):
            skill_time = self.move_stop_time - time.time()

            # ***************************************
            # move_stop 시간이 끝나면 속도 복귀
            # ***************************************
            if (skill_time < 0):
                self.move_stop    = False
                self.x_speed      = self.cur_x_speed
                self.y_speed      = self.cur_y_speed

    # ***************************************
    # damage
    # 장애물과 충돌시 장애물 타입에 따라 처리
    # ***************************************
    def damage(self, obj):
        # ***************************************
        # 장애물이 생명력 충전일 경우 생명력 + 1
        # 최대 5개의 값을 넘지 아니함
        # ***************************************
        if (obj == self.HEART):
            self.life_cnt = self.life_cnt + 1
            self.life_cnt = min(5, self.life_cnt)
            return

        elif(obj == self.SPEED_UP):
            # ***************************************
            # speed_up 아이템은 먹었을 때 한번만 발동
            # 단 이동 금지가 활성화된 상태라면 발동 안됨
            # 연속 발동이 되지 않도록 flag 값으로 체크
            # ***************************************
            if(self.speed_up == False and self.move_stop == False):
                self.speed_up       = True
                self.speed_up_time  = time.time() + 3
                self.x_speed        += 5
                self.y_speed        += 3

        elif (obj == self.TIME_SUB):
            self.time_sub = True

        elif (obj == self.MOVE_STOP):
            # ***************************************
            # move_stop 아이템은 먹었을 때 한번만 발동
            # 연속 발동이 되지 않도록 flag 값으로 체크
            # ***************************************
            if (self.move_stop == False):
                self.move_stop        = True
                self.move_stop_time   = time.time() + 3
                self.x_speed          = 0
                self.y_speed          = 0

        elif (obj == self.TIME_ADD):
            self.time_add = True

        # ***************************************
        # 스킬은 최대 9개 까지만 적용
        # ***************************************
        elif(obj == self.ULTI):
            self.ulti_cnt = min(9, self.ulti_cnt + 1)
        elif(obj == self.GOD):
            self.god_cnt = min(9, self.god_cnt + 1)

        else:
            # ***************************************
            # god True 면 캐릭터 생명력 변화 없음
            # ***************************************
            if (self.god == True):
                return

            self.life_cnt   = self.life_cnt - 1
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

    def settimesub(self):
        self.time_sub       = False

    def settimeadd(self):
        self.time_add = False

    def getulti(self):
        return self.ulti

    def gettimesub(self):
        return self.time_sub

    def gettimeadd(self):
        return self.time_add

    def getcollisionbox(self):
        return self.x - 15, self.y - 25, self.x + 10, self.y + 30

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
    global character
    global game_stop
    global clear_time

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
            if (game_stop == True):
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
    global character

    if character.gettimesub() == True:
        clear_time -= 3
        character.settimesub()
    elif character.gettimeadd() == True:
        clear_time += 3
        character.settimeadd()

    # ***************************************
    # 클리어 시간과 현재 시간과의 차이를 구함
    # ***************************************
    life_time   = max(0, clear_time - time.time())
    str_time    = datetime.datetime.fromtimestamp(life_time).strftime('%M:%S')

    font        = load_font('HMKMRHD.TTF', 20)
    font.draw(225, 380, str_time)

    # ***************************************
    # 스테이지 2 의 클리어시간을 버티면 스테이지 3 전환
    # ***************************************
    if(life_time <= 0 ):
        clear_font = load_font('HMKMRHD.TTF', 50)
        clear_font.draw(45, 200, 'STAGE CLEAR')
        update_canvas()
        delay(1)
        close_canvas()
        stage_3.main()
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
    clear_font.draw(125, 200, 'STAGE2')

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
    # 스테이지 2 에서 장애물은 15개
    # 클리어 시간은 20 초
    #***************************************
    #########################################
    # 현재는 테스트용으로 시간을 10 초만 줌
    #########################################
    obstacle    = [Obstacle() for i in range(15)]
    clear_time  = time.time() + 10

    game_stop   = True
    running     = True

    while running:
        handle_events()

        # ***************************************
        # game_stop 이 True 라면 플레이 상태
        # ***************************************
        if (game_stop == True):
            clear_canvas()

            back_ground.draw()
            character.draw()
            character.drawcollision()

            for bubble in obstacle:
                bubble.draw()
                bubble.drawcollision()
                bubble.update()

            lifetime()

            # ***************************************
            # 궁극기가 눌렸다면 장애물들 초기화 함수 호출
            # ***************************************
            if (character.getulti() == True):
                for bubble in obstacle:
                    bubble.make()

            if (character.update() == False):
                stagefail()

            # ***************************************
            # 장애물이 케릭터와 충돌하면 make 함수를
            # 호출해 다시 재생성 후 케릭터 생명력 1 감소
            # ***************************************
            for bubble in obstacle:
                if collide(character, bubble) == False:
                    character.damage(bubble.getobjtype())
                    bubble.make()

            update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()



