import maps
class generate_bill:
	'''
	input: name,address,priority,list of items
	items is a list of list => [[item,price]]
	'''
	def __init__(self,items,name,address,priority):
		self.name = name
		self.address = address
		self.items = items
		self.priority = priority

	def generate_discount(self,total):
		if self.priority == 'high':
			discount = total*0.1      #10%discount applied
		elif self.priority == 'medium' or self.priority == 'low':
			discount = 0
		return discount

	def generate_amount(self):
		total = 0
		for i in self.items:
			total+=i[1]
		discount = total
		discount = self.generate_discount(discount)
		total -= discount
		return total,discount

	def print_bill(self):
		print('Name:            \t',self.name)
		print('Delivery Address:\t',self.address)
		print('Item             \tAmount')
		for i in self.items:
			print(i[0],"            ",i[1])
		total,discount = self.generate_amount()
		print("Total Amount:    \t",total)
		print('Discount Applied:\t',discount)

	def delivery_time(self):
		time = 15 + int((maps.calculate_dist('kandivali,India',self.address)).split(" ")[0])
		print('Your food will be delivered to you in ',time," minutes")
