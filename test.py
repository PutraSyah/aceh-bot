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
from pyowm.exceptions import OWMError
from threading import Thread
import requests
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler
from gtts import gTTS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import json
import os
import sqlite3

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# initialize the connection to the database
connection = sqlite3.connect('botaceh.sqlite', check_same_thread=False)
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
	user = update.message.from_user
	chat_id = update.message.chat_id
	message = update.message.text 
	logger.info("User login : %s", user.first_name)
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendPhoto(chat_id=chat_id, photo='https://www.instagram.com/p/BqKmt9HhNoB/')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Assalamualaikum, hai {} selamat katroh bak Dedek Bot :D'.format(update.message.from_user.first_name))
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='\nLon jeut lon bantu nging tentang kurikulum semester trkj, kalender akademik, peraturan akademik, struktur pimpinan trkj, unduh file ngon dokumen, ruang belajar tik, lab tik, dosen trkj\n1./kurikulumtrkj \n2./kalenderakademik\n3./peraturanakademik\n4./strukturpimpinantrkj\n5./unduh\n6./ruangbelajartik\n7./labtik\n8./dosentrkj')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Peu na nyang jeut lon bantu {} :)'.format(update.message.from_user.first_name))

def bantu(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	message = update.message.text 
	logger.info("User type help : %s", user.first_name)
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendPhoto(chat_id=chat_id, photo='https://scontent.fpku3-1.fna.fbcdn.net/v/t1.0-9/57000708_377471832858724_6664368777448128512_n.png?_nc_cat=103&_nc_eui2=AeG7055jQnZptW41ATyEdv3SypXAppba10wiJV7EYagD8CV6j-bL6JcbCfxp32VDfGa2ykKrheTbiyjzOmGIz82Z4-IB_dQuMbfIIFRl9Ddn1Q&_nc_ht=scontent.fpku3-1.fna&oh=347da4d451c856fcc8b88c0dd0ebcd31&oe=5D765FC1')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Saleum Meuturi ...\nNan ulon tuan Dedek Bot\nUlon tuan geupeugeut oleh mahasiswa TRKJ nyang nan gobnyan Muhajjirsyah. Ulon tuan jeut lon peugah haba tentang prodi trkj (teknologi rekayasa komputer jaringan)')
	
def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text('Posisi rumoh droeneuh di {} {}'.format(user_location.latitude, user_location.longitude))	
	
def photo(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	photo_file = update.message.photo[-1].get_file()
	photo_file.download('user_photo.jpg')
	logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
	bot.sendMessage(chat_id=chat_id, text='Nyo foto droeneuh {}'.format(update.message.from_user.first_name))
	file='user_photo.jpg'
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendPhoto(chat_id=chat_id, photo=open(file, 'rb'))
	os.remove(file)
	
def audio(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	audio_file = update.message.audio.get_file()
	audio_file.download('audio_user.mp3')
	logger.info("Audio of %s: %s", user.first_name, 'audio_user.mp3')
	bot.sendMessage(chat_id=chat_id, text='Nyo audio droeneuh {}'.format(update.message.from_user.first_name))
	file='audio_user.mp3'
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_AUDIO)
	bot.sendAudio(chat_id=chat_id, audio=open(file, 'rb'))
	os.remove(file)
	
def voice(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	voice_file = update.message.voice.get_file()
	voice_file.download('voice_user.ogg')
	logger.info("Voice of %s: %s", user.first_name, 'voice_user.ogg')
	bot.sendMessage(chat_id=chat_id, text='Nyo su droeneuh {}'.format(update.message.from_user.first_name))
	file='voice_user.ogg'
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_AUDIO)
	bot.sendVoice(chat_id=chat_id, voice=open(file, 'rb'))
	os.remove(file)
	
def contact(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	message = update.message.text 
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	a = update.message.contact
	bot.sendMessage(chat_id=chat_id, text='Teurimong geunaseh {}, kaleuh neu bi nomoi handphone {} droeneuh'.format(a.first_name, a.phone_number))
	bot.sendMessage(update.message.chat_id, text='Hai {}. Nyo nomoi handphone lon 082274791903, neu simpan beh :D'.format(update.message.from_user.first_name))
	logger.info("Contact of %s: %I", a.first_name, a.phone_number)
	
def chatter(bot,update):
    try:
	chat_id = update.message.chat_id
	message = update.message.text
	a = message
	b = a.lower()
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
    try:
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
	
    except (pyowm.exceptions.api_call_error.APICallError):
		update.message.reply_text('Kirem perintah /cuaca <wilayah> untuk teupeu cuaca bak wilayah droeneuh uroe nyoe.'
'\nContoh :\n/cuaca Geudong\n/cuaca Lhokseumawe')
	
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
'\nContoh :\n/shalat Geudong\n/shalat Lhokseumawe\n/shalat Politeknik Negeri Lhokseumawe')

def kurikulumtrkj(bot, update):
    """Send a message when the command /itong is issued."""
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User type kurikulum : %s", user.first_name)
    if message == '/semester1':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 1')
		file1='semester1.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file1, 'rb'))
    elif message == '/semester2':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 2')
		file2='semester2.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file2, 'rb'))
    elif message == '/semester3':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 3')
		file3='semester3.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file3, 'rb'))
    elif message == '/semester4':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 4')
		file4='semester4.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file4, 'rb'))
    elif message == '/semester5':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 5')
		file5='semester5.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file5, 'rb'))
    elif message == '/semester6':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 6')
		file6='semester6.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file6, 'rb'))
    elif message == '/semester7':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 7')
		file7='semester7.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file7, 'rb'))
    elif message == '/semester8':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kurikulum Semester 8')
		file8='semester8.jpg'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=open(file8, 'rb'))
    else:
		update.message.reply_text('Kurikulum Program Studi Teknologi Rekayasa Komputer Jaringan\nJurusan Teknologi Informasi dan Komputer\nPoliteknik Negeri Lhokseumawe')
		update.message.reply_text('Dimiyub nyoe daftar kurikulum per semester prodi TRKJ :\n/semester1. Kurikulum Semester 1\n/semester2. Kurikulum Semester 2\n/semester3. Kurikulum Semester 3\n/semester4. Kurikulum Semester 4\n/semester5. Kurikulum Semester 5\n/semester6. Kurikulum Semester 6\n/semester7. Kurikulum Semester 7\n/semester8. Kurikulum Semester 8')

def dosentrkj(bot, update):
    """Send a message when the command /itong is issued."""
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User type dosentrkj : %s", user.first_name)
    if message == '/dosen1':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-Uqy18HfZIzk/WkD-blyTanI/AAAAAAAAAWI/YDSr0avY6Qoy4mMBso4lSrtMthyI7qodACLcBGAs/s320/Amri.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Amri, SST., M.T'
													 '\nJenis Kelamin : Laki-laki'
													 '\nNIP : 19720202 200012 1 001'
													 '\nNIDN : 0002027212'
													 '\nE-mail : amriaceh72@gmail.com'
													 '\nNomor Telepon / HP : 085261953317'
													 '\nAlamat Kantor : Jln. Banda Aceh Medan Km. 280, Buketrata'
													 '\nNomor Telepon / Fax : 0645-41626')
    elif message == '/dosen2':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-ApX6fiWwVPA/WkD-bjqqUvI/AAAAAAAAAWE/OaWVBw0q4HY0wt3wZNenMg7dEDoR-9irwCLcBGAs/s320/Aswandi.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Aswandi, S.Kom, M.Kom'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional Akademik : Lektor (AK 300) / IIId'
													  '\nJabatan Struktural	: Dosen'
													  '\nNIP : 19720924 201012 1 001'
													  '\nNIDN : 0024097203'
													  '\nE-mail : aswandi@pnl.ac.id'
													  '\nNomor Telepon / HP : 082362851406'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : (0645) 42670 / 42785'
													  '\nMata Kuliah yang Diampu :\n1.  Keamanan Jaringan\n2. Proyek Sistem Jaringan\n3. Jaringan Nirkabel\n4. Jaringan Lanjutan')
    elif message == '/dosen3':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-pJdpyXKXo6g/WkD-iDDZYHI/AAAAAAAAAWk/i_b3MqJOjiogdOvg6agNdKjfPHvYMGy6QCLcBGAs/s1600/Mursyidah.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Mursyidah, ST, MT'
													  '\nJenis Kelamin : Perempuan'
													  '\nJabatan Fungsional : Asisten Ahli'
													  '\nJabatan Struktural	: Ka. Lab Teknologi Komputer Vision'
													  '\nNIP : 	19730105 199903 2 003'
													  '\nNIDN : 0005017304'
													  '\nE-mail : Mursyidahpoli@gmail.com'
													  '\nNomor Telepon / HP : 0852-7763-3000'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Pemodelan dan Simulasi\n2. Isu dan Profesional Teknik Komputer\n3. Grafika Komputer dan Multimedia\n4. Pemodelan 3 Dimensi\n5. Sistem Cerdas\n6. Interaksi Manusia dan Komputer')
    elif message == '/dosen4':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-ISvYes-NPHU/WkD-fW0EE6I/AAAAAAAAAWc/Hh13uuwzB8g1n4oVfJoAYuPcVIzEBvOhACLcBGAs/s200/Husaini.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Husaini, S.Si, M.IT'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : III D/Lektor'
													  '\nNIP : 	19731031 200112 1001'
													  '\nNIDN : 0031107303'
													  '\nE-mail : husaini@pnl.ac.id'
													  '\nNomor Telepon / HP : 085296131985'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Multimedia Technology\n2. Rekayasa Perangkat Lunak\n3. Basis Data\n4. Struktur Data 3 Dimensi\n5. Pemrograman C++\n6. Matematika Terapan')
    elif message == '/dosen5':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-DyAHhm7ZtPA/WkD-idIENJI/AAAAAAAAAWo/KOYGbsWY3h40DbLIrL4T1g9ZF8PGLXthACLcBGAs/s200/M_Nasir.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Muhammad Nasir, ST, MT'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Lektor'
													  '\nNIP : 	19750707 199903 1 002'
													  '\nNIDN : 0007077505'
													  '\nE-mail : masnasir.tmj@gmail.com'
													  '\nNomor Telepon / HP : 0811-671684'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Pengolahan Citra Digital\n2. Pengolahan Sinyal Digital\n3. Embedded System\n4. Elektronika Telekomunikasi\n5. Bahasa Assembly\n6. Rangkaian Logika\n7. Konsep dan Teknologi Informasi\n8. Teknik Riset\n9. Jaringan Komputer\n10. Sistem Pengaturan Komputer')
    elif message == '/dosen6':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-bt0dSspBPo0/Wv0gBAgqI6I/AAAAAAAAAd4/dhxtV9XLw2o2A9ZKdFH690CZMLWfrGYDgCLcBGAs/s1600/Indrawati.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Indrawati, SST, MT'
													  '\nJenis Kelamin : Perempuan'
													  '\nJabatan Fungsional : Asisten Ahli'
													  '\nNIP : 	19740815 200112 2 001'
													  '\nNIDN : 01-1508-7404'
													  '\nE-mail : windra96@yahoo.com'
													  '\nNomor Telepon / HP : 	0852-6010-6989'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Pemrograman Berorientasi Objek\n2. Pemrograman Komputer\n3. Algoritma dan Pemrograman\n4. Rekayasa Perangkat Lunak\n5. Komunikasi Data\n6. Komputer Grafik\n7. Telematika')
    elif message == '/dosen7':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-WPJkSlPh7C8/WkD-bxOSBgI/AAAAAAAAAWM/M4d1X0t8EEoZPhMRIAHxzmOdMLuxq7sIQCLcBGAs/s320/Anwar.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Anwar, S.Si, M.Cs'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Lektor'
													  '\nNIP : 	197510252001121003'
													  '\nNIDN : 0025107501'
													  '\nE-mail : anwar551@yahoo.com'
													  '\nNomor Telepon / HP :	08126966488'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Konsep Jaringan Komputer\n2. Administrasi Jaringan\n3. Keamanan Jaringan\n4. Aplikasi Komputer Bisnis')
    elif message == '/dosen8':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-6S2MwF6raMM/WkD-d1lQ31I/AAAAAAAAAWQ/FV-Hw9xOq1sBFw13UGzWqTv1PR-RwZcJgCLcBGAs/s320/Atthariq.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Atthariq, S.ST, MT'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Asisten Ahli'
													  '\nNIP : 	197807242001121001'
													  '\nAlamat Rumah : Jl. Buloh Bl. Ara No. 94 Ds. Paya Punteut'
													  '\nE-mail : 	atthariq.huzaifah@gmail.com'
													  '\nNomor Telepon / HP : 08116709471'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Computer Vision\n2. Pengolahan Citra\n3. Machine Learning\n4. Data Mining\n5. Jaringan Komputer\n6. Grafika Komputer\n7. Sistem Cerdas')
    elif message == '/dosen9':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-FbKMFcVVEFY/WkD-exuIvwI/AAAAAAAAAWU/Oi83uYuHagIicBM1DAPT6BJccCcfo_9OQCLcBGAs/s200/Hari%2BToha.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Hari Toha Hidayat, S.Si, M.Cs'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Asisten Ahli'
													  '\nJabatan Struktural : Kepala Laboratorium Rekayasa Sistem dan Software'
													  '\nNIP : 	198510142014041001'
													  '\nAlamat Rumah : Jl. Peutua Rumoh Rayeuk Gg Bidan No 107'
													  '\nE-mail :	haritoha@pnl.ac.id'
													  '\nNomor Telepon / HP : 081357389239'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Rekayasa Perangkat Lunak\n2. Computer Vision\n3. Pemrograman Berorientasi Objek\n4. Basis Data')
    elif message == '/dosen10':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-FsybV5ZkJrY/Wv0gZjOlITI/AAAAAAAAAec/3Qt_KCHO57g-lLX9_zhHP60OwXZ3ZZbygCLcBGAs/s1600/Pak-Arhami.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Muhammad Arhami, S.Si, M.Kom'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Lektor'
													  '\nNIP : 	19750707 199903 1 002'
													  '\nNIDN : 0007077505'
													  '\nE-mail : 	muhammad.arhami@gmail.com'
													  '\nNomor Telepon / HP : 08121582408'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	TELP. +62-645-45363,FAX. +62-645-45363')
    elif message == '/dosen11':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-nNtZOS8vO-U/Wv0hCxuZyAI/AAAAAAAAAfU/WofRzTndkUEvVbilfIsaPeQ9_rKsx1B-QCLcBGAs/s1600/Zulfan.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Zulfan Khairil Simbolon, ST, M.eng'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Lektor Kepala'
													  '\nNIP : 	19690902 199303 1 004'
													  '\nNIDN : 0002096906'
													  '\nE-mail : 	zulfan69@gmail.com'
													  '\nNomor Telepon / HP : 08126538848'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Pengenalan Pola\n2.  Keterampilan Komputer\n3. Bahasa Assembly\n4. Teori Bahasa Automata\n5.  Mikroprosessor\n6. Praktikum Mikroprosessor\n7. Matematika Diskrit\n8.  Interaksi Manusia dengan Komputer')
    elif message == '/dosen12':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-LgCv9cE4yp0/Wv0gnXsarUI/AAAAAAAAAe0/QA86HSWOMsQf_tcxWhQkccYsb-NNWWLmgCLcBGAs/s1600/Salahuddin.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Salahuddin, ST, M.Cs'
													  '\nJenis Kelamin : Laki-laki'
													  '\nJabatan Fungsional : Lektor'
													  '\nNIP :	19740424200212 100 1'
													  '\nNIDN : 0024047404'
													  '\nE-mail : 	salahuddintik@pnl.ac.id'
													  '\nNomor Telepon / HP : 081362565454'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax :	(0645) 42760/42785'
													  '\nMata Kuliah yang Diampu :\n1. Basis Data dan Praktikum\n2. Sistem Informasi Berbasis Web\n3. Sistem Informasi Geografis\n4. Jaringan Komputer\n5. Pemrograman Berbasis Objek\n6. Rekayasa Perangkat Lunak\n7. Pemrograman Berbasis Objek Lanjutan\n8. Pemrograman Berbasis Mobile')
    elif message == '/dosen13':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-wUQnMhJe084/XMMdQuldC9I/AAAAAAAAASA/k5ckmtkd1o0VwhZn4WlYPg-FPTAXDFr-gCLcBGAs/s320/fachri.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Fachri Yanuar Rudi F, MT'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP :	19880106 201803 1 001'
													  '\nNIDN : 1306018801'
													  '\nBidang Keahlian : Computer Vision dan Multimedia'
													  '\nAlamat Rumah : Jln. H.Meunasah  Komp.mol No.99D Uteunkot Kec.Muara Dua Lhokseumawe'
													  '\nE-mail : 	Fachri@pnl.ac.id'
													  '\nNomor Telepon / HP : 0852 7046 7045'
													  '\nMata Kuliah yang Diampu :\n1. Computer Vision\n2. Pengolahan Citra\n3. Grafika Komputer dan Multimedia\n4. Pemodelan 3D')
    elif message == '/dosen19':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-kC-d44yhde8/WkD-gOdaVhI/AAAAAAAAAWg/Ymo_pNye4Kwfx9iqniy0BZVj0J4RKDayACLcBGAs/s200/Jamilah.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Dra. Jamilah, M.Pd'
													  '\nJenis Kelamin : Perempuan'
													  '\nJabatan Fungsional :	(IV/A) Lektor Kepala'
													  '\nJabatan Struktural : Staf Pengajar'
													  '\nNIP :	19631231 199303 2 004'
													  '\nNIDN : 00-3012-6311'
													  '\nAlamat Rumah : Gampong Blang Peuria, Kec. Samudera, Aceh Utara'
													  '\nNomor Telepon / HP : 082365381053'
													  '\nAlamat Kantor : Politeknik Negeri Lhokseumawe Jl.Banda Aceh - Medan Km 280,3 Buketrata, 24301, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	Telp.(0645)42670'
													  '\nMata Kuliah yang Diampu :\n1. Tata Tulis Laporan\n2. Bahasa Indonesia\n3. Metode Penelitian')
    elif message == '/dosen24':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-1_L82jFEuW4/Wv0g6tn5I2I/AAAAAAAAAfE/pP_FExdEWKUZj64gdMmwsIrmSKchCBLxgCLcBGAs/s1600/Suryati.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Suryati, S.Si.,M.Si'
													  '\nJenis Kelamin : Perempuan'
													  '\nJabatan Fungsional :	Lektor/IIIC'
													  '\nNIP :	197909182002122002'
													  '\nNIDN : 0018097001'
													  '\nE-mail : suryati_zya@yahoo.com'
													  '\nNomor Telepon / HP : 085260659941'
													  '\nAlamat Kantor : Jl.Banda Aceh - Medan Km 280,3 Buketrata, Lhokseumawe'
													  '\nNomor Telepon / Fax : 	0645-42670 / 0645-42785'
													  '\nMata Kuliah yang Diampu :\n1. Fisika Terapan\n2. Matematika\n3. Aljabar Linier')
    elif message == '/dosen26':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-oLfRSXro25M/XIPbR3oXEDI/AAAAAAAAAQg/CDWsBf74jgcIaeX6gkQchryu73RO_87HQCLcBGAs/s1600/tirta.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Said Arif Tirtana, S.Tr.T'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : -'
													  '\nNIDN : -'
													  '\nBidang Keahlian : -'
													  '\nAlamat : Dsn. Teuladan. Desa Blang Paun Dua. Kec.julok Kab. ATIM'
													  '\nNomor Telepon / HP : 0822 7607 6055'
													  '\nE-mail : Tirtanaabbas@gmail.com'
													  '\nMata Kuliah yang Diampu : Keamanan Jaringan')
    elif message == '/dosen27':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-JouWUK6cjf8/XIPo7J6sDdI/AAAAAAAAAQs/J5Yup1kH0ls8eSMSiZbCu06iL8YxiH_OQCLcBGAs/s1600/taufik.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Taufik, SST'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : -'
													  '\nNIDN : -'
													  '\nBidang Keahlian : IOT, PCD'
													  '\nAlamat : Desa Beunot, Syamtaura Bayu A.Utara'
													  '\nNomor Telepon / HP :	0823 9714 1289'
													  '\nE-mail : Taufikprogram42@gmail.com'
													  '\nMata Kuliah yang Diampu : Embedded Arduino, IOT')
    elif message == '/dosen28':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-8VBS-BqrAmA/XIPsvjZoLOI/AAAAAAAAAQ4/SvAbC4cAguc-2TYZWu70niv0TmbIZILVQCLcBGAs/s1600/haries.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Muhammad Haries, SST'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : -'
													  '\nNIDN : -'
													  '\nBidang Keahlian :	Jaringan'
													  '\nAlamat : Lr. Ulee Gajah Dsn. A Bahagia, Panggoi'
													  '\nNomor Telepon / HP :	0822 7607 6055'
													  '\nE-mail : muhammadhariespnl@gmail.com'
													  '\nMata Kuliah yang Diampu :\n1. Jaringan dasar komputer\n2. Jaringan Nirkabel\n3. Database\n4. Operating Sistem')
    elif message == '/dosen29':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-QbsPXNG56yk/XIU3OZkcoRI/AAAAAAAAARI/rOWrTF0wlxUr9ZrutSfnM4tD3vmOw6TkwCLcBGAs/s1600/saidmahfud.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Said Mahfud, S.Tr.T'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : -'
													  '\nNIDN : -'
													  '\nBidang Keahlian :	Jaringan Komputer'
													  '\nAlamat : Hagu Selatan, Lhokseumawe'
													  '\nNomor Telepon / HP :	0823 6780 4476'
													  '\nE-mail : Saidmahfud02@gmail.com'
													  '\nMata Kuliah yang Diampu :\n1. Prak. Jarinagn Nirkabel\n2. Prak.Interaksi manusia & komputer')
    elif message == '/dosen30':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-mwthXDsT2c0/XLNk1NDMVXI/AAAAAAAAARk/lkfQTI6T7Fsrin1I84-JiujO5VGyCwucQCLcBGAs/s320/mudya.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Mudhyafuddin, SST'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : -'
													  '\nBidang Keahlian :	Multimedia dan Jaringan'
													  '\nNomor Telepon / HP :	0821 6842 9030'
													  '\nE-mail : mudhyafuddin28@gmail.com'
													  '\nMata Kuliah yang Diampu :\n1. Mobile System\n2. Prak.Sistem Pengaturan Komputer 2')
    elif message == '/dosen31':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-scczORXDuHg/XLwzbyMgrOI/AAAAAAAAAR0/Nl9fkFGQszsTl3_IvdvwnCpZag5cCDZEQCLcBGAs/s1600/nanada.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Nanda Saputri, SST,MT'
													  '\nJenis Kelamin : Perempuan'
													  '\nNIP : -'
													  '\nBidang Keahlian :	Pengolahan Citra'
													  '\nNomor Telepon / HP :	-'
													  '\nE-mail : nandasaputri24@gmail.com'
													  '\nMata Kuliah yang Diampu :\n1. Pengenalan PDA\n2. Kecerdasan Buatan\n3. Grafika Komputer\n4. Pengolahan Sinyal Digital\n5. Pengolahan Citra Digital')
    elif message == '/dosen14':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-KpaXwpPTqgQ/Wv0gDO92TPI/AAAAAAAAAd8/YN7uGFT20u07_whjEINm5x8SDivFYmr9ACLcBGAs/s1600/Ipan.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Ipan Suandi, S.T., M.T'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19800510 200501 1 002')
    elif message == '/dosen15':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-XW_NuHUJQLM/Wv0giZ5mgNI/AAAAAAAAAek/28Npz3ze3vAjTwY7YYbEepxpTjFcQfa9QCLcBGAs/s1600/Rachma.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Rachmawati, S.T., M. Eng'
													  '\nJenis Kelamin : Perempuan'
													  '\nNIP : 19790826 200312 2 001')
    elif message == '/dosen16':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-kBCUmMH1Ezs/Wv0f4orCJgI/AAAAAAAAAdo/82nmgN0vhuAuT8R7G2doKTBFQsoePYp4gCLcBGAs/s1600/Aidi.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Aidi Finawan, S.T., M. Eng'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19740619 200012 1 003')
    elif message == '/dosen17':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-MIPVN7-JlDk/Wv0gjtE4iNI/AAAAAAAAAes/t9lVMvX7KVoHjAeR5c98h821vTg-hVqGgCLcBGAs/s1600/Rusli.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Rusli, S.ST., M.T'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19740327 200003 1 001')
    elif message == '/dosen18':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-KvACoLi1gyE/Wv0gTYGf8dI/AAAAAAAAAeQ/UGrM4KwZCFIMpk5MqPO5ysQcZSD7GDubACLcBGAs/s1600/Nelli.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Nelly Safitri, S.ST., M.Eng.Sc., Dr.'
													  '\nJenis Kelamin : Perempuan'
													  '\nNIP : 19780121 200212 2 002')
    elif message == '/dosen20':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-LB--QLQVkh8/Wv0gfrHTMrI/AAAAAAAAAeg/APd-XcZs-y0bG8gHZIRe491uMJ7MACT7QCLcBGAs/s1600/Novi.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Novi Quintena Rahayu, S.H., M.H.'
													  '\nJenis Kelamin : Perempuan'
													  '\nNIP : 19821118 201012 2 002')
    elif message == '/dosen21':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-kEARpH0-mkQ/Wv0gH7UryBI/AAAAAAAAAeE/zG3rk8RvhFse5HrX18VT-MfpEJ1UCjtEQCLcBGAs/s1600/Nasir.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Muhammad Nasir, S.Pd., M.Pd'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19720621 200112 1 001')
    elif message == '/dosen22':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-oL-WJZE5h4U/Wv0gWZMMKdI/AAAAAAAAAeY/Ik8_ZZyb07ohAkX_wFVYxh-HcgW0RItfACLcBGAs/s1600/Nurdan.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Drs. H. Nurdan, M.Ag'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19611110 199303 1 002')
    elif message == '/dosen23':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-eCfnCN_H6qg/Wv0g7CyLwXI/AAAAAAAAAfI/UQUeG1ekJ6Yq8k2FQ5OaNHZedtivJ4kFwCLcBGAs/s1600/Suherman.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Suherman, S.Si., M.Si'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19730725 200112 1 003')
    elif message == '/dosen25':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-AEmwheD8Oj4/Wv0g7bJudII/AAAAAAAAAfM/xnE7jQ0I80A99wOKv7NVXEmkLtphEnn0ACLcBGAs/s1600/Syahroni.png')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Nama Lengkap dan Gelar : Muhammad Syahroni, S.T., M.T'
													  '\nJenis Kelamin : Laki-laki'
													  '\nNIP : 19721026 200604 1 001')
    else:
		update.message.reply_text('Daftar Nama Dosen\nProgram Studi Teknologi Rekayasa Komputer Jaringan\nJurusan Teknologi Informasi dan Komputer\nPoliteknik Negeri Lhokseumawe')
		update.message.reply_text('Dimiyub nyoe daftar nan dosen prodi TRKJ :\n/dosen1. Amri, SST., M.T\n/dosen2. Aswandi, S.Kom., M.Kom\n/dosen3. Mursyidah, S.T., M.T\n/dosen4. Husaini, S.Si., M. IT\n/dosen5. Muhammad Nasir, S.T., M.T\n/dosen6. Indrawati, SST., M.T\n/dosen7. Anwar, S.Si., M.Cs\n/dosen8. Atthariq, SST., M.T\n/dosen9. Hari Toha Hidayat, S.Si., M.Cs\n/dosen10. Muhammad Arhami, S.Si., M.Kom\n/dosen11. Zulfan Khairil Simbolon, S.T., M.Eng\n/dosen12. Salahuddin, SST., M.T\n/dosen13. Fachri Yanuar Rudi F, MT\n/dosen14. Ipan Suandi, S.T., M.T\n/dosen15. Rachmawati, S.T., M. Eng\n/dosen16. Aidi Finawan, S.T., M. Eng\n/dosen17. Rusli, SST., M.T\n/dosen18. Nelly Safitri, SST., M.Eng.Sc., Dr.\n/dosen19. Dra. Jamilah, M.Pd\n/dosen20. Novi Quintena Rahayu, S.H., M.H.\n/dosen21. Muhammad Nasir, S.Pd., M.Pd\n/dosen22. Drs. H. Nurdan, M.Ag\n/dosen23. Suherman, S.Si., M.Si\n/dosen24. Suryati, S.Si., M.Si\n/dosen25. Muhammad Syahroni, S.T., M.T\n/dosen26. Said Arif Tirtana, S.Tr.T\n/dosen27. Taufik, SST\n/dosen28. Muhammad Haries, SST\n/dosen29. Said Mahfud, S.Tr.T\n/dosen30. Mudhyafuddin, SST\n/dosen31. Nanda Saputri, SST, MT')
		
		
