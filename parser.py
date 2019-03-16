import string

class Parser:
	def __init__(self):
		self.curr_input = ''
		self.universals = ['cancel', 'top', 'hot', 'hungry', 'help', 'about', 'change', 'start over', 'menu', 'thirsty']
		self.curse_words = None

	def load_curse(self):
		with open('./datasets/curse_words.txt') as file:
			self.curse_words = file.readlines()
		index = 0
		for curse in self.curse_words:
			curse = self.lower_case(inp=True, sent=curse)
			curse = self.remove_punct(inp=True, sent=curse)
			self.curse_words[index] = curse
			index += 1

	def user_input(self, command_line=True):
		if command_line == True:
			self.curr_input = input('>> ')
			self.remove_punct()
		else:
			pass

	def remove_punct(self, sent='', inp=False):
		remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
		if inp == False:
			self.curr_input = self.curr_input.translate(remove_punct_dict)
		elif inp == True:
			return sent.translate(remove_punct_dict)

	def lower_case(self, sent='', inp=False):
		if inp == False:
			self.curr_input = self.curr_input.strip().lower()
		elif inp == True:
			return sent.strip().lower()

	def level_one_parse(self):
		words = self.curr_input()
		pass