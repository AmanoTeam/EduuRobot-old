import os
import threading
import time
import urllib.request as urllib

import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

def pretty_size(size):
	units = ['B', 'KB', 'MB', 'GB']
	unit = 0
	while size >= 1024:
		size /= 1024
		unit += 1
	return '%0.2f %s' % (size, units[unit])

def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()

def dl_size(fsize, name, extname, sent_id, bot, chat_id):
	os.system('touch "{}"'.format('dls/'+extname))
	time.sleep(1)
	tam = os.stat('dls/'+extname).st_size
	while tam != fsize:
		try:
			bot.editMessageText(
				(chat_id,sent_id),
				text='Baixando <code>{}</code> do YouTube...\n({}/{})'.format(name,pretty_size(tam),pretty_size(fsize)),
				parse_mode='HTML'
			)
		except:
			pass
		time.sleep(0.5)
		tam = os.stat('dls/'+extname).st_size
		

def ytdl_proccess(msg, bot, sent_id, text, msg_id):
	chat_id = msg['chat']['id']
	try:
		yt = ydl.extract_info(text, download=False)
		for format in yt['formats']:
			if format['format_id'] == '140':
				dl_link = format['url']
				fsize = format['filesize']
		name = yt['title']
		extname = yt['title']+'.m4a'
	except:
		return bot.editMessageText(
			(chat_id,sent_id),
			text='Não foi possível obter as informações do vídeo'
		)
	if fsize < 52428800:
		bot.editMessageText(
			(chat_id,sent_id),
			text='Baixando <code>{}</code> do YouTube...\n(null/{})'.format(name,pretty_size(fsize)),
			parse_mode='HTML'
		)
		exec_thread(dl_size, fsize, name, extname, sent_id, bot, chat_id)
		urllib.urlretrieve(dl_link, 'dls/'+extname)
		bot.editMessageText(
			(chat_id,sent_id),
			text='Enviando áudio...'
		)
		bot.sendChatAction(
			chat_id = chat_id,
			action = 'upload_document'
		)
		bot.sendAudio(
			chat_id=chat_id,
			audio=open('dls/'+extname, 'rb'),
			reply_to_message_id=msg_id
		)
		os.remove('dls/'+extname)
		bot.deleteMessage((chat_id,sent_id))
	else:
		bot.editMessageText(
			(chat_id,sent_id),
			text='Ow, o arquivo resultante ({}) ultrapassa o meu limite de 50 MB'.format(pretty_size(fsize))
		)