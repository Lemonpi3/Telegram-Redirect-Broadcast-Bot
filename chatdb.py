import pandas as pd
from telethon import TelegramClient
import configparser

# Genera la base de datos de chats y busca sus ids

SESSION_NAME = "test"

config = configparser.ConfigParser()

config.read('.config')

api_id = config['TELEGRAM_KEYS']['api_id']
api_hash = config['TELEGRAM_KEYS']['api_hash']

client = TelegramClient(SESSION_NAME, api_id,  api_hash, sequential_updates = True).start(phone=config['TELEGRAM_KEYS']['phone'])

async def main():
    dialogs = await client.get_dialogs()
    
    try:
        print('---------Generando IDs----------')

        db=pd.read_excel('chatsdb.xlsx')
        _inputs ,_outputs = db['Chat input'].to_list(), db['Chat output'].to_list()
        _inputs ,_outputs= [_chat.split(';') for _chat in _inputs] ,[_chat.split(';') for _chat in _outputs]
        db['ID input'],db['ID output'] = await chat_to_id(_inputs) ,await chat_to_id(_outputs)
        db.to_excel('./chatsdb.xlsx',index=False)

    except:

        print('no hay chatsdb.excel, creando uno vacio. Si por el contrario existia antes de correr el programa significa q hubo un error')
        temp = {'Chat input':[] , 'Chat output':[], 'ID input':[], 'ID output':[]}
        df = pd.DataFrame(temp)
        df.dropna()
        df.to_excel('./chatsdb.xlsx',index=False)

    print('------------LISTO------------')
    quit()


async def chat_to_id(_chats):
    chats = []
    for chat in _chats:
        try:
            for _chat in chat:
                entety =await client.get_peer_id(_chat)
                entety=await client.get_entity(entety)
                chats.append(str(entety.id))
        except:
            print(f'No se pudo sacar entidad {chat}')
            chats.append('')
    return ';'.join(chats)


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
