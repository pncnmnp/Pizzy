import sqlite3
import yaml
import random
from hashlib import sha1
import ispositive # To check if user is done placing the order
from generate_bill import generate_bill
from parser import Parser
import priority

'''
TODO:
>> Get user priority in a static variable
>> Update the database with all the values
>> Customer priority implementation
>> Customer Annoyance Level and Customer Support implementation
>> Order Menu display with keeping Note of current category [ done ]
>> Time taken implementation [ done ]
>> Bill display [ done ]
'''

class Customer:
	def __init__(self):
		self.name = '' #
		self.priority = 'medium'
		self.order_worth = 0 #
		self.referral_bonus_check = None
		self.referral_code = None
		self.phoneNo = '' #
		self.address = '' #
		self.drop_location = '' #
		self.curr_order_count = 0 #
		self.orders = [] #
		self.r_bill = 0 #
		self.givenDiscount = False #
		self.messages = yaml.load(open('./datasets/welcome.yml'))
		self.last = '' #
		self.newUser = False
		self.flag = False # becomes True when it is time to store the order
		self.conn = sqlite3.connect('./customers.db')
		self.c = self.conn.cursor()
		self.no_of_orders = 1

	def get_address_ref_code(self):
		address_resp = self.messages['address']
		self.address = input(random.choice(address_resp)+'\n>> ')
		referral_resp = self.messages['referral-to-avail']
		referral_code = input(random.choice(referral_resp)+'\n>> ')
		ref_check = self.c.execute("SELECT uid, referral_bonus_ck FROM customers WHERE referral_code=?", (referral_code,)).fetchone()
		if ref_check == None:
			ref_invalid_resp = self.messages['referral-invalid']
			print(random.choice(ref_invalid_resp))
		elif ref_check[0] != None:
			if ref_check[1] == 0:
				ref_repeat = self.messages['referral-repeat']
			elif ref_check[1] == 1:
				ref_repeat = self.messages['referral-true']
				print(random.choice(ref_repeat))
				self.r_bill -= 100
				self.givenDiscount = True
				self.c.execute("UPDATE customers SET referral_bonus_ck=? WHERE uid=?", (0, ref_check[0]))
				self.conn.commit()

	def referral_bonus_ck(self):
		ref_check = self.c.execute("SELECT referral_bonus_ck FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
		if ref_check == 0:
			ref_repeat = self.messages['referral']
			print(random.choice(ref_repeat))
			self.r_bill -= 100
			self.c.execute("UPDATE customers SET referral_bonus_ck=? WHERE ph_no=?", (None, self.phoneNo))
			self.conn.commit()

	def checkPhoneNo(self):
		self.phoneNo = self.getNo()
		count = self.c.execute("SELECT COUNT(ph_no) FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
		if count == 0:
			self.newUser = True
			self.get_address_ref_code()
		elif count > 0:
			prior_resp = self.messages['prior']
			self.address = self.c.execute("SELECT address FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
			print(random.choice(prior_resp))
			self.referral_bonus_ck()

	def init_db(self):
		if self.flag == False:
			self.c.execute('''CREATE TABLE IF NOT EXISTS customers
				(uid INTEGER PRIMARY_KEY,
				name TEXT,
				ph_no TEXT,
				address TEXT,
				no_of_orders INTEGER,
				order_worth INTEGER,
				discount_worth INTEGER,
				priority TEXT,
				referral_bonus_ck BIT,
				referral_code INTEGER)''')

	def user_input(self, command_line=True):
		if command_line == True:
			self.last = input('>> ')
		else:
			pass

	def getNo(self):
		no_str = 'Enter your phone no: '
		print(no_str)
		self.user_input()
		hashed = sha1(self.last.encode()).hexdigest()[:10]
		return hashed

	def getName(self):
		name_str = 'Enter your name: '
		print(name_str)
		self.user_input()
		self.name = self.last
		resp_str = 'Welcome '+self.name+'!'
		print(resp_str)

	def welcome_greeting(self):
		welc_resp = self.messages['conversations']
		print(random.choice(welc_resp))
		return random.choice(welc_resp)

	def place_order(self):
		menu_resp = self.messages['menu']
		print(random.choice(menu_resp))
		parser = Parser()
		order_count = 0
		done = False
		parser.user_input()
		while done == False:
			parser.level_one_parse()
			if len(parser.orders) > order_count:
				order_count = len(parser.orders)
				check = input("Do you want something else\n>> ")
				if ispositive.is_positive(check) == False:
					done = True
					self.orders = parser.orders
					self.curr_order_count = order_count
				else:
					check = parser.lower_case(inp=True, sent=check)
					check = parser.remove_punct(inp=True, sent=check)
					parser.curr_input = check
			else:
				parser.user_input()

	def getPrice(self):
		pi = yaml.load(open('./datasets/pizzas.yml'))
		si = yaml.load(open('./datasets/sides.yml'))
		be = yaml.load(open('./datasets/beverages.yml'))
		pizzas, sides, beves = {}, {}, {}
		for p in pi:
			pizzas[p.lower().strip()] = {'price': pi[p]['price']}
		for s in si:
			sides[s.lower().strip()] = {'price': si[s]['price']}
		for b in be:
			beves[b.lower().strip()] = {'price': be[b]['price']}
		total = 0
		amount = 0
		index = 0
		for order in self.orders:
			amount = 0
			for quantity in range(int(order[1])):
				if order[0] in pizzas:
					total += pizzas[order[0]]['price']
					amount += pizzas[order[0]]['price']
				elif order[0] in sides:
					total += sides[order[0]]['price']
					amount += sides[order[0]]['price']
				elif order[0] in beves:
					total += beves[order[0]]['price']
					amount += beves[order[0]]['price']
			self.orders[index] = [order[0], amount]
			index += 1
		self.order_worth = total

	def bill_statement(self):
		self.getPrice()
		# check for priority
		if self.newUser:
			self.priority = 'medium'
		else:
			self.no_of_orders += self.c.execute("SELECT no_of_orders FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
			order_worth = self.c.execute("SELECT order_worth FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
			self.priority = priority.predict_user_priority([[self.no_of_orders, self.order_worth+order_worth, 150]])
			self.order_worth += order_worth

		if self.priority == 'medium':
			self.referral_code = random.randint(100000,1000000)
			self.referral_bonus_check = 1
			print("You have received referral code: "+self.referral_code", which on passing on to your friends can avail you Rs.100 off on your next Pizza!")
		bill = generate_bill(items=self.orders, name=self.name, address=self.address, priority=self.priority)
		bill.print_bill()

	def execution_order(self):
		self.init_db()
		self.getName()
		self.checkPhoneNo()
		self.welcome_greeting()
		self.place_order()
		self.bill_statement()

if __name__ == '__main__':
	o = Customer()
	o.execution_order()