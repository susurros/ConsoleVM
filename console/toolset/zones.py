import re
from console.models import OsType, Datastore, VHost, VMachine, VDisk
from .ssh import execCMD, sshSession,execSFTP
from DjangoWeb.settings import BASE_DIR
from .guacamole import Add_Client, Remove_Client, Console_Port




#https://ervikrant06.wordpress.com/2014/07/27/how-to-configure-solaris-10-as-branded-zone-in-solaris-11/
#http://thegeekdiary.com/how-to-create-solaris-8-and-9-branded-zones-in-solaris-10/
#http://www.oracle.com/technetwork/server-storage/solaris10/downloads/index.html
#https://docs.oracle.com/cd/E26502_01/html/E29024/gjluk.html  Solaris 10 Branded ZOne
#https://blogs.oracle.com/jsavit/entry/solaris_10_branded_zone_vm
#http://www.oracle.com/technetwork/server-storage/solaris11/documentation/solaris-11-cheat-sheet-1556378.pdf#
#http://www.oracle.com/technetwork/articles/servers-storage-admin/o11-118-s11-script-zones-524499.html
#http://www.oracle.com/technetwork/articles/servers-storage-admin/o11-118-s11-script-zones-524499.html
#http://www.oracle.com/technetwork/server-storage/solaris11/documentation/solaris-11-cheat-sheet-1556378.pdf
#http://theurbanpenguin.com/wp/index.php/solaris-11-virtualization-using-zones/
#http://thegeekdiary.com/solaris-11-ips-hand-on-lab-creating-ips-repository/
#http://thegeekdiary.com/how-to-create-a-zone-in-solaris-11/



