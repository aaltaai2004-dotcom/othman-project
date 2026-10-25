import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent


def main(page: ft.Page):
    page.title="Increment counter"
    page.theme_mode ='light'
    text_number:TextField=TextField(value='0',text_align=ft.TextAlign.RIGHT,width=100)
    def decerment(e:ControlEvent):
        text_number.value=str(int(text_number.value)-1)
        page.update()
    def increment(e:ControlEvent):
     text_number.value=str(int(text_number.value)+1)
     page.update()
    page.add(
    ft.Row(
                [
                    ft.IconButton(ft.Icons.REMOVE,on_click=decerment),
                    text_number,
                    ft.IconButton(ft.Icons.ADD,on_click=increment)
                ]
            )



        )



ft.run(main)