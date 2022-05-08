from telethon import TelegramClient, events
import time, configparser

SESSION_NAME = "test"

config = configparser.ConfigParser()

config.read('.config')

api_id = config['TELEGRAM_KEYS']['api_id']
api_hash = config['TELEGRAM_KEYS']['api_hash']

client = TelegramClient(SESSION_NAME, api_id,  api_hash, sequential_updates = True).start(phone=config['TELEGRAM_KEYS']['phone'])

chats_input = ['1test','Test3','Banana','😁'] #chats a extraer
chats_output = ['1test output']  #chats a enviar

async def main():
    input= chat_to_id(chats_input)
    output = chat_to_id(chats_output)

    @client.on(events.NewMessage(chats=input))
    async def my_event_handler(event):

        msg = event.message

        for chat,id in zip(chats_output,output):
                print(f'enviando a {chat}, id: {id}')
                await client.send_message(id,msg)

print(f'{"-"*50} \n{time.asctime()} - Bot iniciado.\n{"-"*50}')

async def chat_to_id(_chats):
    chats = []
    for chat in _chats:
        try:
            entety =await client.get_peer_id(chat)
            chats.append(await client.get_entity(entety))
        except:
            print(f'No se pudo sacar entidad {chat}')
            continue
    return chats

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()