# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

logging.basicConfig()
names_users = {}

def send_message(msg,user):
    return json.dumps({"type": "message", "message":msg, "user":user})

def users_event():
    return json.dumps({"type": "users", "count": len(names_users)})

def name_event(name):
    return json.dumps({"type": "name", "name": name})

async def msg_to(websocket,msg,user): #Manda msg do user só para websocket
    message = send_message(msg, user)
    await websocket.send(message)

async def msg_from(name,msg):  #Manda msg do name para todos menos para ele
    if len(names_users)>1:
        message = send_message(msg,name)
        for key in names_users:
            if (not(key == name)):
                await names_users[key].send(message)

async def notify_wellcome(websocket):
    message = send_message("Seja bem vindo, digite seu nome no campo de mensagem e clique em Enviar","Chat")
    await websocket.send(message)

async def notify_wellcome_for_all(name):
    if len(names_users)>1:  # asyncio.wait doesn't accept an empty list
        message = send_message((name + " entrou!"),"Chat")
        for key in names_users:
            if (not(key == name)):
                await names_users[key].send(message)

async def notify_name_client(websocket,name):
    message = name_event(name)
    await websocket.send(message)

async def notify_users():
        message = users_event()
        for key in names_users:
            await names_users[key].send(message)

async def register(websocket):

    await notify_wellcome(websocket)
    msg = await websocket.recv()
    data = json.loads(msg)

    while (data["message"] in names_users):
        greeting = "O nome '" + data["message"] + "' já existe, digite outro"
        await msg_to(websocket, greeting, "Chat")
        msg = await websocket.recv()
        data = json.loads(msg)

    names_users[data["message"]] = websocket
    greeting = "Nome do usuário configurado como: " + data["message"]
    await msg_to(websocket, greeting, "Chat")

    await notify_name_client(websocket,data["message"])
    await notify_wellcome_for_all(data["message"])
    await notify_users()

async def unregister(websocket):
    for key in names_users:
        if (names_users[key] == websocket):
            name_to_be_deleted = key
    del names_users[name_to_be_deleted]

    if len(names_users)>0:
        message = send_message(name_to_be_deleted + " saiu!","Chat")
        for key in names_users:
            await names_users[key].send(message)

async def chat(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "message":
                await msg_from(data["user"],data["message"])
            if data["type"] == "private":
                if (data["to"] in names_users):
                    await msg_to(names_users[data["to"]],data["message"], (data["user"]+"-Privado"))
                else:
                    await msg_to(websocket,data["message"], "Chat")
    finally:
        await unregister(websocket)

start_server = websockets.serve(chat, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
