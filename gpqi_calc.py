import csv

codes = {}
# subjectIDs = {}
purchases = []
# key: ID (currently loyaltyID), value: instance of Subject class found below
subjects = {}

# GPQI standard expenditure for each category
STDEXP_Veg = 25.7
STDEXP_GB = 11.7
STDEXP_TF = 17.3
STDEXP_WF = 14.9
STDEXP_WG = 10.9
STDEXP_Dairy = 13.7
STDEXP_TPF = 20.5
STDEXP_SN = 9.2
STD_RG = 3.9
STD_PM = 18.9
STD_Sweets = 15.7

# Exceptions.
# If there is an error parsing the csv:
# add k, v pair to 'exceptions' with the item description and corrected gpqi code,
# where k may be EITHER the item UPC or the item description
#
# ex: item should be counted (i.e. valid food item)
# exceptions["<item description>"] = "<correct gpqi code>"
#
# ex: item should NOT be counted (i.e. coupon, non-food item)
# exceptions["<item description>"] = "skip"
exceptions = {}
exceptions["Boot Camp 20% Off"] = "skip"
exceptions["Boot Camp"] = "skip"
exceptions["Luxe 20% Off"] = "skip"
exceptions["Luxe 20% O"] = "skip"
exceptions["All That Matters 20% Off"] = "skip"
exceptions["All That Matters 20%"] = "skip"
exceptions["All That M"] = "skip"
exceptions["Buy 10 Soap"] = "skip"
exceptions["CALENDAR"] = "skip"
exceptions["$5.00 Beauty & Wellness"] = "skip"
exceptions["$5.00 Beauty & Welln"] = "skip"
exceptions["CARD"] = "skip"
exceptions["CALYPSO CA"] = "skip"
exceptions["CALYPSO CARD"] = "skip"

exceptions["890180200103"] = "999"
exceptions["78945330012"] = "999"
exceptions["81640102074"] = "999"
exceptions["400163850198"] = "999"
exceptions["506046164165"] = "999"
exceptions["WELDA"] = "999"

exceptions["PURE ITALIAN MOZZARELLA 8.8 OZ"] = "6"
exceptions["805367759505"] = "6"

exceptions["890604614311"] = "99"
exceptions["890604614196"] = "99"
exceptions["885053961044"] = "99"
exceptions["885053961043"] = "99"
exceptions["885053961035"] = "99"
exceptions["885053900001"] = "99"
exceptions["803399304371"] = "99"
exceptions["803399304234"] = "99"
exceptions["803338700502"] = "99"
exceptions["803319660137"] = "99"
exceptions["802968900664"] = "99"
exceptions["802968900514"] = "99"
exceptions["802726910512"] = "99"
exceptions["802307400215"] = "99"
exceptions["800691100001"] = "99"
exceptions["5070024719"] = "99"
exceptions["7099214030"] = "99"
exceptions["400163808015"] = "99"
exceptions["400163808838"] = "99"
exceptions["489703931077"] = "99"
exceptions["489703931071"] = "99"
exceptions["489703931070"] = "99"
exceptions["489703931032"] = "99"
exceptions["802273411166"] = "99"
exceptions["803338703003"] = "99"

exceptions["869721700264"] = "11"

exceptions["803348811105"] = "9"
exceptions["803348811062"] = "9"
exceptions["803348811061"] = "9"
exceptions["803348811043"] = "9"
exceptions["803348811015"] = "9"
exceptions["803348811003"] = "9"
exceptions["803348811002"] = "9"
exceptions["803261081296"] = "9"
exceptions["803261081047"] = "9"
exceptions["803261081045"] = "9"
exceptions["803261081044"] = "9"
exceptions["802369600218"] = "9"
exceptions["800729093550"] = "9"
exceptions["800729052155"] = "9"
exceptions["800729084130"] = "9"
exceptions["800729022115"] = "9"
exceptions["800729022113"] = "9"
exceptions["800729022111"] = "9"
exceptions["800287301806"] = "9"
exceptions["800287301803"] = "9"
exceptions["800110001602"] = "9"
exceptions["800110001201"] = "9"
exceptions["800729033045"] = "9"

