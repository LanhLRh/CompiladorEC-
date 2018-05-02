memFunc = 0

def retrieveValueAt(address):
	
	if not isinstance(address,basestring):
		return address

	if address[0]=='(':
		address = int(address[1:len(address)-1])
	else:
		for func in dir_func:
			if address in dir_func.get(func).get('scope').keys():
				address = dir_func.get(func).get('scope').get(address).get('address')

	if not address in memoria.keys():
		print(str(address)+' '+str(currentQuad))
		print('Variable no inicializada')
		sys.exit()
	
	return memoria.get(address)

def maqVirtual():
	
	global currentQuad

	while currentQuad < contQuads:
		executeQuad= quad[currentQuad]
		operation = executeQuad.get('operator')

		if operation == 'GOTO':

			if currentQuad == 0:

				global memFunc
				dicTemp = {}
				ogMem = memFunc
				
				for var in dir_func['MAIN']['scope']:
					dir_func['MAIN']['scope'][var]['address'] = memFunc
					dicTemp[var] = memFunc
					memoria[memFunc] = 0
					memFunc = memFunc + 1

					# if len(dir_func['MAIN']['scope'][var]['dim']) > 0:
					# 	cant = 1
					# 	for i in dir_func['MAIN']['scope'][var]['dim']:
					# 		cant = cant * i.get('Lim')
					# 	for i in range(cant-1):
					# 		memoria[memFunc] = 0
					# 		memFunc = memFunc + 1

				memFunc = ogMem + 1000
				add_pFunc('MAIN')
				add_pVar(dicTemp)

			currentQuad = executeQuad.get('result')

		elif operation == 'GOTOF':

			mem = executeQuad.get('leftOperand')
			val = retrieveValueAt(mem)

			if not val:
				currentQuad = executeQuad.get('result')
			else:
				currentQuad = currentQuad + 1

		elif operation == 'GOSUB':
			func = executeQuad.get('leftOperand')
			dicVars = top_pVar()

			for var in dicVars:
				dir_func[func]['scope'][var]['address'] = dicVars.get(var)

			add_pilaReturn(currentQuad + 1)
			currentQuad = dir_func[func].get('quadStart')

		elif operation == 'ERA':

			global memFunc

			right = executeQuad.get('rightOperand')
			
			dicTemp = {}
			ogMem = memFunc
				
			for var in dir_func[right]['scope']:
				dicTemp[var] = memFunc
				memoria[memFunc] = 0
				memFunc = memFunc + 1

				# if len(dir_func[right]['scope'][var]['dim']) > 0:
				# 	cant = 1
				# 	for i in dir_func[right]['scope'][var]['dim']:
				# 		cant = cant * i.get('Lim')
				# 	for i in range(cant-1):
				# 		memoria[memFunc] = 0
				# 		memFunc = memFunc + 1

			memFunc = ogMem + 1000
			add_pFunc(right)
			add_pVar(dicTemp)
			currentQuad = currentQuad + 1

		elif operation == 'PARAM':

			left = retrieveValueAt(executeQuad.get('leftOperand'))
			func, var = executeQuad.get('result').split(":")

			dicVars = top_pVar()
			memoria[dicVars.get(var)] = left

			currentQuad = currentQuad + 1

		elif operation == 'ENDPROC':

			pop_pVar()
			pop_pFunc()

			dicVars = top_pVar()
			func = top_pFunc()

			if func != 'MAIN':
				for var in dicVars:
					dir_func[func]['scope'][var]['address'] = dicVars.get(var)
			
			currentQuad = pop_pilaReturn()


		elif operation == 'RET':

			right = retrieveValueAt(executeQuad.get('rightOperand'))
			memoria[dir_func['global']['scope'][top_pFunc()].get('address')] = right

			currentQuad = currentQuad + 1 

		elif operation == 'VER':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)

			if not(leftval >= 1 and leftval <= rightval):
				print('Error el indice se sale del limite')
				sys.exit()
			currentQuad = currentQuad + 1

		elif operation == 'DIRBASE':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			cosas= right.split('/')
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval + dir_func[cosas[0]]['scope'][cosas[1]].get('address')

			currentQuad = currentQuad + 1

		elif operation == 'KAMEF':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			tur.forward(float(rightval))
			currentQuad = currentQuad + 1

		elif operation == 'KAMEB':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			tur.backward(float(rightval))
			currentQuad = currentQuad + 1

		elif operation == 'KAMER':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			tur.left(float(rightval))
			currentQuad = currentQuad + 1

		elif operation == 'CIRCLE':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			tur.speed('slowest')
			tur.speed(1)
			tur.right(90)
			tur.penup()
			tur.forward(float(rightval))
			tur.left(90)
			tur.pendown()
			tur.circle(rightval)
			tur.penup()
			tur.left(90)
			tur.forward(float(rightval))
			tur.right(90)
			tur.pendown()
			currentQuad = currentQuad + 1

		elif operation == 'SQUARE':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)

			tur.penup()
			tur.right(90)
			tur.forward(float(rightval)/2)
			tur.left(90)
			tur.pendown()
			tur.forward(float(rightval)/2)
			tur.left(90)
			tur.forward(float(rightval))
			tur.left(90)
			tur.forward(float(rightval))
			tur.left(90)
			tur.forward(float(rightval))
			tur.left(90)
			tur.forward(float(rightval)/2)
			tur.penup()
			tur.left(90)
			tur.forward(float(rightval)/2)
			tur.right(90)
			tur.pendown()
			currentQuad = currentQuad + 1

		elif operation == 'SIZE':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			tur.pensize(rightval*5)
			currentQuad = currentQuad + 1

		elif operation == 'DRAW':
			right = executeQuad.get('result')
			rightval = retrieveValueAt(right)

			if rightval:
				tur.pendown()
			else:
				tur.penup()
			currentQuad = currentQuad + 1

		elif operation == 'COLOR':
			right = executeQuad.get('result')
			tur.color(right)

			currentQuad = currentQuad + 1	


		elif operation == '+':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval + rightval
			currentQuad = currentQuad + 1

		elif operation == '-':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval - rightval
			currentQuad = currentQuad + 1

		elif operation == '*':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval * rightval
			currentQuad = currentQuad + 1

		elif operation == '/':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval / rightval 
			currentQuad = currentQuad + 1

		elif operation == '%':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval % rightval 
			currentQuad = currentQuad + 1

		elif operation == '=':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = rightval
			currentQuad = currentQuad + 1

		elif operation == '<':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval < rightval 
			currentQuad = currentQuad + 1

		elif operation == '<=':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval <= rightval
			currentQuad = currentQuad + 1

		elif operation == '>':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval > rightval 
			currentQuad = currentQuad + 1

		elif operation == '>=':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval >= rightval 
			currentQuad = currentQuad + 1

		elif operation == '==':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval == rightval 
			currentQuad = currentQuad + 1

		elif operation == '&':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval and rightval 
			currentQuad = currentQuad + 1

		elif operation == '|':
			left = executeQuad.get('leftOperand')
			right = executeQuad.get('rightOperand')
			leftval = retrieveValueAt(left)
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = leftval or rightval 
			currentQuad = currentQuad + 1

		elif operation == '!':
			right = executeQuad.get('rightOperand')
			rightval = retrieveValueAt(right)
			result = translateString(executeQuad.get('result'))
			memoria[result] = not rightval 
			currentQuad = currentQuad + 1