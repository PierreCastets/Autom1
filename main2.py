from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import ClockBaseInterrupt, Clock
from random import randint
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from random import random as r
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
#from kivy.core.text.markup import tag


class CasseBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    hit = False

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def bounce_ball(self, ball):
        pass


class TextInput2(Label):
    def __init__(self, **kwargs):
        super(TextInput2, self).__init__(**kwargs)
        self.hit = False

    def bounce_ball(self, ball):
        pass


class CassePaddle(Widget):
    def __init__(self, **kwargs):
        super(CassePaddle, self).__init__(**kwargs)
        self.hit = False

    def bounce_ball(self, ball):
        self.hit = False
        if self.collide_widget(ball):
            ball2 = ball
            ball2.velocity = ball.velocity
            vx, vy = ball2.velocity
            ball2.pos = Vector(vx, -1 * vy) + ball.pos
            if self.collide_widget(ball2):
                bounced = Vector(-1 * vx, vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
            else:
                bounced = Vector(vx, -1 * vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
            self.hit = True


class CasseBrique(Widget):
    def __init__(self, posi, **kwargs):
        super(CasseBrique, self).__init__(**kwargs)
        self.pos = posi
        self.size = (Window.width / 20, Window.height / 40)
        self.hit = False

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball2 = ball
            ball2.velocity = ball.velocity
            vx, vy = ball2.velocity
            ball2.pos = Vector(vx, -1 * vy) + ball.pos
            if self.collide_widget(ball2):
                bounced = Vector(-1 * vx, vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
            else:
                bounced = Vector(vx, -1 * vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
            self.hit = True


class CasseMetal(Widget):
    def __init__(self, posi, **kwargs):
        super(CasseMetal, self).__init__(**kwargs)
        self.pos = posi
        self.size = (Window.width / 20, Window.height / 40)
        self.hit = False
        self.health = 1
        self.canvas.children[0].source = "metal.jpg"

    def bounce_ball(self, ball):
        if self.health == 0:
            self.canvas.children[0].source = "metal2.jpg"
        if self.collide_widget(ball):
            ball2 = ball
            ball2.velocity = ball.velocity
            vx, vy = ball2.velocity
            ball2.pos = Vector(vx, -1 * vy) + ball.pos
            if self.collide_widget(ball2):
                bounced = Vector(-1 * vx, vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
                if self.health == 1:
                    self.health = 0
                else:
                    self.hit = True
            else:
                bounced = Vector(vx, -1 * vy)
                vel = bounced
                ball.velocity = vel.x, vel.y
                if self.health == 1:
                    self.health = 0
                else:
                    self.hit = True


class CasseGame(Widget):
    ball = ObjectProperty(None)
    player = ObjectProperty(None)
    Window.size = (800, 800)
    score = NumericProperty(0)

    def serve_ball(self):
        self.ball.center = self.center
        #self.ball.velocity = Vector(40, 0).rotate(90)
        self.ball.velocity = Vector(8, 0).rotate(randint(20, 160))
        for i in range(20):
            for j in range(10):
                prob_spawn = r()
                prob_type = r()
                if prob_spawn < 0.5:
                    if prob_type < 0.9:
                        self.add_widget(CasseBrique((i * Window.width/20, Window.height * 3/4 + j * Window.height/40)))
                    else:
                        self.add_widget(CasseMetal((i * Window.width/20, Window.height * 3/4 + j * Window.height/40)))

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player.bounce_ball(self.ball)

        # bounce of bricks
        for brick in self.children:
            brick.bounce_ball(self.ball)
            if brick.hit:
                self.remove_widget(brick)
                self.score += 1

        # bounce off top
        if self.ball.top > self.height:
            self.ball.velocity_y *= -1

        # bounce off left and right

        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        if self.ball.y < 0:
            Color(0, 1, 1, mode='hsv')
            self.add_widget(TextInput2(text="[i][color=850606]GAME OVER[/color][/i]", x=self.center_x - 25,
                                       y=self.center_y, font_size=70, markup=True))
    #Bloc pour faire descendre les briques tout les x coups mais j'ai décidé de ne pas ajouter cette fonctionnalité
        '''if self.count == 5:
            for wid in self.children:
                if str(type(wid)) == "<class '__main__.CasseBrique'>" or\
                        str(type(wid)) == "<class '__main__.CasseMetal'>":
                    if wid.y < 30:
                        self.add_widget(TextInput2(text="[i][color=850606]GAME OVER[/color][/i]", x=self.center_x - 25,
                                                   y=self.center_y, font_size=70, markup=True))
                        self.end_game()
                    wid.y = wid.y - Window.height/40
            self.count = 0'''

    def __init__(self, **kwargs):
        super(CasseGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'right':
            self.player.center_x += 60

        if keycode[1] == 'left':
            self.player.center_x -= 60

        #if keycode[1] == 'up':
         #   self.player.center_y += 10

        #if keycode[1] == 'down':
         #   self.player.center_y -= 10

    def end_game(self):
        ClockBaseInterrupt.interupt_next_only


class CasseApp(App):
    def build(self):
        game = CasseGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    CasseApp().run()
