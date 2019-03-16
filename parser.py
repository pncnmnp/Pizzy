import string
import yaml
import random
import ispositive

'''
TODO: 
>> connect change.py for change menu ( add menu changes to change.py )
>> add trending food items using trending.py
>> increase the welcome.yml library
>> bring in botprofile.yml, food.yml, greetings.yml, humor.yml [ done ]
>> ADD the place order implementation
'''

class Parser:
	def __init__(self):
		self.curr_input = ''
		self.universals = ['cancel', 'top', 'hot', 'hungry', 'help', 'about', 'change', 'start over', 'menu', 'thirsty']
		self.curse_words = None
		self.annoyance = 5
		self.generic_dict = dict()
		self.messages = yaml.load(open('./datasets/welcome.yml'))
		self.load_curse()
		self.generic_responses()

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

	def generic_responses(self):
		greet = yaml.load(open('./datasets/greetings.yml'))['conversations']
		humor = yaml.load(open('./datasets/humor.yml'))['conversations']
		food = yaml.load(open('./datasets/food.yml'))['conversations']
		botprofile = yaml.load(open('./datasets/botprofile.yml'))['conversations']
		self.generic_resp_store(greet)
		self.generic_resp_store(humor)
		self.generic_resp_store(food)
		self.generic_resp_store(botprofile)

	def generic_resp_store(self, conversations):
		for conv in conversations:
			conv[0] = self.lower_case(inp=True, sent=conv[0])
			conv[0] = self.remove_punct(inp=True, sent=conv[0])
			if conv[0] in self.generic_dict:
				self.generic_dict[conv[0]].append(conv[1])
			else:
				self.generic_dict[conv[0]] = [conv[1]]

	def curse_parse(self):
		curse_resp = self.messages['curse']
		self.annoyance -= 4
		return random.choice(curse_resp)

	def level_one_parse(self):
		words = self.curr_input.split()
		# GENERAL PURPOSE TEXT WILL BE CHECKED BEFORE ALL THE BELOW CODE!!!
		if self.curr_input in self.generic_dict:
			print(random.choice((self.generic_dict[self.curr_input])))
		elif any(word in words for word in self.curse_words):
			print(self.curse_parse())
		elif any(word in words for word in self.universals):
			print(self.universal_parse(words))
		else:
			pos_check = ispositive.is_positive(self.curr_input)
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
	o.level_one_parse()