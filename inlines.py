import requests
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

geo_ip = 'http://ip-api.com/json/'

def inlines(msg,bot,bot_username):
	first_name = msg['from']['first_name']
	user_id = msg['from']['id']
	if 'username' in msg['from']:
		username = '@'+msg['from']['username']
	else:
		username = 'nenhum'
	if msg['query'].startswith('/ip') and len(msg['query']) > 7:
		r = requests.get(geo_ip + msg['query'][4:])
		x = ''
		for i in r.json():
			x += "*{}*: `{}`\n".format(i, r.json()[i])
		articles = [InlineQueryResultArticle(
			id='abcde', title='Informações do IP', input_message_content=InputTextMessageContent(message_text='*IP*: `'+msg['query'][4:]+'`\n\n'+x, parse_mode="Markdown"))]


	elif msg['query'].startswith('/echo'):
		articles = [InlineQueryResultArticle(
			id='abcde', title=msg['query'][6:], input_message_content=InputTextMessageContent(message_text=msg['query'][6:]))]
	
	
	elif msg['query'].startswith('/invert'):
		query = msg['query'][8:]
		articles = [InlineQueryResultArticle(id='abcde', title=query[::-1],input_message_content=InputTextMessageContent(message_text=query[::-1]))]


	elif msg['query'].startswith('/markdown'):
		articles = [InlineQueryResultArticle(
			id='abcde', title=msg['query'][10:], input_message_content=InputTextMessageContent(message_text=kk, parse_mode='Markdown'))]


	elif msg['query'].startswith('/html'):
		articles = [InlineQueryResultArticle(
			id='abcde', title=msg['query'][6:], input_message_content=InputTextMessageContent(message_text=msg['query'][6:], parse_mode='html'))]


	elif msg['query'].startswith('/faces'):
		articles = [InlineQueryResultArticle(
			id='a', title='¯\\_(ツ)_/¯', input_message_content=InputTextMessageContent(message_text='¯\\_(ツ)_/¯')),
			dict(type='article',
				id='b', title='( ͡° ͜ʖ ͡°)', input_message_content=dict(message_text='( ͡° ͜ʖ ͡°)')),
			dict(type='article',
				id='c', title='( ͡~ ͜ʖ ͡°)', input_message_content=dict(message_text='( ͡~ ͜ʖ ͡°)')),
			dict(type='article',
				id='d', title='( ͡◐ ͜ʖ ͡◑))', input_message_content=dict(message_text='( ͡◐ ͜ʖ ͡◑))')),
			dict(type='article',
				id='e', title='( ͡◔ ͜ʖ ͡◔)', input_message_content=dict(message_text='( ͡◔ ͜ʖ ͡◔)')),
			dict(type='article',
				id='f', title='( ͡⚆ ͜ʖ ͡⚆)', input_message_content=dict(message_text='( ͡⚆ ͜ʖ ͡⚆)')),
			dict(type='article',
				id='g', title='( ͡ʘ ͜ʖ ͡ʘ)', input_message_content=dict(message_text='( ͡ʘ ͜ʖ ͡ʘ)')),
			dict(type='article',
				id='h', title='ヽ༼ຈل͜ຈ༽ﾉ', input_message_content=dict(message_text='ヽ༼ຈل͜ຈ༽ﾉ')),
			dict(type='article',
				id='i', title='༼ʘ̚ل͜ʘ̚༽', input_message_content=dict(message_text='༼ʘ̚ل͜ʘ̚༽')),
			dict(type='article',
				id='j', title='(╯°□°）╯', input_message_content=dict(message_text='(╯°□°）╯')),
			dict(type='article',
				id='k', title='(ﾉ◕ヮ◕)ﾉ', input_message_content=dict(message_text='(ﾉ◕ヮ◕)ﾉ')),
			dict(type='article',
				id='l', title='(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧', input_message_content=dict(message_text='(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')),
			dict(type='article',
				id='m', title='(◕‿◕)', input_message_content=dict(message_text='(◕‿◕)')),
			dict(type='article',
				id='n', title='(｡◕‿‿◕｡)', input_message_content=dict(message_text='(｡◕‿‿◕｡)')),
			dict(type='article',
				id='o', title='(っ◕‿◕)っ', input_message_content=dict(message_text='(っ◕‿◕)っ')),
			dict(type='article',
				id='p', title='(づ｡◕‿‿◕｡)づ', input_message_content=dict(message_text='(づ｡◕‿‿◕｡)づ')),
			dict(type='article',
				id='q', title='༼ つ ◕_◕ ༽つ', input_message_content=dict(message_text='༼ つ ◕_◕ ༽つ')),
			dict(type='article',
				id='r', title='(ง ͠° ͟ل͜ ͡°)ง', input_message_content=dict(message_text='(ง ͠° ͟ل͜ ͡°)ง')),
			dict(type='article',
				id='s', title='(ง\'̀-\'́)ง', input_message_content=dict(message_text='(ง\'̀-\'́)ง')),
			dict(type='article',
				id='t', title='ᕙ(⇀‸↼‶)ᕗ', input_message_content=dict(message_text='ᕙ(⇀‸↼‶)ᕗ')),
			dict(type='article',
				id='u', title='(҂⌣̀_⌣́)', input_message_content=dict(message_text='(҂⌣̀_⌣́)')),
			dict(type='article',
				id='v', title='ᕦ(ò_óˇ)ᕤ', input_message_content=dict(message_text='ᕦ(ò_óˇ)ᕤ')),
			dict(type='article',
				id='w', title='╚(ಠ_ಠ)=┐', input_message_content=dict(message_text='╚(ಠ_ಠ)=┐')),
			dict(type='article',
				id='x', title='ლ(ಠ益ಠლ)', input_message_content=dict(message_text='ლ(ಠ益ಠლ)')),
			dict(type='article',
				id='y', title='\\_(ʘ_ʘ)_/', input_message_content=dict(message_text='\\_(ʘ_ʘ)_/')),
			dict(type='article',
				id='z', title='( ⚆ _ ⚆ )', input_message_content=dict(message_text='( ⚆ _ ⚆ )')),
			dict(type='article',
				id='aa', title='(ಥ﹏ಥ)', input_message_content=dict(message_text='(ಥ﹏ಥ)')),
			dict(type='article',
				id='ab', title='﴾͡๏̯͡๏﴿', input_message_content=dict(message_text='﴾͡๏̯͡๏﴿')),
			dict(type='article',
				id='ac', title='(◔̯◔)', input_message_content=dict(message_text='(◔̯◔)')),
			dict(type='article',
				id='ad', title='(ಠ_ಠ)', input_message_content=dict(message_text='(ಠ_ಠ)')),
			dict(type='article',
				id='ae', title='(ಠ‿ಠ)', input_message_content=dict(message_text='(ಠ‿ಠ)')),
			dict(type='article',
				id='af', title='(¬_¬)', input_message_content=dict(message_text='(¬_¬)')),
			dict(type='article',
				id='ag', title='(¬‿¬)', input_message_content=dict(message_text='(¬‿¬)')),
			dict(type='article',
				id='ah', title='\\ (•◡•) /', input_message_content=dict(message_text='\\ (•◡•) /')),
			dict(type='article',
				id='ai', title='(◕‿◕✿)', input_message_content=dict(message_text='(◕‿◕✿)')),
			dict(type='article',
				id='aj', title='( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)', input_message_content=dict(message_text='( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)'))]
	
	
	elif msg['query'].startswith('/hidemsg'):
		articles = [InlineQueryResultArticle(
			id='abcde', title='Resultado: '+msg['query'][9:], input_message_content=InputTextMessageContent(message_text='\u2060'*3600+msg['query'][9:]))]


	else:
			articles = [InlineQueryResultArticle(
				id='a', title='/echo', description='Repete o texto informado', input_message_content=InputTextMessageContent(message_text='Uso: @{} /echo texto'.format(bot_username))),
			dict(type='article',
				id='b', title='/faces', description='Mostra uma lista de carinhas ¯\\_(ツ)_/¯', input_message_content=dict(message_text='Uso: @{} /faces - exibe uma lista de carinhas ¯\\_(ツ)_/¯'.format(bot_username))),
			dict(type='article',
				id='c', title='/hidemsg', description='Envia uma mensagem que não aparece nas ações recentes ao ser apagada em até 1 minuto.', input_message_content=dict(message_text='Uso: @{} /hidemsg texto para a mensagem\n\nEnvia uma mensagem que se for apagada em até 1 minuto não aparece nas ações recentes do grupo'.format(bot_username))),
			dict(type='article',
				id='d', title='/html', description='Formata um texto usando HTML', input_message_content=dict(message_text='Uso: @{} /html <b>texto</b>'.format(bot_username))),
			dict(type='article',
				id='e', title='/id', description='Exibe informações sobre você', input_message_content=dict(message_text='Suas informações:\n\nNome: '+first_name+'\nID: '+str(user_id)+'\nUsername: '+username)),
			dict(type='article',
				id='f', title='/ip', description='Exibe informações de um IP informado', input_message_content=dict(message_text='Uso: @{} /ip google.com'.format(bot_username))),
			dict(type='article',
				id='g', title='/markdown', description='Formata um texto usando Markdown', input_message_content=dict(message_text='Uso: @{} /markdown *texto*'.format(bot_username)))
			]



	bot.answerInlineQuery(msg['id'],results=articles, is_personal=True)