import os
import threading
import time
import urllib.request as urllib

import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': 'dls/%(title)s.%(ext)s', 'format': '140', 'noplaylist': True})

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

def ytdl_proccess(msg, bot, sent_id, text, msg_id):
	chat_id = msg['chat']['id']
	try:
		yt = ydl.extract_info(text, download=False)
		for format in yt['formats']:
			if format['format_id'] == '140':
				fsize = format['filesize']
		name = yt['title']
		extname = yt['title']+'.m4a'
	except Exception as e:
		return bot.editMessageText(
			(chat_id,sent_id),
			text='Não foi possível obter as informações do vídeo\n\n'+str(e)
		)
	if fsize < 52428800:
		first = time.time()
		bot.editMessageText(
			(chat_id,sent_id),
			text='Baixando <code>{}</code> do YouTube...\n({})'.format(name,pretty_size(fsize)),
			parse_mode='HTML'
		)
		ydl.extract_info(text, download=True)
		bot.editMessageText(
			(chat_id,sent_id),
			text='Enviando áudio...'
		)
		bot.sendChatAction(
			chat_id = chat_id,
			action = 'upload_document'
		)
		sent = bot.sendAudio(
			chat_id=chat_id,
			audio=open(ydl.prepare_filename(yt), 'rb'),
			caption=name,
			reply_to_message_id=msg_id
		)['message_id']
		bot.editMessageCaption(
			(chat_id,sent),
			caption=name+' (Concluído em {}s)'.format(int(time.time()-first))
		)
		os.remove(ydl.prepare_filename(yt))
		bot.deleteMessage((chat_id,sent_id))
	else:
		bot.editMessageText(
			(chat_id,sent_id),
			text='Ow, o arquivo resultante ({}) ultrapassa o meu limite de 50 MB'.format(pretty_size(fsize))
		)