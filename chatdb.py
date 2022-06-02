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

        db=pd.read_csv('./chatsdb.csv')
        _inputs ,_outputs = db['Chat input'].to_list(), db['Chat output'].to_list()
        print(_inputs)
        _inputs = [str(chat).split(";") for chat in _inputs]
        _outputs = [str(chat).split(";") for chat in _outputs]
        print('----Inputs----')
        db['ID input'] = await chat_to_id(_inputs)
        print('----Ouputs----')
        db['ID output'] =await chat_to_id(_outputs)
        db.to_csv('./chatsdb.csv',index=False)

    except:
        print('No hay chatsdb.csv, creando uno vacio. Si por el contrario existia antes de correr el programa significa q hubo un error')
        temp = {'Chat input':[] , 'Chat output':[], 'ID input':[], 'ID output':[]}
        df = pd.DataFrame(temp)
        df.dropna()
        df.to_csv('./chatsdb.csv',index=False)

    print('------------LISTO------------')
    quit()


async def chat_to_id(value):
    print(f'---  {value}')
    out = []
    for _chats in value:
        temp = []
        for chat in _chats:
            try:
                entety=await client.get_peer_id(chat)
                entety=await client.get_entity(entety)
                temp.append(str(entety.id))
            except:
                print(f'No se pudo sacar entidad {chat}')
                temp.append('')
        temp = ";".join(temp)
        out.append(temp)
    print(len(value),len(out))
    return out

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
