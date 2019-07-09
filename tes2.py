"""
This script demonstrates how to create a bare-bones, fully functional
chatbot using PyAIML.
"""

import aiml
import sys
import time
import signal
import telegram
import random
from datetime import date
import pyowm
from threading import Thread
import requests
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#from gtts import gTTS
import logging
import json
import os
from fatsecret import Fatsecret
import sqlite3
from collections import Counter
from string import punctuation
from math import sqrt


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# initialize the connection to the database
connection = sqlite3.connect('tes.sqlite', check_same_thread=False)
cursor = connection.cursor()
 
# create the tables needed by the program
create_table_request_list = [
    'CREATE TABLE aiml(pattern TEXT UNIQUE, template TEXT UNIQUE)',
]
for create_table_request in create_table_request_list:
    try:
        cursor.execute(create_table_request)
    except:
        pass

def start(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text    
    #bot.sendPhoto(chat_id=chat_id, photo='https://media.giphy.com/media/uooHb19hRELeM/giphy.gif')
    bot.sendMessage(update.message.chat_id, text='Hai, selamat katroh bak Dedek Bot :D')

def bantu(bot, update):
    bot.sendMessage(update.message.chat_id, text='Saleum Meuturi ...\nNan ulon tuan Dedek Bot\nUlon tuan geupeuget oleh mahasiswa TRKJ yang hobi gobnyan peuget YouTube. Dan channel gobnyan bak YouTube nan jih Putra Gamer, bek tuwo neu subscribe beh. Nyo pat link channel YouTube gobnyan https://www.youtube.com/putragamer \n\nUlon tuan adalah chatbot multifungsi. Ulon tuan jeut lon peuget hal yang dimiyub nyo:\n1. Peugah haba\n2. Nging cuaca. Cara jih " /cuaca <nan kota> " contoh jih " /cuaca geudong "\n3. Nging jadwal wate shalat. Cara jih " /shalat <nan kota> " contoh jih " /shalat geudong "\n4. Baca Al - Quran. Cara jih " /quran <surat:ayat> " contoh jih " /quran 2:255 "\n5. Sitet kata nibak Al - Quran untuk peuleumah ayat yang na kata nyan. Cara jih " /sitet <kata> " contoh jih " /sitet puasa "\n6. Nging catatan DEPAG tentang terjemahan bak ayat nyan. Cara jih " /catatan <nomoi> " contoh jih " /catatan 5 "\n7. Baca doa. Cara jih " /doa <nomoi doa> " contoh jih " /doa 1 "\n8. Peuatoe mangat meureumpok ayat yang geupilih tip uroe. Cara jih " /atoeuroe " ')
	

def chatter(bot,update):
    try:
	chat_id = update.message.chat_id
	message = update.message.text
	a = message
	b = a.lower()
	#c = re.compile("haba")
	#f = re.findall(c,b)
	key = b
	print key
	row = cursor.fetchone()
	cursor.execute("SELECT template FROM aiml WHERE pattern LIKE ?", (key,))
	row = cursor.fetchone()
	jawaban = row[0]
	bot.sendMessage(chat_id=chat_id, text=jawaban)
    except (TypeError):
		bot.sendMessage(chat_id=chat_id, text="tidak ada jawaban")
		
def cuaca(bot, update, args):
    """Define weather at certain location"""
    owm = pyowm.OWM('93e430eaf5690c0ec4ae89e4f84a7d7d')
    text_location = "".join(str(x) for x in args)
    observation = owm.weather_at_place(text_location)
    w = observation.get_weather()
    humidity = w.get_humidity()
    wind = w.get_wind()
    temp = w.get_temperature('celsius')
    convert_temp = temp.get('temp')
    convert_wind = wind.get('speed')
    convert_humidity = humidity
    text_temp = str(convert_temp)
    text_wind = str(convert_wind)
    text_humidity = str(convert_humidity)
    update.message.reply_text("Temperatur, celsius:")
    update.message.reply_text(text_temp)
    update.message.reply_text("Angen tajam, m/s:")
    update.message.reply_text(text_wind)
    update.message.reply_text("Kelembaban, %:")
    update.message.reply_text(text_humidity) 
	
def shalat(bot, update, args):
    try:
	arg = args[0]
	addr = args[0:]
	payload = {'address' : '{}'.format(addr), 'method' : '4'}
	r = requests.get('http://api.aladhan.com/timingsByAddress', params=payload)
	data = json.loads(r.content)
	#jadwal = data['data']['timings']
	#for key, value in jadwal.items():
		#update.message.reply_text('{} {}'.format(key, value))
	fajr = data['data']['timings']['Fajr']
	sunrise = data['data']['timings']['Sunrise']
	dhuhr = data['data']['timings']['Dhuhr']
	asr = data['data']['timings']['Asr']
	sunset = data['data']['timings']['Sunset']
	maghrib = data['data']['timings']['Maghrib']
	isha = data['data']['timings']['Isha']
	imsak = data['data']['timings']['Imsak']
	midnight = data['data']['timings']['Midnight']
	date = data['data']['date']['readable']

	update.message.reply_text("--Jadwal {}--\nSubuh {}\nMatauroe Itubit {}\nDzuhur {}\nAshar {}\nMatauroe Ilop {}\nMaghrib {}\nIsya {}\nImsak {}\nTeungeuh Malam {}\n\nMetode : Umm al-Qura, Makkah\n\nPeubiasa shalat bak awai wate, beuh! :)".format(date, fajr, sunrise, dhuhr, asr, sunset, maghrib, isha, imsak, midnight))

    except (IndexError, ValueError):
        update.message.reply_text('Kirem perintah /shalat <wilayah> untuk teupeu jadwal shalat bak wilayah droeneuh uroe nyoe.'
'\nContoh :\n/shalat Geudong\n/shalat Lhokseumawe/n\shalat Politeknik Negeri Lhokseumawe')

# Menampilkan ayat Al-Qur'an 
def quran(bot, update, args):
    try:
	x = args[0]
	x.split(',')
	s, a = x.split(':')
	match = re.match("\d+\-\d*", a)
	if match is not None:
		awal, akhir = a.split('-')
		akhir = int(akhir)-int(awal)+1
		r = requests.get('https://api.banghasan.com/quran/format/json/surat/{}/ayat/{}'.format(s, a))
		data=r.content
		data=json.loads(data)
		for i in range(akhir):
			ayat = data['ayat']['data']['ar'][i]['teks'].encode('utf-8')
			arti = data['ayat']['data']['id'][i]['teks'].encode('utf-8')
			update.message.reply_text('{}\n{}'.format(ayat, arti))
	else:
		r = requests.get('https://api.banghasan.com/quran/format/json/surat/{}/ayat/{}'.format(s, a))
		data=r.content
		data=json.loads(data)
		ayat = data['ayat']['data']['ar'][0]['teks'].encode('utf-8')
		arti = data['ayat']['data']['id'][0]['teks'].encode('utf-8')
		update.message.reply_text('{}\n{}'.format(ayat, arti))
		
	
    except (IndexError, ValueError):
        update.message.reply_text("Kirem perintah /quran <surat:ayat> untuk peuleumah ayat Al-Qur'an yang neu pileh droeneuh!"
"\nContoh :\n/quran 2:255\n/quran 2:255-256"
"\n\nKeterangan :\n Nomoi lam kurung kurawal {3} lage nyoe maksud jih adalah catatan depag tentang terjemahan nyan."
"\nNging catatan depag ngon cara kirem perintah /catatan <nomoi>."
"\nDroeneuh jeut syit neu sitet kata dan peuleumah surat dan ayat padum manteng dalam Al-Qur'an yang na kata nyan. Kirem perintah /sitet <kata>")

# Menampilkan pencarian kata pada Al-Qur'an
def sitet(bot, update, args):
    try:
	kata = args[0].lower()
	r = requests.get('https://api.banghasan.com/quran/format/json/cari/{}/bahasa/id/mulai/0/limit/100'.format(kata))

	data = json.loads(r.content)
	qs = []
	for i in range(100):
		try :
			surat = data['cari']['id']['data'][i]['surat']
			ayat = data['cari']['id']['data'][i]['ayat']
			carian = 'QS. {} : {}'.format(surat, ayat)
			qs.append(carian)
		except:
			None
	qs = '\n'.join(qs)
	if qs == '':
		update.message.reply_text('Hana hasil dari kata yang disitet {}'.format(kata))
	else:
		update.message.reply_text('Hasil sitet untuk kata {}:\n{}'.format(kata, qs))
	
    except (IndexError, ValueError):
        update.message.reply_text("Kirem perintah /sitet <kata> untuk peuleumah surat dan ayat peu manteng lam Al-Qur'an yang na kata nyan."
"\nContoh :\n/sitet puasa"
"\n\nMaksimal surat dan ayat yang deuh 100")

def catatan (bot, update, args):
    try:
	no = int(args[0])
	if no in range(1, 1611):
		r = requests.get('https://api.banghasan.com/quran/format/json/catatan/{}'.format(no))
		data = json.loads(r.content)
		cttn = data['catatan']['teks']
		nmr = data['catatan']['nomor']
		update.message.reply_text('Catatan nomoi {}:\n{}'.format(nmr, cttn))	
	else:
		update.message.reply_text('Hana catatan depag ngon nomoi {}.'.format(no))	

    except (IndexError, ValueError):
        update.message.reply_text('Kirem perintah /catatan <nomoi> untuk teupeu catatan depag tentang terjemahan ayat nyan.'
'\nContoh :\n/catatan 5\n/catatan 256')
   
# Menampilkan do'a	
def doa (bot, update, args):
    try:
	arg = int(args[0])
	kode = arg-1
	if kode in range(0, 20):
		with open('scraping.json', 'r') as fp:
			data = json.load(fp)
		name = data['dua'][kode]
		ref = data['reference'][kode]
		pronun = data['pronunciation'][kode]
		trans = data['translation'][kode]
		hadith = data['hadith'][kode]
		no = str(arg)
		img = 'd'+no+'.png'	
		update.message.reply_photo(open(img, 'rb'))
		update.message.reply_text("Du'a:\n{}\n\nReference:\n{}\n\nPronunciation:\n{}\n\nTranslation:\n{}\n\nHadith/Benefit:\n{}\n\nSumber: Daily essential duas oleh http://www.duaandazkar.com/".format(name, ref, pronun, trans, hadith))
	else:
		update.message.reply_text("Nomoi {} hana lam daftar do'a. Do'a cuma na 20 do'a. Untuk nging daftar jih, kirem perintah /doa".format(arg))
    except (IndexError, ValueError):
        update.message.reply_text("Kirem perintah /doa <nomoi do'a> untuk peuleumah do'a uroe-uroe . Meuah do'a jih lam bahasa Inggreh"
"\nContoh jih :\n/doa 1\n/doa 18."
"\n\nDimiyub nyoe adalah daftar do'a uroe yang na :\n"
"1. Seugolom eh\n"
"2. Beudeuh eh\n"
"3. Tameng kama manoe\n"
"4. Tubit kama manoe\n"
"5. Tung ie sembahyang\n"
"6. Aleuh tung ie sembahyang\n"
"7. Tameng masjid\n"
"8. Tubit Masjid\n"
"9. Seugolom pajoh bu\n"
"10. Tuwo baca Bismillah\n"
"11. Aleuh pajoh bu\n"
"12. Aleuh pajoh bu (Pilihan Kedua)\n"
"13. Tubit Rumoh\n"
"14. Tameng Rumoh\n"
"15. Lam Perjalanan\n"
"16. Wo dari perjalanan\n"
"17. Wate bersyen\n"
"18. Wate deungo ureueng bersyen\n"
"19. Ureueung bersyen jaweub balik\n"
"20. Tameung pasai\n")

def alarm(bot, job):
    """Function to send the alarm message"""
    with open("dailyquran.txt", "r") as f:
    	x=f.readlines() 

    pilihan = x[random.randint(0,len(x)-1)]

    pilihan.split(',')
    s, a = pilihan.split(':')
    match = re.match("\d+\-\d*", a)
    bot.send_message(job.context, text="Assalamu'alaikum! Ayat pilehan uroe nyoe adalah QS.{}:{}".format(s, a))
		
    if match is not None:
    	awal, akhir = a.split('-')
	akhir = int(akhir)-int(awal)+1
	r = requests.get('https://api.banghasan.com/quran/format/json/surat/{}/ayat/{}'.format(s, a))
	data=r.content
	data=json.loads(data)
	for i in range(akhir):
		ayat = data['ayat']['data']['ar'][i]['teks'].encode('utf-8')
		arti = data['ayat']['data']['id'][i]['teks'].encode('utf-8')
		bot.send_message(job.context, text='{}\n{}'.format(ayat, arti))
    else:
	r = requests.get('https://api.banghasan.com/quran/format/json/surat/{}/ayat/{}'.format(s, a))
	data=r.content
	data=json.loads(data)
	ayat = data['ayat']['data']['ar'][0]['teks'].encode('utf-8')
	arti = data['ayat']['data']['id'][0]['teks'].encode('utf-8')
	bot.send_message(job.context, text='{}\n{}'.format(ayat, arti))
    

def atoeuroe(bot, update, job_queue, chat_data):
    """Adds a job to the queue"""
    chat_id = update.message.chat_id
    try:
        #days = (0, 1, 2, 3, 4, 5, 6)
        #job = job_queue.run_daily(alarm, time(14, 9), days, context=chat_id)
	job = job_queue.run_repeating(alarm, 86400, first=15, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Kirem ayat pilehan uroe kaleuh meuatoe !')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /atoeuroe')
		
def itong(bot, update):
    """Send a message when the command /itong is issued."""
    exp = update.message.text.replace('/itong', '')
    exp = "".join(exp.split())
    if re.match('^([-+]?([(]?[0-9][)]?[+-/*]?))*$', exp):
        try:
            update.message.reply_text(eval(exp))
        except:
            update.message.reply_text('Kirem perintah /itong <operasi matematika> untuk kalkulator.')
    else:
        update.message.reply_text('Hana perintah tentang nyan. Kirem perintah /itong <operasi matematika>.')
		
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Lon lake meu'ah, perintah nyang droeneuh paso hana. Kirem perintah /bantu untuk lon bantu.")	

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))
	
