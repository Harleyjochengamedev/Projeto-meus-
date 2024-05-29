import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')

class Segundo(App):
    def build(self):
        b = BoxLayout(orientation='vertical')
        t = TextInput(font_size=50,height=100,size_hint_y=None)
        f = FloatLayout()
        s = Scatter()
        l = Label(text='Olá Planeta!',font_size=50)
        f.add_widget(s)
        s.add_widget(l)
        b.add_widget(t)
        b.add_widget(f)
        t.bind(text=l.setter('text'))
        return b

if __name__ == '__main__':
    Segundo().run()