# Generated from Daedalus.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DaedalusParser import DaedalusParser
else:
    from DaedalusParser import DaedalusParser

# This class defines a complete generic visitor for a parse tree produced by DaedalusParser.

class DaedalusVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DaedalusParser#daedalusFile.
    def visitDaedalusFile(self, ctx:DaedalusParser.DaedalusFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#blockDef.
    def visitBlockDef(self, ctx:DaedalusParser.BlockDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#inlineDef.
    def visitInlineDef(self, ctx:DaedalusParser.InlineDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#externFunctionDecl.
    def visitExternFunctionDecl(self, ctx:DaedalusParser.ExternFunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#functionDef.
    def visitFunctionDef(self, ctx:DaedalusParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#constDef.
    def visitConstDef(self, ctx:DaedalusParser.ConstDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#classDef.
    def visitClassDef(self, ctx:DaedalusParser.ClassDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#prototypeDef.
    def visitPrototypeDef(self, ctx:DaedalusParser.PrototypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#instanceDef.
    def visitInstanceDef(self, ctx:DaedalusParser.InstanceDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#instanceDecl.
    def visitInstanceDecl(self, ctx:DaedalusParser.InstanceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#varDecl.
    def visitVarDecl(self, ctx:DaedalusParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#constArrayDef.
    def visitConstArrayDef(self, ctx:DaedalusParser.ConstArrayDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#constArrayAssignment.
    def visitConstArrayAssignment(self, ctx:DaedalusParser.ConstArrayAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#constValueDef.
    def visitConstValueDef(self, ctx:DaedalusParser.ConstValueDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#constValueAssignment.
    def visitConstValueAssignment(self, ctx:DaedalusParser.ConstValueAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#varArrayDecl.
    def visitVarArrayDecl(self, ctx:DaedalusParser.VarArrayDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#varArrayAssignment.
    def visitVarArrayAssignment(self, ctx:DaedalusParser.VarArrayAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#varValueDecl.
    def visitVarValueDecl(self, ctx:DaedalusParser.VarValueDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#varValueAssignment.
    def visitVarValueAssignment(self, ctx:DaedalusParser.VarValueAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#parameterList.
    def visitParameterList(self, ctx:DaedalusParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#parameterDecl.
    def visitParameterDecl(self, ctx:DaedalusParser.ParameterDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#statementBlock.
    def visitStatementBlock(self, ctx:DaedalusParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#statement.
    def visitStatement(self, ctx:DaedalusParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#functionCall.
    def visitFunctionCall(self, ctx:DaedalusParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#assignment.
    def visitAssignment(self, ctx:DaedalusParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#elseBlock.
    def visitElseBlock(self, ctx:DaedalusParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#elseIfBlock.
    def visitElseIfBlock(self, ctx:DaedalusParser.ElseIfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#ifBlock.
    def visitIfBlock(self, ctx:DaedalusParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#ifBlockStatement.
    def visitIfBlockStatement(self, ctx:DaedalusParser.IfBlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#returnStatement.
    def visitReturnStatement(self, ctx:DaedalusParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#whileStatement.
    def visitWhileStatement(self, ctx:DaedalusParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#breakStatement.
    def visitBreakStatement(self, ctx:DaedalusParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#continueStatement.
    def visitContinueStatement(self, ctx:DaedalusParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#bitMoveExpression.
    def visitBitMoveExpression(self, ctx:DaedalusParser.BitMoveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#valueExpression.
    def visitValueExpression(self, ctx:DaedalusParser.ValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#eqExpression.
    def visitEqExpression(self, ctx:DaedalusParser.EqExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#addExpression.
    def visitAddExpression(self, ctx:DaedalusParser.AddExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#compExpression.
    def visitCompExpression(self, ctx:DaedalusParser.CompExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#logOrExpression.
    def visitLogOrExpression(self, ctx:DaedalusParser.LogOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#binAndExpression.
    def visitBinAndExpression(self, ctx:DaedalusParser.BinAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#binOrExpression.
    def visitBinOrExpression(self, ctx:DaedalusParser.BinOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#multExpression.
    def visitMultExpression(self, ctx:DaedalusParser.MultExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#bracketExpression.
    def visitBracketExpression(self, ctx:DaedalusParser.BracketExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#unaryExpression.
    def visitUnaryExpression(self, ctx:DaedalusParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#logAndExpression.
    def visitLogAndExpression(self, ctx:DaedalusParser.LogAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#arrayIndex.
    def visitArrayIndex(self, ctx:DaedalusParser.ArrayIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#arraySize.
    def visitArraySize(self, ctx:DaedalusParser.ArraySizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#integerLiteralValue.
    def visitIntegerLiteralValue(self, ctx:DaedalusParser.IntegerLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#floatLiteralValue.
    def visitFloatLiteralValue(self, ctx:DaedalusParser.FloatLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#stringLiteralValue.
    def visitStringLiteralValue(self, ctx:DaedalusParser.StringLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#nullLiteralValue.
    def visitNullLiteralValue(self, ctx:DaedalusParser.NullLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#noFuncLiteralValue.
    def visitNoFuncLiteralValue(self, ctx:DaedalusParser.NoFuncLiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#functionCallValue.
    def visitFunctionCallValue(self, ctx:DaedalusParser.FunctionCallValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#referenceValue.
    def visitReferenceValue(self, ctx:DaedalusParser.ReferenceValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#referenceAtom.
    def visitReferenceAtom(self, ctx:DaedalusParser.ReferenceAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#reference.
    def visitReference(self, ctx:DaedalusParser.ReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#dataType.
    def visitDataType(self, ctx:DaedalusParser.DataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#nameNode.
    def visitNameNode(self, ctx:DaedalusParser.NameNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#parentReference.
    def visitParentReference(self, ctx:DaedalusParser.ParentReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:DaedalusParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#addOperator.
    def visitAddOperator(self, ctx:DaedalusParser.AddOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#bitMoveOperator.
    def visitBitMoveOperator(self, ctx:DaedalusParser.BitMoveOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#compOperator.
    def visitCompOperator(self, ctx:DaedalusParser.CompOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#eqOperator.
    def visitEqOperator(self, ctx:DaedalusParser.EqOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#unaryOperator.
    def visitUnaryOperator(self, ctx:DaedalusParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#multOperator.
    def visitMultOperator(self, ctx:DaedalusParser.MultOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#binAndOperator.
    def visitBinAndOperator(self, ctx:DaedalusParser.BinAndOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#binOrOperator.
    def visitBinOrOperator(self, ctx:DaedalusParser.BinOrOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#logAndOperator.
    def visitLogAndOperator(self, ctx:DaedalusParser.LogAndOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaedalusParser#logOrOperator.
    def visitLogOrOperator(self, ctx:DaedalusParser.LogOrOperatorContext):
        return self.visitChildren(ctx)



del DaedalusParser