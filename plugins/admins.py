def call_admins(msg,bot,chat_id,msg_id):
	ademirs = bot.getChatAdministrators(chat_id)
	num = 0
	try:
		message_id = msg['reply_to_message']['message_id']
	except:
		message_id = msg_id
	try:
		msg_url = '*•* [Ir para a mensagem](https://t.me/' + msg['chat']['username'] + '/' + str(message_id)
	except:
		msg_url = ''
	sent = bot.sendMessage(
		chat_id=chat_id,
		text='Aguarde enquanto eu notifico os admins...',
		parse_mode='Markdown',
		reply_to_message_id=msg_id
	)
	for status in ademirs:
		adm_id = status['user']['id']
		try:
			if 'reply_to_message' in msg:
				bot.forwardMessage(
					chat_id=adm_id,
					from_chat_id=chat_id,
					message_id=message_id
				)
			bot.sendMessage(
				chat_id=adm_id,
				text='''
*Mensagem de administração:*
		
*• Mensagem relatada por:* {} ({})
*• Grupo:* {}
{}'''.format(
					msg['from']['first_name'],
					msg['from']['id'],
					msg['chat']['title'],
					msg_url
				),
				parse_mode='Markdown'
			)
			num += 1
		except:
			pass
	bot.editMessageText(
		(chat_id,sent['message_id']),
		text='*Eu notifiquei com sucesso {} admins!*'.format(
			num
		),
		parse_mode='Markdown'
	)