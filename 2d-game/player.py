import pyglet
# class which holds all relevant elements of the player object
class Player:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.elements = []
        player_width = 40
        player_height = 24
        self.elements.append(pyglet.shapes.Rectangle(WINDOW_WIDTH / 2 - player_width / 2,
                                                    WINDOW_HEIGHT / 10, 
                                                    player_width,
                                                    player_height,
                                                    color=(0, 255, 0)))
        self.elements.append(pyglet.shapes.Rectangle(WINDOW_WIDTH / 2 - player_height/3/2, 
                                                    WINDOW_HEIGHT / 10 + self.elements[0].height, 
                                                    player_height/3, 
                                                    player_height/3, 
                                                    color=(0, 255, 0)))
        self.elements.append(pyglet.shapes.Triangle(WINDOW_WIDTH/2 - player_height/3/2,
                                                    self.elements[1].y + self.elements[1].height,
                                                    WINDOW_WIDTH/2 + player_height/3/2,
                                                    self.elements[1].y + self.elements[1].height,
                                                    WINDOW_WIDTH/2,
                                                    self.elements[1].y + self.elements[1].height + 5,
                                                    color=(0, 255, 0)))

    #changes the x position of all elements but makes sure that the new x value can not lay outside the window
    def change_x(self, x_value):
        for element in self.elements:
            element.x += x_value
        if(self.elements[0].x + self.elements[0].width > self.window_width):
            reset_value = self.elements[0].x + self.elements[0].width - self.window_width
            for element in self.elements:
                element.x -= reset_value
        elif(self.elements[0].x < 0):
            reset_value = self.elements[0].x
            for element in self.elements:
                element.x -= reset_value

    # method for drawing the player object
    def draw(self):
        for element in self.elements:
            element.draw()

    #returns the width of the big rectangle
    def get_width(self):
        return self.elements[0].width
    
    #returns the x of the big rectangle
    def get_x(self):
        return self.elements[0].x
    
    #returns the y-position of the tip of the triangle
    def get_gun_point_y(self):
        return self.elements[2].y