def zone_parser(option,data,**kwargs):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vmname variable
    :return:
    '''

    if kwargs.get('vmname'):
        vmname = kwargs['vmname']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']

    if kwargs.get('vmdir'):
        vmdir = kwargs['vmdir']

    if kwargs.get('vmfile'):
        vmfile = kwargs['vmfile']

    if kwargs.get('vmdisk'):
        vmdisk = kwargs['vmdisk']


    # Commands Hosts

    if option == "ifaces":
        ifaces = []
        for line in data:
            ifaces.append(line)
        return line

    elif option == "port_groups":
        portgroups = []
        for line in data:
            portgroups.append(re.sub('\n','',line))
        print (portgroups)
        return portgroups

    elif option == "zpool":
        zpool = []
        for line in data:
            zpool.append(re.sub('\n','',line))
        return zpool

    elif option == "datastore":
        dslist = []
        for line in data:
            rx = re.search('(.+)\s;\s(.+)',line)
            print(rx)
            if rx:
                vmname = re.match('(.+)\s;\s(.+)',line).group(1)
                dpath = re.sub('/'+vmname,'',re.match('(.+)\s;\s(.+)',line).group(2))
                dname = re.match('.+\/(.+)\/' + vmname,line).group(1)
                if len(dslist) == 0:
                    data = {
                        'dname': dname,
                        'dpath': dpath,
                    }
                    dslist.append(data)
                else:
                    for ds in dslist:
                        if not ds['dpath'] == dpath:
                            data = {
                                'dname': dname,
                                'dpath': dpath,
                            }
                            dslist.append(data)
        print(dslist)
        return dslist

    #Commands Info_Zones

    elif option == "list_all":

        list_machines = []
        for line in data:
            rx = re.search('^.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line)
            if rx:
                machine = {
                    'name': re.match('.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(1),
                    'uuid': re.match('.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(2),
                }
                list_machines.append(machine)
        return list_machines

    elif option == "list_all_run":
        list_machines = []
        for line in data:
            rx = re.search('.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line)
            if rx:
                machine = {
                    'name': re.match('.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(1),
                    'uuid': re.match('.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(2),
                }
                list_machines.append(machine)
        return list_machines

    elif option == "list_run":
        for line in data:
            rx = re.search('.*:(\d+|\w+):(\w+):.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line)
            if rx:
                if re.match('.*:(\d+|\w+):(\w+):.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(2) == "running":
                    return True
                else:
                    return False
            else:
                return False

    elif option == "get_uuid":
        for line in data:
            rx = re.search('^.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line)
            if rx:
                uuid = re.match('^.*:(\d+|\w+):\w+:.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(2)
                return uuid

    elif option == "ostypes":
        target = open(data, 'r')
        vmostype = []
        for line in target:
            rx = re.search('^(.+)\s;\s(.+)', line)
            if rx:
                os = {
                    "id": re.match('^(.+)\s;\s(.+)', line).group(1),
                    "desc": re.match('^(.+)\s;\s(.+)', line).group(2)
                }
                vmostype.append(os)

        target.close()
        return vmostype

    elif option == "vm_uptime":
        print ("utime")
        for line in data:
            print (line)
            rx = re.search ('\s+\d+:\d\d\w\w\s+up\s(.+),\s+\d+\s+user',line)
            if rx:
                regex = re.sub('"','',re.match('\s+\d+:\d\d\w\w\s+up\s(.+),\s+\d+\s+user',line).group(1))
                print (regex)
                return regex

    elif option == "vm_state":
        for line in data:
            rx = re.search('.*:(\d+|\w+):(\w+):.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line)
            if rx:
                state = re.match('^.*:(\d+|\w+):(\w+):.+?:([a-f|0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}):', line).group(2)
                if state == "installed":
                    return "PW"

                elif state== "running":
                    return "RN"
                else:
                    return state

    elif option == "vm_installed":
        pass  # CHECK IF is necessary

    elif option == "vm_mem":
        for line in data:
            rx = re.search('^\s+physical:\s*(\d+)(\w)',line)
            if rx:
                mem = re.match('^\s+physical:\s*(\d+)(\w)',line).group(1)
                mag = re.match('^\s+physical:\s*(\d+)(\w)',line).group(2)
                if mag == "G":
                    return (int(mem) * 1024)
                else:
                    return mem

    elif option == "vm_path":
        for line in data:
            rx = re.search('^zonepath:\s+(.+)', line)
            if rx:
                return re.match('^zonepath:\s+(.+)', line).group(1)

    elif option == "vm_ncpu":

        for line in data:
            rx = re.search('^ncpus:\s*(\d+)',line)
            if rx:
                cpu = re.match('ncpus:\s*(\d+)', line).group(1)
                return cpu

    elif option == "datastore_zfs_path":
        for line in data:
            return re.sub('\\n',"",line)

    elif option == "vm_nic":
        for line in data:
            rx = re.search('^\s+physical:\s+(.+)', line)
            if rx:
                return re.match('^\s+physical:\s+(.+)', line).group(1)



    elif option == "vm_link":
        for line in data:
            rx = re.search('.+\s;\s(.+)',line)
            if rx:
                return re.match('.+\s;\s(.+)',line).group(1)

def zone_info(option,**kwargs):
    '''
       :param option:
       :param kwargs:
           - vhost object
           - vmname variable
       :return:
       '''

    if kwargs.get('vmname'):
        vmname = kwargs['vmname']

    if kwargs.get('vuuid'):
        vuuid = kwargs['vuuid']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']

    if kwargs.get('vmdir'):
        vmdir = kwargs['vmdir']

    if kwargs.get('vmfile'):
        vmfile = kwargs['vmfile']

    if kwargs.get('datastore'):
        datastore = kwargs['datastore']

    if kwargs.get('portgroup'):
        portgroup = kwargs['portgroup']

    # Comands HOSTs

    if option == "port_groups":
        cmdCLI = "dladm show-etherstub | grep -v LINK"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "ifaces":
        cmdCLI == "dladm  show-ether | grep -v LINK | awk '{print $1}'"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "port_group_exists":
        cmdCLI = "dladm show-etherstub"
        for port in zone_parser(option="port_groups", data=execCMD(vhost=vhost, cmd=cmdCLI)):
            vhost_port = re.sub('\s','', port)
            port_form = re.sub('\s','', portgroup)
            if str(vhost_port) == str(port_form):
                return True
        return False

    elif option == "zpool":
        cmdCLI = "zpool list | grep -v 'NAME' | awk '{print $1}'"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "datastore":
        cmdCLI = "zoneadm list -pi | grep -v global | awk -F\: '{print $2," + '";"' + ",$4}'"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    # Commands Info_Zones
    elif option == "list_all":
        cmdCLI = "zoneadm list -ip | grep -v global"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "list_all_run":
        cmdCLI = "zoneadm list -pi | egrep -v 'ID|global' | grep running"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "list_run":
        cmdCLI = "zoneadm -z " + vmname + " list -p"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "get_uuid":
        cmdCLI = "zoneadm -z " + vmname + " list -p"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "ostypes":
        filename = BASE_DIR + "/console/toolset/cfg/zones_os_guest.csv"
        return zone_parser(option=option, data=filename)

    elif option == "vm_uptime":
        cmdCLI = "zlogin " + vmname + " uptime"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_state":

        cmdCLI = "zoneadm -z " + vmname + " list -p"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_installed":
        pass  # CHECK IF is necessary

    elif option == "vm_mem":
        cmdCLI = "zonecfg -z " + vmname + "  info capped-memory| grep physical"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_ncpu":
        cmdCLI = "zonecfg -z " + vmname + "  info capped-cpu [ncpus] | cut -d '[' -f 2| cut -d ']' -f1| grep ncpu "
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_path":
        cmdCLI = "zonecfg -z " + vmname + "  info zonepath"
        return zone_parser(option="vm_path", data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_disk_size":
        cmdCLI = "zonecfg -z " + vmname + "  info zonepath"
        vdisk_path = zone_parser(option="vm_path", data=execCMD(vhost=vhost, cmd=cmdCLI))
        cmdCLI = "zfs list" + vdisk_path + " | grep -v MOUNTPOINT| awk '{print $1}' "
        return execCMD(vhost=vhost, cmd=cmdCLI)

    elif option == "vm_disk_zfs_path":
        cmdCLI = "zonecfg -z " + vmname + "  info zonepath"
        vdisk_path = zone_parser(option="vm_path", data=execCMD(vhost=vhost, cmd=cmdCLI))
        cmdCLI = "zfs list" + vdisk_path + " | grep -v MOUNTPOINT| awk '{print $1}' "
        return execCMD(vhost=vhost, cmd=cmdCLI)

    elif option == "datastore_zfs_path":
        cmdCLI = "zfs list " + datastore + " | grep -v MOUNTPOINT| awk '{print $1}' "
        return zone_parser(option="datastore_zfs_path", data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_nic":
        cmdCLI = "zonecfg -z " + vmname + " info net | grep physical"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))


    elif option == "vm_vrde":
        pass  # TODO SSH connection or ZLOGIN

    elif option == "vm_os":
        return "solaris11"

    elif option == "vm_link":
        cmdCLI = 'dladm show-link | grep ' + vmname + ' | awk ' + "'{print $1," + '";"' + ",$5}'"
        return zone_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

def zone_control(option,**kwargs):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vm variable
    :return:
    '''

    if kwargs.get('vm'):
        vmachine = kwargs['vm']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']

    print ("CONTROL ZONE")

    if option == "start_vm":
        cmdCLI = "zoneadm -z " + vmachine.name + " boot"
        execCMD(vhost=vhost, cmd=cmdCLI)
        if zone_info(option="list_run",vhost=vhost,vmname=vmachine.name):
            vmachine.state = zone_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
            vmachine.uptime = zone_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
            vmachine.save()
            return True
        else:
            return False

    elif option == "stop_vm":
        print ("STOP VN")

        cmdCLI = "zoneadm -z " + vmachine.name + " halt "
        print (cmdCLI)

        execCMD(vhost=vhost, cmd=cmdCLI)
        vmachine.state = zone_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
        vmachine.uptime = zone_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
        vmachine.save()

        if not zone_info(option="list_run",vhost=vhost,vmname=vmachine.name):
            return True
        else:
            return False

