import sqlite3
import yaml
import random
from hashlib import sha1

class Customer:
	def __init__(self):
		self.name = ''
		self.phoneNo = ''
		self.address = ''
		self.drop_location = ''
		self.orders = []
		self.bill = 0
		self.givenDiscount = False
		self.messages = yaml.load(open('./datasets/welcome.yml'))
		self.last = ''
		self.newUser = False
		self.flag = False # becomes True when it is time to store the order
		self.conn = sqlite3.connect('./customers.db')
		self.c = self.conn.cursor()

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
				self.bill -= 100
				self.givenDiscount = True
				self.c.execute("UPDATE customers SET referral_bonus_ck=? WHERE uid=?", (0, ref_check[0]))
				self.conn.commit()

	def referral_bonus_ck(self):
		ref_check = self.c.execute("SELECT referral_bonus_ck FROM customers WHERE ph_no=?", (self.phoneNo,)).fetchone()[0]
		if ref_check == 0:
			ref_repeat = self.messages['referral']
			print(random.choice(ref_repeat))
			self.bill -= 100
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

	def execution_order(self):
		self.init_db()
		self.getName()
		self.checkPhoneNo()
		self.welcome_greeting()

if __name__ == '__main__':
	o = Customer()
	o.execution_order()