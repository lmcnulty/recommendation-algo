# Recommender Algorithm

To use this program, you must have Python 3 and pip installed. To 
install the recommender, run: `pip3 install .`

This package includes two scripts: `fsrecommend` and `gqpi`

```
usage: fsrecommend [-h] [--start START] [--compatibilitycsv COMPATIBILITYCSV]
                   [--secretkey SECRETKEY] [--couponscsv COUPONSCSV]
                   [--endpoint ENDPOINT] [--subjectscsv SUBJECTSCSV]
                   [--purchasescsv PURCHASESCSV] [--subjectid SUBJECTID]
                   [--loyaltyid LOYALTYID] [--narrate] [--gqpi GQPI]
                   [--UPCS UPCS]

Output coupons for a specified user.

optional arguments:
  -h, --help            show this help message and exit
  --start START         The index at which to start the file numbering.
  --compatibilitycsv COMPATIBILITYCSV
                        A csv file containing coupon compatibilities
  --secretkey SECRETKEY
                        The secret AWS access key. If not passed, the program
                        will try to read data from csv files
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
  --gqpi GQPI           The csv file containing the subjects GQPI Scores.
  --UPCS UPCS           The CSV file containing coupon UPCS
```

```
$ gqpi --help
usage: gqpi [-h] [--codes CODES]

Output GQPI csv.

optional arguments:
  -h, --help     show this help message and exit
  --codes CODES  A csv file containing GQPI codes for each item
```

## To do

Work to be done is documented inline in the source files. To list all
TODOs, run `grep "TODO" fsrecommend gqpi`.