def zone_create_vm(vhost,vm):

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    zonetemplate = vm['datastore'] + "/template/"
    if not zone_info(option="template", vhost=vhost, vmname=vm):
        cmdCLI = 'mkdir -p ' + zonetemplate
        ssh.addCommand(cmdCLI)

    cmdCLI = 'cd '+ zonetemplate
    ssh.addCommand(cmdCLI)

    #Create Zone Template
    cmdCLI = 'zonecfg -z ' + vm['name'] + ' "create"'
    ssh.addCommand(cmdCLI)

    #Create Storage: Zone Path
    # CReate datastore zfs create -o mountpoint=/zones rpool/zones
    ds_zfs_path = zone_info(option="datastore_zfs_path",vhost=vhost,datastore=vm['datastore'])
    zdisk = str(ds_zfs_path) + "/" + vm['name']
    dpath = vm['datastore'] + "/" + vm['name']
    cmdCLI = 'zfs create -o mountpoint=' + dpath + " " + zdisk
    ssh.addCommand(cmdCLI)
    cmdCLI = 'zfs set quota=' + vm['dsize'] + "M  " + zdisk
    ssh.addCommand(cmdCLI)
    cmdCLI = 'zonecfg -z ' + vm['name'] + ' "set set zonepath=' + dpath + '"'
    ssh.addCommand(cmdCLI)

    #Create Network
    znic = vm['name'] + '_nic1'
    cmdCLI = 'dladm create-vnic -l ' + vm['net'] + ' ' + znic
    ssh.addCommand(cmdCLI)

    cmdCLI = 'zonecfg -z ' + vm['name'] + ' "add net; set physical=' + znic + ' ;end"'
    ssh.addCommand(cmdCLI)


    #Limit Resources CPU and Mem zonecfg -z ' + vm['name']  + '" https://docs.oracle.com/cd/E23824_01/html/821-1460/z.config.ov-3.html
    #http://www.oracle.com/technetwork/server-storage/solaris11/technologies/os-zones-hard-partitioning-2347187.pdf

    cmdCLI = 'zonecfg -z ' + vm['name']  + ' "add capped-cpu; set ncpus=' + vm['cpu']  + ';end"'
    ssh.addCommand(cmdCLI)

    cmdCLI = 'zonecfg -z ' + vm['name']  + ' "add capped-memory; set physical=' + vm['mem']+ 'm' + ';end"'
    ssh.addCommand(cmdCLI)

    cmdCLI = 'zonecfg -z ' + vm['name']  + ' "commit"'
    ssh.addCommand(cmdCLI)

    #Export Template
    cmdCLI = 'zonecfg -z ' + vm['name'] + ' "export -f ' + zonetemplate + vm['name'] + '"'
    ssh.addCommand(cmdCLI)

    #Install ZOne

    cmdCLI = 'zoneadm -z ' + vm['name'] + ' install'
    ssh.addCommand(cmdCLI)


    log = ssh.execCMD()

    ssh.closeSession()

    vm_uuid =zone_info(option="get_uuid", vhost=vhost, vmname=vm['name'])

    if vm_uuid:

        new_vm = VMachine(
            vuuid=vm_uuid,
            name=vm['name'],
            cpu=vm['cpu'],
            mem=vm['mem'],
            VHost_id=vhost.id,
            OsType_id= OsType.objects.get(name=vm['ostype']).id,
            Datastore_id= Datastore.objects.get(dpath=vm['datastore']).id,
        )

        new_vm.save()

        Add_Client(name=new_vm.name,protocol="ssh",hostname=vhost.ipaddr,port=vhost.sshport,password="test",username=vhost.user)


        new_dsk = VDisk (
            name = vm['name'],
            VMachine_id= new_vm.id,
            size = vm['dsize'],
        )

        new_dsk.save()

        return True
    else:
        return False