def nutrisi(bot, update):
	exp = update.message.text.replace('/nutrisi', '')
	exp = "".join(exp.split())
	foods = fs.foods_search(exp)
	foods = foods[0:9]
	food_name = foods['food_name']
	food_description = foods['food_description']
	bot.sendMessage(chat_id=update.message.chat_id, text="Search Results: \n{}\n{}".format(food_name, food_description))
    #print(json.dumps(dict, indent = 4))
	
def stop_and_restart():
	"""Gracefully stop the Updater and replace the current process with a new one"""
	restart = Updater("673443169:AAEpuO2XbZcoa7Jw9wZhHyWQIyaGRFi7M8k")
	restart.stop()
	os.execl(sys.executable, sys.executable, *sys.argv)

def restart(bot, update):
    update.message.reply_text('Dedek Bot ulang balek ...')
    Thread(target=stop_and_restart).start()
		
def main():
    # Create the EventHandler and pass it your bot's token.
    # sara
    #updater = Updater("223436029:AAEgihik3KXielXe7lBuP9H7o4M-eUdL_LU")
    #testbot
	updater = Updater("673443169:AAEpuO2XbZcoa7Jw9wZhHyWQIyaGRFi7M8k")
    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("nutrisi", nutrisi))
	dp.add_handler(CommandHandler("itong", itong))
	dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@PutraSyah035')))
	dp.add_handler(CommandHandler("cuaca", cuaca, pass_args=True))
	dp.add_handler(CommandHandler('shalat', shalat, pass_args=True))
	dp.add_handler(CommandHandler('quran', quran, pass_args=True))
	dp.add_handler(CommandHandler('sitet', sitet, pass_args=True))
	dp.add_handler(CommandHandler('catatan', catatan, pass_args=True))
	#dp.add_handler(CommandHandler('doa', doa, pass_args=True))
	dp.add_handler(CommandHandler('atoeuroe', atoeuroe,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
	dp.add_handler(CommandHandler("bantu", bantu))
	   
	dp.add_error_handler(error)

    # on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler([Filters.text], chatter))
	dp.add_handler(MessageHandler([Filters.command], unknown)) 

    # Start the Bot
	updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
    main()