def ruangbelajartik(bot, update):
    """Send a message when the command /itong is issued."""
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User type ruangbelajartik : %s", user.first_name)
    if message == '/ruangbelajar1':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 1')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-g6leiu3WjR4/W1AQcWULiOI/AAAAAAAAAlk/rIVrbN21ahw0VLfb01AtcVb5QynfFtZTACLcBGAs/s640/RUANG-TIK-01_2.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-tHqZpXqcVTM/W1AQoHmuRbI/AAAAAAAAAls/VlGyUug21O8Jrwun3k-FJAOqfsC5hI_4gCLcBGAs/s640/RUANG-TIK-01_3.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-gVCR2tbYulk/W1ATdLAgP6I/AAAAAAAAAmE/1UjMPN8qAl8ak4SWbbCnEIZWyZtjsyoFACLcBGAs/s640/RUANG-TIK-01_4.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-MGM3vAMu_5k/W1ATc-Hk5UI/AAAAAAAAAmA/e2hZATiQJys4BIu3jMbcv23orsfJddzjgCLcBGAs/s640/RUANG-TIK-01_5.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-JW4OSTMdsx4/W1ATdbXpmXI/AAAAAAAAAmI/mtEYEsqvJ9IOB_1JmykqKE1elq0QZtBGwCLcBGAs/s640/RUANG-TIK-01_6.JPG')
    elif message == '/ruangbelajar2':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 2')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-AYiQg-vJ09g/W1Bh-x5WoYI/AAAAAAAAAqQ/uNNiQt7b7eMEe-VKjDGMq1C7KIS585GLgCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-HUF5AWiejOA/W1Bh-Pb7CyI/AAAAAAAAAqI/kKfKuY_l7mQR49V0qV55X_WScpZFSNoiwCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-g8Lq5Sd1e-c/W1BiMW3suMI/AAAAAAAAAqc/EetjZsIIR7UHKEyyFpvXFyns8iiWUtifACLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-g8Lq5Sd1e-c/W1BiMW3suMI/AAAAAAAAAqc/EetjZsIIR7UHKEyyFpvXFyns8iiWUtifACLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-oJfnNt2gz6g/W1BiN9myXhI/AAAAAAAAAqg/10jrRABXPhsQdVBERR0mmIA2-kpmHKkRwCLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar3':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 3')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-Nf13X-s-5pw/W1BigQMzT8I/AAAAAAAAArE/Ugao5C_UwiMhPi5bnFPzVE8RTYo-Tz-JACLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-VEVrTGG6oPM/W1BigFZRFFI/AAAAAAAAAq8/5u1zMEwl4joMCJjyreSmwOVyLjdfORrvACLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-e5bHXXqOa5E/W1Bit0nxySI/AAAAAAAAArM/1gV9Vu3FKSAIUhBD3J-qc3ApLjNAqlDhACLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-G88C2WPNSAo/W1Biu6hRB0I/AAAAAAAAArU/zar9RXe-qsAquE7WQUAWDhhCEg5TIlkNwCLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-aSNzpKukCZU/W1BiuG11tGI/AAAAAAAAArQ/fnyNTIN9vgUKqOpQte9bAVy0cX6FNURLgCLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar4':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 4')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-EktdY81dBMY/W1Bj9L1V-rI/AAAAAAAAAsQ/otTEo_6GWaIoHohYva-8OCCSZaOysQK9gCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-Y5Htw7YhsJ4/W1BkB35t-CI/AAAAAAAAAsc/qmDSmaM8JrgeYh20J-FaFg2R_742I2iHQCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-Ei5XxPeB06o/W1BkYLTVKzI/AAAAAAAAAtE/e0ONLAk403AGPHq4S-dmAvuDKHNYgivOwCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-0CeXZLG6iYU/W1BkauxDhBI/AAAAAAAAAtI/dm3WgJ2UR1Mp_HmrcR5WATnxFm5IfNVkQCLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar5':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 5')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-XjOwNG_l_OE/W1Bjg_vVB1I/AAAAAAAAArw/a8hBBT2vR-89TdfQiKE1hieWdN8057MRwCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-wm49iRo-r9Q/W1BjgsoXdeI/AAAAAAAAArs/XPFWW4sHC5QYxaxpdU0UfwIITAR5cabzACLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-ze4Mvxp7wVE/W1BjzVXXNmI/AAAAAAAAAsE/DldaHrm7jnkycOXR-EDYhsDOJq76788twCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-YaM_YDNTvUM/W1Bj01uP_yI/AAAAAAAAAsI/nbmiqSRwaRQZ1DXL9ymIkTgdm_HGpoASACLcBGAs/s640/RUANG-TIK-05.JPG')
    elif message == '/ruangbelajar6':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 6')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-Oh9ImLjeuKo/W1BkWqqatCI/AAAAAAAAAs4/RISXrVfl5ZMUfSUr7aPtsTaYz46ZZ-CFwCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-iJvhotYWkQI/W1Bkit_x09I/AAAAAAAAAtU/P2WaiRMbwpIfPt4TBqSXH8-AaiRLvErYgCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-oZ3GPnExtjk/W1BkjrCd93I/AAAAAAAAAtg/BsRBe7KdyqUvmvfMsPVlvZC6WqrU0oI4wCLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-zhTK195wPYQ/W1Bkn7VuHGI/AAAAAAAAAtk/uEA4-ltZG70cIna3LiFzm15JfheSCo64QCLcBGAs/s640/RUANG-TIK-07.JPG')
    elif message == '/ruangbelajar7':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 7')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-cVxgczyO5po/W1BoIe7FjUI/AAAAAAAAAvo/G6RauG6qV88dRPK7qtHkjYauGW_FtVCsQCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-zbc_PdZPEbI/W1BoJA6U9YI/AAAAAAAAAvs/YzDVL969-mkhD3RNtxjJCQBMrsTZ-uiygCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-DhMLRcM_WVw/W1Bo7li7H_I/AAAAAAAAAws/PzJ9CXpKhXs3t-r3_m-mhfS28XxFOftiQCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-ac4sgVIGbkw/W1BpELb5mMI/AAAAAAAAAxA/N392bT3uaaABT-24HPEvjBgSgJ7m1h5ZQCLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar8':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 8')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-Eby3XCzmmzE/W1BlcHNQjKI/AAAAAAAAAuI/CvOXNe7lTD0lRZtPJooohJPOPJJMUxf-QCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-RTK2RQ66DCM/W1BlcR8HHfI/AAAAAAAAAuQ/bjfRQkHOF7wnyc8va8cPC5LWTDEuYVXxQCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-KEmUSkoukAQ/W1Blu-qacqI/AAAAAAAAAuk/pIJPhBnGEVUk307ZfbQlczxW3K6iL2t1QCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-CYtB9k3RBLo/W1Blw8FPDkI/AAAAAAAAAuo/nekx4I5tRVw1n_SgGsNooLgDWv_kYrSBwCLcBGAs/s640/RUANG-TIK-05.JPG')
    elif message == '/ruangbelajar9':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 9')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    elif message == '/ruangbelajar10':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 10')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-V0N-hO8dsYE/W1BoSw2OjII/AAAAAAAAAwQ/Ih2gORqPKFAV6TbWrVsPoV0Xx8iMDBsMACPcBGAYYCw/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-zbc_PdZPEbI/W1BoJA6U9YI/AAAAAAAAAwQ/lENXJtPXCTItB31A-94eZDj7QRscc_vMgCPcBGAYYCw/s640/RUANG-TIK-03.JPG')
    elif message == '/ruangbelajar11':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 11')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-fBvCukCxBUE/W1Bo0ChHXLI/AAAAAAAAAwg/S3t8dtmVB_czkOfL24-AgrJ0WcavJMb3ACLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-eZp4Z4OoRzc/W1BouZEvq4I/AAAAAAAAAwY/X9LX4vI3jAAeVNqocT_JPkLIXPwfyPj-ACLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-tlFSneBxrWQ/W1BpM6yS_RI/AAAAAAAAAxM/auMt1n1xIgkRXxW9r2KuzK7Wrs3q-LVtgCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-bjbvWqKOUgs/W1BpNO2S9pI/AAAAAAAAAxQ/aI8kTbBOr4MujMXKdqvjYwfyIdbjp95GACLcBGAs/s640/RUANG-TIK-05.JPG')
    elif message == '/ruangbelajar12':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 12')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-z1_5af9u4qg/W1CLsUX5WhI/AAAAAAAAA2U/W-tbtcqubj0YuUXHhkBimuNd5A2XLhALACLcBGAs/s640/RUANG-KULIAH-TIK-1.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-yPnmyKDsNQM/W1CLsWErhmI/AAAAAAAAA2c/QGzLyhWbwCwxyg3sky6nbdhr6otN9Lo8ACLcBGAs/s640/RUANG-KULIAH-TIK-2.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-lAnasuMriE0/W1CLsamw5BI/AAAAAAAAA2Y/_SegZUvb-b0A7B8tJbkA88T-2ipQeNeYgCLcBGAs/s640/RUANG-KULIAH-TIK-3.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-kFYe5oss5hM/W1CL2Gu_t3I/AAAAAAAAA2k/6oqr5EPixzQ9hf4svDUKbjWGIJyxA20XQCLcBGAs/s640/RUANG-KULIAH-TIK-4.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-uAD-P0hwfno/W1CL134F_zI/AAAAAAAAA2g/29NpoJ-5eiUBF8uzRvp2RvuvMmWuH6eMwCLcBGAs/s640/RUANG-KULIAH-TIK-5.JPG')
    elif message == '/ruangbelajar13':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 13')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-3WHosYgyK5I/W1BtrngtwSI/AAAAAAAAAzY/iC6eIlrH5PorrkqGf-c1N2P3U963XTXTgCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-Mg-sMfhGCsA/W1Btn6OLiAI/AAAAAAAAAzQ/OzqvZxluxQERESUOt_W3RtIgVbFUw1hcwCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-w9E0SEhdLHY/W1BuCFpEkII/AAAAAAAAAzs/Lx1yl6pCPuMclZXtYOxquInktWkIEL7rACLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-qoz2o5kG9uY/W1BuBFPOH7I/AAAAAAAAAzo/JuNMMY2yKDYswygS8_sr-9cEB2f81wIhwCLcBGAs/s640/RUANG-TIK-05.JPG')
    elif message == '/ruangbelajar14':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 14')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-slKCf5cidmg/W1Bsg0Q0ZJI/AAAAAAAAAyo/WdprPXaxrfgsTMD3e_PYpj-IlA7O7pPvQCLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-qaaHfqv92Hw/W1BsbNHaLEI/AAAAAAAAAyg/hxTu-KO1RxI2acwF22Ke3GVDPUQng0sGgCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-4nc95Z3AjJY/W1BsmVnoWoI/AAAAAAAAAys/scmZJLbFOmkxOde9ys8JzmNcNEYa1OtwgCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-GnSyj6Gw4go/W1BsrSL0f5I/AAAAAAAAAyw/qR6D2fWFQF4G9tjpJFIEqUzggO2xOgeKACLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-fuGuclFY1XM/W1BssbR_Q4I/AAAAAAAAAy0/FLfvlciFaiE3i8pyVQIx0pelEqfJVABlwCLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar15':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 15')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-Re6Srb1MVGI/W1BqWTYJwII/AAAAAAAAAyI/o9awbLrr1M8IxWg3wy--Qu1DAWEfydZrQCEwYBhgL/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-RhhRUBtZxLs/W1BqaSUrocI/AAAAAAAAAyU/T-yfqCBJCX4yMyCsNL9el9t64LnqcerBgCEwYBhgL/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-qxPBDh6-nq0/W1Bqj1zjilI/AAAAAAAAAyY/dnJ-B4ntn_wH9Noda5OQOnY58TXNQqYHgCEwYBhgL/s640/RUANG-TIK-07.JPG')
    elif message == '/ruangbelajar16':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 16')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-hPIo-8JeE2U/W1BhUFoDSQI/AAAAAAAAApc/bFM3KtwlQ3IbNGTmwfEOyfLOO8bb_rdHgCLcBGAs/s640/RUANG-TIK-01.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-vvI3eqPrrME/W1BhTZRBCJI/AAAAAAAAApU/CkXfkSEdBPUpsOr0lCb-b-z4F02GvPCrACLcBGAs/s640/RUANG-TIK-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-ri5NGsR73F8/W1BhTgTxCnI/AAAAAAAAApY/ic_Rol8vKXksYzy9f72zvJXFPJ9gqAEoQCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-VFJDQcN9Ny4/W1Bhgfjc8pI/AAAAAAAAApk/xNVxyJj7xr0n3PzlBvCmwKfyNeiLclpQQCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-tGWmXw7fmjA/W1BhhK6-v-I/AAAAAAAAApo/EqFBdsDgn1cb6gOdTbwL6otrGXxsrpZ6QCLcBGAs/s640/RUANG-TIK-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-OQ8z4JQNip4/W1Bhh8jZ6eI/AAAAAAAAAps/MlALJdP8BiYpLctTIczbCCVnwlEWSBwqACLcBGAs/s640/RUANG-TIK-06.JPG')
    elif message == '/ruangbelajar17':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 17')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-Re6Srb1MVGI/W1BqWTYJwII/AAAAAAAAAxs/kj2KxnxysfUE-geTgxqcBsbkkuuRQg_oQCLcBGAs/s640/RUANG-TIK-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-RhhRUBtZxLs/W1BqaSUrocI/AAAAAAAAAxw/mu6xQHpahOEsWrsVtlTebxv0aA7MeCF_QCLcBGAs/s640/RUANG-TIK-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-bUOkdnIwhvk/W1Bqh0cC25I/AAAAAAAAAyA/HUxe5e72MSoGV2FVkWWgp890GrKjeLXRgCLcBGAs/s640/RUANG-TIK-06.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-qxPBDh6-nq0/W1Bqj1zjilI/AAAAAAAAAyE/EEkxtd5q0o8jB_30_ZJaPNRSxaH2r0kYwCLcBGAs/s640/RUANG-TIK-07.JPG')
    elif message == '/ruangbelajar18':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 18')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    elif message == '/ruangbelajar19':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Ruang Belajar 19')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    else:
		update.message.reply_text('Fasilitas Ruang Belajar Mahasiswa\nProgram Studi Teknologi Rekayasa Komputer Jaringan\nJurusan Teknologi Informasi dan Komputer\nPoliteknik Negeri Lhokseumawe')
		update.message.reply_text('Dimiyub nyoe daftar ruang belajar prodi TRKJ :\n/ruangbelajar1. Gedung Lobi Lantai 1 Sayap Kanan, Jurusan TIK\n/ruangbelajar2. Gedung Lobi Lantai 1 Sayap Kanan, Jurusan TIK\n/ruangbelajar3. Gedung Lobi Lantai 1 Sayap Kanan, Jurusan TIK\n/ruangbelajar4. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar5. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar6. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar7. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar8. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar9. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar10. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar11. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar12. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK\n/ruangbelajar13. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar14. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar15. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar16. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar17. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar18. Gedung Lobi Lantai 2 Sayap Kanan, Jurusan TIK\n/ruangbelajar19. Gedung Lobi Lantai 3 Sayap Kanan, Jurusan TIK')

