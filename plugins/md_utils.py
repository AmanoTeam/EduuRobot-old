# Code writen by @marminino to escape Markdown code on Telegram API

def escape(text):
	text = text.replace('[', '\[')
	text = text.replace('_', '\_')
	text = text.replace('*', '\*')
	text = text.replace('`', '\`')
	
	return text