#!/usr/bin/env python3

import csv
from collections import defaultdict
from random import randint, random

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

# This should return the GQPI for the category of the coupon for the
# customer in `customer_id`
def get_gqpi(customer_id, coupon):
	return random()
	
def get_lift(trips, couponA, couponB):
	An = str(couponA.number)
	Bn = str(couponB.number)

	num_trips = len(trips)
	A_trips   = len([trip for trip in trips if An in trip])
	B_trips   = len([trip for trip in trips if Bn in trip])
	AB_trips  = len([t for t in trips if An in t and Bn in t])
	
	prob_A         = A_trips / num_trips
	prob_B         = B_trips / num_trips
	prob_AB        = AB_trips / num_trips
	prob_A_given_B = prob_AB / prob_B

	return prob_A_given_B / prob_A if prob_A > 0 else 0

def select(loyalty_id):

	# Selection all the products purchased by the subject in the daily download. (755)
	purchases = get_user_purchases(loyalty_id)

	trips = defaultdict(lambda: [])
	for purchase in purchases:
		trips[purchase[1]].append(purchase[3])

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

	preferences = get_user_preferences(loyalty_id)
	
	# Select the coupon from the same categories of these products.
	with open ("data/CouponCodebookSASIMPEDIT.csv") as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == "CouponNumber": continue
			coupon = Coupon(row)
			if not coupon.is_compatible(preferences): continue
			coupons.append(coupon)
			if row[3] in categories:
				triggers.append(Coupon(row))

	ex("Keep only the coupon which can be use by the subject")
	for coupon in triggers: print(coupon)

	selection = []

	# If there is no trigger
	if len(triggers) < 1:
		# use the worst GQPI (or HEI if we don’t have the GQPI data 
		# or if the subject had purchased for less than 50$ in the 
		# month) categories with coupon that could been used by the 
		# subject as a list of possible coupon. Choose the first coupon 
		# randomly in this list.
		coupons.sort(key=lambda x: get_gqpi(loyalty_id, x))
		selection.append(coupons[-1])

		# Add to the list of possible coupon the list of coupon that can 
		# improve the next worst GQPI(or HEI) category.
		possible_pairs = [
			coupon for coupon in coupons 
			if coupon.category != selection[0].category
		]
		# Give a weight to all the coupon using the lift between two
		# coupon. 
		possible_pairs.sort(
			key=lambda coupon: get_lift(loyalty_id, selection[0], coupon)
		)

		# Choose randomly (?) the second coupon using the weight.
		selection.append(possible_pairs[-1])

	# If there is one trigger
	elif len(triggers) == 1:

		# the first coupon is the trigger.
		selection = triggers

		# Select the list of coupon improving the worst 3 GQPI (or HEI)  
		# categories. Give a weight to all the coupon using the lift  
		# between two coupon. Choose randomly the second coupon using 
		# the weight.
		# (I don't really understand what this means, so I'm just using
		#  the best lift score given the first selection.)
		selection.append(
			sorted(coupons, key=lambda coupon: get_lift(loyalty_id, selection[0], coupon))[-1]
		)

	# If there is two triggers
	elif len(triggers) == 2:
		# the two coupon will be the two triggers
		selection = triggers

	# If there is more than two triggers
	else:
		ex("There are more than two triggers")

		# give a weight to all the triggers according if the GQPI 
		# categories they improve need to be improve or not
		triggers.sort(key=lambda x: get_gqpi(loyalty_id, x))

		# Select the first coupon using this weight
		selection.append(triggers[-1])

		# Give a weight to all the other triggers according to the 
		# lift between the first coupon and the trigger
		triggers.sort(key=lambda x: get_lift(loyalty_id, selection[0], x))

		# Select the second coupon using this weight
		selection.append(triggers[-1])

	# TODO:
	# Select the educational content randomly in the list of educational 
	# content that can be related with one of the two coupons and that 
	# had not been send to the subject in the past weeks.

	# TODO:
	# If one of the coupon can be part of one of the recipes and that
	# this recipes had not been send in the past weeks, select this 
	# recipes.

# This function gets called if you run the script directly, but not if
# you import it as a library.
if __name__ == "__main__":
	loyalty_id = "43610000389"
	loyalty_id = "43610003420"
	select(loyalty_id)