def labtik(bot, update):
    """Send a message when the command /itong is issued."""
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User type lab : %s", user.first_name)
    if message == '/lab1':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Komputer Vision')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Mahdi, ST., M.Cs\nTeknisi Laboratorium: Ramadhona, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Lab-Komputer-Vision_04-768x576.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Lab-Komputer-Vision_01-768x576.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Lab-Komputer-Vision_02-768x576.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Lab-Komputer-Vision_03-768x576.jpg')
    elif message == '/lab2':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Broadcasting Multimedia')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Atthariq, SST. MT\nTeknisi Laboratorium: Mudhiyafuddin, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-ForWhfaImHM/WzoTtAY8fvI/AAAAAAAAAgY/pEU6RgECwF48OTlTDc_GpUkzdt6PXaBUgCLcBGAs/s640/Lab-Broadcasting-Multimedia-01.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-em6BiGKxa4g/WzoTuL01utI/AAAAAAAAAgg/lYmobiyv04U854YKy4KOgJjrWJFJKc4rwCLcBGAs/s640/Lab-Broadcasting-Multimedia-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-FJkWTmDSHlg/WzoTtbe4bAI/AAAAAAAAAgc/NiSFdVjtDUkL4aGr03m9X98F2a--Nm5UACLcBGAs/s640/Lab-Broadcasting-Multimedia-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-E5g2luyE2b0/WzoTz7MNZ4I/AAAAAAAAAgk/w8u_Chn-HwgebPO7leOdS3D9BnL-sGIUQCLcBGAs/s640/Lab-Broadcasting-Multimedia-04.JPG')
    elif message == '/lab3':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Sistem Operasi dan Sistem Komputer')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Hendrawati, ST. MT\nTeknisi Laboratorium: Yuyun Anisfu, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Laboratorium-Sistem-Operasi-dan-Komputer-02-768x511.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Laboratorium-Sistem-Operasi-dan-Komputer-03-768x511.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/07/Laboratorium-Sistem-Operasi-dan-Komputer-04-768x511.jpg')
    elif message == '/lab4':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Information Processing')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Zulfan Khairil Simbolon, S.T., M.Eng\nTeknisi Laboratorium: Ibnu Khaldun, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-8R3vEfCOUHM/WzoWML6v3sI/AAAAAAAAAhU/1abPRaYKaMA8BpFSfKFC0KS2kshAnzASwCLcBGAs/s640/IP01.jpeg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-FjF5OgJ7XH8/WzoWMF8pq9I/AAAAAAAAAhQ/5JMLqy4nM5MwLtGpORE7OZEkDFve8ycNwCLcBGAs/s640/IP02.jpeg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-LphZM9kJMRk/WzoWMVfl4FI/AAAAAAAAAhY/7Pb9WXHao0kMVrNG8428njPot9i7SECWACLcBGAs/s640/IP03.jpeg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-mQ_qoIN26cI/WzoWMxf7xGI/AAAAAAAAAhc/rh9Hh6-7rPM8XilNMrus4IbHEI6Mf7V-wCLcBGAs/s640/IP04.jpeg')
    elif message == '/lab5':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Teknologi Komputer')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Muhammad  Nasir, ST. MT\nTeknisi Laboratorium: Taufik, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. CCTV\n4. Modul Arduino\n5. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-2gtBedTqFk4/W0DPFb-ktzI/AAAAAAAAAh8/XhSYU4f320APU_Ws8h_dkjhInr0nKxakgCLcBGAs/s640/Lab-Teknologi-Komputer-01.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-AHPDWyZINAc/W0DPI6qfy5I/AAAAAAAAAiA/eXXyEFf0FTIlCGNDobJQpnB9sZHXh7yKACLcBGAs/s640/Lab-Teknologi-Komputer-02.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-CAv10NCRZUM/W0DPE4SjehI/AAAAAAAAAh4/kNBoDOl7mBUUQ0WnaqpSVisnMbrw8T31QCLcBGAs/s640/Lab-Teknologi-Komputer-03.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-INd2fQpME2U/W0DPZjZ8kTI/AAAAAAAAAiM/EU0YQseodAwFvuWVQR8Guf5ToSzNgFYjACLcBGAs/s640/Lab-Teknologi-Komputer-04.jpg')
    elif message == '/lab6':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Jaringan dan Multimedia')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Aswandi, S.Kom. M.Kom\nTeknisi Laboratorium: Muhammad Haries, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. Modul MikroTik\n4. AC\n5. CCTV')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-3gm9kRQzAjA/W0DVF0_duYI/AAAAAAAAAiY/bOw9OQdhxH0AIYWlMxlIdtWOioc9m89pwCLcBGAs/s640/Lab-Jaringan-dan-Multimedia-02.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://1.bp.blogspot.com/-2V5hF_tvSh4/W0DVW-LP4NI/AAAAAAAAAig/kTYTqkH7tv8ILlLV1Z7vZvHqjIvVPBjbgCLcBGAs/s640/Lab-Jaringan-dan-Multimedia-03.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-XCuhg9-8If8/W0DWIWwVrXI/AAAAAAAAAio/vpIpgSE1jqEIvEE-seMWik6VDuORq_wsgCLcBGAs/s640/Lab-Jaringan-dan-Multimedia-04.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-fJAhOyjXJYo/W0DZuEuYqXI/AAAAAAAAAi0/YSIXrywJs0keOL9rBJj8q0qpHrIXy-rKgCLcBGAs/s640/Lab-Jaringan-dan-Multimedia-05.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-LP3VC7WhlZU/W0DaERgTYQI/AAAAAAAAAi8/Y8TvECFLY2YoE6aAtGLPsZ_L0v_JtdjkACLcBGAs/s640/Lab-Jaringan-dan-Multimedia-06.JPG')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-s5oAaNmqM5k/W0DaTmtx7eI/AAAAAAAAAjA/JVmCQm8ARDgwL_PZ6esKazCHh8OyEZyjACLcBGAs/s640/Lab-Jaringan-dan-Multimedia_01.JPG')
    elif message == '/lab7':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Telematika')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Azhar, ST., MT\nTeknisi Laboratorium: Irfan Afriadi, A.Md')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-U3PX2A5tan0/W0M2-gByp0I/AAAAAAAAAjU/3WQy91aNwVIxysNta2kxlHsa46du5RukwCLcBGAs/s640/Laboratorium-Telematika-01.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-UKSQIR0LEt8/W0M2_SewAsI/AAAAAAAAAjY/_A0bZM5jJMU4ykiAjNwgYf_0BmS1y3vqACLcBGAs/s640/Laboratorium-Telematika-02.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-ORtBiWlpcA0/W0M29guBtpI/AAAAAAAAAjQ/EAUvI1NksnwES_9iFQgXOY9sP96MOrsGQCLcBGAs/s640/Laboratorium-Telematika-03.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-duAhSDjVqmA/W0M3BFhwhEI/AAAAAAAAAjc/0-0eCUtYj3EFTfzUDOlQlJfh4Pxq1qbBwCLcBGAs/s640/Laboratorium-Telematika-04.jpg')
    elif message == '/lab8':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Rekayasa System dan Software')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Hari Toha Hidayat, S.Si. M.Cs\nTeknisi Laboratorium: Hamzul Azkia, SST')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC\n4. CCTV')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-4Tc0Ia-gbbc/W0M36U8jO7I/AAAAAAAAAjw/LOVaOb-MiF8wITmC4sRybYSbQse15eV8QCLcBGAs/s640/Lab-Rekayasa-Perangkat-Lunak-01.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-p8W8uzl_DXQ/W0M36pC_zpI/AAAAAAAAAj0/ztDDw6-uBGUVNDHNz_lUEZd93PW8Qvm_gCLcBGAs/s640/Lab-Rekayasa-Perangkat-Lunak-02.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://2.bp.blogspot.com/-Nd0RruASuR8/W0M4AyVIVxI/AAAAAAAAAj4/wKBCFeLIkg4ci7x22s0bDiom2IszfgZjQCLcBGAs/s640/Lab-Rekayasa-Perangkat-Lunak-03.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-NyunbBDpFTM/W0M4CGjEFOI/AAAAAAAAAj8/REJrjI-RkTclcg6ekS6V6njAIJgY8lxfQCLcBGAs/s640/Lab-Rekayasa-Perangkat-Lunak-04.jpg')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo='https://3.bp.blogspot.com/-myCZj4F6iMQ/W0M354IKiOI/AAAAAAAAAjs/diZT4vDpPfs93V8N97Jg1xETHtFCyAMhQCLcBGAs/s640/Lab-Rekayasa-Perangkat-Lunak-015.jpg')
    elif message == '/lab9':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Jaringan Telekomunikasi')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Hanafi, ST., M.T\nTeknisi Laboratorium: ')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC\n4. CCTV')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    elif message == '/lab10':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Laboratorium Mikroprosessor & Interface')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Manajemen Laboratorium :\nKepala Laboratorium: Syamsul, ST., M.T\nTeknisi Laboratorium: ')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Fasilitas :\n1. Personal Computer ( PC )\n2. Jaringan WIFI ( Local Area Network ) & Wireless\n3. AC')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Dokumentasi :')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    else:
		update.message.reply_text('Laboratorium Praktikum Mahasiswa\nProgram Studi Teknologi Rekayasa Komputer Jaringan\nJurusan Teknologi Informasi dan Komputer\nPoliteknik Negeri Lhokseumawe')
		update.message.reply_text('Dimiyub nyoe daftar lab jurusan tik :\n/lab1. Komputer Vision\n/lab2. Broadcasting Multimedia\n/lab3. Sistem Operasi dan Sistem Komputer\n/lab4. Information Processing\n/lab5. Teknologi Komputer\n/lab6. Jaringan dan Multimedia\n/lab7. Telematika\n/lab8. Rekayasa System dan Software\n/lab9. Jaringan Telekomunikasi\n/lab10. Mikroprosessor & Interface')

		
