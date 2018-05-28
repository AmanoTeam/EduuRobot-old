from telepot.namedtuple import InlineKeyboardMarkup

start = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='📚 Comandos', callback_data='all_cmds')]+
	[dict(text='ℹ️ Informações', callback_data='infos')],
	[dict(text='🤖 Iniciar uma conversa', url='https://t.me/eduurobot?start')]
])

start_pv = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='📚 Comandos', callback_data='all_cmds')]+
	[dict(text='ℹ️ Informações', callback_data='infos')],
	[dict(text='🔎 Modo inline', switch_inline_query_current_chat='/')],
	[dict(text='➕ Me adicione em um grupo', url='https://t.me/EduuRobot?startgroup=new')]
])

all_cmds = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='👮 Admins', callback_data='admin_cmds')]+
	[dict(text='\ud83d\udc64 Usuários', callback_data='user_cmds')],
	[dict(text='🔧 Ferramentas', callback_data='tools_cmds')],
	[dict(text='⬅️ Voltar', callback_data='start_back')]
])

start_back = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='⬅️ Voltar', callback_data='start_back')]
])

cmds_back = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='⬅️ Voltar', callback_data='all_cmds')]
])

del_msg = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='🗑 Deletar mensagem', callback_data='del_msg')]
])

ia_question = InlineKeyboardMarkup(inline_keyboard=[
	[dict(text='✅ Aceitar', callback_data='ia_yes')]+
	[dict(text='❌ Recusar', callback_data='ia_no')]
])
