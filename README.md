# pib

Download magazines from [New IndiaSamachar, Press Information Bureau, India](http://newindiasamachar.pib.gov.in/archive.aspx).
This might be helpful for candidates preparing for different govt examinations.

## How to use:

```shell

#Clone the repo with:
git clone https://github.com/nit-in/nis
#cd to the cloned repo
cd nis
#installing required packages
pip install -r requirements.txt
#when these steps are done,you are ready to run the spider and download the articles.

#source the env file
source .env
#run the spider

For the language:
Options(1: English, 2: Hindi, 3: Urdu, 4: Bengali, 6: Punjabi, 8: Kannada, 9: Marathi, 10: Assamese, 11: Tamil, 13: Gujarati, 15: Malayalam, 16: Telugu, 18: Odia)

For the fortnight:
Options(1: 1st fortnight, 2: 2nd fortnight)

For the month
Options(Number of the month\nJan: January, Feb: February,...Dec: December)

For the year
Options(Number of the year\n2021,2020)

Command should be in format:
nis lang_code fortnight_code month_code year_code

Example:
For NIS magazine of 1st Fortnight of July 2021 in English Language
nis 1 1 Jul 2021
```

Any suggestions and improvements are welcome.
