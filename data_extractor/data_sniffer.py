import antlr4

import re
import sys

from data_extractor.daedalus_classes import CNpc, CInfo, AIOutput
from data_extractor.grammar.DaedalusLexer import DaedalusLexer
from data_extractor.grammar.DaedalusParser import DaedalusParser
from data_extractor.grammar.DaedalusVisitor import DaedalusVisitor
from data_extractor.syntax_error_listener import SyntaxErrorListener


class DataSniffer:
    PLAYER_NPC = CNpc(identifier=None, name="Player")
    UNKNOWN_NPC = CNpc(identifier=None, name="Unknown")

    def __init__(self):
        self.id_2_npc = {
            "PLAYER": DataSniffer.PLAYER_NPC,
            "UNKNOWN": DataSniffer.UNKNOWN_NPC,
        }
        self.id_2_info = {}

    def update_data(self, npcs, infos):
        for npc in npcs:
            self.id_2_npc[npc.identifier] = npc
        for info in infos:
            self.id_2_info[info.identifier] = info

    def sniff(self, file_path):
        with open(file_path, encoding='windows-1250') as file:
            content = file.read()
            lines = content.split('\n')

        input_stream = antlr4.InputStream(content)
        lexer = DaedalusLexer(input_stream)
        token_stream = antlr4.CommonTokenStream(lexer)
        parser = DaedalusParser(token_stream)

        listener = SyntaxErrorListener()
        parser.addErrorListener(listener)
        parse_tree = parser.daedalusFile()

        if listener.errors_count:
            msg = f"{listener.errors_count} syntax error generated"
            print(msg, file=sys.stderr)
            return

        init_visitor = InitializationVisitor()
        init_visitor.visit(parse_tree)
        self.update_data(init_visitor.npcs, init_visitor.infos)

        sniffing_visitor = DataSniffingVisitor(lines, self.id_2_npc, self.id_2_info)
        sniffing_visitor.visit(parse_tree)

    def get_data(self):
        return [
            npc.serialize()
            for npc in self.id_2_npc.values()
            if npc.ai_outputs
        ]


class InitializationVisitor(DaedalusVisitor):
    C_INFO = "C_INFO"
    C_NPC = "C_NPC"
    NPC_DEFAULT = "NPC_DEFAULT"
    NPC_TYPES = (C_NPC, NPC_DEFAULT)
    INSTANCE_CONTEXTS = (DaedalusParser.InstanceDefContext, DaedalusParser.InstanceDeclContext)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.npcs = []
        self.infos = []

    def _add_instance(self, identifier, parent):
        if parent == self.C_INFO:
            self.infos.append(CInfo(identifier))
        elif parent in self.NPC_TYPES:
            self.npcs.append(CNpc(identifier))

    def visitInlineDef(self, ctx: DaedalusParser.InlineDefContext):
        child_ctx = ctx.instanceDecl()
        if child_ctx:
            self.visitInstanceDecl(child_ctx)

    def visitBlockDef(self, ctx: DaedalusParser.BlockDefContext):
        child_ctx = ctx.instanceDef()
        if child_ctx:
            self.visitInstanceDef(child_ctx)

    def visitInstanceDef(self, ctx: DaedalusParser.InstanceDefContext):
        parent_ctx = ctx.parentReference()
        parent_identifier = parent_ctx.getText().upper()
        identifier = ctx.nameNode().getText().upper()
        self._add_instance(identifier, parent_identifier)

    def visitInstanceDecl(self, ctx: DaedalusParser.InstanceDeclContext):
        parent_ctx = ctx.parentReference()
        parent_identifier = parent_ctx.getText().upper()
        for name_node in ctx.nameNode():
            identifier = name_node.getText().upper()
            self._add_instance(identifier, parent_identifier)


class DataSniffingVisitor(DaedalusVisitor):
    C_INFO = "C_INFO"
    C_NPC = "C_NPC"
    NPC_DEFAULT = "NPC_DEFAULT"
    NPC_TYPES = (C_NPC, NPC_DEFAULT)
    NPC = "NPC"
    INFORMATION = "INFORMATION"
    NAME = "NAME"
    AI_OUTPUT = "AI_OUTPUT"
    INFO_ADDCHOICE = "INFO_ADDCHOICE"
    SPECIAL_CHAR_PATTERN = re.compile('[.()[\\]]')


    func_2_info = {}

    def __init__(self, lines, id_2_npc, id_2_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lines = lines
        self.id_2_npc = id_2_npc
        self.id_2_info = id_2_info

        self.npc_active = None
        self.info_active = None
        self.func_active = None

    def visitInstanceDef(self, ctx: DaedalusParser.InstanceDefContext):
        parent_ctx = ctx.parentReference()
        parent_identifier = parent_ctx.getText().upper()
        identifier = ctx.nameNode().getText().upper()

        if parent_identifier == self.C_INFO:
            self.info_active = self.id_2_info[identifier]

        elif parent_identifier in self.NPC_TYPES:
            self.npc_active = self.id_2_npc[identifier]

        super().visitInstanceDef(ctx)

        self.npc_active = None
        self.info_active = None

    def visitAssignment(self, ctx: DaedalusParser.AssignmentContext):
        reference_identifier = ctx.reference().getText().upper()

        rvalue = ctx.expression().getText().strip('"')
        if re.search(self.SPECIAL_CHAR_PATTERN, rvalue):
            return

        if self.npc_active:
            if reference_identifier == self.NAME:
                self.npc_active.name = rvalue

        elif self.info_active:
            rvalue = rvalue.upper()
            if reference_identifier == self.NPC:
                self.info_active.npc = self.id_2_npc.get(rvalue, DataSniffer.UNKNOWN_NPC)
            elif reference_identifier == self.INFORMATION:
                self.func_2_info[rvalue] = self.info_active

    def visitFunctionDef(self, ctx: DaedalusParser.FunctionDefContext):
        self.func_active = ctx.nameNode().getText().upper()
        super().visitFunctionDef(ctx)
        self.func_active = None

    def visitFunctionCall(self, ctx: DaedalusParser.FunctionCallContext):
        identifier = ctx.nameNode().getText().upper()
        if identifier == self.AI_OUTPUT:
            line = self.lines[ctx.stop.line-1]
            c_info_instance = self.func_2_info.get(self.func_active)
            AIOutput(ctx, c_info_instance, DataSniffer, line)

        elif identifier == self.INFO_ADDCHOICE:
            _, _, func_ref_ctx = ctx.expression()
            function_identifier = func_ref_ctx.getText().upper()
            c_info_instance = self.func_2_info.get(self.func_active)
            self.func_2_info[function_identifier] = c_info_instance
