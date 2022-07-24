import random
from paho.mqtt.client import MQTTMessage, Client
from database.db import HandleDB

BROKER = "200.201.88.141"
PORT = 1883

db_handler = HandleDB()

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'plataforma-smartoffice'
password = '123456'

def connect_mqtt():
    def on_connect(client: Client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(client: Client, userdata, msg: MQTTMessage):
        print(f" Received {msg.payload.decode()} from {msg.topic} topic ")
        handle_message(msg.topic, msg.payload.decode())

    client = Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    subscribe_topicos(client)
    return client



def subscribe_topicos(client: Client):
    topicos = get_topicos()
    for topico, in topicos:
        print(topico)
        client.subscribe(topico)

def get_topicos():
    db_handler.execute('SELECT mqtt_topic FROM sensor;')
    return db_handler.fetch_all()

def buscar_sensor(topico):
    db_handler.execute(f''' SELECT id FROM sensor WHERE sensor.mqtt_topic = '{topico}'; ''')
    return db_handler.fetch_one()

def tipos_leitura_sensor(sensor_id):
    db_handler.execute(f''' SELECT tipo_valor, id_tipo_leitura FROM sensor_has_tipo_leitura WHERE sensor_has_tipo_leitura.sensor_id = {sensor_id}; ''')
    return db_handler.fetch_all()

def insert_dado_int(dado: int, timestmp, id_sensor, nome_leitura, id_tipo_leitura):
    db_handler.execute(f''' INSERT INTO leitura_int(valor_dado, timestamp, id_sensor,id_tipo_leitura, nome) VALUES ({dado},'{timestmp}',{id_sensor},{id_tipo_leitura},'{nome_leitura}'); ''')
    db_handler.commit()
    
def insert_dado_double(dado: float, timestmp, id_sensor, nome_leitura, id_tipo_leitura):
    db_handler.execute(f'''INSERT INTO leitura_double(valor_dado, timestamp, id_sensor,id_tipo_leitura, nome) VALUES ({dado},'{timestmp}',{id_sensor},{id_tipo_leitura},'{nome_leitura}');''')
    db_handler.commit()

def insert_dado_boolean(dado: bool, timestmp, id_sensor, nome_leitura, id_tipo_leitura):
    db_handler.execute(f'''INSERT INTO leitura_boolean(valor_dado, timestamp, id_sensor,id_tipo_leitura, nome) VALUES ({dado},'{timestmp}',{id_sensor},{id_tipo_leitura},'{nome_leitura}');''')
    db_handler.commit()

def handle_insert_dado(tipo_valor_leitura, dado, timestmp, id_sensor, nome_leitura, id_tipo_leitura):
    if tipo_valor_leitura == 'int':
        insert_dado_int(int(dado), timestmp, id_sensor, nome_leitura, id_tipo_leitura)
    elif tipo_valor_leitura == 'double':
        insert_dado_double(float(dado), timestmp, id_sensor, nome_leitura, id_tipo_leitura)
    else:
        insert_dado_boolean(bool(dado), timestmp, id_sensor, nome_leitura, id_tipo_leitura)

def get_tipo_leitura(id):
    db_handler.execute(f''' SELECT tipo FROM tipo_leitura WHERE tipo_leitura.id = {id}''')
    return db_handler.fetch_one()

def convert_to_dict(payload: str):
    'temperatura/valor@umidade/valor@corrente/valor@tensao/valor@tempo/2022-06-18 14:35:47.60209-03'
    if payload.count('@') + payload.count('/') > 0:
        dados = payload.split("@")
        d = dict()
        for i in range(len(dados)):
            key, value = dados[i].split('/')
            d[key] = value
        return d

def handle_message(topico: str, payload: str):
    id_sensor, = buscar_sensor(topico)
    if id_sensor is None:
        print(f'Sensor com topico {topico} nao cadastrado')
        return
    tipos_valor_leitura:list[tuple] = tipos_leitura_sensor(id_sensor)
    dados_as_dict = convert_to_dict(payload)
    if dados_as_dict is not None:
        keys = dados_as_dict.keys()
        timestmp = dados_as_dict.pop('tempo')
        for tipo_valor_leitura, id_tipo_leitura in tipos_valor_leitura:
            tipo_leitura, = get_tipo_leitura(id_tipo_leitura)
            if tipo_leitura is not None:
                handle_insert_dado(tipo_valor_leitura, dados_as_dict[tipo_leitura], timestmp, id_sensor, 'atributo_' + tipo_leitura, id_tipo_leitura)
            else:
                print(f''' Propriedade '{tipo_leitura}' do sensor nao esta cadastrada no banco ''')
    else:
        print(' Payload não formatado corretamente ')

def run():
    client = connect_mqtt()
    client.loop_forever()


if __name__ == '__main__':
    run()
