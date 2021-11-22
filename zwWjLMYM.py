import telebot
import config
import random
import re
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['mail'])
def mail(message):
	#print(message.text)
	if re.search('тема письма:(.*)\n', message.text) is not None:
		topic = re.search('тема письма:(.*)\n', message.text)
		adress = re.search('адреса получателя:(.*)\n', message.text)

		adresses = re.split(' ', adress.group(1))

		times = re.search('время отправки:(.*)\n', message.text)
		text = re.search('текст письма:(.*)', message.text)
		sender = config.SENDER
		server = config.SERVER
		user = config.USER
		password = config.PASSWORD

		msg = MIMEMultipart('alternative')
		msg['Subject'] = topic.group(1)
		msg['From'] = 'Python script <' + sender + '>'
		msg['To'] = ', '.join(adresses)
		msg['Reply-To'] = sender
		msg['Return-Path'] = sender
		msg['X-Mailer'] = 'Python/' + (python_version())

		part_text = MIMEText(text.group(1), 'plain')

		msg.attach(part_text)
		if times.group(1) == 'сейчас':

			mail = smtplib.SMTP_SSL(server)
			mail.login(user, password)
			mail.sendmail(sender, adresses, msg.as_string())
			mail.quit()
			bot.send_message(message.chat.id, 'сообщение отправлено')
		elif times.group(1) == 'в течении дня':
			time.sleep(5)
			mail = smtplib.SMTP_SSL(server)
			mail.login(user, password)
			mail.sendmail(sender, adresses, msg.as_string())
			mail.quit()
			bot.send_message(message.chat.id, 'сообщение отправлено')

@bot.message_handler(commands=['help'])
def mail(message):
	bot.send_message(message.chat.id, 'Пример команды\n /mail\nтема письма:текст\nадреса получателя:адрес получателя через пробел\nвремя отправки:в течении дня\nтекст письма:текст\n\nЕсли вы хотите отправить сообщение нескольким пользователям вводите адреса через пробел')
# RUN
bot.polling(none_stop=True)