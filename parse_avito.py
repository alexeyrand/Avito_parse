import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import threading
from threading import Thread
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.window import WindowTypes
from selenium import webdriver


class AvitoParse:          
	def __init__(self, url: list, username: str, password: str, hookurl: list, items, count: int, pause: int):
		"""Функция иницилизирует парсер, сохраняя в переменные заданные параметры"""
		self.url = url
		self.username = username
		self.password = password
		self.hookurl = hookurl
		self.items = items
		self.count = count
		self.pause = pause
		self.data = []       #   Запоминает товары, которые уже опубликованы на сервере в Дискорде
		self.blacklist = []  #   Черный список продавцов

   
	def __set_up(self):
		"""Функция открытия браузера"""
		print(len(self.url), len(self.hookurl))
		options = Options()
		#options.add_argument('--headless')
		options.add_argument("--incognito")
		options.add_argument('--disable-popup-blocking')
		self.driver = uc.Chrome(options=options, version_main=116)
		
		self.driver.implicitly_wait(3)
		
		

	def __get_url(self):
		"""Функция открытия требуемого сайта"""
		self.driver.get(self.url[0])
		self.driver.implicitly_wait(3)
		for j in range(1, 10):
			self.driver.execute_script(f"window.open('{self.url[j]}')")
			#self.driver.implicitly_wait(3)
			time.sleep(20)
		print("Начало работы")


		#self.driver.find_element(By.CSS_SELECTOR, "body").send_keys()
		#self.driver.find_element(By.NAME, "login").send_keys(self.username)
		#self.driver.find_element(By.CSS_SELECTOR, "[data-marker='login-form/password/input']").send_keys(self.password)
		#self.driver.find_element(By.CSS_SELECTOR, "[data-marker='login-form/submit']").click()
		#time.sleep(50)
		#self.driver.refresh()

	def __item(self, titles):
			pass
   
	def __parse_page(self, i, h):
		"""Функция парсинга одной страницы"""
		
		titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
		k = 0
		for title in titles:
			#     формирование характиристик товара 
			flag = False
			date = title.find_element(By.CSS_SELECTOR, "[data-marker='item-date']").text
			itemid = title.get_attribute("id")
			#author = title.find_element(By.CSS_SELECTOR, "[class*='iva-item-userInfoStep']").text
			#print(author)
			if date in ['1 минуту назад', '2 минуты назад', '3 минуты назад', '4 минуты назад', '5 минут назад', 'Несколько секунд назад'] and itemid not in self.data:
				url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
				name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
				description = title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
				price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
				try:
					image = title.find_element(By.CSS_SELECTOR, "[class*='photo-slider-image']").get_attribute("src")
				except NoSuchElementException:
					image = 'No image'
				print(f'Опубликован новый товар {date}')

				#   Формирование embed карточки товара для дискорда
				if  True:
					# f"# ------------------------------------------------------------\n## {data['name']} \nОписание: {data['description'][:160]}\n\nЦена: {data['price']} рублей\n{data['time']} ({data['date']})\n[Ссылка на товар](<{data['url']}>)[.]({data['image']})"
					self.data.append(itemid)
					if len(self.data) > 60:
						self.data = []
					x = datetime.datetime.now()
					if date == 'Несколько секунд назад':
						y = datetime.timedelta(minutes=0)
					else:
						y = datetime.timedelta(minutes=int(date[0]))
					webhook = DiscordWebhook(url=self.hookurl[i], content=None)
					embed = DiscordEmbed(title=f'{name}', description=description[:220], color='03b2f8')
					embed.set_image(url=image)
					embed.set_timestamp()
					embed.set_url(url=url)
					embed.add_embed_field(name='Цена', value=f'{price} рублей')
					embed.add_embed_field(name='Время публикации', value=f'{(x-y).strftime("Сегодня в %H:%M")}')
					#embed.add_embed_field(name='Автор', value=f'{author2} {author2}')
					webhook.add_embed(embed)
					response = webhook.execute()
					flag = True
					time.sleep(1)

			if flag==False:
				print("Новых товаров не появилось")     #   Если новых товаров нет, браузер через время t = pause обналвяет страницу и заново запускает функцию __parse_page()
				time.sleep(2)
				self.driver.refresh()
				if i == 0:
					i = 1
				elif i == 1:
					i = 2
				elif i == 2:
					i = 3
				elif i == 3:
					i = 4
				elif i == 4:
					i = 5
				elif i == 5:
					i = 6
				elif i == 6:
					i = 7
				elif i == 7:
					i = 8
				elif i == 8:
					i = 9
				elif i == 9:
					i = 0
		
				self.driver.switch_to.window(h[i])
				self.__parse_page(i, h)


	def parse(self):
		"""Функция для старта отслеживания новых товаров.
  		   Последовательно запускаются три функции: открытие браузера, открытие сайта, парсинг страницы
       	   Функция parse() запускается из файла start.py"""
		self.__set_up()
		self.__get_url()
		h = []
		for handle in self.driver.window_handles:
			h.append(handle)
		try:
			i = 0
			self.__parse_page(i, h)
			
		except StaleElementReferenceException:
			print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
		#	if self.driver:
		#		self.driver.close()
			time.sleep(300)
			try:
				i = 0
				self.__parse_page(i, h)
			except StaleElementReferenceException:
				print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
				time.sleep(300)
				try:
					i = 0
					self.__parse_page(i, h)
				except StaleElementReferenceException:
					print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
					time.sleep(300)
  