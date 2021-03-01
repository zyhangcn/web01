import io
import json
from configparser import ConfigParser

import nacos

SERVER_ADDRESSES = 'https://nacos.hypers.cc:443'

NAMESPACE = 'e631719f-38d9-40f7-8165-18bdbd255088'

client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username='admin', password='criusadmin',
                           )
client.set_options(no_snapshot=True)
data_id = 'haa_configss'
group = 'DEFAULT_GROUP'
nacos_conf = client.get_config(data_id, group)
nacos_setting = json.loads(nacos_conf)
NACOS_SETTING = dict()
for key in nacos_setting.keys():
    NACOS_SETTING[key] = nacos_setting[key]

print(NACOS_SETTING["RABBITMQ"])
print(NACOS_SETTING)
