from typing import Union

from data_extractor.grammar import DaedalusParser


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

    def serialize(self):
        return {
            'name': self.name,
            'identifier': self.identifier,
            'ai_outputs': [
                ai_output.serialize()
                for ai_output in self.ai_outputs
                if ai_output.comment
            ]
        }


class AIOutput:
    SELF = "SELF"
    OTHER = "OTHER"

    def __init__(
            self,
            ctx: DaedalusParser.FunctionCallContext,
            c_info_instance: Union[CInfo, None],
            data_sniffer,
            line: str):

        speaker, listener, name = ctx.expression()
        self.speaker = speaker.getText().upper()
        self.listener = listener.getText().upper()
        self.name = name.getText().strip('"')

        if self.speaker == AIOutput.OTHER:
            c_npc_instance = data_sniffer.PLAYER_NPC
        else:
            if c_info_instance and c_info_instance.npc:
                c_npc_instance = c_info_instance.npc
            else:
                c_npc_instance = data_sniffer.UNKNOWN_NPC

        self.c_info_instance = c_info_instance
        self.c_npc_instance = c_npc_instance
        c_npc_instance.ai_outputs.append(self)

        parts = line.split('//')
        assert len(parts) == 2
        self.comment = parts[-1].strip()

    def serialize(self):
        return {
            'wav_filename': self.name,
            'text': self.comment,
        }
