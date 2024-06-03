import app
from tildagonos import tildagonos

from events.input import Buttons, BUTTON_TYPES
from app_components import clear_background

import random

PX_SIZE = 10
PX_SIZE_H = 5
CAT_OFFSET = -2
EYE_OFFSET = CAT_OFFSET + 3
FACE_ANIMATIONS = [] 

class Pallet(object):
    def __init__(self, 
                 bg=(0, 0.2, 0.2), 
                 fg = (0, 1, 0), 
                 eye = (0, 0, 0),
                 scan = (0,0,0)):
        self.bg = bg
        self.fg = fg
        self.eye = eye
        self.scan = scan

class Anim(object):
    def __init__(self, pallet):
        self.pallet = pallet

    def draw_pixel(self, ctx, x, y, x_count=1, y_count=1, colour=None):
        if colour is None:
            colour = self.pallet.fg
        x_loc = PX_SIZE*x - PX_SIZE_H
        y_loc = PX_SIZE*y - PX_SIZE_H
        ctx.rgb(*colour).rectangle(x_loc, y_loc, PX_SIZE*x_count, PX_SIZE*y_count).fill()
    
    def draw_ears(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -6, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, -6, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, -6, CAT_OFFSET -3)
        # Ear R
        self.draw_pixel(ctx, 4, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, 5, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, 6, CAT_OFFSET -3)
    
    def draw_eyes(self, ctx):
        self.draw_pixel(ctx, -4, EYE_OFFSET, x_count=2, y_count=2, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET, x_count=2, y_count=2, colour=self.pallet.eye)

    def update(self, delta):
        pass

    def frame(self, ctx):
        self.draw_ears(ctx)
        self.draw_eyes(ctx)

    def done(self):
        return True

class SingleFrameAnim(Anim):
    len = 700
    def __init__(self, pallet):
        super().__init__(pallet)

    def update(self, delta):
        self.len = self.len - delta
    
    def isDone(self):
        return self.len <= 0
    

class Face(Anim):
    def frame(self, ctx):
        self.draw_pixel(ctx, -6, CAT_OFFSET, x_count=13, y_count=6)
        self.draw_pixel(ctx, -5, CAT_OFFSET+6, x_count=11)
        self.draw_pixel(ctx, -4, CAT_OFFSET+7, x_count=9)

class Blink(SingleFrameAnim):
    
    def frame(self, ctx):
        self.draw_ears(ctx)

        self.draw_pixel(ctx, -4, EYE_OFFSET + 1, x_count=3, colour=self.pallet.eye)
        self.draw_pixel(ctx, 2, EYE_OFFSET + 1, x_count=3, colour=self.pallet.eye)

class Wink(SingleFrameAnim):
    len = 1100

    def __init__(self, pallet):
        super().__init__(pallet)
        self.variant = random.randint(0,1)
    
    def wink_l(self, ctx):
        self.draw_pixel(ctx, -4, EYE_OFFSET, x_count=2, colour=self.pallet.eye)
        self.draw_pixel(ctx, -3, EYE_OFFSET + 1, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET, x_count=2, y_count=2, colour=self.pallet.eye)

        self.draw_pixel(ctx, -8, CAT_OFFSET + 3, colour=(0.9,0,0))
        self.draw_pixel(ctx, -10, CAT_OFFSET + 3, colour=(0.9,0,0))
        self.draw_pixel(ctx, -10, CAT_OFFSET + 4, x_count=3, colour=(0.7,0,0))
        self.draw_pixel(ctx, -9, CAT_OFFSET + 5, colour=(0.5,0,0))

    def wink_r(self, ctx):
        self.draw_pixel(ctx, -4, EYE_OFFSET, x_count=2, y_count=2, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET, x_count=2, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET +1, colour=self.pallet.eye)

        self.draw_pixel(ctx, 8, CAT_OFFSET + 1, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 10, CAT_OFFSET + 1, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 8, CAT_OFFSET + 2, x_count=3, colour=(1,0.5,0.5))
        self.draw_pixel(ctx, 9, CAT_OFFSET + 3, colour=(1,0.5,0.5))
    
    def frame(self, ctx):
        self.draw_ears(ctx)

        if self.variant:
            self.wink_l(ctx)
        else:
            self.wink_r(ctx)

FACE_ANIMATIONS.append(Wink)

class EarTwitch(SingleFrameAnim):
    def __init__(self, pallet):
        super().__init__(pallet)
        self.variant = random.randint(0,1)
    
    def ear_l(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -5, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, -4, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, -3, CAT_OFFSET -3)
        self.draw_pixel(ctx, -6, CAT_OFFSET, colour=self.pallet.bg)
        # Ear R
        self.draw_pixel(ctx, 4, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, 5, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, 6, CAT_OFFSET -3)
    
    def ear_r(self, ctx):
        # Ear L
        self.draw_pixel(ctx, -6, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, -6, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, -6, CAT_OFFSET -3)
        # Ear R
        self.draw_pixel(ctx, 3, CAT_OFFSET -1, x_count=3)
        self.draw_pixel(ctx, 3, CAT_OFFSET -2, x_count=2)
        self.draw_pixel(ctx, 3, CAT_OFFSET -3)
        self.draw_pixel(ctx, 6, CAT_OFFSET, colour=self.pallet.bg)

    def frame(self, ctx):
        self.draw_eyes(ctx)

        if self.variant:
            self.ear_l(ctx)
        else:
            self.ear_r(ctx)
    
FACE_ANIMATIONS.append(EarTwitch)

