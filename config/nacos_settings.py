import io
import json
from configparser import ConfigParser

import nacos

SERVER_ADDRESSES = 'nacos.hypers.cc:443'

NAMESPACE = 'e631719f-38d9-40f7-8165-18bdbd255088'
client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username='admin', password='criusadmin',
                           protocol='https')
data_id = 'EXPORT_PUBLISH_MQ'
group = 'DEFAULT_GROUP'
nacos_conf = client.get_config(data_id, group)
nacos_setting = json.loads(nacos_conf)
NACOS_SETTING = dict()
for key in nacos_setting.keys():
    NACOS_SETTING[key]= nacos_setting[key]

# print(nacos_setting.keys())
# QUEUE = nacos_setting['queue']
# print(json.loads(nacos_conf))
# print(QUEUE)
# print(type(json.loads(nacos_conf)))
# print(pickle.loads(nacos_conf))