import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class MyApp(App):

    def build(self):
        return Label(text='Olá Planeta!')


if __name__ == '__main__':
    MyApp().run()