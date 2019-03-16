import string
import yaml
import random
import ispositive

class Parser:
	def __init__(self):
		self.curr_input = ''
		self.universals = ['cancel', 'top', 'hot', 'hungry', 'help', 'about', 'change', 'start over', 'menu', 'thirsty']
		self.curse_words = None
		self.annoyance = 5
		self.messages = yaml.load(open('./datasets/welcome.yml'))

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
			self.lower_case()
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

	def universal_parse(self, words):
		'''
		"universals" are : 'cancel', 'top', 'hot', 'hungry', 'help', 'about', '@change', '@start over', '@menu', 'thirsty'
		"words" are: list of user entered words
		'''
		key = [word for word in words if (word in self.universals)]
		key = key[0]
		if key == 'cancel':
			cancel_resp = self.messages['cancel']
			return random.choice(cancel_resp)
		elif key == 'top' or key == 'hot' or key == 'hungry':
			# Trending food method will come here
			pass
		elif key == 'thirsty':
			# Trending beverages will come here
			pass
		elif key == 'help' or key == 'about':
			help_resp = self.messages['help']
			self.annoyance -= 2
			return random.choice(help_resp)

	def curse_parse(self):
		curse_resp = self.messages['curse']
		self.annoyance -= 4
		return random.choice(curse_resp)

	def level_one_parse(self):
		words = self.curr_input.split()
		# GENERAL PURPOSE TEXT WILL BE CHECKED BEFORE ALL THE BELOW CODE!!!
		if any(word in words for word in self.curse_words):
			print(self.curse_parse())
		elif any(word in words for word in self.universals):
			print(self.universal_parse(words))
		else:
			pos_check = ispositive.is_positive(self.curr_input)
			print(pos_check)
			if pos_check == False:
				help_resp = self.messages['help']
				print(random.choice(help_resp))
			elif pos_check == True:
				self.order_parse()

	def order_parse(self):
		pass

if __name__ == '__main__':
	o = Parser()
	o.user_input()
	o.load_curse()
	o.level_one_parse()