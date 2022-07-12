def insert_usuario(nome:str, email:str, senha:str, isadm: int='NULL', apik: str='NULL'):
    ''' INSERT INTO usuario (nome,email,senha,is_admin,grafana_api_key) VALUES ('{nome}','{email}','{senha}','{isadm}','{apik}'); '''
    return  f''' INSERT INTO usuario (nome,email,senha,is_admin,grafana_api_key) VALUES ('{nome}','{email}','{senha}',{isadm},'{apik}'); '''

def delete_usuario(id):
    id = int(id)
    ''' DELETE FROM usuario WHERE usuario.id = '{id}'; '''
    return f''' DELETE FROM usuario WHERE usuario.id = {id}; '''

def select_id_email(email):
    ''' SELECT id FROM usuario WHERE usuario.email = 'email' '''
    return  f''' SELECT id FROM usuario WHERE usuario.email = '{email}' '''

def select_email_id(id):
    ''' SELECT email FROM usuario WHERE usuario.id = 'id' '''
    return  f''' SELECT email FROM usuario WHERE usuario.id = '{id}' '''

def select_isadmin_id(id):
    ''' SELECT is_admin FROM usuario WHERE usuario.id = 'id' '''
    return  f''' SELECT is_admin FROM usuario WHERE usuario.id = {id} '''

def select_nome_id(id):
    ''' SELECT nome FROM usuario WHERE usuario.id = 'id' '''
    return  f''' SELECT nome FROM usuario WHERE usuario.id = '{id}' '''

def select_user_id(id):
    id = int(id)
    ''' SELECT nome,email,grafana_api_key FROM usuario WHERE usuario.id = 'id' '''
    return  f''' SELECT nome,email,grafana_api_key FROM usuario WHERE usuario.id = {id} '''

def usuario_select_all():
    ''' SELECT * FROM usuario; '''
    return f''' SELECT * FROM usuario; '''

def usuario_select_all_email():
    ''' SELECT id, email FROM usuario; '''
    return f''' SELECT id, email FROM usuario; '''

def select_id(email, senha):
    ''' SELECT id FROM usuario WHERE usuario.email='{email}' AND usuario.senha='{senha}'; '''
    return f''' SELECT id FROM usuario WHERE usuario.email='{email}' AND usuario.senha='{senha}'; '''

def select_senha(id):
    id = int(id)
    ''' SELECT senha FROM usuario WHERE usuario.id='{id}'; '''
    return f''' SELECT senha FROM usuario WHERE usuario.id={id}; '''

# seleciona os modulos de um usuario
def select_user_modules(id):
    id = int(id)
    ''' SELECT modulo_id FROM usuario_modulo WHERE usuario_modulo.usuario_id='{id}'; '''
    return f''' SELECT modulo_id FROM usuario_modulo WHERE usuario_modulo.usuario_id={id}; '''

# seleciona os sensores
def select_module_sensors(id):
    id = int(id)
    ''' SELECT id, id_tipo FROM sensor WHERE sensor.id_modulo='{id}'; '''
    return f''' SELECT id, id_tipo FROM sensor WHERE sensor.id_modulo={id}; '''

def select_dados(id_sensor):
    id_sensor = int(id_sensor)
    ''' SELECT id, id_tipo FROM sensor WHERE sensor.id_modulo='{id}'; '''
    return f''' SELECT id, id_tipo FROM sensor WHERE sensor.id_modulo={id}; '''

def select_dados_grafana(id_sensor):
    id_sensor = int(id_sensor)
    ''' SELECT id, id_tipo FROM sensor WHERE sensor.id_modulo='{id}'; '''
    return f''' 
        SELECT
            time_bucket_gapfill('5 minutes', "time") as time,
            LOCF(AVG(temperature)) AS sensor_1
        FROM sensor_data
        WHERE
            $__timeFilter("time") AND
            sensor_id = 1
        GROUP BY time_bucket_gapfill('5 minutes', "time")
        ORDER BY 1
'''

def select_modulo_nome(nome):
    ''' SELECT id FROM modulo WHERE modulo.nome = '{nome}'; '''
    return f''' SELECT id FROM modulo WHERE modulo.nome = '{nome}'; '''

def insert_modulo(nome):
    ''' INSERT INTO modulo(nome) VALUES {nome}'''
    return f''' INSERT INTO modulo(nome) VALUES ('{nome}') RETURNING id; '''

