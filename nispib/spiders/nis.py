import scrapy
from scrapy_selenium import SeleniumRequest
from pathlib import Path
import requests
from datetime import datetime
import subprocess																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																		

url = "http://newindiasamachar.pib.gov.in/archive.aspx"
nis_url = "https://pib.gov.in/PressReleaseIframePage.aspx?PRID="
cwd = Path.cwd()
chromedriver = "selenium/chromedriver"
chromedriver_path = Path(cwd,chromedriver).expanduser()


class NISSpider(scrapy.Spider):
	name = 'nis'
	allowed_domains = ['newindiasamachar.pib.gov.in/']


	custom_settings = {
		'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
		'SELENIUM_DRIVER_EXECUTABLE_PATH' : str(chromedriver_path)
	}

	def start_requests(self):

		self.rel_lang = 1
		self.rel_lang_str = self.lang_name(self.rel_lang)

		if str(self.rel_fort_night) == "1":
			self.rel_fortnight_str = "Fortnight_" + str(self.rel_fort_night)
			self.rel_fortnight = 14
		elif str(self.rel_fort_night) == "2":
			self.rel_fortnight_str = "Fortnight_" + str(self.rel_fort_night)
			self.rel_fortnight = 16
		else:
			print("Enter 1 or 2 for 1st and 2nd fortnight respectively")

		self.rel_month = datetime.strptime(str(self.rel_rmonth),"%b").strftime("%m")
		self.rel_month_str = datetime.strptime(str(self.rel_rmonth),"%b").strftime("%b")
		self.rel_year = datetime.strptime(self.rel_ryear,"%Y").strftime("%Y")
		self.jlang = f"document.forms.form1.ContentPlaceHolder1_ddlLanguage.value={str(self.rel_lang).lstrip('0')};" 
		self.jfrnight = f"document.forms.form1.ContentPlaceHolder1_dd_fortnight.value={str(self.rel_fortnight).lstrip('0')};"
		self.jmon = f"document.forms.form1.ContentPlaceHolder1_dd_month.value={str(self.rel_month).lstrip('0')};"
		self.jyr = f"document.forms.form1.ContentPlaceHolder1_dd_year.value={str(self.rel_year).lstrip('0')};"

		self.submit = f"document.forms.form1.submit()"
		self.jsub = self.jlang + self.jfrnight + self.jmon + self.jyr + self.submit
		yield SeleniumRequest(url=url, callback=self.parse_js,script=self.jsub)

	def parse_js(self,response):
		for i in response.xpath("//i[contains(@class, 'fa fa-download')]"):
			self.nis_mag_link = i.xpath("//../a[contains(@href,'.pdf')]/@href").get()
			self.download_mag(self.nis_mag_link, self.rel_lang_str, self.rel_fortnight_str, self.rel_month_str, self.rel_year)

	def download_mag(self,mag_link, mag_lang, mag_fn, mag_month, mag_year):

		nis_dir = "~/NIS"
		nis_dir_path = Path(nis_dir).expanduser()
		self.check_folder(nis_dir_path)
		nis_yr_path = Path(nis_dir_path, mag_year)
		self.check_folder(nis_yr_path)
		nis_month_path = Path(nis_yr_path, mag_month)
		self.check_folder(nis_month_path)
		nis_fortnight_path = Path(nis_month_path, mag_fn)
		self.check_folder(nis_fortnight_path)
		nis_lang_path = Path(nis_fortnight_path, mag_lang)
		self.check_folder(nis_lang_path)
		mag_name = "NIS_" + str(mag_lang) + "_" + str(mag_fn) + "_" + str(mag_month) + "_" + str(mag_year) + ".pdf"
		mag_path = Path(nis_lang_path, mag_name)
		mag_size = requests.head(mag_link).headers["Content-Length"]
		if not self.check_file(mag_path, mag_size):
			program = "wget"
			arg1 = "--show-progress"
			arg2 = "--server-response"
			arg3 = "--continue"
			arg4 = "-O"
			print(f"Downloading {mag_name} to ",f"{str(mag_path)}")
			subprocess.run([program, arg1, arg2, arg3, str(mag_link), arg4, str(mag_path)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	def lang_name(self, lang_code):
		lang={
		1: "English",
		2: "Hindi", 
		3: "Urdu",
		4: "Bengali", 
		6: "Punjabi",
		8: "Kannada", 
		9: "Marathi", 
		10: "Assamese",
		11: "Tamil", 
		13: "Gujarati",
		15: "Malayalam",
		16: "Telugu",
		18: "Odia"
		}
		return lang[lang_code]

	def check_folder(self, fpath):
		if not fpath.exists():
			fpath.mkdir(parents=True)
		else:
			pass

	def check_file(self,pdf_path,pdf_size):
		if pdf_path.exists() and int(pdf_path.stat().st_size) == int(pdf_size):
			return True
		else:
			return False