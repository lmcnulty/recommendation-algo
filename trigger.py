#!/usr/bin/env python3

import csv
from random import randint

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
				return row[1:-1]

def get_user_purchases(id):
	with open("data/appendeseptmay.csv") as append:
		reader = csv.reader(append)
		return [row for row in reader if row[0] == id]

def check_compatible(preferences, group):
	for i in range(len(group)):
		if preferences[i] == "1" and group[i] == "0":
			#print(i)
			return False
	return True

#for e in sorted(get_user_data("43610000389"), key=lambda row: row[2]):
	#print(" ".join(e))


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
				#purchase.append(row[-1])
				#categoried.append(purchase)
				categories.add(row[-1])
	#purchases = categoried

coupons = []

preferences = get_user_preferences(loyalty_id)

compatability = {}

with open("data/CouponCompatibilitywithParticPref.csv") as f:
	reader = csv.reader(f)
	for row in reader:
		compatability[row[0]] = row[2:-1]

# Select the coupon from the same categories of these products.
with open ("data/CouponCodebookSASIMPEDIT.csv") as f:
	reader = csv.reader(f)
	for row in reader:
		if row[3] in categories:
			coupons.append(row)

ex("Select the coupon from the same categories of these products.")
out_list(coupons)

"""
for coupon in coupons:
	if not coupon in compatability: continue
	 and check_compatible(preferences, compatability[coupon]):
"""

coupons = [coupon for coupon in coupons if coupon[3] in preferences and check_compatible(preferences, compatability[coupon[3]])]

ex("Keep only the coupon which can be use by the subject")
out_list(coupons)


