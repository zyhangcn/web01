import json
import nacos

SERVER_ADDRESSES = 'nacos.hypers.cc:443'
NAMESPACE = 'e631719f-38d9-40f7-8165-18bdbd255088'

client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username='admin',
                           password='criusadmin', protocol='https')
data_id = 'CPO'
group = 'DEFAULT_GROUP'

resp = client.get_config(data_id, group)
nacos_setting = json.loads(resp)
db_data_id = 'haa'
# group = 'DATABASE'
sesss = client.get_configs(group=group)

print(sesss['pageItems'])
for sett in sesss['pageItems']:
    print(sett['content'])
class CPO_SETTINGS:

    def __init__(self, defauls):
        self.defauls = defauls

    def __getattr__(self, item):
        return self.defauls.get(item, "")


NACOS_SETTINGS = CPO_SETTINGS(nacos_setting)
# DB_SETTINGS = CPO_SETTINGS()