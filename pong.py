import pygame, random

'''
velocities in pix/sec
'''

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
fps = 60
background = (0, 255, 0)
game_over = False

#dict of keycode: is it pressed
keys = {
        119: False, #w
        115: False, #s
        273: False, #up   arrow
        274: False  #down arrow
}

class RenderItem():
        def update(self):
                raise NotImplementedError
        def render(self):
                raise NotImplementedError

class Ball(RenderItem):
        def __init__(self, color, radius, x, y, vx, vy, bounce_v_incr):
                self.color = color
                self.radius = radius
                self.x = x
                self.y = y
                self.vx = vx
                self.vy = vy
                self.bounce_v_incr = bounce_v_incr
        def update(self):
                global game_over
                next_pos = {'x': self.x + self.vx * vel_fact,
                                        'y': self.y + self.vy * vel_fact}
                if next_pos['y'] - self.radius < 0 or next_pos['y'] + self.radius > screen_height:
                        self.vy *= -1
                elif next_pos['x'] - self.radius < Paddle.width:
                        paddle = next(thing for thing in  things_to_render if isinstance(thing, Paddle) and thing.side == 'left')
                        if paddle.y > self.y or (paddle.y + Paddle.height) < self.y:
                                game_over = True
                        else:
                                self.vx *= -self.bounce_v_incr
                elif next_pos['x'] + self.radius > screen_width - Paddle.width:
                        paddle = next(thing for thing in things_to_render if isinstance(thing, Paddle) and thing.side == 'right')
                        if paddle.y > self.y or (paddle.y + Paddle.height) < self.y:
                                game_over = True
                        else:
                                self.vx *= -self.bounce_v_incr
                else:
                        self.x = next_pos['x']
                        self.y = next_pos['y']
        def render(self):
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Paddle(RenderItem):
        speed = 400
        height = 80
        width = 20
        def __init__(self, color, side, controls):
                '''
                side must be either 'left' or 'right'
                controls must be a dict with 'up' and 'down' attrs
                '''
                assert side in ('left', 'right')
                self.color = color
                self.side = side
                self.x = 0 if side == 'left' else screen_width - Paddle.width
                self.y = screen_height / 2 - Paddle.height / 2
                self.controls = controls
        def update(self):
                if keys[self.controls['up']] and self.y > 0:
                        self.y -= Paddle.speed * vel_fact
                elif keys[self.controls['down']] and self.y + Paddle.height < screen_height:
                        self.y += Paddle.speed * vel_fact
        def render(self):
                pygame.draw.rect(screen, self.color, [self.x, self.y, Paddle.width, Paddle.height])


things_to_render = [
                                        Ball((255, 0, 0), 10, 100, 100, 150, random.randint(-200, 200), 1.1),
                                        Paddle((0,0,255), 'left' , {'up': 119,'down': 115}),
                                        Paddle((0,0,255), 'right', {'up': 273,'down': 274})
                                   ]

clock  = pygame.time.Clock()
while True:
        time_delta = clock.tick(fps)
        vel_fact = time_delta / 1000
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                        quit()
                elif e.type in (pygame.KEYDOWN, pygame.KEYUP):
                        if e.key in keys:
                                keys[e.key] = e.type == pygame.KEYDOWN
                        else:
                                print('invalid key!')

        if game_over:
                print('game_over')
        else:
                screen.fill(background)
                for thing in things_to_render:
                        thing.update()
                        thing.render()

        pygame.display.update()
