class Expression(object):
	def evaluate(self): # Aca se implementa cada tipo de expresion.
		raise NotImplementedError

class Number(Expression):
	def __init__(self, value):
		self.value = value
	def evaluate(self):
		return self.value

class BinaryOperation(Expression):
	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator

	def evaluate(self):
		res_l = self.left.evaluate()
		res_r = self.right.evaluate()
		return self.operator(res_l, res_r)

from operator import add, mul
from expressions import BinaryOperation, Number

def p_expression_plus(expr):
	'expression : expression PLUS term'
	expr[0] = BinaryOperation(expr[1], expr[3], add)

def p_term_times(expr):
	'term : term TIMES factor'
	expr[0] = BinaryOperation(expr[1], expr[3], mul)

def p_factor_number(expr):
	'factor : NUMBER'
	expressions[0] = Number(expr[1])

text = "(14 + 6) * 2"
lexer = lex(module=lexer_rules) parser = yacc(module=parser_rules)
expression = parser.parse(text, lexer)
result = expression.evaluate() print result
>> 40