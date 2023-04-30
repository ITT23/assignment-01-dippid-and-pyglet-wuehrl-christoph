# A simple implementation of space invaders that can be controlled with the DIPPID app
# After the game starts and no DIPPID app is connected there is a start screen with instructions
# You can control the player sprite by tilting your device and shoot with the button 4
# Kill all enemies before they reach the red line
# The speed of the enemies will increase over time
# After your lose you can restart the game with button 1
# The program should be closed using the terminal

from DIPPID import SensorUDP
import time
import pyglet
from threading import Thread
from player import Player
from ufo import Enemy

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PORT = 5700
END_LINE_Y = 150
ENEMY_START_SPEED = 8
BULLET_SPEED = 5
ROWS_OF_ENEMIES = 5
COLUMNS_OF_ENEMIES = 15
NUMBER_OF_TICKS_TO_INCREASE_ENEMY_SPEED = 1000
POINTS_FOR_KILLED_ENEMY = 5
ENEMIES_X_MOVEMENT = 5
GUN_COOL_DOWN = 0.8


sensor = SensorUDP(PORT)
shot_fired = False
points_value = 0
points_text = 'points: '
ticks = 0
shoots = []
enemies = []
enemies_moving_right = True
enemies_movement_speed = ENEMY_START_SPEED
game_over = False


def main():
    global game_over
    global points_value
    win = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    # sets up batches, that multiple elements can be drawn with one method call
    enemy_batch = pyglet.graphics.Batch()
    shoots_batch = pyglet.graphics.Batch()
    start_screen_batch = pyglet.graphics.Batch()
    end_screen_batch = pyglet.graphics.Batch()

    # sets up all relevant text elements for the start screen
    start_screen_elements = get_start_screen(start_screen_batch)

    # sets up the score view and the red line
    points = pyglet.text.Label('Points: 0', font_name='Times New Roman', font_size=12, x=WINDOW_WIDTH - WINDOW_WIDTH/10, y=WINDOW_HEIGHT - WINDOW_HEIGHT/10)
    end_line = pyglet.shapes.Rectangle(0, END_LINE_Y, WINDOW_WIDTH, 2, color=(255, 0, 0))

    # sets up the player and enemy objects
    setup_enemies(enemy_batch)
    player = Player(WINDOW_WIDTH, WINDOW_HEIGHT)


    #draw cycle
    @win.event
    def on_draw():
        global game_over
        global points_value
        global enemies_movement_speed
        win.clear()
        if(check_all_enemies_killed()): # resets when all enemies are killed
            reset_enemies_and_bullets(enemy_batch)
        if(game_over): # shows the game over screen and handles the restart
            end_screen_elements = get_end_screen(end_screen_batch)
            end_screen_batch.draw()
            if(sensor.get_value('button_1') == 1): # handles the restart
                points_value = 0
                enemies_movement_speed = ENEMY_START_SPEED
                reset_enemies_and_bullets(enemy_batch)
                game_over = False
        elif(not sensor.get_capabilities() == []): # game cycle
            # handles player movement
            if(sensor.get_value('gravity')['y'] > 1 and player.get_x() + player.get_width() < WINDOW_WIDTH):
                player.change_x(sensor.get_value('gravity')['y'])
            elif(sensor.get_value('gravity')['y'] < -1 and player.get_x() > 0):
                player.change_x(sensor.get_value('gravity')['y'])

            # handles the shoot event
            if(sensor.get_value('button_4') == 1 and not shot_fired):
                shot_thread = Thread(target=wait_for_new_shot, daemon=True)
                shot_thread.start()
                shoots.append(pyglet.shapes.Rectangle(player.get_x() + player.get_width() / 2 - 1, player.get_gun_point_y(), 2, 5, color=(0,255,0), batch=shoots_batch))
            animate_enemies()
            
            # moves the bullets
            for shoot in shoots:
                shoot.y += BULLET_SPEED
                if(shoot.y > WINDOW_HEIGHT):
                    shoots.remove(shoot)
            
            check_collision()

            #draws all elements
            player.draw()
            shoots_batch.draw()
            enemy_batch.draw()
            end_line.draw()
            points.text = f'{points_text}{points_value}'
            points.draw()
        else: # shows start screen when no DIPPID app is connected
            start_screen_batch.draw()

    
    pyglet.app.run()


# sets up rows and columns of enemies at a fixed distance
def setup_enemies(enemy_batch):
    enemies.clear()
    for i in range(ROWS_OF_ENEMIES):
        enemies.append([])
        for j in range(COLUMNS_OF_ENEMIES):
            enemies[i].append(Enemy(j * 40 + 50, WINDOW_HEIGHT - 100 - i * 40, enemy_batch))


