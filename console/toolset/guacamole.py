from DjangoWeb.settings import BASE_DIR
from xml.etree import ElementTree as ET

#http://mussol.org/2013/07/26/parsing-and-building-xml-files-with-python/

conf_file = BASE_DIR + "/console/toolset/cfg/noauth-config.xml"



def Add_Client(name,protocol,hostname,port,username,password):

    xml_conf =  ET.parse(conf_file)
    xml_root = xml_conf.getroot()
    list_clients = xml_root.getchildern()

    client = list_clients[0]

    if client.attrib['name'] == "dummy":
        list_param = client.getchildren()
        for item in list_param:
            if item.attrib['name'] == "hostname":
                item.attrib['value'] = hostname
            elif item.attrib['name'] == "port":
                item.attrib['value'] = port
            elif item.attrib['name'] == "username":
                item.attrib['value'] = username
            elif item.attrib['name'] == "password":
                item.attrib['value'] = password

        client.attrib['name'] = name
        client.attrib['protocol'] = protocol

    else:

        new_client = ET.Element('config', name= name, protocol= protocol)
        for item in ["hostname","port","username","password"]:
            if item == "hostname":
                new_param = ET.Element('param',name=item, value=hostname)
                new_client.append(new_param)
            elif item == "port":
                new_param = ET.Element('param', name=item, value=port)
                new_client.append(new_param)
            elif item == "username":
                new_param = ET.Element('param', name=item, value=username)
                new_client.append(new_param)
            elif item == "password":
                new_param = ET.Element('param', name=item, value=password)
                new_client.append(new_param)
        xml_root.append(new_client)

    xml_conf.write(conf_file)


def Remove_Client(name):

    xml_conf = ET.parse(conf_file)
    xml_root = xml_conf.getroot()
    list_clients = xml_root.getchildern()


    for item in  list_clients:
        if item.attrib['name'] == name:
            xml_root.remove (item)

    xml_conf.write(conf_file)


def Modify_Client(name, **kwargs):
    '''
    :param option:
    :param kwargs:
        - protocol variable
        - port variable
        - username variable
        - password variable
    :return:
    '''

    if kwargs.get('new_name'):
        new_name = kwargs['new_name']

    if kwargs.get('protocol'):
        protocol = kwargs['protocol']

    if kwargs.get('hostname'):
        hostname = kwargs['hostname']

    if kwargs.get('port'):
        port = kwargs['port']

    if kwargs.get('username'):
        username = kwargs['username']

    if kwargs.get('password'):
        password = kwargs['password']

    xml_conf = ET.parse(conf_file)
    xml_root = xml_conf.getroot()
    xml_conf.write(conf_file)

    list_clients = xml_root.getchildern()

    for item in list_clients:
        if item.attrib['name'] == name:
            params = item.getchildren()
            if new_name:
                item.attrib['name'] = name
            elif protocol:
                item.attrib['protocol'] = protocol
            for item in params:
                if item.attrib['hostname'] == "hostname" and hostname:
                    item.attrib['hostname'] = hostname
                elif item.attrib['port'] =="port" and port:
                    item.attrib['port'] = port
                elif item.attrib['username'] == "username" and username:
                    item.attrib['username'] = username
                elif item.attrib['password'] == "password" and password:
                    item.attrib['password'] = password

    xml_conf.write(conf_file)

