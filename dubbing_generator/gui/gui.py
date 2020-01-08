from asciimatics.effects import RandomNoise
from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    Text,
    Button,
    TextBox,
    Widget,
    DropdownList)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from google.cloud import texttospeech

from collections import defaultdict
import sys


from .edit_view import EditView
from .list_view import ListView


def log(*args):
    with open('log.txt', 'a') as file:
        print(*args, file=file)


class NPC:
    def __init__(self, name, identifier, ai_outputs, language, voice, pitch, speed):
        self.name = name
        self.identifier = identifier
        self.ai_outputs = ai_outputs

        self.language = language
        self.voice = voice
        self.pitch = pitch
        self.speed = speed

    def __repr__(self):
        return f'<NPC {self.name} ({self.identifier})>'

    def __str__(self):
        if self.identifier:
            return f'{self.name} ({self.identifier})'
        return self.name


class AIOutput:
    def __init__(self, wav_filename, text):
        self.wav_filename = wav_filename
        self.text = text

    def __repr__(self):
        return f'<AIOutput {self.wav_filename} ({self.text})'


class DialogLinesListView(ListView):
    TITLE = "DIALOG LINES"

    def __init__(self, screen, gui):
        super().__init__(screen, [], self.TITLE)

        self.gui = gui
        self.element = None
        self.buttons = [
            Button("Back", self._back),
        ]
        super().__post__init__()

    def reset(self):
        super().reset()
        self.element = self.gui.selected_element

        if self.element:
            self._elements = [x for x in self.element.ai_outputs]
            self._list_view.options = self._prepared_elements()
            # self._list_view.update(frame_no=None)

    def _prepared_elements(self):
        return tuple((f'{i:03}: {element.text}', element.wav_filename) for i, element in enumerate(self._elements))

    def _generate_dubbing(self):
        pass

    def _on_select(self):
        # play sound
        pass

    def _back(self):
        self.save()
        raise NextScene(NPCEditView.TITLE)


class NPCsListView(ListView):
    TITLE = "NPCs"

    def __init__(self, screen, gui):
        super().__init__(screen, gui.npcs, self.TITLE)

        self.gui = gui
        self._generate_button = Button("Generate dubbing for every NPC", self._generate_dubbing)
        self.buttons = [
            self.remove_button,
            self._generate_button,
            self.quit_button,
        ]

        super().__post__init__()

    def _generate_dubbing(self):
        pass

    def _on_change(self):
        super()._on_change()
        self._generate_button.disabled = self._list_view.value is None

    def _on_select(self):
        self.save()
        self.gui.selected_element = self.data[self.title]

        with open('log.txt', 'w') as file:
            print(self.gui.selected_element, file=file)
            print(type(self.gui.selected_element), file=file)

        self.gui.npc_edit_view.title = f'Edit {self.gui.selected_element}'
        raise NextScene(NPCEditView.TITLE)


def pitch_validator(pitch):
    try:
        pitch = float(pitch)
        if pitch < -20 or pitch > 20:
            return False
    except ValueError:
        return False
    return True


def speed_validator(pitch):
    try:
        pitch = float(pitch)
        if pitch < 0.25 or pitch > 4.0:
            return False
    except ValueError:
        return False
    return True


