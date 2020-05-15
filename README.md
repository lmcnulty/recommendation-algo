# Recommender Algorithm

This program outputs a selection of coupons and education content for a
single user. It is capable of connecting to the AWS database or reading
data from CSV files. It should be run on a weekly basis. This can be
accomplished with cron. To add cronjobs, run `crontab -e`. For
documentation on formatting cronjobs, run `man cron`.

To use this program, you must have Python 3 and pip installed. To 
install the recommender, run: `pip3 install .`

This package includes two scripts: `fsrecommend` and `gqpi`. The latter
produces data nexessary for the program to function correctly and must
be run separately.

For an explanation of how the algorithm gets its results, refer to
comments in the source code, or run `fsrecommend --narrate` for a 
running explanation.

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

![A data-flow diagram of the recommender algorithm](diagram.png)

