from telethon import TelegramClient, events
import time, configparser
import pandas as pd

try:
    df = pd.read_csv('./chatsdb.csv')
    df.iloc[0]
    # print(df.head())
except:
    print('NO HAY BASE DE DATOS O ESTA VACIA')
    quit()

SESSION_NAME = "test"

config = configparser.ConfigParser()

config.read('.env')

api_id = config['TELEGRAM_KEYS']['api_id']
api_hash = config['TELEGRAM_KEYS']['api_hash']

client = TelegramClient(SESSION_NAME, api_id,  api_hash, sequential_updates = True).start(phone=config['TELEGRAM_KEYS']['phone'])

chats_input, chats_output= df['Chat input'].to_list() , df['Chat output'].to_list()
chats_output = [chat.split(';') for chat in chats_output]

async def main():
    dialogs = await client.get_dialogs()
    
    print(f'\n{"-"*50}Cargando IDS Input{"-"*50}')
    _input= await chat_to_id(chats_input)
    _input = [x.id for x in _input]

    print(f'\n{"-"*50}Cargando IDS Output{"-"*50}')
    _output = [await chat_to_id(chat) for chat in chats_output]
    
    chat_dict = dict(zip(_input,_output))

    @client.on(events.NewMessage(chats=_input))
    async def my_event_handler(event):

        msg = event.message

        for output in chat_dict[event.peer_id.channel_id]:
            try:
                await client.send_message(output,msg)
            except:
                print(f'No se puedo enviar mensaje a {output}')
    
    print(f'{"-"*50} \n{time.asctime()} - Bot iniciado.\n{"-"*50}')

async def chat_to_id(_chats):
    print(f'cargando {_chats}')
    chats = []
    x = 1
    for chat in _chats:
        print(f'{x} : {len(_chats)}')
        try:
            entety =await client.get_peer_id(chat)
            chats.append(await client.get_entity(entety))
            x = x+1
        except:
            print(f'No se pudo sacar entidad {chat}')
            chats.append(None)
            x = x+1
            continue
    print(f'Ids: {[a.id for a in chats]}')
    return chats

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()