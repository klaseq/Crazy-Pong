import pyglet
from pyglet import gl
import random
from pyglet.window import key
from config import config

if __name__ == "__main__":
    
    image = pyglet. resource. image('space2.jpg')

    def draw_rectangle(x1, y1, x2, y2):
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2d(int(x1), int(y1))
        gl.glVertex2d(int(x1), int(y2))
        gl.glVertex2d(int(x2), int(y2))
        gl.glVertex2d(int(x2), int(y1))
        gl.glEnd()

    def draw():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor3f(1, 1, 1)
        image.blit(0, 0)

        draw_rectangle(
            config.ball_position[0] - config.ball_size //2, 
            config.ball_position[1] - config.ball_size //2,
            config.ball_position[0] + config.ball_size //2, 
            config.ball_position[1] + config.ball_size //2) #ball
        draw_rectangle(0, config.bar_position[0] - config.bar_height // 2, config.bar_width, config.bar_position[0] + config.bar_height // 2) # bar 1
        draw_rectangle(config.field_width - config.bar_width, config.bar_position[1] - config.bar_height // 2, config.field_width, config.bar_position[1] + config.bar_height // 2) # bar 2
        draw_rectangle(config.bar_position[2] - config.bar_height // 2, 0, config.bar_position[2] + config.bar_height // 2, config.bar_width) # bar 3
        draw_rectangle(config.bar_position[3] - config.bar_height // 2, config.field_height - config.bar_width, config.bar_position[3] + config.bar_height // 2, config.field_height) # bar 4
        
        draw_text(str(config.score[0]), x=config.text_indentation, y=config.field_height - config.font - config.text_indentation, x_position='left') # player 1 config.score
        draw_text(str(config.score[1]), x=config.field_width - config.text_indentation, y=config.field_height - config.font - config.text_indentation, x_position='right') # player 2 config.score

    def draw_text(text, x, y, x_position):
        inscription = pyglet.text.Label(text, font_size=config.font, x=x, y=y, anchor_x=x_position)
        inscription.draw()

    def press_key(character, modifiers):
        if character == key.W:
            config.keys_pressed.add(('up', 0))
        if character == key.S:
            config.keys_pressed.add(('down', 0))
        if character == key.A:
            config.keys_pressed.add(('left', 3))
        if character == key.D:
            config.keys_pressed.add(('right', 3))
        if character == key.UP:
            config.keys_pressed.add(('up', 1))
        if character == key.DOWN:
            config.keys_pressed.add(('down', 1))
        if character == key.LEFT:
            config.keys_pressed.add(('left', 2))
        if character == key.RIGHT:
            config.keys_pressed.add(('right', 2))

    def release_key(character, modifiers):
        if character == key.W:
            config.keys_pressed.discard(('up', 0))
        if character == key.S:
            config.keys_pressed.discard(('down', 0))
        if character == key.A:
            config.keys_pressed.discard(('left', 3))
        if character == key.D:
            config.keys_pressed.discard(('right', 3))
        if character == key.UP:
            config.keys_pressed.discard(('up', 1))
        if character == key.DOWN:
            config.keys_pressed.discard(('down', 1))
        if character == key.LEFT:
            config.keys_pressed.discard(('left', 2))
        if character == key.RIGHT:
            config.keys_pressed.discard(('right', 2))

    def refresh_state(dt):
        for bar_number in (0, 1):
            if('up', bar_number) in config.keys_pressed:
                config.bar_position[bar_number] += config.bar_speed * dt
            if ('down', bar_number) in config.keys_pressed:
                config.bar_position[bar_number] -= config.bar_speed * dt
            
            if config.bar_position[bar_number] < config.bar_height / 2:
                config.bar_position[bar_number] = config.bar_height / 2
            if config.bar_position[bar_number] > config.field_height - config.bar_height / 2:
                config.bar_position[bar_number] = config.field_height - config.bar_height / 2
        
        for bar_number in (2, 3):
            if ('left', bar_number) in config.keys_pressed:
                config.bar_position[bar_number] -= config.bar_speed * dt
            if ('right', bar_number) in config.keys_pressed:
                config.bar_position[bar_number] += config.bar_speed * dt
            
            if config.bar_position[bar_number] < config.bar_height / 2:
                config.bar_position[bar_number] = config.bar_height / 2
            if config.bar_position[bar_number] > config.field_width - config.bar_height / 2:
                config.bar_position[bar_number] = config.field_width - config.bar_height / 2
        
        config.ball_position[0] += config.ball_speed[0] * dt
        config.ball_position[1] += config.ball_speed[1] * dt

        bar_min_vertical = config.ball_position[1] - config.ball_size / 2 - config.bar_height / 2
        bar_max_vertical = config.ball_position[1] + config.ball_size / 2 + config.bar_height / 2
        bar_min_horizontal = config.ball_position[0] - config.ball_size / 2 - config.bar_height / 2
        bar_max_horizontal = config.ball_position[0] + config.ball_size / 2 + config.bar_height / 2

        if config.ball_position[0] < config.bar_width + config.ball_size / 2:
            if bar_min_vertical < config.bar_position[0] < bar_max_vertical:
                config.ball_speed[0] = abs(config.ball_speed[0])
            else:
                config.score[1] += 1
                reset()

        if config.ball_position[0] > config.field_width - (config.bar_width + config.ball_size / 2):
            if bar_min_vertical < config.bar_position[1] < bar_max_vertical:
                config.ball_speed[0] =  -abs(config.ball_speed[0])
            else:
                config.score[0] += 1
                reset()
        
        if config.ball_position[1] < config.bar_width + config.ball_size / 2:
            if bar_min_horizontal < config.bar_position[2] < bar_max_horizontal:
                config.ball_speed[1] = abs(config.ball_speed[1])
            else:
                config.score[0] += 1
                reset()
        
        if config.ball_position[1] > config.field_height - (config.bar_width + config.ball_size / 2):
            if bar_min_horizontal < config.bar_position[3] < bar_max_horizontal:
                config.ball_speed[1] = -abs(config.ball_speed[1])
            else:
                config.score[1] += 1
                reset()
        

    def reset():
        config.ball_position[0] = config.field_width // 2
        config.ball_position[1] = config.field_height // 2

        if random.randint(0, 1):
            config.ball_speed[0] = config.general_speed
        else:
            config.ball_speed[0] = - config.general_speed
        
        config.ball_speed[1] = random.uniform(-1, 1) * config.general_speed

    reset()

    window = pyglet.window.Window(width=config.field_width, height=config.field_height)
    window.push_handlers(on_draw=draw, on_key_press=press_key, on_key_release=release_key)
    pyglet.clock.schedule(refresh_state)




    pyglet.app.run()