import random
from DjangoWeb.settings import BASE_DIR
from xml.etree import ElementTree as ET
from console.models import VHost,VType, VMachine,   Datastore, OsType, Snapshot, Remote_Admin, VSwitch, Medium

#http://mussol.org/2013/07/26/parsing-and-building-xml-files-with-python/

conf_file = BASE_DIR + "/console/toolset/cfg/noauth-config.xml"

def Remove_Client(name):

    xml_conf = ET.parse(conf_file)
    xml_root = xml_conf.getroot()
    list_clients = xml_root.getchildren()


    for item in  list_clients:
        if item.attrib['name'] == name:
            print("Cliente dummy", item)
            xml_root.remove (item)

    xml_conf.write(conf_file)

def Add_Client(name,protocol,hostname,port,password,**kwargs):

    if kwargs.get('username'):
        username = kwargs['username']



    xml_conf =  ET.parse(conf_file)
    xml_root = xml_conf.getroot()

    if port == None:
        port = " "
    if password == None:
        password = " "


    new_client = ET.Element('config', name=name, protocol=protocol)
    for item in ["hostname", "port", "username", "password"]:
        if item == "hostname":
            new_param = ET.Element('param', name=item, value=hostname)
            new_client.append(new_param)
        elif item == "port":
            new_param = ET.Element('param', name=item, value=str(port))
            new_client.append(new_param)
        elif item == "username" and not protocol == "vnc":
            new_param = ET.Element('param', name=item, value=username)
            new_client.append(new_param)
        elif item == "password":
            new_param = ET.Element('param', name=item, value=password)
            new_client.append(new_param)
    xml_root.append(new_client)
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

    list_clients = xml_root.getchildren()

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

def Console_Port(option,vhost,**kwargs):

    if kwargs.get('rdport'):
        remote_port = kwargs['rdport']
        print ("Puerto Remote", remote_port)


    if option == "enable":
        OK_port = False
        while not OK_port:
            remote_port = random.randint(60000,65000)

            print ("PUERTO", remote_port)

            if not Remote_Admin.objects.filter(VHost_id=vhost.id, rdport=remote_port).exists():

                print ("Ceando nuvo pierto")
                new_port = Remote_Admin(
                    VHost=vhost,
                    rdport=remote_port,
                    used=True,
                )

                print (new_port.VHost.id)
                new_port.save()
            return new_port.rdport
    elif option == "disable":
        dis_port = Remote_Admin.objects.get(VHost_id=vhost.id, rdport=remote_port)
        dis_port.delete()
        return True

def Update_Model(list_machines):

 #   xml_conf = ET.parse(conf_file)
#    xml_root = xml_conf.getroot()

    for item in list_machines:
        Remove_Client(item.name)
        if item.VHost.VType.vendor == "VB":
            Add_Client(name=item.name, protocol="rdp", hostname=item.VHost.ipaddr, port=item.rdport, username=item.rdpuser,password=item.rdppass)
        elif item.VHost.VType.vendor == "VW":
            Add_Client(name=item.name, protocol="vnc", hostname=item.VHost.ipaddr, port=item.rdport, password=item.rdppass)