def unduh(bot, update):
    """Send a message when the command /itong is issued."""
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    logger.info("User type unduh : %s", user.first_name)
    if message == '/unduh1':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Form Biodata Mahasiswa Baru')
		file1='Form BIODATA-MAHASISWA baru.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file1, 'rb'))
    elif message == '/unduh2':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Form Biodata Alumni Mahasiswa')
		file2='FORM BIODATA  Alumni MHS.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file2, 'rb'))
    elif message == '/unduh3':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Form Bimbingan Akademik - TRKJ')
		file3='FORM BIMBINGAN AKADEMIK - TMJ.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file3, 'rb'))
    elif message == '/unduh4':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Form Kunjungan Perpustakaan')
		file4='FORM_KUNJUNGAN_PERPUSTAKAAN_TMJ.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file4, 'rb'))
    elif message == '/unduh5':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Surat Aktif Kuliah')
		file5='surat aktif kuliah.pdf'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file5, 'rb'))
    elif message == '/unduh6':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Surat Keterangan Izin')
		file6='SURAT KETERANGAN IZIN.pdf'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file6, 'rb'))
    elif message == '/unduh7':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Format Proposal PKL Prodi TRKJ 2019')
		file7='Format-Proposal-PKL-Prodi-TRKJ-2019.rtf'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file7, 'rb'))
    elif message == '/unduh8':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Kontrak Konsul TGA - TRKJ')
		file8='KONTRAK KONSUL TGA  - TMJ.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file8, 'rb'))
    elif message == '/unduh9':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Label CD TRKJ')
		file9='Label CD TMJ.pub'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file9, 'rb'))
    elif message == '/unduh10':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Lembar Pengesahan Pembimbing TGA')
		file10='LEMBAR PENGESAHAN PEMBIMBING TGA.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file10, 'rb'))
    elif message == '/unduh11':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Panduan Penulisan Proposal Tugas Akhir')
		file11='PANDUAN PENULISAN PROPOSAL TUGAS AKHIR.pdf'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file11, 'rb'))
    elif message == '/unduh12':
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendMessage(update.message.chat_id, text='Format Penulisan Buku TGA TMJ')
		file12='FORMAT-PENULISAN-BUKU-TGA-TMJ.docx'
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
		bot.sendDocument(chat_id=chat_id, document=open(file12, 'rb'))
    else:
		update.message.reply_text('Unduh Dokumen ngon File')
		update.message.reply_text('Dimiyub nyoe daftar unduh dokumen ngon file :\n/unduh1. Form Biodata Mahasiswa Baru\n/unduh2. Form Biodata Alumni Mahasiswa\n/unduh3. Form Bimbingan Akademik\n/unduh4. Form Kunjungan Perpustakaan\n/unduh5. Surat Aktif Kuliah\n/unduh6. Surat Keterangan Izin\n/unduh7. Format Proposal PKL Prodi TRKJ 2019\n/unduh8. Kontrak Konsul TGA - TRKJ\n/unduh9. Label CD TMJ\n/unduh10. Lembar Pengesahan Pembimbing TGA\n/unduh11. Panduan Penulisan Proposal Tugas Akhir\n/unduh12. Format Penulisan Buku TGA TMJ')

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
		