def insert_usuario_modulo(usuario_id, modulo_id):
    ''' INSERT INTO usuario_modulo(usuario_id, modulo_id) VALUES {usuario_id, modulo_id}'''
    return f''' INSERT INTO usuario_modulo(usuario_id, modulo_id) VALUES ('{usuario_id}','{modulo_id}'); '''

def select_modulos_id(id_user):
    ''' SELECT modulo.nome, modulo.id FROM modulo, usuario_modulo WHERE usuario_modulo.modulo_id = modulo.id AND usuario_modulo.usuario_id = 11; '''
    return f''' SELECT modulo.nome, modulo.id FROM modulo, usuario_modulo WHERE usuario_modulo.modulo_id = modulo.id AND usuario_modulo.usuario_id = {id_user}; '''

def select_modulos():
    ''' SELECT modulo.id, usuario.email, modulo.nome FROM usuario, modulo, usuario_modulo WHERE usuario.id = usuario_modulo.usuario_id AND modulo.id = usuario_modulo.modulo_id; '''
    return f''' SELECT modulo.id, usuario.email, modulo.nome FROM usuario, modulo, usuario_modulo WHERE usuario.id = usuario_modulo.usuario_id AND modulo.id = usuario_modulo.modulo_id; '''

def select_nome_modulo(id):
    ''' SELECT nome FROM modulo WHERE modulo.id = {id}; '''
    return f''' SELECT nome FROM modulo WHERE modulo.id = {id}; '''

def select_sensores_modulo(id_modulo):
    ''' 
    SELECT 
        sensor.nome, tipo_sensor.tipo, tipo_leitura.tipo, sensor_has_tipo_leitura.tipo_valor 
    FROM 
        sensor, tipo_sensor, sensor_has_tipo_leitura, tipo_leitura 
    WHERE
            sensor.id_modulo = {id_modulo} 
        AND 
            sensor.id_tipo = tipo_sensor.id 
        AND 
            sensor_has_tipo_leitura.sensor_id = sensor.id 
        AND
            sensor_has_tipo_leitura.id_tipo_leitura = tipo_leitura.id;
        '''
    return f''' 
            SELECT 
                sensor.nome, tipo_sensor.tipo, tipo_leitura.tipo, sensor_has_tipo_leitura.tipo_valor 
            FROM 
                sensor, tipo_sensor, sensor_has_tipo_leitura, tipo_leitura 
            WHERE
                    sensor.id_modulo = {id_modulo} 
                AND 
                    sensor.id_tipo_sensor = tipo_sensor.id 
                AND 
                    sensor_has_tipo_leitura.sensor_id = sensor.id 
                AND
                    sensor_has_tipo_leitura.id_tipo_leitura = tipo_leitura.id;
    '''

def select_tipos_sensor():
    ''' SELECT id, tipo FROM tipo_sensor; '''
    return f''' SELECT id, tipo FROM tipo_sensor; '''

def select_tipos_leitura():
    ''' SELECT id, tipo FROM tipo_leitura; '''
    return f''' SELECT id, tipo FROM tipo_leitura; '''

def insert_sensor(id_tipo_sensor, id_modulo, mqtt_topic, nome):
    ''' INSERT INTO sensor(id_tipo_sensor, id_modulo, mqtt_topic, nome) VALUES ({id_tipo_sensor}, {id_modulo}, {mqtt_topic}, {nome}) RETURNING id; '''
    return f''' INSERT INTO sensor(id_tipo_sensor, id_modulo, mqtt_topic, nome) VALUES ({id_tipo_sensor}, {id_modulo}, {mqtt_topic}, {nome}) RETURNING id; '''

def select_enum_values():
    return '''SELECT enum_range(NULL::tipo_valor);'''

def insert_sensor_has_tipo_leitura(id_tipo_leitura, sensor_id, tipo_dado):
    return f''' INSERT INTO sensor_has_tipo_leitura(id_tipo_leitura, sensor_id, tipo_valor) VALUES ({id_tipo_leitura},{sensor_id},{tipo_dado});'''

def insert_chave(chave, id_usuario, id_sensor):
    return f''' INSERT INTO chaves(chave,id_usuario,id_sensor) VALUES ({chave}, {id_usuario}, {id_sensor}) '''