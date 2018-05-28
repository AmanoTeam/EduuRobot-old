# Arquivo de configuração de bots da Amano Team

######    Imports    ######
import telepot
import redis
import aiml

######  URLs / APIs  ######
tr_api    = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
geo_ip    = 'http://ip-api.com/json/'
gitapi    = 'https://api.github.com/users/'
adfly_url = 'http://api.adf.ly/api.php?key={}&uid={}&advert_type=int&domain=adf.ly&url={}'


###### Tokens / Keys ######
TOKEN          = '' # Seu token de bot do Telegram
tr_key         = '' # Seu token da API de tradução do Yandex
screenshot_key = '' # Sua Key da API de screenshots

# uid e key do adf.ly, caso queira contribuir com o bot, mantenha essas keys :D
adfly_uid      = '14773265'
adfly_key      = 'c24270ca22b6d55aa35150a0d9d1304e'
giphy_key      = '' # Sua Key da API do Giphy 


###### Configs gerais ######
sudos       = [123892996, 200097591, 204807919, 269122834, 276145711, 337730276, 398410916]
owners_id   = sudos
ia          = True
max_time    = 30
ap_list     = [279312106]
logs_id     = -1001297931062
ia_chat     = -1001378862339
ia_pattern  = r"\b(eduu)\b"

version     = '5.2.5'
db          = redis.StrictRedis(host='localhost', port=6379, db=0)
print_msgs  = False
k           = aiml.Kernel()
bot         = telepot.Bot(TOKEN)
