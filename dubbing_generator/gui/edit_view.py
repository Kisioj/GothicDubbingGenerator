from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    Text,
    Button,
    TextBox,
    Widget,
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


class EditView(Frame):
    def __init__(self, screen, element, title):
        super().__init__(
            screen,
            screen.height * 2 // 3,
            screen.width * 2 // 3,
            hover_focus=True,
            can_scroll=False,
            title=title,
            reduce_cpu=True,
        )

        self.title = title
        self._element = element

        self.buttons = [
            Button("Quit", self._quit)
        ]

    def __post__init__(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        for form_field in self.form_fields:
            layout.add_widget(form_field)

        # layout.add_widget(Divider())

        navbar = Layout([1] * len(self.buttons))
        self.add_layout(navbar)
        for i, button in enumerate(self.buttons):
            navbar.add_widget(button, i)

        self.fix()

    # def reset(self):
    #     super().reset()
    #     self.data = self._element

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

    '''
    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")
    '''
