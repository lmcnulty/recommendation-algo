#!/usr/bin/env python3

import csv
from random import randint

compatability = {}

with open("data/CouponCompatibilitywithParticPref.csv") as f:
	reader = csv.reader(f)
	for row in reader:
		compatability[row[0]] = row[2:-1]

class Coupon:
	def __init__(self, csv_row):
		self.number = int(csv_row[0])
		self.category = int(csv_row[1])
		self.subgroup = int(csv_row[2])
		self.name = csv_row[3]
		self.compatability = [
			bool(int(x)) for x in
			compatability[csv_row[3]]
		] if csv_row[3] in compatability else [1] * 16
	def __str__(self):
		return str(self.number) + " " + self.name
	def is_compatible(self, preferences):
		for i, e in enumerate(self.compatability):
			if preferences[i] and not e: 
				return False
		return True

def ex(s): print("\n" + s + "\n")

def out_list(l):
	for i in range(5 if len(l) > 5 else len(l)):
		print(" ".join(l[i]))
	if len(l) > 5:
		print("...")

def get_stars(upc):
	# TODO: This
	return randint(0, 3)

def get_user_preferences(id):
	# TODO: Get the correct user preferences based on ID
	with open ("data/subject_description.csv") as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == "Subj088":
				return [bool(int(x)) for x in row[1:-1]]

def get_user_purchases(id):
	with open("data/appendeseptmay.csv") as append:
		reader = csv.reader(append)
		return [row for row in reader if row[0] == id]


loyalty_id = "43610000389"
loyalty_id = "43610003420"


# Selection all the products purchased by the subject in the daily download. (755)
purchases = get_user_purchases(loyalty_id)

ex("Get the subject purchases")
out_list(purchases)


# From this list, keep the products with 0 or 1 star 
purchases = [row for row in purchases if get_stars(row[3]) < 2]

ex("From this list, keep the products with 0 or 1 star")
out_list(purchases)

categories = set()

# which has a brand(?) and a sub categories known.
with open("data/CouponedUPCS.csv") as couponedUPCS:
	reader = csv.reader(couponedUPCS)
	categoried = []
	for row in reader:
		for purchase in purchases:
			if row[0] == purchase[3]:
				categories.add(row[-1])

triggers = []
coupons = []

# Select the coupon from the same categories of these products.
with open ("data/CouponCodebookSASIMPEDIT.csv") as f:
	reader = csv.reader(f)
	for row in reader:
		if row[0] == "CouponNumber": continue
		coupon = Coupon(row)
		coupons.append(coupon)
		if row[3] in categories:
			triggers.append(Coupon(row))


preferences = get_user_preferences(loyalty_id)

triggers = [
	coupon for coupon in triggers if coupon.is_compatible(preferences)
]

ex("Keep only the coupon which can be use by the subject")
for coupon in triggers: print(coupon)

triggers = coupons

def get_lift(loyalty_id):
	# TODO: Return a dictionary mapping food groups to differences
	# between desired GQPI expenditure and actual for given subject.
	return {}

def coupon_lift(lift, coupon):
	# TODO: Return a single numeric value for the amount that the
	# coupon will improve the gqpi score
	return 1

def augment_lift(lift, coupon):
	# TODO: Return a likewise dictionary, but considering the GQPI 
	# accounting for the coupons
	return {}

selection = []

# If there is no trigger
if len(triggers) < 1:
	pass

# If there is one trigger
elif len(triggers) == 1:
	pass

# If there is two triggers
elif len(triggers) == 2:
	selection = triggers

# If there is more than two triggers
else:
	triggers.sort(key=lambda x: coupon_lift(get_lift(loyalty_id), x))
	selection.append(triggers[-1])

	triggers.sort(key=lambda x: coupon_lift(augment_lift(get_lift(loyalty_id),
		selection[0]
	), x))

	selection.append(triggers[-1])

