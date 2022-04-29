from telethon import TelegramClient, events
import time, configparser, os, sys

os.chdir(sys.path[0])

#limpia sesiones previas
SESSION_NAME = "test"
if f"{SESSION_NAME}.session" in os.listdir():
    os.remove(f"{SESSION_NAME}.session")

#carga de api keys
config = configparser.ConfigParser()

config.read('.config')

api_id = config['TELEGRAM_KEYS']['api_id']
api_hash = config['TELEGRAM_KEYS']['api_hash']

client = TelegramClient(SESSION_NAME, api_id,  api_hash, sequential_updates = True).start()

chats_input = ['Test3','Test2'] #chats a extraer
chats_output = ['😵']  #chats a enviar

async def main():
    @client.on(events.NewMessage(chats=chats_input))
    async def my_event_handler(event):
        #check if not private
        if not event.is_private:
            sender = await event.get_sender()
            msg = event.message.to_dict()
            print(f'\n{time.asctime()}\nmsg: {msg["message"]} media: {bool(msg["media"])}')

            if msg['media']:
                #tube q hacer esta cirujeada pq sino no se enviaban, lo q hace es bajar los archivos adjuntos a una carpeta temporal, los envia y luego lo borra para no llenar el disco
                await event.message.download_media(file="./temp_mediafiles/temp",progress_callback=download_callback,)
                temp = os.listdir('./temp_mediafiles/')[0]
                
                for chat in chats_output:
                    print(f'enviando a {chat}')
                    await client.send_message(chat,msg["message"],file=f"./temp_mediafiles/{temp}")
                    os.remove(f"./temp_mediafiles/{temp}")
            else:
                for chat in chats_output:
                    print(f'enviando a {chat}')
                    await client.send_message(chat,msg["message"])

print(f'{"-"*50} \n{time.asctime()} - Bot iniciado.\n{"-"*50}')

def download_callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()