# sets a timer for a new shoot to be fired
def wait_for_new_shot():
    global shot_fired
    shot_fired = True
    time.sleep(GUN_COOL_DOWN)
    shot_fired = False

# checks for collision between the bullets and enemies
def check_collision():
    global points_value
    for shoot in shoots:
        for enemy_list in enemies:
            if(enemy_list[0].get_y_baseplate() <= shoot.y + shoot.height and enemy_list[0].get_y_baseplate() + enemy_list[0].get_height_baseplate() >= shoot.y + shoot.height):
                for enemy in enemy_list:
                    if(not enemy.get_visibility()):
                        continue
                    if(enemy.get_x_baseplate() < shoot.x and enemy.get_x_baseplate() + enemy.get_width_baseplate() > shoot.x):
                        shoots.remove(shoot)
                        enemy.set_visibility(False)
                        points_value += POINTS_FOR_KILLED_ENEMY

# takes care of the movement of the enemies and increases the movement speed
def animate_enemies():
    global ticks
    global enemies_moving_right
    global enemies_movement_speed
    ticks += 1
    if(ticks % enemies_movement_speed == 0):
        set_enemies_x_movement()
        for enemy_list in enemies:
            for enemy in enemy_list:
                if(enemies_moving_right):
                    enemy.change_x(ENEMIES_X_MOVEMENT)
                else:
                    enemy.change_x(-ENEMIES_X_MOVEMENT)
    if(ticks >= NUMBER_OF_TICKS_TO_INCREASE_ENEMY_SPEED):
        ticks = 0
        if(enemies_movement_speed > 1):
            enemies_movement_speed -= 1 
                
# handles the enemies moment in y direction
def set_enemies_y():
    global game_over
    for enemy_list in enemies:
        for enemy in enemy_list:
            enemy.set_y()
            if(enemy.get_visibility() and enemy.get_y_baseplate() < END_LINE_Y):
                game_over = True

# helper function to handle the enemy movement
def set_enemies_x_movement():
    global enemies_moving_right
    enemies_move_down = False
    for enemy_list in enemies:
        for enemy in enemy_list:
            if(enemy.get_x_baseplate() + enemy.get_width_baseplate() >= WINDOW_WIDTH and enemy.get_visibility()):
                enemies_moving_right = False
            elif(enemy.get_x_baseplate() <= 0 and enemy.get_visibility()):
                enemies_moving_right = True
                enemies_move_down = True
    if(enemies_move_down):
        set_enemies_y()

# checks if all enemies are killed an should respawn
def check_all_enemies_killed():
    for enemy_list in enemies:
        for enemy in enemy_list:
            if(enemy.get_visibility()):
                return False
    return True

#sets up the elements for the start screen
def get_start_screen(start_screen_batch):
    start_texts = []
    start_texts.append(pyglet.text.Label('Connect with your DIPPID app', font_name='Times New Roman', font_size=32, x=WINDOW_WIDTH/2-275, y=WINDOW_HEIGHT/2 + 50, batch=start_screen_batch))
    start_texts.append(pyglet.text.Label('You can move by tilting your device and shoot with the 4 button', font_name='Times New Roman', font_size=16, x=125, y=WINDOW_HEIGHT/2 -10, batch=start_screen_batch))
    start_texts.append(pyglet.text.Label('As time progresses the enemies will get faster', font_name='Times New Roman', font_size=16, x=175, y=WINDOW_HEIGHT/2 -50, batch=start_screen_batch))
    start_texts.append(pyglet.text.Label('You should kill them before they reach the red line', font_name='Times New Roman', font_size=16, x=150, y=WINDOW_HEIGHT/2 - 90, batch=start_screen_batch))
    return start_texts

#sets up the elements for the end screen
def get_end_screen(end_screen_batch):
    elements = []
    elements.append(pyglet.text.Label(("You are game over"), font_name='Times New Roman', font_size=32, x=200, y=WINDOW_HEIGHT/2 + 50, batch=end_screen_batch))
    score_string = 'score: '
    score_text = f'{score_string}{points_value}'
    elements.append(pyglet.text.Label(score_text, font_name='Times New Roman', font_size=12, x=200, y=WINDOW_HEIGHT / 2, batch=end_screen_batch))
    elements.append(pyglet.text.Label("Restart with the 1 Button", font_name='Times New Roman', font_size=12, x=200, y=WINDOW_HEIGHT / 2 - 50, batch=end_screen_batch))
    return elements

# reset after game over and when all enemies are killed
def reset_enemies_and_bullets(enemy_batch):
    shoots.clear()
    setup_enemies(enemy_batch)

main()