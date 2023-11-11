from fastapi import FastAPI
import requests
app = FastAPI()

state = {'1':
            {'estado':0,
             },
        '2':
            {'estado':0,
             },
        '3':
            {'estado':0,
             },
         }
esp32_ip = "192.168.251.146"
esp32_port = 80


@app.get("/",tags=['ROOT'])
async def send_get_request():
    url = f"http://{esp32_ip}:{esp32_port}"
    print("Me quede colgado")
    response = requests.get(url)
    print("aca")
    return {"status_code": response.status_code, "content": response.text,"estados":state}


@app.get('/verification', tags=['VERIFICATION'])
async def hardware_verification():
    data_to_send = {"accion":"verificacion","casillero":"1"}
    url = f"http://{esp32_ip}:{esp32_port}"
    response = requests.post(url,json=data_to_send)
    print(response.text)

    if response.status_code == 200:
        return {"content": response.text}
    else:
        return {"message": "Failed to send POST request to ESP32", "status_code": response.status_code,"estados":state}
    

@app.post('/cargar', tags=['CARGAR'])
async def cargar(cajon:str): #TODO NUMERO DE CAJON

    #VERIFICAR QUE EL CASILLERO ESTE RESERVADOR
    if state[cajon]["estado"] !=2:
        return {"message": "Failed to Cargar, no esta Reservado"}

    data_to_send = {"accion":"cargar","casillero":cajon}
    url = f"http://{esp32_ip}:{esp32_port}"
    response = requests.post(url,json=data_to_send)


    if response.status_code == 200:
        state[cajon]["estado"] = 1
        return {"content": response.text}
    else:
        return {"message": "Failed to send POST request to ESP32", "status_code": response.status_code}

@app.post('/retirar', tags=['RETIRAR'])
async def cargar(cajon:str): #TODO NUMERO DE CAJON

    #VERIFICAR QUE EL CASILLERO ESTE RESERVADOR
    if state[cajon]["estado"] != 1:
        return {"message": "Failed to Retirar"}


    data_to_send = {"accion":"retirar","casillero":cajon}
    url = f"http://{esp32_ip}:{esp32_port}"
    response = requests.post(url,json=data_to_send)
    # print("papi que ta pasando")
    # return {"content": "RETIRADO "}

    if response.status_code == 200:
        state[cajon]["estado"] = 0

        return {"content": response.text}
    else:
        return {"message": "Failed to send POST request to ESP32", "status_code": response.status_code}

@app.post('/reservar', tags=['RESERVAR'])
async def cargar(cajon:str): #TODO NUMERO DE CAJON

    #VERIFICAR QUE EL CASILLERO ESTE RESERVADOR
    if state[cajon]["estado"] != 0:
        return {"message": "Failed to Reservar, No esta disponible"}
        
    data_to_send = {"accion":"retirar","casillero":cajon}
    url = f"http://{esp32_ip}:{esp32_port}"
    #TODO DINAMICO
    state["1"]["estado"] = 2
    return {"content":"Exito!"}