import nacos

SERVER_ADDRESSES='nacos.hypers.cc'

NAMESPACE ='haa'
client = nacos.NacosClient(SERVER_ADDRESSES,namespace=NAMESPACE)
data_id = 'EXPORT_PUBLISH_MQ'
group='DEFAULT_GROUP'
print(client.get_config(data_id,group))