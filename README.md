# EduuRobot

Instalação e execução


Requerimentos:

- Python 3.4+
- python3-pip
- redis
- Um SO Linux (O bot em Windows não funciona corretamente)
- Módulos: telepot, requests, python-aiml, pytube, pyspeedtest, redis e pyfiglet


Recomendações:
- Sistema operacional: Ubuntu, CentOS ou Debian
- Python 3.6+


Instalação:

- Abra o Terminal na pasta do bot
- Digite pip3 install -r requirements.txt
- Instale o Redis, apos isso use o comando service redis start


Configuração:

- Vá ao @BotFather e envie o comando /setprivacy, clique no bot escolhido, então clique em Disable
- Abra o arquivo config.py
- Coloque o token do seu bot em TOKEN
- Coloque sua ID em sudos e em owners_id
- Coloque a sua ID ou a de um grupo/canal em logs_id


Executando:

- Para iniciar o bot use o comando ./run.sh, ou python3 bot.py
- Para saber que o bot está executando verifique se ele mandou uma mensagem para o chat definido no logs_id, ou mande a ele um /ping


Notas:

- Alguns comandos podem não funcionar corretamente caso o bot não for executado em um sistema totalmente compatível (Veja as recomendações)