def zone_delete_vm(vhost,vm):

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    cmdCLI = 'zoneadm -z ' + vm.name + ' unistall -F'
    ssh.addCommand(cmdCLI)
    cmdCLI = 'zonecfg -z ' + vm.name + ' delete -F'
    ssh.addCommand(cmdCLI)
    ds_zfs_path = zone_info(option="datastore_zfs_path",vhost=vhost,datastore=vm.Datastore.dpath)
    zdisk = ds_zfs_path + "/" + vm.name
    cmdCLI = 'zfs destroy -r ' + zdisk
    ssh.addCommand(cmdCLI)
    cmdCLI = 'dladm delete-vnic ' + vm.name + '_nic1'
    ssh.addCommand(cmdCLI)

    log = ssh.execCMD()
    ssh.closeSession()

    if not zone_info(option="get_uuid", vhost=vhost, vmname=vm.name):
        vmdel = VMachine.objects.get(id=vm.id)
        Remove_Client(name=vmdel.name)
        vmdel.delete()
        return True
    else:
        return False

def zone_clone(vhost,vm,clone_name):

    #https://docs.oracle.com/cd/E23824_01/html/821-1460/gbwmc.html

    remote_port = Console_Port(option="enable",vhost=vhost)

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()


    #Halt zone
    if vm.state=="RN":
        zone_control(option="stopvm",vhost=vhost,vm=vm)


    dlink = zone_info(option="vm_link", vhost=vhost, vmname=vm.name)
    tmp_template = "/tmp/zone_master"
    tmp_clone = "/tmp/zone_clone"

    cmdCLI ="rm " + tmp_template + " " + tmp_clone
    ssh.addCommand(cmdCLI)

    #Clone zone.cfg
    cmdCLI = 'zonecfg -z ' + vm.name + ' export -f '+ tmp_template
    ssh.addCommand(cmdCLI)

    cmdCLI ="sed -e s/" + vm.name + "/" + clone_name + "/g " + tmp_template + " > " + tmp_clone
    ssh.addCommand(cmdCLI)

    # Create New Nic
    znic = clone_name + "_nic1"
    cmdCLI = 'dladm create-vnic -l ' + dlink + ' ' + znic
    ssh.addCommand(cmdCLI)


    # Clone configration template
    cmdCLI = 'zonecfg -z ' + clone_name + ' -f ' + tmp_clone
    ssh.addCommand(cmdCLI)

    #Clone Zone
    cmdCLI = 'zoneadm -z ' + clone_name + ' clone ' + vm.name
    ssh.addCommand(cmdCLI)

    cmdCLI = "zoneadm -z " + vm.name + " rename " + clone_name
    ssh.addCommand(cmdCLI)


    print (ssh.showCommand())




    log = ssh.execCMD()
    ssh.closeSession()

    print (log)

    vuuid = zone_info(option="get_uuid", vhost=vhost, vmname=clone_name)
    if vuuid:

        new_vm = VMachine(
            vuuid=vuuid,
            name=clone_name,
            cpu=vm.cpu,
            mem=vm.mem,
            VHost_id=vhost.id,
            OsType_id=vm.OsType.id,
            Datastore_id=vm.Datastore.id,
            VSwitch_id=vm.VSwitch.id,
        )

        Add_Client(name=new_vm.name,protocol="ssh",hostname=vhost.ipaddr,port=vhost.sshport,password="test",username=vhost.user)

        new_vm.save()

        return True

    else:
        return False

