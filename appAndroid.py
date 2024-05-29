from kivymd.app import MDApp
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton,MDFloatingActionButton

class MeuApp(MDApp):
    def build(self):
        tela = Screen()
        rotulo = MDLabel(text='Olá Planeta Terra e todos os que habitam nele.',
                         halign='center',
                         theme_text_color='Error',
                         font_style='H1'
                         )
        icone = MDIcon(icon='bee',halign='left')
        botao = MDRectangleFlatButton(text='Ir para Lua',
                                      pos_hint={'center_x':0.8,'center_y':0.8})
        botao_icone = MDFloatingActionButton(icon='coffee',
                                             pos_hint={'center_x':0.4,'center_y':0.8})

        tela.add_widget(rotulo)
        tela.add_widget(icone)
        tela.add_widget(botao)
        tela.add_widget(botao_icone)

        return tela

MeuApp().run()