from pico2d import *
import random
import math

#***************************************
# 스테이지 3
#***************************************
# 기본 인자 초기화
#***************************************
running     = None
character   = None
obstacle    = None

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

    def draw(self):
        self.image.draw(self.x, self.y)

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
    # x, y 값은 정해진 위치에 따라 생성, 속도 7~12
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
        self.speed      =random.randint(7, 12)
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
         # **************************************
        if (self.x < - 30 or self.x > 530 or self.y < - 30 or self.y > 430):
            self.make(chr_x, chr_y)

    def draw(self):
        self.image.draw(self.x, self.y)

#***************************************
# Character
# 캐릭터를 담당하는 클래스
#***************************************
class Character:
    def __init__(self):
        self.x, self.y  = 250, 200
        self.speed      = 12
        self.frame      = 0
        self.image      = load_image('stage_3_cha.png')

    def handle_event(self, event):
        # ***************************************
        # ->,<-,↑,↓ 키 입력시 캐릭터 이동
        # 스테이지 3 에서는 x 값을 12 씩 이동
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.x += self.speed
            elif event.key == SDLK_LEFT:
                self.x -= self.speed
            elif event.key == SDLK_UP:
                self.y += self.speed
            elif event.key == SDLK_DOWN:
                self.y -= self.speed

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

    def getposx(self):
        return self.x

    def getposy(self):
        return self.y

    def draw(self):
        self.image.clip_draw(self.frame * 70, 0, 70, 70, self.x, self.y)

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

def main():
    open_canvas(500, 400)

    global running
    global character
    global obstacle

    back_ground = Background()
    character   = Character()
    #***************************************
    # 스테이지 3 에서 기본 장애물 10, 유도 장애물 2
    #***************************************
    obstacle    = [Obstacle() for i in range(10)]
    guided_obs  = [GuidedObstacle() for i in range(2)]

    running     = True

    while running:
        handle_events()
        character.update()

        clear_canvas()

        back_ground.draw()
        character.draw()

        for meteor in obstacle:
            meteor.draw()
            meteor.update()

        for guided_meteor in guided_obs:
            guided_meteor.draw()
            guided_meteor.update(character.getposx(), character.getposy())

        update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()



