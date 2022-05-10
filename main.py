from telethon import TelegramClient, events
import time, configparser
import pandas as pd

try:
    df = pd.read_excel('./chatsdb.xlsx')
except:
    print('NO HAY BASE DE DATOS')
    quit()

SESSION_NAME = "test"

config = configparser.ConfigParser()

config.read('.config')

api_id = config['TELEGRAM_KEYS']['api_id']
api_hash = config['TELEGRAM_KEYS']['api_hash']

client = TelegramClient(SESSION_NAME, api_id,  api_hash, sequential_updates = True).start(phone=config['TELEGRAM_KEYS']['phone'])

chats_input, chats_output= df['Chat input'].to_list() , df['Chat output'].to_list()
chats_output = [chat.split(';') for chat in chats_output]


async def main():
    dialogs = await client.get_dialogs()

    _input= await chat_to_id(chats_input)
    _input = [x.id for x in _input]

    _output = [await chat_to_id(chat) for chat in chats_output]
    
    
    chat_dict = dict(zip(_input,_output))

    @client.on(events.NewMessage(chats=_input))
    async def my_event_handler(event):

        msg = event.message

        for output in chat_dict[event.peer_id.channel_id]:
            await client.send_message(output,msg)
        
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