def kalenderakademik(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User type kalenderakademik : %s", user.first_name)
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Kalender Akademik Politeknik Negeri Lhokseumawe')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendPhoto(chat_id=chat_id, photo='http://tmj.pnl.ac.id/wp-content/uploads/2018/12/WhatsApp-Image-2018-12-07-at-10.14.55.jpeg')
	
def peraturanakademik(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User type peraturanakademik : %s", user.first_name)
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Peraturan Akademik Politeknik Negeri Lhokseumawe')
	file='Peraturan Akademik - PNL.pdf'
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendDocument(chat_id=chat_id, document=open(file, 'rb'))
	
def strukturpimpinantrkj(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	logger.info("User type strukturpimpinantrkj : %s", user.first_name)
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Struktur Pimpinan Program Studi Teknologi Rekayasa Komputer Jaringan\nJurusan Teknologi Informasi dan Komputer\nPoliteknik Negeri Lhokseumawe')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendPhoto(chat_id=chat_id, photo='https://4.bp.blogspot.com/-SFGiJcJZhoo/W5fCIgjRWTI/AAAAAAAAAPM/RGBjmdvzihcLO8zpXiRKnmR0_SkRCT8mACLcBGAs/s1600/STRUKTUR%2BPRODI%2BTRKJ2.jpg')
	
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Lon lake meu'ah, perintah nyang droeneuh paso hana. Kirem perintah /bantu untuk lon bantu.")	

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))
	
def stop_and_restart():
	"""Gracefully stop the Updater and replace the current process with a new one"""
	restart = Updater("673443169:AAEpuO2XbZcoa7Jw9wZhHyWQIyaGRFi7M8k")
	restart.stop()
	os.execl(sys.executable, sys.executable, *sys.argv)

def restart(bot, update):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text('Dedek Bot ulang balek ...')
    Thread(target=stop_and_restart).start()
		
def main():
    # Create the EventHandler and pass it your bot's token.
    # sara
	#updater = Updater("573130501:AAEtE3qXLGiesj2L2c4v821bvLi2CnTDW8Q")
    #testbot
	updater = Updater("673443169:AAEpuO2XbZcoa7Jw9wZhHyWQIyaGRFi7M8k")
    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("itong", itong))
	dp.add_handler(CommandHandler("kurikulumtrkj", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester1", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester2", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester3", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester4", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester5", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester6", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester7", kurikulumtrkj))
	dp.add_handler(CommandHandler("semester8", kurikulumtrkj))
	dp.add_handler(CommandHandler("labtik", labtik))
	dp.add_handler(CommandHandler("lab1", labtik))
	dp.add_handler(CommandHandler("lab2", labtik))
	dp.add_handler(CommandHandler("lab3", labtik))
	dp.add_handler(CommandHandler("lab4", labtik))
	dp.add_handler(CommandHandler("lab5", labtik))
	dp.add_handler(CommandHandler("lab6", labtik))
	dp.add_handler(CommandHandler("lab7", labtik))
	dp.add_handler(CommandHandler("lab8", labtik))
	dp.add_handler(CommandHandler("lab9", labtik))
	dp.add_handler(CommandHandler("lab10", labtik))
	dp.add_handler(CommandHandler("unduh", unduh))
	dp.add_handler(CommandHandler("unduh1", unduh))
	dp.add_handler(CommandHandler("unduh2", unduh))
	dp.add_handler(CommandHandler("unduh3", unduh))
	dp.add_handler(CommandHandler("unduh4", unduh))
	dp.add_handler(CommandHandler("unduh5", unduh))
	dp.add_handler(CommandHandler("unduh6", unduh))
	dp.add_handler(CommandHandler("unduh7", unduh))
	dp.add_handler(CommandHandler("unduh8", unduh))
	dp.add_handler(CommandHandler("unduh9", unduh))
	dp.add_handler(CommandHandler("unduh10", unduh))
	dp.add_handler(CommandHandler("unduh11", unduh))
	dp.add_handler(CommandHandler("unduh12", unduh))
	dp.add_handler(CommandHandler("dosentrkj", dosentrkj))
	dp.add_handler(CommandHandler("dosen1", dosentrkj))
	dp.add_handler(CommandHandler("dosen2", dosentrkj))
	dp.add_handler(CommandHandler("dosen3", dosentrkj))
	dp.add_handler(CommandHandler("dosen4", dosentrkj))
	dp.add_handler(CommandHandler("dosen5", dosentrkj))
	dp.add_handler(CommandHandler("dosen6", dosentrkj))
	dp.add_handler(CommandHandler("dosen7", dosentrkj))
	dp.add_handler(CommandHandler("dosen8", dosentrkj))
	dp.add_handler(CommandHandler("dosen9", dosentrkj))
	dp.add_handler(CommandHandler("dosen10", dosentrkj))
	dp.add_handler(CommandHandler("dosen11", dosentrkj))
	dp.add_handler(CommandHandler("dosen12", dosentrkj))
	dp.add_handler(CommandHandler("ruangbelajartik", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar1", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar2", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar3", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar4", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar5", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar6", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar7", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar8", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar9", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar10", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar11", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar12", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar13", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar14", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar15", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar16", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar17", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar18", ruangbelajartik))
	dp.add_handler(CommandHandler("ruangbelajar19", ruangbelajartik))
	dp.add_handler(CommandHandler("kalenderakademik", kalenderakademik))
	dp.add_handler(CommandHandler("peraturanakademik", peraturanakademik))
	dp.add_handler(CommandHandler("strukturpimpinantrkj", strukturpimpinantrkj))
	dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@PutraSyah035')))
	dp.add_handler(CommandHandler("cuaca", cuaca, pass_args=True))
	dp.add_handler(CommandHandler('shalat', shalat, pass_args=True))
	dp.add_handler(CommandHandler("bantu", bantu))
	dp.add_error_handler(error)

    # on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler([Filters.text], chatter))
	dp.add_handler(MessageHandler([Filters.command], unknown)) 
	dp.add_handler(MessageHandler([Filters.location], location))
	dp.add_handler(MessageHandler([Filters.photo], photo))
	dp.add_handler(MessageHandler([Filters.audio], audio))
	dp.add_handler(MessageHandler([Filters.voice], voice))
	dp.add_handler(MessageHandler([Filters.contact], contact))

    # Start the Bot
	updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
    main()