def zone_create_net(vhost,pg_name):

    cmdCLI = "dladm create-etherstub " + pg_name
    execCMD(vhost=vhost, cmd=cmdCLI)

    if zone_info(option="port_group_exists",vhost=vhost,portgroup=pg_name):
        return True
    else:
        return False

def zone_delete_net(vhost_id,pg_name):

    vhost = VHost.objects.get(id=vhost_id)
    cmdCLI = "dladm delete-etherstub " + pg_name
    print (cmdCLI)
    execCMD(vhost=vhost, cmd=cmdCLI)

    if zone_info(option="port_group_exists",vhost=vhost,portgroup=pg_name):
        return False
    else:
        return True

def zone_create_dstore(vhost,dname,zpool):

    dstore_path = zpool + "/" + dname
    cmdCLI = "zfs create " + dstore_path
    execCMD(vhost=vhost, cmd=cmdCLI)

    if zone_info(option="datastore_zfs_path",vhost=vhost,datastore=dstore_path) == dstore_path:
        return True
    else:
        return False

def zone_delete_dstore(vhost,dpath):

    dstore_path = dpath[1:]

    print (dstore_path)

    if not dstore_path == "rpool" or not dstore_path == "/rpool":
        cmdCLI = "zfs destroy -rf " + dstore_path
        print (cmdCLI)
        execCMD(vhost=vhost, cmd=cmdCLI)

        if zone_info(option="datastore_zfs_path",vhost=vhost,datastore=dstore_path) == dstore_path:
            return False
        else:
            return True

def zone_modify(vhost,vm,data):


    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    cmdCLI = 'zonecfg -z ' + vm.name + '"add capped-cpu; set ncpu=' + data['cpu'] + ';end"'
    ssh.addCommand(cmdCLI)

    cmdCLI = 'zonecfg -z ' + vm.name + '"add capped-memory; set physical=' + data['mem'] + ';end"'
    ssh.addCommand(cmdCLI)

    old_nic = zone_info(option="vm_nic",vhost=vhost,vmname=vm.name)
    cmdCLI = 'dladm delete-vnic ' + old_nic
    ssh.addCommand(cmdCLI)

    znic = data['name']  + '_nic1'
    cmdCLI = 'dladm create-vnic -l ' + data['net'] + ' ' + znic
    ssh.addCommand(cmdCLI)


    cmdCLI = "zoneadm -z " + vm.name + " rename " + data['name']
    ssh.addCommand(cmdCLI)
    ssh.execCMD()

    print (zone_info(option="get_uuid", vhost=vhost, vmname=data['name']))


    if zone_info(option="get_uuid", vhost=vhost, vmname=data['name']):
        mod_vm = VMachine.objects.get(id=vm.id)
        mod_vm.name = data['name']
        mod_vm.OsType.id = data['osid']
        mod_vm.cpu = int(data['cpu'])
        mod_vm.mem = int(data['mem'])
        mod_vm.VSwitch.id = data['vswid']
        mod_vm.save()

        Remove_Client(name=vm.name)
        Add_Client(name=mod_vm.name,protocol="ssh",hostname=vhost.ipaddr,port=vhost.sshport,password="test",username=vhost.user)

        print ("Cambios", mod_vm.cpu, " ", mod_vm.mem)
        print("DE MOD")

        return True

    else:
        return False
