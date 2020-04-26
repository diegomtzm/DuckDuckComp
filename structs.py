# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp
# Definition of data structures used in the project

class Stack:
	def __init__(self):
		self.st = []

	def push(self, e):
		return self.st.append(e)

	def pop(self):
		return self.st.pop()

	def size(self):
		return len(self.st)

	def top(self):
		return self.st[-1]

	def empty(self):
		return len(self.st) == 0

	def get(self):
		return self.st


