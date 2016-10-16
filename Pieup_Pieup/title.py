from pico2d import *
import stage_1

#***************************************
# 타이틀
#***************************************
# 기본 인자 초기화
#***************************************
running     = None

#***************************************
# Background
# 타이틀 배경을 담당하는 클래스
#***************************************
class Background:
    def __init__(self):
        self.image = load_image('title.png')

    def draw(self):
        self.image.draw(250, 200)

def handle_events():
    global running
    global character

    events = get_events()
    # ***************************************
    # 스페이스바를 눌렀을 경우 stage_1 호출
    # ***************************************
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            close_canvas()
            stage_1.main()

def main():
    open_canvas(500, 400)

    global running

    back_ground = Background()

    running     = True

    while running:
        handle_events()

        clear_canvas()

        back_ground.draw()

        update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()