exceptions["802968900612"] = "3"
exceptions["802142300955"] = "3"
exceptions["750302423810"] = "3"

exceptions["300001002504"] = "4"

exceptions["800469425314"] = "8"

exceptions["801713910405"] = "2"
exceptions["801713910468"] = "2"
exceptions["801713910190"] = "2"
exceptions["801713910046"] = "2"
exceptions["780466815003"] = "2"
exceptions["780466178001"] = "2"
exceptions["780462807146"] = "2"
exceptions["780461359031"] = "2"
exceptions["780460243005"] = "2"
exceptions["780012200043"] = "2"
exceptions["775126200320"] = "2"
exceptions["775126200201"] = "2"
exceptions["539700502203"] = "2"
exceptions["803350932526"] = "2"
exceptions["505037211700"] = "2"
exceptions["505037211800"] = "2"
exceptions["750301578005"] = "2"

exceptions["7800015345"] = "11"

# load data
with open("data/masterGQPIcodes.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        try:
            upc = int(row[0])
        except ValueError:
            upc = None
        try:
            gpqi = int(row[2])
        except ValueError:
            gpqi = None
        if upc != None and gpqi != None:
            codes[row[0]] = int(row[2])

# with open("insert subjectID file") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         subjectIDs[int(row[0])] = int(row[1])

# remove all non-food items from Weleda skincare brand because it shows up a lot
def remove_WELEDA(description):
    try:
        brand = description.split()[0]
    except IndexError:
        return description
    if brand == "WELEDA" or brand == "WELDA" or brand == "WELEDS":
        return "WELDA"
    else:
        return description

class Purchase():
    def __init__(self, csv_row):
        self.loyaltyID = int(csv_row[0])
        # self.subjectID = subjectIDs[self.loyaltyID]
        self.date = csv_row[1]
        self.department = int(csv_row[2])
        self.upc = csv_row[3]
        self.description = remove_WELEDA(csv_row[4])
        try:
            self.retail = float(csv_row[7])
        except ValueError:
            self.retail = 0
        self.retail_sum = float(csv_row[8])
        UPC_exception = exceptions.get(self.upc, None)
        Desc_exception = exceptions.get(self.description, None)
        if UPC_exception != None:
            self.gpqi = int(UPC_exception)
        elif Desc_exception != None:
            if Desc_exception == "skip":
                self.gpqi = "skip"
            else:
                self.gpqi = int(Desc_exception)
        else:
            try:
                self.gpqi = codes[self.upc]
                int(self.gpqi)
            except (KeyError, ValueError):
                self.gpqi = None



class Subject():
    def __init__(self, ID):
        self.ID = ID
        self.total_spent = 0
        self.spent_by_category = {}
        for i in range(1, 12):
            self.spent_by_category[i] = 0
        self.spent_by_category[99] = 0
        self.spent_by_category[999] = 0
        self.total_score = 0
        self.score_by_category = {}

with open("data/appendeseptmay.csv") as f:
    reader = csv.reader(f)
    next(reader)
    linenum = 0
    for row in reader:
        linenum += 1
        # print(linenum)
        # if linenum == 2516:
        if row[2] != "9000":
            this_purchase = Purchase(row)
            purchases.append(this_purchase)
            if this_purchase.gpqi == None:
                print("Could not find GPQI code for the item listed below")
                print("Item: {}".format(this_purchase.description))
                print("UPC: {}".format(this_purchase.upc))
                print("Follow instructions under 'Exceptions' in this python script to correct the GPQI code for this item.")
            elif this_purchase.gpqi != "skip":
                this_subject = subjects.get(this_purchase.loyaltyID, None)
                if this_subject == None:
                    subjects[this_purchase.loyaltyID] = Subject(this_purchase.loyaltyID)
                    this_subject = subjects[this_purchase.loyaltyID]
                this_subject.total_spent += this_purchase.retail
                this_subject.spent_by_category[this_purchase.gpqi] += this_purchase.retail

def register_score(subject, category, score, max_score):
    if score > max_score:
        score = max_score
    elif score < 0:
        score = 0
    subject.score_by_category[category] = score
    subject.total_score += score

# calculates gpqi scores for all subjects
def calculate_scores():
    with open("GPQIscores.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        headers = ["Subject", "Total Score", "Total Vegetables", "Greens and Beans",
                   "Total Fruit", "Whole Fruit", "Whole Grains", "Dairy",
                   "Total Protein Foods", "Seafood and Nuts", "Refined Grains",
                   "Processed Meats", "Sweets and Sodas"]
        writer.writerow(headers)
        for this_subject in subjects.values():
            tot_expend = this_subject.total_spent

            veg = ((((this_subject.spent_by_category[3] + this_subject.spent_by_category[4]) / tot_expend) * 100) / STDEXP_Veg) * 5
            register_score(this_subject, "Total Vegetables", veg, 5)

            greens_beans = (((this_subject.spent_by_category[4] / tot_expend) * 100) / STDEXP_GB) * 5
            register_score(this_subject, "Greens and Beans", greens_beans, 5)

            tot_fruit = ((((this_subject.spent_by_category[1] + this_subject.spent_by_category[2]) / tot_expend) * 100) / STDEXP_TF) * 5
            register_score(this_subject, "Total Fruit", tot_fruit, 5)

            whole_fruit = (((this_subject.spent_by_category[2] / tot_expend) * 100) / STDEXP_WF) * 5
            register_score(this_subject, "Whole Fruit", whole_fruit, 5)

            whole_grain = (((this_subject.spent_by_category[5] / tot_expend) * 100) / STDEXP_WG) * 10
            register_score(this_subject, "Whole Grains", whole_grain, 10)

            dairy = (((this_subject.spent_by_category[6] / tot_expend) * 100) / STDEXP_Dairy) * 10
            register_score(this_subject, "Dairy", dairy, 10)

            tot_protein_food = ((((this_subject.spent_by_category[7] + this_subject.spent_by_category[8]) / tot_expend) * 100) / STDEXP_TPF) * 5
            register_score(this_subject, "Total Protein Foods", tot_protein_food, 5)

            seafood_nuts = (((this_subject.spent_by_category[8] / tot_expend) * 100) / STDEXP_SN) * 5
            register_score(this_subject, "Seafood and Nuts", seafood_nuts, 5)

            refined_grains = 10 * (1 - ((((this_subject.spent_by_category[9] / tot_expend) * 100) - 1) / STD_RG))
            register_score(this_subject, "Refined Grains", refined_grains, 10)

            processed_meats = 5 * (1 - ((((this_subject.spent_by_category[10] / tot_expend) * 100) - 1) / STD_PM))
            register_score(this_subject, "Processed Meats", processed_meats, 5)

            sweets_sodas = 10 * (1 - ((((this_subject.spent_by_category[11] / tot_expend) * 100) - 1) / STD_Sweets))
            register_score(this_subject, "Sweets and Sodas", sweets_sodas, 10)

            row = [this_subject.ID, this_subject.total_score]
            for score in this_subject.score_by_category.values():
                row.append(score)
            writer.writerow(row)

            # print("Subject: {}".format(this_subject.ID))
            # print("Total Score: {}".format(this_subject.total_score))
            # for category, score in this_subject.score_by_category.items():
            #     print("\t{}: {}".format(category, score))

answer = raw_input("Would you like to calculate GPQI scores? (y/n): ")
while answer != "y" and answer != "n":
    answer = raw_input("Please type 'y' or 'n': ")
if answer[0] == "y":
    calculate_scores()
else:
    quit()