class NPCEditView(EditView):
    TITLE = "Edit NPC"

    def __init__(self, screen, gui):
        super().__init__(screen, gui.selected_element, self.TITLE)

        self.buttons = [
            Button("Lines", self._to_dialog_lines),
            Button("Back", self._back),
        ]

        self.gui = gui
        self.element = None

        language_choices = [(x, x) for x in gui.voices_per_language]

        self.pitch_input = Text("Pitch [-20.0, 20.0]:", "pitch", validator=pitch_validator, on_change=self._change_pitch)
        self.speed_input = Text("Speed [0.25, 4.0]:", "speed", validator=speed_validator, on_change=self._change_speed)

        self.voice_dropdown = DropdownList([], "Voice:", "voice", on_change=self._select_voice)
        self.lang_dropdown = DropdownList(language_choices, "Language:", "lang", on_change=self._select_lang)

        self.form_fields = [
            self.lang_dropdown,
            self.voice_dropdown,
            self.pitch_input,
            self.speed_input,
        ]

        super().__post__init__()

    def reset(self):
        super().reset()

        self.element = self.gui.selected_element
        if self.element:
            log(1, self.element)
            log(2, self.element.pitch)
            log(3, self.element.speed)
            log(4, self.element.language)
            log(5, self.element.voice)
            voice = self.element.voice

            self.pitch_input.value = str(self.element.pitch)
            self.speed_input.value = str(self.element.speed)

            self.lang_dropdown.value = self.element.language
            self.voice_dropdown.value = voice

    def _select_lang(self):
        self.element.language = self.lang_dropdown.value

        self.voice_choices = [
            (str(x), str(x))
            for x in self.gui.voices_per_language[self.lang_dropdown.value].values()
        ]
        self.voice_dropdown._options = self.voice_choices
        self.voice_dropdown.value = self.voice_choices[0][0]

        self.screen.clear()

    def _select_voice(self):
        self.element.voice = self.voice_dropdown.value

        self.screen.clear()

    def _change_pitch(self):
        try:
            self.element.pitch = float(self.pitch_input.value)
        except ValueError:
            pass

    def _change_speed(self):
        try:
            self.element.speed = float(self.speed_input.value)
        except ValueError:
            pass

    def _back(self):
        #self.save()
        raise NextScene(NPCsListView.TITLE)

    def _to_dialog_lines(self):
        self.save()
        self.gui.dialog_lines_list_view.title = f'Lines: {self.gui.selected_element}'
        raise NextScene(DialogLinesListView.TITLE)


class Voice:
    def __init__(self, language, name, gender):
        self.language = language
        self.name = name
        self.gender = gender
        if gender == 1:
            self.gender_txt = "MALE"
        elif gender == 2:
            self.gender_txt = "FEMALE"

    def __repr__(self):
        return f'<Voice {self.language} {self.name} {self.gender_txt}>'

    def __str__(self):
        return f'{self.name} ({self.gender_txt})'


class Gui:
    SCENE_NPCS = "NPCs"

    def __init__(self, data, args_lang, args_gender):
        self.data = data

        self.client = texttospeech.TextToSpeechClient()
        voices = tuple(self.client.list_voices().voices)

        self.voices_per_language = defaultdict(dict)
        for voice in voices:
            lang_code = voice.language_codes[0]
            self.voices_per_language[lang_code][voice.name] = Voice(lang_code, voice.name, voice.ssml_gender)

        # setup default language
        default_lang = tuple(self.voices_per_language.keys())[0]
        for language in self.voices_per_language:
            if language.endswith(args_lang):
                default_lang = language

        # setup default voice
        default_voice = tuple(self.voices_per_language[default_lang].keys())[0]
        for voice in self.voices_per_language[default_lang].values():
            if voice.gender_txt == args_gender:
                default_voice = str(voice)
                break

        # setup npc list
        self.npcs = []
        for npc in data:
            ai_outputs = []
            for ai_output in npc['ai_outputs']:
                ai_outputs.append(AIOutput(ai_output['wav_filename'], ai_output['text']))
            self.npcs.append(
                NPC(
                    npc['name'],
                    npc['identifier'],
                    ai_outputs,
                    npc.get('language', default_lang),
                    npc.get('voice', default_voice),
                    npc.get('pitch', 0.0),
                    npc.get('speed', 1.0),
                )
            )

        self.selected_element = None

    def run(self):
        def demo(screen, scene):
            self.npcs_list_view = NPCsListView(screen, self)
            self.npc_edit_view = NPCEditView(screen, self)
            self.dialog_lines_list_view = DialogLinesListView(screen, self)

            scenes = [
                Scene([self.npcs_list_view], -1, name=NPCsListView.TITLE),
                Scene([self.npc_edit_view], -1, name=NPCEditView.TITLE),
                Scene([self.dialog_lines_list_view], -1, name=DialogLinesListView.TITLE),
            ]

            screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

        last_scene = None
        while True:
            try:
                Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
