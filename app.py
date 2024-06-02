import app
from tildagonos import tildagonos

from events.input import Buttons, BUTTON_TYPES
from app_components import clear_background

import random

PX_SIZE = 10
PX_SIZE_H = 5

BLINK = 1
WINK_L = 2
WINK_R = 3
EAR_TWITCH_L = 4
EAR_TWITCH_R = 5
IDEA = 6
EXCLAIM = 7
FACE_ANIMATIONS = (WINK_L, WINK_R, EAR_TWITCH_L, EAR_TWITCH_R, IDEA, EXCLAIM)



class PixelCat(app.App):

    def __init__(self):
        self.button_states = Buttons(self)

        self.bg = (0, 0.2, 0.2)
        self.fg = (0, 1, 0)
        self.eye = (0, 0, 0)
        self.scan = (0,0,0)
        
        self.next_anim = 0
        self.animation = None

        self.cat_offset = -2
        self.eye_offset = self.cat_offset + 3

    def update(self, delta):

        # Exit
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        
        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.animation = BLINK
            self.next_anim = -499
        elif self.button_states.get(BUTTON_TYPES["UP"]) and self.animation is None:
            self.button_states.clear()
            self.set_random_animation()
            self.next_anim = -1
        else:
            self.next_anim = self.next_anim - delta

        if self.next_anim < -700:
            self.resetAnimTimer()
            self.animation = None
        elif self.next_anim < 0 and self.animation is None:
            if random.randint(1,5) is 5:
                self.set_random_animation()
            else:
                self.animation = BLINK

    # -12 to + 12
    def draw_pixel(self, ctx, x, y, x_count=1, y_count=1, colour=None):
        if colour is None:
            colour = self.fg
        x_loc = PX_SIZE*x - PX_SIZE_H
        y_loc = PX_SIZE*y - PX_SIZE_H
        ctx.rgb(*colour).rectangle(x_loc,y_loc,PX_SIZE*x_count,PX_SIZE*y_count).fill()

    def set_random_animation(self):
        self.animation = random.choice(FACE_ANIMATIONS)

    def resetAnimTimer(self):
        self.next_anim = random.randint(1000, 7000)

    def draw_eyes(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset, x_count=2, y_count=2, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset, x_count=2, y_count=2, colour=self.eye)

    def draw_idea(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset -1, x_count=2, y_count=3, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset -1, x_count=2, y_count=3, colour=self.eye)

        self.draw_pixel(ctx, -1, self.cat_offset -7, x_count=3, colour=(1.0, 1.0, 1.0))
        self.draw_pixel(ctx, -2, self.cat_offset -6, x_count=5, y_count=3, colour=(1.0, 1.0, 1.0))
        self.draw_pixel(ctx, -1, self.cat_offset -3, x_count=3, colour=(1.0, 1.0, 1.0))

        self.draw_pixel(ctx, 0, self.cat_offset -5, y_count=3, colour=(1.0, 1.0, 0))
        self.draw_pixel(ctx, -1, self.cat_offset -2, x_count=3, colour=(0.9, 0.8, 0))
    
    def draw_exclaim(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset -1, x_count=2, y_count=3, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset -1, x_count=2, y_count=3, colour=self.eye)

        blue = (0.0, 0.5, 1.0)

        self.draw_pixel(ctx, 0, self.cat_offset -8, colour=blue)
        self.draw_pixel(ctx, -1, self.cat_offset -7, x_count=3, y_count=2, colour=blue)
        self.draw_pixel(ctx, 0, self.cat_offset -5, y_count=2, colour=blue)
        self.draw_pixel(ctx, 0, self.cat_offset -2, colour=blue)

    def draw_wink_l(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset, x_count=2, colour=self.eye)
        self.draw_pixel(ctx, -3, self.eye_offset + 1, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset, x_count=2, y_count=2, colour=self.eye)

        self.draw_pixel(ctx, -8, self.cat_offset + 3, colour=(0.9,0,0))
        self.draw_pixel(ctx, -10, self.cat_offset + 3, colour=(0.9,0,0))
        self.draw_pixel(ctx, -10, self.cat_offset + 4, x_count=3, colour=(0.7,0,0))
        self.draw_pixel(ctx, -9, self.cat_offset + 5, colour=(0.5,0,0))

    def draw_wink_r(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset, x_count=2, y_count=2, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset, x_count=2, colour=self.eye)
        self.draw_pixel(ctx, 3, self.eye_offset +1, colour=self.eye)

        self.draw_pixel(ctx, 8, self.cat_offset + 1, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 10, self.cat_offset + 1, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 8, self.cat_offset + 2, x_count=3, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 9, self.cat_offset + 3, colour=(1,0.5,0.5))

    def draw_blink(self, ctx):
        self.draw_pixel(ctx, -4, self.eye_offset + 1, x_count=3, colour=self.eye)
        self.draw_pixel(ctx, 2, self.eye_offset + 1, x_count=3, colour=self.eye)
    
    def draw_ears(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -6, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, -6, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, -6, self.cat_offset -3)
        # Ear R
        self.draw_pixel(ctx, 4, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, 5, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, 6, self.cat_offset -3)

    def draw_ear_twitch_l(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -5, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, -4, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, -3, self.cat_offset -3)
        self.draw_pixel(ctx, -6, self.cat_offset, colour=self.bg)
        # Ear R
        self.draw_pixel(ctx, 4, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, 5, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, 6, self.cat_offset -3)
    
    def draw_ear_twitch_r(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -6, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, -6, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, -6, self.cat_offset -3)
        # Ear R
        self.draw_pixel(ctx, 3, self.cat_offset -1, x_count=3)
        self.draw_pixel(ctx, 3, self.cat_offset -2, x_count=2)
        self.draw_pixel(ctx, 3, self.cat_offset -3)
        self.draw_pixel(ctx, 6, self.cat_offset, colour=self.bg)
    
    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(*self.bg).rectangle(-120,-120,240,240).fill()

        # Face
        self.draw_pixel(ctx, -6, self.cat_offset, x_count=13, y_count=6)
        self.draw_pixel(ctx, -5, self.cat_offset+6, x_count=11)
        self.draw_pixel(ctx, -4, self.cat_offset+7, x_count=9)

        # Ears
        if self.animation is EAR_TWITCH_L:
            self.draw_ear_twitch_l(ctx)
        elif self.animation is EAR_TWITCH_R:
            self.draw_ear_twitch_r(ctx)
        else:
            self.draw_ears(ctx)

        # Eyes
        if self.animation is BLINK:
            self.draw_blink(ctx)
        elif self.animation is WINK_L:
            self.draw_wink_l(ctx)
        elif self.animation is WINK_R:
            self.draw_wink_r(ctx)
        elif self.animation is IDEA:
            self.draw_idea(ctx)
        elif self.animation is EXCLAIM:
            self.draw_exclaim(ctx)
        else:
            self.draw_eyes(ctx)


        ctx.begin_path()
        for i in range(-120 - PX_SIZE_H, 120, PX_SIZE):
            # draw indicator lines for x
            ctx.move_to(i, -120)
            ctx.line_to(i, 120)
            # draw indicator lines for y
            ctx.move_to(-120, i)
            ctx.line_to(120, i)

            # TODO hide partial edge pixels

        ctx.rgb(*self.scan).stroke()

__app_export__ = PixelCat