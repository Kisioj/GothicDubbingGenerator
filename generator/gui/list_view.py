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


class ListView(Frame):
    def __init__(self, screen, elements, title):
        super().__init__(
            screen,
            screen.height * 2 // 3,
            screen.width * 2 // 3,
            on_load=self._on_load,
            hover_focus=True,
            can_scroll=False,
            title=title
        )

        self.title = title
        self._elements = elements
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            self._prepared_elements(),
            name=self.title,
            add_scroll_bar=True,
            on_change=self._on_change,
            on_select=self._on_select,
        )

        self.remove_button = Button("Remove", self._remove)
        self.quit_button = Button("Quit", self._quit)
        self.buttons = [
            self.remove_button,
            self.quit_button,
        ]

    def __post__init__(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(self._list_view)
        layout.add_widget(Divider())

        navbar = Layout([1] * len(self.buttons))
        self.add_layout(navbar)
        for i, button in enumerate(self.buttons):
            navbar.add_widget(button, i)

        self.fix()
        self._on_change()

    def _prepared_elements(self):
        return tuple((str(element), element) for element in self._elements)

    def _on_change(self):
        self.remove_button.disabled = self._list_view.value is None

    def _on_load(self, new_value=None):
        self._list_view.options = self._prepared_elements()
        self._list_view.value = new_value

    def _on_select(self):
        raise NotImplementedError

    def _remove(self):
        self.save()

        remove_element = self.data[self.title]
        remove_index = self._elements.index(remove_element)

        new_index = remove_index + 1
        new_element = self._elements[new_index] if new_index < len(self._elements) else None
        if not new_element:
            new_index = remove_index - 1
            new_element = self._elements[new_index] if new_index > 0 else None

        del self._elements[remove_index]
        self._on_load(new_element)

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")
