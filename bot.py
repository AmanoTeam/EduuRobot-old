# coding: utf-8

import sys

try:
	from config import *
	import datetime
	import html
	import json
	import os
	import random
	import re
	import requests
	import shutil
	import subprocess
	import threading
	import time
	from pyfiglet import figlet_format
	from telepot.exception import TelegramError, NotEnoughRightsError, UnauthorizedError
	from telepot.loop import MessageLoop
	from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
	from time import sleep
	from plugins import admins as ademirs
	from plugins import md_utils
	from plugins import yt
	from plugins import ytdl
	import keyboard
	from inlines import inlines
except (NameError, ImportError) as erro:
	print('Não foi possível importar os módulos necessários\n\nCausa:', erro)
	sys.exit()

print('''
 _____    _             ____       _           _   
| ____|__| |_   _ _   _|  _ \ ___ | |__   ___ | |_ 
|  _| / _` | | | | | | | |_) / _ \| '_ \ / _ \| __|
| |__| (_| | |_| | |_| |  _ < (_) | |_) | (_) | |_ 
|_____\__,_|\__,_|\__,_|_| \_\___/|_.__/ \___/ \__|
                                       v{}


Iniciando...
'''.format(version))

me = bot.getMe()
bot_name = me['first_name']
bot_username = me['username']
bot_id = me['id']

k.learn("cerebro.xml")
k.respond("LOAD PADRAO")


def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()


