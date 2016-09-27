from pico2d import *

#***************************************
# 스테이지 2
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
        self.image = load_image('stage_2.png')

    def draw(self):
        self.image.draw(250, 200)

#***************************************
# Obstacle
# 게임내 장애물을 담당하는 클래스
#***************************************
class Obstacle:
    def __init__(self):
        self.image = load_image('stage_2_bubble.png')

    def draw(self):
        self.image.draw(250, 300)

#***************************************
# Character
# 캐릭터를 담당하는 클래스
#***************************************
class Character:
    def __init__(self):
        self.x, self.y  = 250, 40
        self.frame      = 0
        self.image = load_image('stage_2_cha.png')

    def handle_event(self, event):
        # ***************************************
        # →,←,↑ 키 입력시 캐릭터 이동
        # 물에서는 움직임이 느리기 때문에
        # 스테이지2 에서는 x, y값을 5 씩 이동
        # 현재는 테스트 중이므로 10으로 설정
        # ***************************************
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.x += 10
            elif event.key == SDLK_LEFT:
                self.x -= 10
            elif event.key == SDLK_UP:
                self.y += 10

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

        # ***************************************
        # 캐릭터는 바닥으로 계속 하강 상태
        # ***************************************
        self.y -= 1

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
    obstacle    = Obstacle()

    running = True

    while running:
        handle_events()
        character.update()

        clear_canvas()

        back_ground.draw()
        character.draw()
        obstacle.draw()

        update_canvas()

        delay(0.04)

    close_canvas()

if __name__ == '__main__':
    main()



