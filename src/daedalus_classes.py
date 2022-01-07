from typing import Union

from grammar.DaedalusParser import DaedalusParser

import logging
logging.basicConfig(filename='output/debug.log', filemode='w', level=logging.DEBUG)


class CInstance:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f'<{self.identifier}>'


class CInfo(CInstance):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.npc = None


class CNpc(CInstance):
    def __init__(self, identifier, name=None):
        super().__init__(identifier)
        self.name = name
        self.ai_outputs = []
        self.gender = 'M'

    def serialize(self, with_dialogues=False, with_gender=False):
        data = {
            'name': self.name,
            'identifier': self.identifier,
        }
        if with_dialogues:
            data['ai_outputs'] = [
                ai_output.serialize()
                for ai_output in self.ai_outputs
                if ai_output.comment
            ]

        if with_gender:
            data['gender'] = self.gender

        return data


class AIOutput:
    SELF = "SELF"
    OTHER = "OTHER"
    cache = set()

    def __init__(
            self,
            ctx: DaedalusParser.FunctionCallContext,
            c_info_instance: Union[CInfo, None],
            data_sniffer,
            line: str,
            current_self,
            file_path: str,
    ):
        if '//' not in line:
            logging.error(f'{file_path}:{ctx.start.line}')
            logging.error(line)
            return

        speaker, listener, name = ctx.expression()
        self.speaker = speaker.getText().upper()
        self.listener = listener.getText().upper()
        self.name = name.getText().strip('"').upper()

        if self.name in AIOutput.cache:
            return
        AIOutput.cache.add(self.name)

        if self.speaker == AIOutput.OTHER:
            c_npc_instance = data_sniffer.PLAYER_NPC
        else:
            c_npc_instance = current_self

        self.c_info_instance = c_info_instance
        self.c_npc_instance = c_npc_instance
        c_npc_instance.ai_outputs.append(self)

        parts = line.split('//')
        if line.count('//') > 1:
            logging.debug(f'{file_path}:{ctx.start.line}')
            logging.debug(line)
            parts = line.split('//')
            _, self.comment, *_ = parts
        else:
            self.comment = parts[-1].strip()

    def serialize(self):
        return {
            'wav_filename': self.name,
            'text': self.comment.lower(),
        }
