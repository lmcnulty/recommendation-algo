# Recommender Algorithm

To use this program, you must have Python 3 and pip installed.

To install the recommender, run:

  pip3 install .

After installing, you can invoke the program by running `fsrecommend`

```
$ fsrecommend --help

usage: fsrecommend [-h] [--start START] [--compatibilitycsv COMPATIBILITYCSV]
                   [--secretkey SECRETKEY] [--couponscsv COUPONSCSV]
                   [--endpoint ENDPOINT] [--subjectscsv SUBJECTSCSV]
                   [--purchasescsv PURCHASESCSV] [--subjectid SUBJECTID]
                   [--loyaltyid LOYALTYID] [--narrate]

Output coupons for a specified user.

optional arguments:
  -h, --help            show this help message and exit
  --start START         The index at which to start the file numbering.
  --compatibilitycsv COMPATIBILITYCSV
                        A csv file containing coupon compatibilities
  --secretkey SECRETKEY
                        The secret AWS access key
  --couponscsv COUPONSCSV
                        A csv file containing coupon information
  --endpoint ENDPOINT   The endpoint to query dynamodb from
  --subjectscsv SUBJECTSCSV
                        A csv file containing the subject descriptions.
  --purchasescsv PURCHASESCSV
                        A csv file containing user purchases
  --subjectid SUBJECTID
                        The subject ID in the descriptions csv
  --loyaltyid LOYALTYID
                        The subject's loyalty ID
  --narrate             Pass this flag to give a running explanation of the
                        algorithm.
```
