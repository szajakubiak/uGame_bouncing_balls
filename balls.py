import ugame, stage

bounce_ball = open("bounce_ball.wav", "rb")
sound = ugame.audio
sound.mute(False)

class Ball(stage.Sprite):
    def __init__(self, x, y, dx, dy, sx = 15, sy = 15):
        super().__init__(bank, 1, x, y)
        self.dx = dx
        self.dy = dy
        self.sx = sx
        self.sy = sy
        self.set_rotation(self.dx, self.dy)
    
    def set_rotation(self, dx, dy):
        '''
        Changes animation of ball according to it's speed values in directions x and y
        '''
        if dx > 0 and dy > 0:
            self.set_frame(self.frame, 2)
        elif dx < 0 and dy > 0:
            self.set_frame(self.frame, 3)
        elif dx < 0 and dy < 0:
            self.set_frame(self.frame, 0)
        else:
            self.set_frame(self.frame, 1)
    
    def update(self):
        super().update()
        self.set_frame(self.frame % 4 + 1)
        # Check for collision with screen edge
        if not 0 <= self.x + self.dx < (128 - self.sx):
            self.dx = -self.dx
            self.set_rotation(self.dx, self.dy)
        if not 0 <= self.y + self.dy < (128 - self.sy):
            self.dy = -self.dy
            self.set_rotation(self.dx, self.dy)
        self.move(self.x + self.dx, self.y + self.dy)

def collision(sprite1, sprite2):
    status = False
    if abs(sprite1.x - sprite2.x) <= sprite1.sx / 2 + sprite2.sx / 2:
        if abs(sprite1.y - sprite2.y) <= sprite1.sy / 2 + sprite2.sy / 2:
            status = True
    return status

bank = stage.Bank.from_bmp16("ball.bmp")
background = stage.Grid(bank)
ball1 = Ball(64, 0, 1, 3)
ball2 = Ball(0, 76, 2, 2)
ball3 = Ball(111, 64, 2, 3)
ball4 = Ball(32, 20, 3, 2)
ball5 = Ball(90, 90, 2, 1)
ball6 = Ball(5, 15, 2, 2)
game = stage.Stage(ugame.display, 24)
sprites = [ball1, ball2, ball3, ball4, ball5, ball6]
game.layers = [ball1, ball2, ball3, ball4, ball5, ball6, background]
game.render_block()

while True:
    for sprite in sprites:
		# Create a list of objects which can collide with sprite
        other_spr = sprites[:]
        other_spr.remove(sprite)
        for other in other_spr:
			# Check if there is a collison
            if collision(sprite, other):
                sound.play(bounce_ball)
                # Check different cases of collisions to decide about a bounce
                if abs(sprite.x - other.x) > abs(sprite.y - other.y): # sides of objects collide
                    if sprite.dx * other.dx > 0: # both object are moving in the same direction
						# Faster object changes it's direction
                        if sprite.dx > other.dx:
                            sprite.dx = -sprite.dx
                        else:
                            other.dx = -other.dx
                    else: # objects moving in different directions
						# Object on the right will have positive value of speed after collision
                        if sprite.x > other.x:
                            sprite.dx = abs(sprite.dx)
                            other.dx = -abs(other.dx)
                        else:
                            sprite.dx = -abs(sprite.dx)
                            other.dx = abs(other.dx)
                else: # top of one object collide with bottom of second one
                    if sprite.dy * other.dy > 0:
                        if sprite.dy > other.dy:
                            sprite.dy = -sprite.dy
                        else:
                            other.dy = -other.dy
                    else:
                        if sprite.y > other.y:
                            sprite.dy = abs(sprite.dy)
                            other.dy = -abs(other.dy)
                        else:
                            sprite.dy = -abs(sprite.dy)
                            other.dy = abs(other.dy)
                sprite.set_rotation(sprite.dx, sprite.dy)
                other.set_rotation(other.dx, other.dy)
        sprite.update()
    game.render_sprites(sprites)
    game.tick()
