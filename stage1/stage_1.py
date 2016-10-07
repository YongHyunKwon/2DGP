from pico2d import *
import random

#***************************************
# 스테이지 1
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
        self.image = load_image('stage_1.png')

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
            Obstacle.image = load_image('stage_1_stone.png')

    #***************************************
    # make
    # 장애물 재생성 함수
    # x: 20~480, y: 400, 속도: 5~10
    #***************************************
    def make(self):
        self.x, self.y = random.randint(20, 480), 400
        self.speed = random.randint(5, 10)

    def update(self):
        #***************************************
        # y 값은 속도 값에 비례하게 하강
        # 땅 밑으로 장애물이 사라지면 make 호출
        #***************************************
        self.y -=   self.speed

        if(self.y < -20):
            self.make()

    def draw(self):
        self.image.draw(self.x, self.y)

#***************************************
# Character
# 캐릭터를 담당하는 클래스
#***************************************
class Character:
    def __init__(self):
        self.x, self.y  = 250, 40
        self.speed      = 10
        self.frame      = 0
        self.image      = load_image('stage_1_cha.png')

    def handle_event(self, event):
        # ***************************************
        # ->,<- 키 입력시 캐릭터 이동
        # 스테이지1 에서는 x 값을 10 씩 이동
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.x += self.speed
            elif event.key == SDLK_LEFT:
                self.x -= self.speed

    def update(self):
        self.frame = (self.frame + 1) % 8
        # ***************************************
        # 화면을 벗어나지 않게 x 값을 조정
        # ***************************************
        if self.x > 500:
            self.x = 500
        elif self.x < 0:
            self.x = 0

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
    # 스테이지 1 에서 장애물은 10개
    #***************************************
    obstacle    = [Obstacle() for i in range(10)]

    running     = True

    while running:
        handle_events()
        character.update()

        clear_canvas()

        back_ground.draw()
        character.draw()

        for stone in obstacle:
            stone.draw()
            stone.update()

        update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()