def handle_thread(*args, **kwargs):
	t = threading.Thread(target=handle, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()


def handle(msg):
	if 'from' in msg:
		first_name = msg['from']['first_name']

	if 'text' in msg:

		text = msg['text']
		if print_msgs:
			print(first_name + ':', text)
	else:
		text = ''

	if 'data' in msg:
		if print_msgs:
			print(first_name, 'usou o botão', msg['data'])
		chat_id = msg['message']['chat']['id']

	if 'chat' in msg:
		chat_type = msg['chat']['type']
		chat_id = msg['chat']['id']

	if 'date' in msg:
		msg_date = msg['date']
	else:
		msg_date = time.time()

	if 'last_name' in msg['from']:
		last_name = msg['from']['last_name']
	else:
		last_name = ''

	if 'username' in msg['from']:
		username = '@' + msg['from']['username']
	else:
		username = 'nenhum'

	user_id = msg['from']['id']

	if 'message_id' in msg:
		msg_id = msg['message_id']

	if 'language_code' in msg['from']:
		lang_code = msg['from']['language_code']
	else:
		lang_code = '-'

	if 'query' in msg:
		exec_thread(inlines, msg, bot, bot_username)

	elif (time.time() - msg_date) > max_time:
		return

	elif text == '/start' or text == '!start' or text == '/start@' + bot_username or text.startswith('/start '):
		if text.startswith('/start rules'):
			text = text[13:]
			rules = db.hget('rules', text)
			if rules == None:
				rules = 'Sem regras'
			else:
				rules = rules.decode('utf-8')
			bot.sendMessage(
				chat_id=chat_id,
				text=rules,
				parse_mode='Markdown',
				disable_web_page_preview=True
			)
		else:
			if msg['chat']['type'] == 'private':
				teclado = keyboard.start_pv
			else:
				teclado = keyboard.start
			bot.sendMessage(
				chat_id=chat_id,
				text="Olá! eu sou o EduuRobot, para descobrir mais sobre mim e meus comandos clique nos botões abaixo",
				reply_markup=teclado,
				reply_to_message_id=msg_id
			)


	elif text.startswith('/ytdl'):
		text = text[6:]
		if text == '':
			bot.sendMessage(
				chat_id=chat_id,
				text='Uso: /ytdl URL do vídeo ou nome',
				reply_to_message_id=msg_id
			)
		elif 'youtu.be' in text or 'youtube.com' in text:
			sent_id = bot.sendMessage(
				chat_id=chat_id,
				text='Obtendo informações do vídeo...',
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)['message_id']
		else:
			sent_id = bot.sendMessage(
				chat_id=chat_id,
				text='Pesquisando o vídeo no YouTube...',
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)['message_id']
			text = yt.search_query_yt(text)['bot_api_yt'][0]['url']
		exec_thread(
			# nome da função
			ytdl.ytdl_proccess,
			# argumentos
			msg,
			bot,
			sent_id,
			text,
			msg_id
		)


	elif text.startswith('/figlet'):
		text = text[8:]
		if text != '':
			res = figlet_format(text)
			bot.sendMessage(
				chat_id=chat_id,
				text='<pre>' + html.escape(res) + '</pre>',
				parse_mode='HTML'
			)


	elif text.startswith('s/'):
		reply_text = msg['reply_to_message']['text']
		cmd, text, replace = text.split('/')
		res = re.sub(text, replace, reply_text).strip()
		bot.sendMessage(
			chat_id=chat_id,
			text='<pre>' + html.escape(res) + '</pre>',
			reply_to_message_id=msg['reply_to_message']['message_id'],
			parse_mode='HTML'
		)


	elif text.startswith('/suco'):
		if user_id in sudos:
			l = '✅'
		else:
			l = '❌'
		bot.sendMessage(
			chat_id=chat_id,
			text=l + '🍹',
			reply_to_message_id=msg_id
		)


	elif text == '/roleta':
		settings = db.hget('roleta', chat_id)
		if settings == None:
			settings = 'on kick'
		else:
			settings = settings.decode('utf-8')
		if settings.split()[0] == 'on':
			res = random.choice(['Bam', 'passou', 'passou', 'passou', 'passou', 'passou'])
			bot.sendMessage(
				chat_id=chat_id,
				text=res,
				reply_to_message_id=msg_id
			)
			if res == 'Bam':
				if settings.split()[1] == 'mute':
					bot.restrictChatMember(chat_id, user_id, until_date=int(time.time()) + 120)
				else:
					bot.kickChatMember(chat_id, user_id)
					bot.unbanChatMember(chat_id, user_id)


	elif text.startswith('/yt '):
		res = yt.search_query_yt(text[4:])
		vids = ''
		for i in res['bot_api_yt']:
			vids += '• <a href="{}">{}</a>\n\n'.format(i['url'], i['title'])
		bot.sendMessage(
			chat_id=chat_id,
			text=vids,
			reply_to_message_id=msg_id,
			parse_mode='HTML',
			disable_web_page_preview=True
		)


	elif text == '/configroleta':
		admins = bot.getChatAdministrators(chat_id)
		adms_id = []
		for adm in admins:
			adms_id.append(adm['user']['id'])
		if user_id in adms_id:
			settings = db.hget('roleta', chat_id)
			if settings == None:
				settings = 'on kick'
			else:
				settings = settings.decode('utf-8')
			if settings.split()[0] == 'on':
				status = '✅'
			else:
				status = '❌'
			roleta = InlineKeyboardMarkup(inline_keyboard=[
				[dict(text='Ativado', callback_data='null')] +
				[dict(text=status, callback_data='roleta on' if status == '❌' else 'roleta off')],
				[dict(text='Ação', callback_data='null')] +
				[dict(text=settings.split()[1],
					  callback_data='roleta kick' if settings.split()[1] == 'mute' else 'roleta mute')]
			])
			bot.sendMessage(
				chat_id=chat_id,
				text='Configurações da Roleta Russa:',
				reply_markup=roleta,
				reply_to_message_id=msg_id
			)


	elif text.startswith('/echo ') or text.startswith('!echo '):
		if 'reply_to_message' in msg:
			reply_id = msg['reply_to_message']['message_id']
		else:
			reply_id = None
		bot.sendMessage(
			chat_id=chat_id,
			text=text[6:],
			reply_to_message_id=reply_id
		)


	elif text.startswith('/print ') or text.startswith('!print '):
		text = text[7:]
		print(text)
		bot.sendPhoto(
			chat_id=chat_id,
			photo='http://api.screenshotmachine.com/?key={}&dimension={}&url={}'.format(
				screenshot_key,
				'1280x720',
				text
			),
			reply_to_message_id=msg_id
		)


	elif text.startswith('/add ') or text.startswith('!add '):
		if db.hget('addtimeout', str(user_id)) == None:
			tempo = int(time.time()) - 60
		else:
			tempo = db.hget('addtimeout', str(user_id)).decode('utf-8')
		if int(time.time()) - int(tempo) < 60 and user_id not in sudos:
			bot.sendMessage(
				chat_id=chat_id,
				text='Por favor aguarde mais {} segundos antes de usar o comando novamente.'.format(
					str((int(time.time()) - int(tempo)) - 60).replace('-', '')),
				reply_to_message_id=msg_id
			)
		else:
			perg, resp = text[5:].strip().split('|')
			ia_question = InlineKeyboardMarkup(inline_keyboard=[
				[dict(text='✅ Aceitar', callback_data='ia_yes')] +
				[dict(text='❌ Recusar', callback_data='ia_no')]
			])
			bot.sendMessage(
				chat_id=ia_chat,
				text='''
<b>{}</b> enviou uma sugestão:

<b>Frase:</b> {}
<b>Resposta:</b> {}
'''.format(first_name, html.escape(perg), html.escape(resp)),
				parse_mode='HTML',
				reply_markup=ia_question
			)
			bot.sendMessage(
				chat_id=chat_id,
				text='Eu enviei com sucesso a sua sugestão para a minha equipe!',
				reply_to_message_id=msg_id
			)
			db.hset('addtimeout', str(user_id), int(time.time()))


	elif text.startswith('/gif ') or text.startswith('!gif '):
		text = text[5:]
		rjson = requests.get(
			"http://api.giphy.com/v1/gifs/search?q=" + text + "&api_key=" + giphy_key + "&limit=10").json()
		res = random.choice(rjson["data"])
		result = res["images"]["original_mp4"]["mp4"]
		bot.sendVideo(
			chat_id=chat_id,
			video=result,
			reply_to_message_id=msg_id
		)


	elif text.startswith('/mark ') or text.startswith('!mark '):
		if 'reply_to_message' in msg:
			reply_id = msg['reply_to_message']['message_id']
		else:
			reply_id = None
		bot.sendMessage(
			chat_id=chat_id,
			text=text[6:],
			parse_mode='Markdown',
			reply_to_message_id=reply_id
		)


	elif text.startswith('/html ') or text.startswith('!html '):
		if 'reply_to_message' in msg:
			reply_id = msg['reply_to_message']['message_id']
		else:
			reply_id = None
		bot.sendMessage(
			chat_id=chat_id,
			text=text[6:],
			parse_mode='HTML',
			reply_to_message_id=reply_id
		)


	elif text.startswith('/erro') or text.startswith('!erro'):
		text = text[6:]
		if text == '' or text == bot_username:
			bot.sendMessage(
				chat_id=chat_id,
				text='Uso: /erro descrição do bug',
				reply_to_message_id=msg_id
			)
		else:
			bot.sendMessage(
				chat_id=logs_id,
				text='''
{} reportou um bug

ID: {}
Username: {}
Mensagem: {}'''.format(
					first_name,
					user_id,
					username,
					text
				)
			)
			bot.sendMessage(
				chat_id=chat_id,
				text='O bug foi reportado com sucesso para o meu desenvolvedor!',
				reply_to_message_id=msg_id
			)


	elif text.lower() == 'rt':
		reply_name = msg['reply_to_message']['from']['first_name']
		reply_id = msg['reply_to_message']['from']['id']
		reply_text = msg['reply_to_message']['text']
		if reply_text.lower() != 'rt':
			bot.sendMessage(
				chat_id=chat_id,
				text='''🔃 <b>{}</b> retweetou:

👤 <b>{}</b>: <i>{}</i>'''.format(
					first_name,
					reply_name,
					reply_text
				),
				parse_mode='HTML',
				reply_to_message_id=msg_id
			)


	elif text.startswith('/ip') or text.startswith('!ip'):
		text = text[4:]
		r = requests.get(geo_ip + text)
		if len(text) <= 1:
			return bot.sendMessage(
				chat_id=chat_id,
				text='Uso: `/ip IP/endereço`',
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)
		x = ''
		for i in r.json():
			x += "*{}*: `{}`\n".format(i.title(), r.json()[i])
		bot.sendMessage(
			chat_id=chat_id,
			text=x.replace('_', ' '),
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		)
		bot.sendLocation(
			chat_id=chat_id,
			latitude=r.json()['lat'],
			longitude=r.json()['lon'],
			reply_to_message_id=msg_id
		)


	elif text == '!ping' or text == '/ping' or text == '/ping@' + bot_username:
		first_time = time.time()
		message_id = bot.sendMessage(
			chat_id=chat_id,
			text='*Pong!*',
			parse_mode='markdown',
			reply_to_message_id=msg_id
		)['message_id']
		second_time = time.time()
		bot.editMessageText(
			(chat_id, message_id),
			text='*Pong!* `{}`s'.format(str(second_time - first_time)[:5]),
			parse_mode='Markdown'
		)


	elif text == '!king' or text == '/king' or text == '/king@' + bot_username:
		bot.sendMessage(
			chat_id=chat_id,
			text='*Kong*',
			parse_mode='markdown',
			reply_to_message_id=msg_id
		)


	elif text.startswith('!adfly') or text.startswith('/adfly'):
		r = requests.get(adfly_url.format(adfly_key, adfly_uid, text[7:]))
		bot.sendMessage(
			chat_id=chat_id,
			text=r.text,
			reply_to_message_id=msg_id,
			disable_web_page_preview=True
		)


	elif text == '!regras' or text == '/regras' or text == '/regras@' + bot_username:
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			rules = db.hget('rules', str(chat_id))
			if rules == None:
				rules = 'Sem regras!'
			else:
				rules = rules.decode('utf-8')
			bot.sendMessage(
				chat_id=chat_id,
				text=rules,
				parse_mode='markdown',
				reply_to_message_id=msg_id,
				disable_web_page_preview=True
			)


	elif text == '!link' or text == '/link' or text == '/link@' + bot_username:
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			link = db.hget('linkz', str(chat_id))
			if link == None:
				link = 'Sem link'
			else:
				link = link.decode('utf-8')
			bot.sendMessage(
				chat_id=chat_id,
				text=link.replace('_', '\_'),
				parse_mode='Markdown',
				reply_to_message_id=msg_id,
				disable_web_page_preview=True
			)


	elif text.startswith('/token') or text.startswith('!token'):
		text = text[7:]
		try:
			bot_token = telepot.Bot(text).getMe()
			bt_name = bot_token['first_name']
			bt_user = bot_token['username']
			bt_id = bot_token['id']
			bot.sendMessage(
				chat_id=chat_id,
				text='''
Informações do bot:

Nome: {0}
Username: @{1}
ID: {2}'''.format(bt_name, bt_user, bt_id))

		except UnauthorizedError:
			return bot.sendMessage(
				chat_id=chat_id,
				text='Token inválido.'
			)


	elif text.startswith('/git') or text.startswith('!git'):
		text = text[5:]
		r = requests.get(gitapi + text)
		result = r.json()
		if 'avatar_url' not in result:
			return bot.sendMessage(
				chat_id=chat_id,
				text='Usuário não encontrado.',
				reply_to_message_id=msg_id
			)
		else:
			bot.sendMessage(
				chat_id=chat_id,
				text='''
*Nome:* `{0}`
*Login:* `{1}`
*Localização:* `{2}`
*Tipo:* `{3}`
*Bio:* `{4}`'''.format(
					result['name'],
					result['login'],
					result['location'],
					result['type'],
					result['bio']
				),
				parse_mode='Markdown'
			)


	elif 'new_chat_member' in msg:
		bvsetting = db.hget('bvsetting', str(chat_id))
		if bvsetting == None:
			chat_title = msg['chat']['title']
			first_name = msg['new_chat_member']['first_name']
			user_id = msg['new_chat_member']['id']
			if msg['new_chat_member']['id'] == bot_id:
				bot.sendMessage(
					chat_id=chat_id,
					text='Olá pessoal do {}, eu sou o EduuRobot!'.format(chat_title)
				)
				bot.sendMessage(
					chat_id=200097591,
					text='''O bot foi adicionado em um novo grupo!

Nome do grupo: {}
ID do grupo: {}'''.format(msg['chat']['title'], msg['chat']['id']))
			elif msg['chat']['id'] == -1001089627772 and msg['new_chat_member']['is_bot'] == False:
				welcome = 'Hi, {}!\nI\'ve just put you as admin in the group!'.format(first_name)
				rules_markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='😄 Thanks!',callback_data='thanks')],[dict(text='Demote me',callback_data='demote')]])
				bot.promoteChatMember(
					chat_id=chat_id,
					user_id=msg['new_chat_member']['id'],
					can_change_info=True,
					can_delete_messages=True,
					can_invite_users=True,
					can_restrict_members=True,
					can_pin_messages=True,
					can_promote_members=True
				)
			else:
				welcome = db.hget('welcome', chat_id)
				if welcome != None:
					welcome = welcome.decode('utf-8').replace('$name', md_utils.escape(first_name)).replace('$title', md_utils.escape(chat_title)).replace('$id', str(user_id))
				else:
					welcome = 'Olá *{}*, seja bem-vindo(a) ao *{}*!'.format(first_name,md_utils.escape(chat_title))
				if '$rules' in welcome:
					welcome = welcome.replace('$rules', '')
					rules_markup = InlineKeyboardMarkup(inline_keyboard=[
						[dict(text='Leia as regras',
								  url='https://t.me/{}?start=rules_{}'.format(bot_username, chat_id))]
					])
				else:
					rules_markup = None
			bot.sendMessage(
				chat_id=chat_id,
				text=welcome,
				parse_mode='Markdown',
				reply_to_message_id=msg_id,
				reply_markup=rules_markup
			)


	elif 'left_chat_member' in msg:
		first_name = msg['left_chat_member']['first_name']
		bot.sendMessage(
			chat_id=chat_id,
			text='Tchau {}'.format(first_name),
			reply_to_message_id=msg_id
		)


	elif text == '/sudos' or text == '!sudos':
		if user_id in sudos:
			bot.sendMessage(
				chat_id,
				parse_mode='Markdown',
				text='''
_Lista de sudos:_

*Argumentos:* \[Requerido] <Opcional>


*!backup* _<privado>_ - Faz backup da source do bot e envia no chat
*!chat* _[chat ID]_ - Obtem o máximo de informações de um chat
*!cmd* _[Comando]_ - Executa um comando no Terminal
*!del* _[Reply]_ - Deleta a mensagem respondida
*!doc* _[Localização]_ - Envia um arquivo direto do servidor
*!leave* _<chat ID>_ - O bot sai do chat
*!promote* _[Reply]_ - Promove um usuário a administrador
*!promoteme* - Promove você a administrador
*!r_ban* _[chat ID] [user ID]_ - Bane um usuário remotamente
*!r_kick* _[chat ID] [user ID]_ - Kicka um usuário remotamente
*!r_unban* _[chat ID] [user ID]_ - Desbane um usuário remotamente
*!restart* _<bot username>_ - Reinicia o bot
*!php* _[código]_ - Executa um código PHP
*!py* _[código]_ - Executa um código Python
*!send* _[chat ID]|[text/Reply]_ - Envia uma mensagem para uma ID
*!upload* _[Arquivo]_ - Envia o arquivo respondido para o servidor
''',
				reply_markup=keyboard.del_msg
			)


	elif text.startswith('!send'):
		if user_id in sudos:
			text = text[6:]
			try:
				chat, mensagem = text.split("|")
			except:
				pass
			try:
				if 'reply_to_message' in msg:
					bot.forwardMessage(
						chat_id=text,
						from_chat_id=chat_id,
						message_id=msg['reply_to_message']['message_id']
					)
					bot.sendMessage(
						chat_id=chat_id,
						text='✅ encaminhei a parada para `{}` com sucesso!'.format(text),
						parse_mode='Markdown',
						reply_to_message_id=msg_id
					)
				else:
					bot.sendMessage(
						chat_id=text.split("|")[0],
						parse_mode='Markdown',
						text=text.split("|")[1]
					)
					bot.sendMessage(
						chat_id=chat_id,
						text='✅ mandei a parada para `{}` com sucesso!'.format(chat),
						parse_mode='Markdown',
						reply_to_message_id=msg_id
					)
			except TelegramError:
				bot.sendMessage(
					chat_id,
					text='Esse chat nem existe aqui',
					reply_to_message_id=msg_id
				)
			except:
				bot.sendMessage(
					chat_id,
					text='Teve como mandar não, resolve essa fita ae',
					reply_to_message_id=msg_id
				)


	elif text.startswith('/tr'):
		if 'reply_to_message' in msg:
			try:
				idioma = text.split(' ')[1]
			except:
				idioma = 'pt'
			text = msg['reply_to_message']['text'].replace('#', '%23')
		else:
			idioma = text.split(' ')[1]
			text = text.replace('/tr ' + idioma + ' ', '').replace('/tr ', '').replace('#', '%23')
		message_id = bot.sendMessage(
			chat_id=chat_id,
			text='Traduzindo...',
			reply_to_message_id=msg_id
		)['message_id']
		try:
			r = requests.get(tr_api + '?key=' + tr_key + '&lang=' + idioma + '&text=' + text)
			texto = r.json()['text'][0]
		except:
			r = requests.get(tr_api + '?key=' + tr_key + '&lang=pt&text=' + idioma + ' ' + text)
			texto = r.json()['text'][0]

		bot.editMessageText(
			(chat_id, message_id),
			text='''
<b>Idioma:</b> {0}
<b>Tradução:</b> <code>{1}</code>'''.format(
				r.json()['lang'],
				html.escape(texto)
			),
			parse_mode='html'
		)


	elif text.startswith('!leave'):
		if ' ' in text:
			chat_id = text.split()[1]
		if user_id in sudos:
			bot.sendMessage(
				chat_id=chat_id,
				text='Tou saindo daqui flws',
			)
			bot.leaveChat(
				chat_id=chat_id,
			)


	elif text.startswith('!chat'):
		if ' ' in text:
			chat = text.split()[1]
		else:
			chat = chat_id
		if user_id in sudos:
			sent = bot.sendMessage(
				chat_id=chat_id,
				text='⏰ Obtendo informações do chat...',
				reply_to_message_id=msg_id
			)['message_id']
			try:
				res_chat = bot.getChat(chat)
			except TelegramError:
				bot.editMessageText(
					(chat_id, sent),
					text='Chat não encontrado'
				)
			if res_chat['type'] != 'private':
				try:
					link = bot.exportChatInviteLink(chat)
				except:
					link = 'Não disponível'
				try:
					members = bot.getChatMembersCount(chat)
				except:
					members = 'erro'
				try:
					username = '@' + res_chat['username']
				except:
					username = 'nenhum'
				bot.editMessageText(
					(chat_id, sent),
					text='''
<b>Informações do chat:</b>

<b>Título:</b> {}
<b>Username:</b> {}
<b>ID:</b> {}
<b>Link:</b> {}
<b>Membros:</b> {}
'''.format(html.escape(res_chat['title']), username, res_chat['id'], link, members),
					parse_mode='HTML',
					disable_web_page_preview=True
				)
			else:
				try:
					username = '@' + res_chat['username']
				except:
					username = 'nenhum'
				bot.editMessageText(
					(chat_id, sent),
					text='''
<b>Informações do chat:</b>

<b>Nome:</b> {}
<b>Username:</b> {}
<b>ID:</b> {}
'''.format(html.escape(res_chat['first_name']), username, res_chat['id']),
					parse_mode='HTML',
					disable_web_page_preview=True
				)


	elif text == '!promoteme':
		if user_id in owners_id:
			for perms in bot.getChatAdministrators(chat_id):
				if perms['user']['id'] == bot_id:
					bot.promoteChatMember(
						chat_id=chat_id,
						user_id=user_id,
						can_change_info=perms['can_change_info'],
						can_delete_messages=perms['can_delete_messages'],
						can_invite_users=perms['can_invite_users'],
						can_restrict_members=perms['can_restrict_members'],
						can_pin_messages=perms['can_pin_messages'],
						can_promote_members=True
					)


	elif text == '!promote':
		if user_id in owners_id:
			if 'reply_to_message' in msg:
				reply_id = msg['reply_to_message']['from']['id']
			else:
				return
			for perms in bot.getChatAdministrators(chat_id):
				if perms['user']['id'] == bot_id:
					bot.promoteChatMember(
						chat_id=chat_id,
						user_id=reply_id,
						can_change_info=perms['can_change_info'],
						can_delete_messages=perms['can_delete_messages'],
						can_invite_users=perms['can_invite_users'],
						can_restrict_members=perms['can_restrict_members'],
						can_pin_messages=perms['can_pin_messages'],
						can_promote_members=True
					)


	elif text.startswith('/admins'):
		adms = bot.getChatAdministrators(chat_id)
		name = ''
		a = 1
		for user in adms:
			name += '{} - <a href="tg://user?id={}">{}</a>\n'.format(
				a,
				user['user']['id'],
				html.escape(user['user']['first_name'])
			)
			a += 1
		bot.sendMessage(
			chat_id=chat_id,
			text=name,
			parse_mode='html',
			reply_to_message_id=msg_id
		)


	elif text == '!restart' or text == '!restart @' + bot_username:
		if user_id in sudos:
			bot.sendMessage(
				chat_id=chat_id,
				text='Reiniciando...'
			)
			sleep(3)
			os.execl(sys.executable, sys.executable, *sys.argv)
			del threading.Thread


	elif text.startswith('!cmd'):
		if user_id in owners_id:
			text = text[5:]
			res = subprocess.getstatusoutput(text)[1]
			if res != '':
				bot.sendMessage(
					chat_id=chat_id,
					text=res,
					reply_to_message_id=msg_id
				)
			else:
				bot.sendMessage(
					chat_id=chat_id,
					text='O comando foi executado',
					reply_to_message_id=msg_id
				)


	elif text.startswith('!py'):
		if user_id in owners_id:
			text = text[4:]
			with open('temp.py', 'w') as arquivo:
				arquivo.write(text)
			res = subprocess.getstatusoutput('python3 temp.py')[1]
			os.remove('temp.py')
			bot.sendMessage(
				chat_id=chat_id,
				text='<b>Resultado:</b>\n\n<pre>' + html.escape(res) + '</pre>',
				parse_mode='HTML',
				reply_to_message_id=msg_id
			)


	elif text.startswith('!php'):
		if user_id in owners_id:
			text = '<?php ' + text[5:] + ' ?>'
			with open('temp.php', 'w') as arquivo:
				arquivo.write(text)
			res = subprocess.getstatusoutput('php temp.php')[1]
			os.remove('temp.php')
			bot.sendMessage(
				chat_id=chat_id,
				text='<b>Resultado:</b>\n\n<pre>' + html.escape(res) + '</pre>',
				parse_mode='HTML',
				reply_to_message_id=msg_id
			)


	elif text == '!del':
		admins = bot.getChatAdministrators(chat_id)
		adm_id = []
		for adms in admins:
			adm_id.append(adms['user']['id'])
		if user_id in sudos or user_id in adm_id:
			if 'reply_to_message' in msg:
				reply_id = msg['reply_to_message']['message_id']
			else:
				bot.sendMessage(
					chat_id=chat_id,
					text='Responda a uma mensagem com o comando para deletar a mensagem'
				)
			try:
				bot.deleteMessage((chat_id, reply_id))
				bot.deleteMessage((chat_id, msg_id))
			except TelegramError:
				pass


	elif text.startswith('!r_ban'):
		chat = text.split()[1]
		user = text.split()[2]
		if user_id in sudos:
			try:
				bot.kickChatMember(
					chat_id=chat,
					user_id=user
				)
				bot.sendMessage(
					chat_id=chat_id,
					text='pronto!'
				)
			except TelegramError:
				bot.sendMessage(
					chat_id=chat_id,
					text='Chat ou usuario nao encontrado'
				)
			except:
				bot.sendMessage(
					chat_id=chat_id,
					text='Ocorreu um erro.'
				)


	elif text.startswith('!r_kick'):
		chat = text.split()[1]
		user = text.split()[2]
		if user_id in sudos:
			try:
				bot.kickChatMember(
					chat_id=chat,
					user_id=user
				)
				bot.unbanChatMember(
					chat_id=chat,
					user_id=user
				)
				bot.sendMessage(
					chat_id=chat_id,
					text='pronto!'
				)
			except TelegramError:
				bot.sendMessage(
					chat_id=chat_id,
					text='Chat ou usuario nao encontrado'
				)
			except:
				bot.sendMessage(
					chat_id=chat_id,
					text='Ocorreu um erro.'
				)


	elif text.startswith('!r_unban'):
		chat = text.split()[1]
		user = text.split()[2]
		if user_id in sudos:
			try:
				bot.unbanChatMember(
					chat_id=chat,
					user_id=user
				)
				bot.sendMessage(
					chat_id=chat_id,
					text='pronto!'
				)
			except TelegramError:
				bot.sendMessage(
					chat_id=chat_id,
					text='Chat ou usuario nao encontrado'
				)
			except:
				bot.sendMessage(
					chat_id=chat_id,
					text='Ocorreu um erro.'
				)


	elif text.startswith('!backup'):
		if user_id in sudos:
			hora = str(int(time.time()))
			sent = bot.sendMessage(
				chat_id=chat_id,
				text='Iniciando backup...',
				reply_to_message_id=msg_id
			)['message_id']
			os.system('tar -czf backup-' + hora + '.tar.gz --exclude __pycache__ dls *')
			if 'privado' in text or 'pv' in text:
				bot.editMessageText(
					(chat_id, sent),
					text='Estou enviando o backup no seu pv'
				)
				chat_id = user_id
			bot.sendDocument(
				chat_id=chat_id,
				document=open('backup-' + hora + '.tar.gz', 'rb')
			)
			os.remove('backup-' + hora + '.tar.gz')


	elif text.startswith('!doc'):
		if user_id in sudos:
			file = text[5:]
			try:
				bot.sendDocument(chat_id, open(file, 'rb'))
			except FileNotFoundError:
				bot.sendMessage(
					chat_id=chat_id,
					text='Arquivo não encontrado.',
					reply_to_message_id=msg_id
				)
			except:
				bot.sendMessage(
					chat_id=chat_id,
					text='Ocorreu um erro ao enviar o arquivo.',
					reply_to_message_id=msg_id
				)


	elif text.startswith('!upload'):
		if user_id in sudos:
			text = text[8:]
			if 'reply_to_message' in msg:
				sent = bot.sendMessage(
					chat_id=chat_id,
					text='⏰ Enviando arquivo para o servidor...'
				)['message_id']
				try:
					file_path = msg['reply_to_message']['document']['file_id']
					file_name = msg['reply_to_message']['document']['file_name']
					if text == '':
						file_name = './' + file_name
					else:
						file_name = text + '/' + file_name
					bot.download_file(file_path, file_name)
					bot.editMessageText(
						(chat_id, sent),
						text='✅ Envio concluído!'
					)
				except:
					bot.editMessageText(
						(chat_id, sent),
						text='❌ Ocorreu um erro!'
					)


	elif text.startswith('/title') or text.startswith('!title'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			text = text[7:]
			for status in admins:
				if user_id == status['user']['id']:
					if text == '':
						bot.sendMessage(
							chat_id=chat_id,
							text='Uso: /title titulo do grupo',
							reply_to_message_id=msg_id
						)
					else:
						try:
							bot.setChatTitle(chat_id, text)
							bot.sendMessage(
								chat_id=chat_id,
								text='O novo título do grupo foi definido com sucesso!',
								reply_to_message_id=msg_id
							)
						except NotEnoughRightsError:
							bot.sendMessage(
								chat_id=chat_id,
								text='Eu nao tenho tenho permissão para alterar as informações do grupo',
								reply_to_message_id=msg_id
							)
						except:
							bot.sendMessage(
								chat_id=chat_id,
								text='Ocorreu um erro.',
								reply_to_message_id=msg_id
							)


	elif text.startswith('/welcome') or text.startswith('!welcome'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			text = text[9:]
			for status in admins:
				if user_id == status['user']['id']:
					if text == '' or text == bot_username:
						bot.sendMessage(
							chat_id=chat_id,
							text='Uso: /welcome on/off/reset/mensagem de boas-vindas do grupo (suporta Markdown e as tags $name, $title, $id e $rules)',
							reply_to_message_id=msg_id
						)
					elif text == 'on':
						db.hdel('bvsetting', chat_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='A mensagem de boas-vindas foi ativada',
							reply_to_message_id=msg_id
						)
					elif text == 'off':
						db.hset('bvsetting', chat_id, 'off')
						bot.sendMessage(
							chat_id=chat_id,
							text='A mensagem de boas-vindas foi desativada',
							reply_to_message_id=msg_id
						)
					elif text == 'reset':
						db.hdel('welcome', chat_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='A mensagem de boas-vindas foi redefinida',
							reply_to_message_id=msg_id
						)
					else:
						db.hset('welcome', chat_id, text)
						bot.sendMessage(
							chat_id=chat_id,
							text='A mensagem de boas-vindas foi definida',
							reply_to_message_id=msg_id
						)


	elif text.startswith('/defregras') or text.startswith('!defregras'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			text = text[11:]
			for status in admins:
				if user_id == status['user']['id']:
					if text == '':
						bot.sendMessage(
							chat_id=chat_id,
							text='Uso: /defregras Regras do grupo (suporta Markdown)',
							reply_to_message_id=msg_id
						)
					elif text == 'reset':
						db.hdel('rules', str(chat_id))
						bot.sendMessage(
							chat_id=chat_id,
							text='Regras redefinidas com sucesso!',
							reply_to_message_id=msg_id
						)
					else:
						db.hset('rules', str(chat_id), text)
						bot.sendMessage(
							chat_id=chat_id,
							text='As regras do grupo foram definidas com sucesso!',
							reply_to_message_id=msg_id
						)


	elif text.startswith('/deflink') or text.startswith('!deflink'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			text = text[9:]
			for status in admins:
				if user_id == status['user']['id']:
					if text == '':
						bot.sendMessage(
							chat_id=chat_id,
							text='Uso: /deflink Link do grupo',
							reply_to_message_id=msg_id
						)
					elif text == 'reset':
						db.hdel('linkz', str(chat_id))
						bot.sendMessage(
							chat_id=chat_id,
							text='Link redefinido com sucesso!',
							reply_to_message_id=msg_id
						)
					else:
						db.hset('linkz', str(chat_id), text)
						bot.sendMessage(
							chat_id=chat_id,
							text='O link do grupo foi definido com sucesso!',
							reply_to_message_id=msg_id
						)


	elif text.startswith('/maxadvs') or text.startswith('!maxadvs'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			text = text[9:]
			for status in admins:
				if user_id == status['user']['id']:
					if text == '':
						bot.sendMessage(
							chat_id=chat_id,
							text='Uso: /maxadvs numero máximo de advertências permitidas no grupo',
							reply_to_message_id=msg_id
						)
					else:
						db.hset('maxadvs', str(chat_id), text)
						bot.sendMessage(
							chat_id=chat_id,
							text='Salvo com sucesso!',
							reply_to_message_id=msg_id
						)


	elif text.startswith('/ban') or text.startswith('!ban'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				if bot_id in adm_id:
					if reply_id in adm_id:
						bot.sendMessage(
							chat_id=chat_id,
							text='Esse aí tem admin',
							reply_to_message_id=msg_id
						)
					else:
						bot.kickChatMember(chat_id, reply_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='{} baniu {}!'.format(
								first_name,
								reply_name
							),
							reply_to_message_id=msg_id
						)
				else:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Ô poha, eu nao tenho admin aqui nessa bagaça''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/kick') or text.startswith('!kick'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				if bot_id in adm_id:
					if reply_id in adm_id:
						bot.sendMessage(
							chat_id=chat_id,
							text='Esse aí tem admin',
							reply_to_message_id=msg_id
						)
					else:
						bot.unbanChatMember(chat_id, reply_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='{} kickou {}!'.format(
								first_name,
								reply_name
							),
							reply_to_message_id=msg_id
						)
				else:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Ô poha, eu nao tenho admin aqui nessa bagaça''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/tempban') or text.startswith('!tempban'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			temp = int(text.split(' ')[1])
			udate = int(time.time()) + temp
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				try:
					bot.kickChatMember(chat_id=chat_id, user_id=reply_id, until_date=udate)
					bot.sendMessage(
						chat_id=chat_id,
						text='{} baniu {} por {} segundos!'.format(
							first_name,
							reply_name,
							temp
						),
						reply_to_message_id=msg_id
					)
				except:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Eu não posso banir esse usuário.

Verifica ae se eu tenho permissão no grupo, e se quem você quer banir não é um admin''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/mute') or text.startswith('!mute'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				if bot_id in adm_id:
					if reply_id in adm_id:
						bot.sendMessage(
							chat_id=chat_id,
							text='Esse aí tem admin karai',
							reply_to_message_id=msg_id
						)
					else:
						bot.restrictChatMember(chat_id, reply_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='{} restringiu {}!'.format(
								first_name,
								reply_name
							),
							reply_to_message_id=msg_id
						)
				else:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Ô poha, eu nao tenho admin aqui nessa bagaça''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/unmute') or text.startswith('!unmute'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				try:
					bot.restrictChatMember(
						chat_id=chat_id,
						user_id=reply_id,
						can_send_messages=True,
						can_send_media_messages=True,
						can_send_other_messages=True,
						can_add_web_page_previews=True
					)
					bot.sendMessage(
						chat_id=chat_id,
						text='{} agora pode enviar mensagens aqui!'.format(
							reply_name
						),
						reply_to_message_id=msg_id
					)
				except:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Eu não posso desrestringir esse usuário.

Verifica ae se eu tenho permissão no grupo, e se quem você quer restringir não é um admin''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/ban') or text.startswith('!ban'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				if bot_id in adm_id:
					if reply_id in adm_id:
						bot.sendMessage(
							chat_id=chat_id,
							text='Esse aí tem admin',
							reply_to_message_id=msg_id
						)
					else:
						bot.kickChatMember(chat_id, reply_id)
						bot.unbanChatMember(chat_id, reply_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='{} kickou {}!'.format(
								first_name,
								reply_name
							),
							reply_to_message_id=msg_id
						)
				else:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Ô poha, eu nao tenho admin aqui nessa bagaça''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/unban') or text.startswith('!unban'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				try:
					bot.unbanChatMember(chat_id, reply_id)
					bot.sendMessage(
						chat_id=chat_id,
						text='{} desbaniu {}!'.format(
							first_name,
							reply_name
						),
						reply_to_message_id=msg_id
					)
				except:
					bot.sendMessage(
						chat_id=chat_id,
						text='''Eu não posso desbanir esse usuário.

Verifica ae se eu tenho permissão nesse grupo.''',
						reply_to_message_id=msg_id
					)


	elif text.startswith('/warn') or text.startswith('!warn'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					reply_name = msg['reply_to_message']['from']['first_name']
					reply_id = msg['reply_to_message']['from']['id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda alguém karai',
						reply_to_message_id=msg_id
					)
				warn = db.hget('warn', str(reply_id))
				if warn == None:
					db.hset('warn', str(reply_id), '1')
					warns = '1'
				else:
					db.hset('warn', str(reply_id), str(int(warn) + 1))

				warns = db.hget('warn', reply_id).decode('utf-8')
				maxwarns = db.hget('maxadvs', chat_id)
				if maxwarns == None:
					maxwarns = '3'
				if int(warns) >= int(maxwarns):
					try:
						bot.kickChatMember(chat_id, reply_id)
						bot.sendMessage(
							chat_id=chat_id,
							text='{} foi banido porque atingiu o limite de advertencias'.format(reply_name),
							reply_to_message_id=msg_id
						)
						db.hdel('warn', str(reply_id))
					except:
						bot.sendMessage(
							chat_id=chat_id,
							text='Não foi possivel banir este usuário.',
							reply_to_message_id=msg_id
						)
				else:
					bot.sendMessage(
						chat_id=chat_id,
						text='{} foi advertido <pre>[{}/{}]</pre>'.format(
							html.escape(reply_name),
							warns,
							maxwarns
						),
						parse_mode='HTML'
					)


	elif text.startswith('/unwarn') or text.startswith('!unwarn'):
		admins = bot.getChatAdministrators(chat_id)
		adm_id = []
		for ids in admins:
			adm_id.append(ids['user']['id'])
		if user_id in adm_id:
			reply_id = msg['reply_to_message']['from']['id']
			db.hdel('warn', str(reply_id))
			bot.sendMessage(
				chat_id=chat_id,
				text='Advertências removidas!',
				reply_to_message_id=msg_id
			)


	elif text.startswith('/IA') or text.startswith('!IA'):
		text = text[4:]
		if msg['chat']['type'] == 'private':
			adm_id = [user_id]
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
		if user_id in adm_id or user_id in sudos:
			if text == 'on':
				db.hdel('ia_setting', chat_id)
				bot.sendMessage(
					chat_id=chat_id,
					text='A IA do bot foi ativada',
					reply_to_message_id=msg_id
				)
			elif text == 'off':
				db.hset('ia_setting', chat_id, 'off')
				bot.sendMessage(
					chat_id=chat_id,
					text='A IA do bot foi desativada',
					reply_to_message_id=msg_id
				)
			else:
				bot.sendMessage(
					chat_id=chat_id,
					text='Uso: /IA on/off',
					reply_to_message_id=msg_id
				)


	elif text == '/pin' or text == '!pin':
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				if 'reply_to_message' in msg:
					msg_reply = msg['reply_to_message']['message_id']
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Responda a uma mensagem.',
						reply_to_message_id=msg_id
					)
				try:
					bot.pinChatMessage(chat_id, msg_reply)
					bot.sendMessage(
						chat_id=chat_id,
						text='Mensagem fixada',
						reply_to_message_id=msg_id)
				except NotEnoughRightsError:
					bot.sendMessage(
						chat_id,
						text='Eu não tenho permissões suficientes',
						reply_to_message_id=msg_id
					)


	elif text == '/unpin' or text == '!unpin':
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				bot.unpinChatMessage(chat_id)
				bot.sendMessage(
					chat_id=chat_id,
					text='Mensagem desfixada',
					reply_to_message_id=msg_id
				)


	elif text.startswith('/antipedro'):
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='Este comando só funciona em grupos ¯\\_(ツ)_/¯'
			)
		else:
			admins = bot.getChatAdministrators(chat_id)
			adm_id = []
			for ids in admins:
				adm_id.append(ids['user']['id'])
			if user_id in adm_id:
				text = text[11:]
				if text == 'on':
					db.hset('antipedro', str(chat_id), text)
					bot.sendMessage(
						chat_id=chat_id,
						text='O antipedro foi ativado'
					)
				elif text == 'off':
					db.hset('antipedro', str(chat_id), text)
					bot.sendMessage(
						chat_id=chat_id,
						text='O antipedro foi desativado'
					)
				else:
					return bot.sendMessage(
						chat_id=chat_id,
						text='Uso: /antipedro on/off'
					)


	elif text == '@admin':
		exec_thread(
			ademirs.call_admins,
			msg,
			bot,
			chat_id,
			msg_id
		)


	elif text == '/dados' or text == '!dados' or text == '/dados@' + bot_username:
		dados = random.randint(1, 6)
		bot.sendMessage(
			chat_id=chat_id,
			text='🎲 O dado parou no número: {}'.format(
				dados
			),
			reply_to_message_id=msg_id
		)


	elif text.startswith('/jsondump') or text.startswith('!jsondump') or text == '/jsondump@' + bot_username:
		try:
			if '-f' not in text:
				bot.sendMessage(
					chat_id=chat_id,
					text='`' + json.dumps(msg, indent=2, sort_keys=False) + '`',
					parse_mode='Markdown',
					reply_to_message_id=msg_id
				)
			else:
				bot.sendChatAction(
					chat_id=chat_id,
					action='upload_document'
				)
				with open('dump.json', 'wb') as i:
					i.write(bytes(str(json.dumps(msg, indent=2, sort_keys=False)), 'utf-8'))
				bot.sendDocument(
					chat_id=chat_id,
					document=open('dump.json', 'rb'),
					reply_to_message_id=msg_id
				)
				os.remove('dump.json')
		except:
			bot.sendChatAction(
				chat_id=chat_id,
				action='upload_document'
			)
			with open('dump.json', 'wb') as i:
				i.write(bytes(str(json.dumps(msg, indent=2, sort_keys=False)), 'utf-8'))
			bot.sendDocument(
				chat_id=chat_id,
				document=open('dump.json', 'rb'),
				reply_to_message_id=msg_id
			)
			os.remove('dump.json')


	elif text.startswith('/sorteio'):
		try:
			cmd, max = text.split()
			sort = random.randint(1, int(max))
			bot.sendMessage(
				chat_id=chat_id,
				text='O número sorteado foi: {}'.format(sort),
				reply_to_message_id=msg_id
			)
		except:
			bot.sendMessage(
				chat_id=chat_id,
				text='Por favor verifique se você usou o comando corretamente. Ex: /sorteio 100',
				reply_to_message_id=msg_id
			)


	elif text.startswith('/request ') or text.startswith('!request '):
		text = text[9:]
		if 'http' not in text:
			text = 'http://' + text
		try:
			r = requests.get(text)
		except:
			bot.sendMessage(
				chat_id=chat_id,
				text='Ocorreu um erro, verifique se a URL está correta.',
				reply_to_message_id=msg_id
			)
		conteudo = r.text
		if len(conteudo) < 4075:
			bot.sendMessage(
				chat_id=chat_id,
				text='*Conteúdo:*\n`{}`'.format(conteudo),
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)
		else:
			bot.sendMessage(
				chat_id=chat_id,
				text='*Conteúdo:*\n`O conteudo era muito grande para ser enviado :(`',
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)


	elif text == '/id' or text == '/id@' + bot_username or text == '!id':
		if chat_type == 'private':
			bot.sendMessage(
				chat_id=chat_id,
				text='''
_Informações:_

*Nome:* `{}`
*Sobrenome:* `{}`
*Username:* `{}`
*ID:* `{}`
*Idioma:* `{}`
*Tipo de chat:* `{}`'''.format(
					first_name,
					last_name,
					username,
					user_id,
					lang_code,
					chat_type
				),
				parse_mode='Markdown',
				reply_to_message_id=msg_id
			)
		else:
			message_id = bot.sendMessage(
				chat_id=chat_id,
				text='⏰ Consultando informações...',
				reply_to_message_id=msg_id
			)['message_id']
			chat_title = msg['chat']['title']
			members = bot.getChatMembersCount(chat_id)
			if 'username' in msg['chat']:
				chat_username = '@' + msg['chat']['username']
			else:
				chat_username = 'nenhum'
			if 'reply_to_message' in msg:
				from_info = msg['reply_to_message']['from']
				first_name = from_info['first_name']

				if 'last_name' in from_info:
					last_name = from_info['last_name']
				else:
					last_name = ''

				user_id = from_info['id']

				if 'username' in from_info:
					username = '@' + from_info['username']
				else:
					username = 'nenhum'

				if 'language_code' in from_info:
					lang_code = from_info['language_code']
				else:
					lang_code = '-'

				if msg['reply_to_message']['from']['id'] == 448359768:
					lang_code = 'en-US'

			bot.editMessageText(
				(chat_id, message_id),
				text='''
_Informações do chat:_

*Nome:* `{}`
*Sobrenome:* `{}`
*Username:* `{}`
*ID:* `{}`
*Idioma:* `{}`

*Nome do grupo:* `{}`
*Username do grupo:* `{}`
*ID do chat:* `{}`
*Total de mensagens:* `{}`
*Tipo de chat:* `{}`
*Total de membros:* `{}`'''.format(
					first_name,
					last_name,
					username,
					user_id,
					lang_code,
					chat_title,
					chat_username,
					chat_id,
					msg_id,
					chat_type,
					members
				),
				parse_mode='Markdown'
			)


	elif text.startswith('/kc '):
		text = text[4:]
		try:
			text, color, color2 = text.split('|')
		except ValueError:
			color = 'FF0000'
			color2 = 'FFFFFF'
		bot.sendPhoto(
			chat_id=chat_id,
			photo='http://www.keepcalmstudio.com/-/p.php?t=%EE%BB%AA%0D%0AKEEP%0D%0ACALM%0D%0A{0}&bc={1}&tc={2}&cc={2}&uc=true&ts=true&ff=PNG&w=1080&ps=sq'.format(
				text,
				color,
				color2
			)
		)


	elif 'data' in msg:
		data = msg['data']

		if data == 'tools_cmds':
			bot.editMessageText(
				(chat_id, msg['message']['message_id']),
				text='''Ferramentas:

*/echo* - Repete o texto informado
*/gif* - Pesquisa e envia uma GIF no chat
*/git* - Envia informações de um user do GitHub
*/html* - Repete o texto informado usando HTML
*/ip* - Exibe informações sobre um IP/domínio
*/jsondump* - Envia o json da mensagem
*/mark* - Repete o texto informado usando Markdown
*/print* - Envia uma print de um site
*/request* - Faz uma requisição a um site
*/token* - Exibe informações de um token de bot
*/tr* - Traduz um texto
*/ytdl* - Baixa o áudio de um vídeo no YouTube
''',
				parse_mode='Markdown',
				reply_markup=keyboard.cmds_back
			)

		if data.startswith('roleta '):
			setting = db.hget('roleta', chat_id)
			if setting == None:
				setting = 'on kick'
			else:
				setting = setting.decode('utf-8')

			if 'on' in data or 'off' in data:
				setting = setting.replace(setting.split()[0], data.split()[1])
			elif 'kick' in data or 'mute' in data:
				setting = setting.replace(setting.split()[1], data.split()[1])
			db.hset('roleta', chat_id, setting)
			if setting.split()[0] == 'on':
				status = '✅'
			else:
				status = '❌'
			roleta = InlineKeyboardMarkup(inline_keyboard=[
				[dict(text='Ativado', callback_data='null')] +
				[dict(text=status, callback_data='roleta on' if status == '❌' else 'roleta off')],
				[dict(text='Ação', callback_data='null')] +
				[dict(text=setting.split()[1],
					  callback_data='roleta kick' if setting.split()[1] == 'mute' else 'roleta mute')]
			])
			bot.editMessageReplyMarkup(
				(chat_id, msg['message']['message_id']),
				reply_markup=roleta)

		if data == 'admin_cmds':
			bot.editMessageText(
				(chat_id, msg['message']['message_id']),
				text='''Comandos administrativos:

*/ban* - Bane um usuário
*/defregras* - Define as regras do grupo
*/kick* - Kicka um usuário
*/mute* - Restringe um usuário
*/pin* - Fixa uma mensagem no grupo
*/title* - Define o título do grupo
*/unban* - Desbane um usuário
*/unmute* - Desrestringe um usuário
*/unpin* - Desfixa a mensagem fixada no grupo
*/unwarn* - Remove as advertências do usuário
*/warn* - Adverte um usuário
*/welcome* - Define a mensagem de welcome
''',
				parse_mode='Markdown',
				reply_markup=keyboard.cmds_back
			)

		if data == 'user_cmds':
			bot.editMessageText(
				(chat_id, msg['message']['message_id']),
				text='''Comandos para usuários normais:

*/add* - Envia uma sugestão para a IA do bot
*/admins* - Mostra a lista de admins do chat
*/dados* - Envia um número aleatório de 1 a 6
*/erro* - Reporta um bug ao meu desenvolvedor
*/id* - Exibe suas informações ou de um usuário
*/ping* - Responde com uma mensagem de ping
*/regras* - Exibe as regras do grupo
''',
				parse_mode='Markdown',
				reply_markup=keyboard.cmds_back
			)

		if msg['message']['chat']['type'] == 'private':
			teclado = keyboard.start_pv
		else:
			teclado = keyboard.start

		if data == 'start_back':
			print(msg)
			bot.editMessageText(
				(chat_id, msg['message']['message_id']),
				text="Olá! eu sou o EduuRobot, para descobrir mais sobre mim e meus comandos clique nos botões abaixo",
				reply_markup=teclado
			)

		if data == 'ia_yes':
			if chat_id == ia_chat:
				data = data[7:]
				bot.editMessageText(
					(chat_id, msg['message']['message_id']),
					text='<b>' + html.escape(msg['message']['text']).replace(' enviou', '</b> enviou').replace('Frase:',
																											   '<b>Frase:</b>').replace(
						'Resposta:', '<b>Resposta:</b>') + '\n\nSugestão aceita por {}!'.format(
						first_name
					),
					parse_mode='HTML'
				)
				aiml = open('aiml/padrao.aiml', 'r').read()
				perg = msg['message']['text'].split('\n')[2].replace('Frase: ', '')
				resp = msg['message']['text'].split('\n')[3].replace('Resposta: ', '')
				modml = aiml.replace('<!-- reservado -->', '''<category>
		<pattern>{}</pattern>
		<template>
			{}
		</template>
	</category>
	
	<!-- reservado -->'''.format(perg.upper(), resp))
				arq = open('aiml/padrao.aiml', 'w')
				arq.write(modml)
				arq.close()
				k.respond("LOAD PADRAO")

		if data == 'ia_no':
			bot.editMessageText(
				(chat_id, msg['message']['message_id']),
				text='<b>' + html.escape(msg['message']['text']).replace(' enviou', '</b> enviou').replace('Frase:',
																										   '<b>Frase:</b>').replace(
					'Resposta:', '<b>Resposta:</b>') + '\n\nSugestão recusada por {}!'.format(
					first_name
				),
				parse_mode='HTML'
			)

		if data == 'all_cmds':
			bot.editMessageText(
				msg_identifier=(chat_id, msg['message']['message_id']),
				text='Selecione uma categoria de comando para visualizar',
				reply_markup=keyboard.all_cmds
			)

		if data == 'del_msg':
			if user_id in sudos:
				bot.deleteMessage(
					(chat_id, msg['message']['message_id'])
				)
			else:
				bot.answerCallbackQuery(msg['id'], text='Você não tem permissão para usar este botão u.u',show_alert=True)
		
		if data == 'thanks':
			if msg['message']['reply_to_message']['from']['id'] == msg['from']['id']:
				bot.deleteMessage(
					(chat_id, msg['message']['message_id'])
				)
			else:
				bot.answerCallbackQuery(msg['id'], text='Ops, this message is not for you...',show_alert=True)

		if data == 'demote':
			if msg['message']['reply_to_message']['from']['id'] == msg['from']['id']:
				bot.deleteMessage(
					(chat_id, msg['message']['message_id'])
				)
				bot.answerCallbackQuery(msg['id'], text='Ok...')
				bot.promoteChatMember(
					chat_id=chat_id,
					user_id=msg['from']['id'],
					can_change_info=False,
					can_delete_messages=False,
					can_invite_users=False,
					can_restrict_members=False,
					can_pin_messages=False,
					can_promote_members=False
				)
			else:
				bot.answerCallbackQuery(msg['id'], text='Ops, this message is not for you...',show_alert=True)

		if data == 'infos':
			bot.editMessageText(
				msg_identifier=(chat_id, msg['message']['message_id']),
				text='''
🤖 <b>EduuRobot</b>

• Version: {}
• Developer: <a href="tg://user?id=200097591">Alisson</a>
• Owner: <a href="tg://user?id=123892996">Edu :3</a>
• Contributors:
» <a href="tg://user?id=156902435">Paulo</a>
» <a href="tg://user?id=479278708">Francis</a>
» <a href="tg://user?id=138662736">Henx</a>
» <a href="tg://user?id=142681748">Mário</a>
• Partnerships:
» <a href="https://t.me/hpxlist">HPXList - by usernein</a>
________
<a href="https://t.me/AmanoTeam">Amano Team™</a> ©2018'''.format(
					version
				),
				parse_mode='html',
				reply_markup=keyboard.start_back,
				disable_web_page_preview=True
			)


	elif user_id in ap_list:
		antipedro = db.hget('antipedro', chat_id)
		if antipedro != None:
			antipedro = antipedro.decode('utf-8')
		if antipedro == 'on':
			k.respond("LOAD ANTIPEDRO")
			response = k.respond("antipedru")
			k.respond("LOAD PADRAO")
			sleep(1)
			bot.sendMessage(
				chat_id=chat_id,
				text=response,
				reply_to_message_id=msg_id
			)
		else:
			pass


	else:
		ia_setting = db.hget('ia_setting', chat_id)
		if ia == True and ia_setting == None:
			response = ''
			text = text.replace('.', '')
			if chat_type == 'private':
				now = datetime.datetime.now()
				response = k.respond(text.upper()).replace('$hora', '`{}:{}`'.format(now.hour, now.minute))
				msg_id = None
			elif '-sr' not in text:
				try:
					if re.search(ia_pattern, text.lower()) or msg['reply_to_message']['from']['id'] == bot_id:
						now = datetime.datetime.now()
						response = k.respond(text.upper()).replace('$hora', '`{}:{}`'.format(now.hour, now.minute))
				except KeyError:
					pass
			if response != '':
				bot.sendChatAction(
					chat_id=chat_id,
					action='TYPING'
				)
				sleep(0.5)
				for msgs in response.split('#'):
					bot.sendMessage(
						chat_id=chat_id,
						text=msgs,
						parse_mode='markdown',
						reply_to_message_id=msg_id,
						disable_web_page_preview=True
					)


bot.sendMessage(
	chat_id=logs_id,
	text='''*Bot iniciado*

*Nome:* {}
*Username:* @{}
*ID:* {}
*Token:* {}

*Versão:* {}
*Logs ID:* {}
*Sudos:* {}
'''.format(
		bot_name,
		bot_username,
		bot_id,
		TOKEN[:13] + '...',
		version,
		logs_id,
		str(sudos).replace('[', '').replace(']', '')
	),
	parse_mode='Markdown'
)

print('Iniciado com sucesso\n')

MessageLoop(bot,handle_thread).run_forever()