class Idea(SingleFrameAnim):
    len = 1000
    def frame(self, ctx):
        self.draw_ears(ctx)

        self.draw_pixel(ctx, -4, EYE_OFFSET -1, x_count=2, y_count=3, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET -1, x_count=2, y_count=3, colour=self.pallet.eye)

        self.draw_pixel(ctx, -1, CAT_OFFSET -7, x_count=3, colour=(1.0, 1.0, 1.0))
        self.draw_pixel(ctx, -2, CAT_OFFSET -6, x_count=5, y_count=3, colour=(1.0, 1.0, 1.0))
        self.draw_pixel(ctx, -1, CAT_OFFSET -3, x_count=3, colour=(1.0, 1.0, 1.0))

        self.draw_pixel(ctx, 0, CAT_OFFSET -5, y_count=3, colour=(1.0, 1.0, 0))
        self.draw_pixel(ctx, -1, CAT_OFFSET -2, x_count=3, colour=(0.9, 0.8, 0))

FACE_ANIMATIONS.append(Idea)

class Exclaim(SingleFrameAnim):
    len = 1000
    def frame(self, ctx):
        self.draw_ears(ctx)

        self.draw_pixel(ctx, -4, EYE_OFFSET -1, x_count=2, y_count=3, colour=self.pallet.eye)
        self.draw_pixel(ctx, 3, EYE_OFFSET -1, x_count=2, y_count=3, colour=self.pallet.eye)

        blue = (0.0, 0.5, 1.0)

        self.draw_pixel(ctx, 0, CAT_OFFSET -8, colour=blue)
        self.draw_pixel(ctx, -1, CAT_OFFSET -7, x_count=3, y_count=2, colour=blue)
        self.draw_pixel(ctx, 0, CAT_OFFSET -5, y_count=2, colour=blue)
        self.draw_pixel(ctx, 0, CAT_OFFSET -2, colour=blue)

FACE_ANIMATIONS.append(Exclaim)

class Stars(Anim):
    len = 300
    frames = 6

    def update(self, delta):
        self.len = self.len - delta
        if self.len <= 0:
            self.frames = self.frames -1
            self.len = 300
    
    def isDone(self):
        return  self.frames <= 0

    def frame(self, ctx):
        self.draw_ears(ctx)

        white = (1.0, 1.0, 1.0)
        self.draw_pixel(ctx, -4, EYE_OFFSET - 1, x_count=3, y_count=3, colour=white)
        self.draw_pixel(ctx, 2, EYE_OFFSET -1, x_count=3, y_count=3, colour=white)

        self.draw_pixel(ctx, -3, EYE_OFFSET - 1, y_count=3, colour=self.pallet.bg)
        self.draw_pixel(ctx, 3, EYE_OFFSET -1, y_count=3, colour=self.pallet.bg)

        self.draw_pixel(ctx, -4, EYE_OFFSET, x_count=3, colour=self.pallet.bg)
        self.draw_pixel(ctx, 2, EYE_OFFSET, x_count=3, colour=self.pallet.bg)

        yellow = (1.0, 1.0, 0.0)
        if self.frames % 2:
            self.draw_pixel(ctx, -3, CAT_OFFSET -6, colour=yellow)
            self.draw_pixel(ctx, 2, CAT_OFFSET -4, colour=yellow)
        else:
            self.draw_pixel(ctx, -4, CAT_OFFSET -6, x_count=3, colour=yellow)
            self.draw_pixel(ctx, -3, CAT_OFFSET -7, y_count=4, colour=yellow)

            self.draw_pixel(ctx, 1, CAT_OFFSET -4, x_count=3, colour=yellow)
            self.draw_pixel(ctx, 2, CAT_OFFSET -5, y_count=3, colour=yellow)

FACE_ANIMATIONS.append(Stars)

class PixelCat(app.App):

    def __init__(self):
        self.button_states = Buttons(self)

        self.pallet = Pallet()
        
        self.next_anim = 500
        self.animation = None

        self.base_face = Face(self.pallet)
        self.base_extras = Anim(self.pallet)

    def update(self, delta):

        # Exit
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            self.animation = Blink(self.pallet)
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            self.set_random_animation()
        # elif self.button_states.get(BUTTON_TYPES["CONFIRM"]):
        #     self.button_states.clear()
        #     self.animation = Stars(self.pallet)
        elif self.animation:
            self.animation.update(delta)

            if self.animation.isDone():
                self.animation = None
                self.resetAnimTimer()
        else:
            self.next_anim = self.next_anim - delta
            if self.next_anim <= 0:
                if random.randint(1, 5) is 5:
                    self.set_random_animation()
                else:
                    self.animation = Blink(self.pallet)

    def set_random_animation(self):
        anim_class = random.choice(FACE_ANIMATIONS)
        self.animation = anim_class(self.pallet)

    def resetAnimTimer(self):
        self.next_anim = random.randint(1000, 7000)
    
    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(*self.pallet.bg).rectangle(-120,-120,240,240).fill()

        # Face
        self.base_face.frame(ctx)

        if self.animation:
            self.animation.frame(ctx)
        else:
            self.base_extras.frame(ctx)


        ctx.begin_path()
        for i in range(-120 - PX_SIZE_H, 120, PX_SIZE):
            # draw indicator lines for x
            ctx.move_to(i, -120)
            ctx.line_to(i, 120)
            # draw indicator lines for y
            ctx.move_to(-120, i)
            ctx.line_to(120, i)

            # TODO hide partial edge pixels

        ctx.rgb(*self.pallet.scan).stroke()

__app_export__ = PixelCat