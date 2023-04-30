import pyglet

ENEMY_Y_MOVEMENT = 15

# class to hold all relevant elements for an enemy object
class Enemy():
    def __init__(self, x , y, enemy_batch):
        self.elements = []
        self.elements.append(pyglet.shapes.Rectangle(x, y, 30, 10, color=(255, 255, 255), batch=enemy_batch))
        self.elements.append(pyglet.shapes.Rectangle(x + 15 - 7.5, y + 10, 15, 5, color=(255, 255, 255), batch=enemy_batch))
        self.elements.append(pyglet.shapes.Circle(x + 14.5, y + 15, 7.5, color=(255, 255, 255), batch=enemy_batch))

    # method to draw the enemy object
    def draw(self):
        for element in self.elements:
            element.draw()

    # returns the width of the rectangle on the bottom
    def get_width_baseplate(self):
        return self.elements[0].width
    
    # returns the x value of the rectangle on the bottom
    def get_x_baseplate(self):
        return self.elements[0].x
    
    # returns the y value of the rectangle on the bottom
    def get_y_baseplate(self):
        return self.elements[0].y
    
    # returns the hight of the rectangle on the bottom
    def get_height_baseplate(self):
        return self.elements[0].height
    
    # moves all elements by the x value
    def change_x(self, x):
        for element in self.elements:
            element.x += x

    # moves all elements for a fixed y value
    def set_y(self):
        for element in self.elements:
            element.y -= ENEMY_Y_MOVEMENT

    # shows if the enemy object is visible
    def get_visibility(self):
        return self.elements[0].visible
    
    # can be used to change the visibility of the enemy object
    def set_visibility(self, visibility):
        for element in self.elements:
            element.visible = visibility