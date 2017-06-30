import re
from console.models import OsType, Datastore, VHost, VMachine,  VDisk, Snapshot
from .ssh import execCMD, sshSession, execSFTP
from DjangoWeb.settings import BASE_DIR
from .guacamole import Add_Client, Modify_Client, Remove_Client




'''
Bibilio
http://www.doublecloud.org/2013/11/vmware-esxi-vim-cmd-command-a-quick-tutorial/
http://searchitchannel.techtarget.com/feature/Creation-of-virtual-machines-utilizing-command-line-tools
http://www.tamas.io/automatic-virtual-machine-creation-from-command-line-in-vmwares-esxi
http://jensd.be/370/linux/create-a-new-virtual-machine-in-vsphere-with-python-pysphere-and-the-vmware-api
https://github.com/vmware/pyvmomi
http://searchitchannel.techtarget.com/feature/Scripting-Creation-of-Virtual-Machines-in-Perl-Scripts
http://searchitchannel.techtarget.com/feature/Scripting-creation-of-virtual-machines-in-ESX-shell
http://www.doublecloud.org/2013/11/vmware-esxi-vim-cmd-command-a-quick-tutorial/
https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2012964
http://www.blackmanticore.com/206da0c17840b37177b113a44d96e1c4
http://stackoverflow.com/questions/29213289/create-vm-using-pyvmomi-module-from-vmx-and-vmdk-files/29217223#29217223
http://jensd.be/370/linux/create-a-new-virtual-machine-in-vsphere-with-python-pysphere-and-the-vmware-api
https://github.com/argos83/pysphere/blob/master/pysphere/vi_virtual_machine.py
https://github.com/palli/python-virtinst/blob/master/virtconv/parsers/vmx.py
https://www.vmware.com/support/developer/vcli/
http://pubs.vmware.com/vsphere-60/index.jsp?topic=%2Fcom.vmware.vcli.ref.doc%2Fvcli-right.html&__utma=207178772.847578794.1464786859.1464786859.1464786859.1&__utmb=207178772.0.10.1464786859&__utmc=207178772&__utmx=-&__utmz=207178772.1464786859.1.1.utmcsr=%28direct%29|utmccn=%28direct%29|utmcmd=%28none%29&__utmv=-&__utmk=107057153
https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2012964
http://blog-lrivallain.rhcloud.com/2015/02/26/play-vm-snapshots-esxi-command-line-tools/
http://www.vm-help.com/esx40i/manage_without_VI_client_1.php
'''



def esx_parser(option,data,**kwargs):

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

    # COMMANDS Virtual Hosts

    elif option == "list_all":
        list_machines = []
        for line in data:
            rx = re.search('(\d+)\s;\s(.+)', line)
            if rx:
                machine = {
                    'name': re.match('(\d+)\s;\s(.+)', line).group(2),
                    'uuid': re.match('(\d+)\s;\s(.+)', line).group(1),
                }
                list_machines.append(machine)
        return list_machines

    elif option == "vswitch-portgroup":
        network = []
        name = ""
        for line in data:
            rx_sw = re.search('^\s+name\s=\s"(.+)"\,',line)
            rx_pg = re.search('\s+<.+PortGroup-(.+)>',line)
            if rx_sw:
                name = re.match('^\s+name\s=\s"(.+)"\,',line).group(1)
            elif rx_pg:
                net = {
                    'vswitch' : name,
                    'portgroup': re.match('\s+<.+PortGroup-(.+)>',line).group(1),
                }
                network.append(net)
        return network

    elif option == "vswitch-nic":
        network = []
        for line in data:
            rx1 = re.search('(.+)\s;\s(.+)',line)
            rx2 = re.search('(.+)\s;\s$',line)
            if rx1:
                net = {
                    'vswitch' : re.match('(.+)\s;\s(.+)',line).group(1),
                    'vmnic' : re.match('(.+)\s;\s(.+)',line).group(2),
                }
                network.append(net)
            elif rx2:
                net = {
                    'vswitch' : re.match('(.+)\s;\s$',line).group(1),
                    'vmnic' : "none",
                }
                network.append(net)

        return network

    elif option == "vswitch":
        name = ""
        for line in data:
            rx_sw = re.search('^\s+name\s=\s"(.+)"\,', line)
            rx_pg = re.search('\s+<.+PortGroup-(.+)>',line)
            if rx_sw:
                name = re.match('^\s+name\s=\s"(.+)"\,',line).group(1)
        return name

    elif option == "port_groups":  #Borrar si no es neceario
        portgroup = []
        for line in data:
            rx_pg = re.search('\s+<.+PortGroup-(.+)>', line)
            if rx_pg:
                portgroup.append(re.match('\s+<.+PortGroup-(.+)>', line).group(1))
        return portgroup

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
    
    elif option == "ifaces":
        ifaces = []
        for line in data:
            ifaces.append(line)
        return ifaces

    elif option == "datastore":
        dstore = []
        for line in data:
            rx = re.search('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$',line)
            if rx:
                data = {
                    #'dpath': re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$',line).group(1),
                    'dpath': "/vmfs/volumes/" + re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$', line).group(2),
                    'dname': re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$', line).group(2),
                    'dtype': re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$', line).group(3),
                    'dsize': re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$', line).group(4),
                    'dfree': re.match('^(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s;\s(.+)\s$', line).group(5),
                }
                dstore.append(data)
        print (dstore)
        return dstore

    
    # COMMANDS Virtual Machines Control
    
    if option == "vm_dir":
        for line in data:
            if re.sub('\n',"",line) == vmdir:
                return True
            else:
                return False

    elif option == "vm_file":
        for line in data:
            regex = vmdir + '/(.+)'
            rx =  re.search(regex,line)
            if rx:
                if re.match(regex,line).group(1) == vmfile:
                    return True
                else:
                    return False
            else:
                return False

    elif option == "vm_disk":
        for line in data:
            for line in data:
                if re.sub('\n', "", line) == vmdisk:
                    return True
                else:
                    return False
                
    elif option == "get_name":
        for line in data:
            rx = re.search('(\d+)\s;\s(.+)', line)
            if rx:
                if re.match('(\d+)\s;\s(.+)', line).group(2) == vmname:
                    return re.match('(\d+)\s;\s(.+)', line).group(2)

    elif option == "get_uuid":
        for line in data:
            rx = re.search('(\d+)\s;\s(.+)', line)
            if rx:
                if re.match('(\d+)\s;\s(.+)', line).group(2) == vmname:
                    return re.match('(\d+)\s;\s(.+)', line).group(1)

    # Commands  Info_VM

    elif option == "vm_run":
        for line in data:
            rx = re.sub('\s','',line)
            if rx == "Poweredoff":
                return "PW"
            elif rx == "Poweredon":
                return "RN"
            elif rx == "suspended":
                return "PA"
            else:
                return "Error"
    
    # COMMANDS Virtual Machines Data


    elif option == "vm_uptime":
        for line in data:
            rx = re.search ('\s+(\w+)\s=\s(.+),',line)
            if rx:
                regex = re.sub('"','',re.match('\s+(\w+)\s=\s(.+),',line).group(2))
                return regex

    elif option == "vm_state":
        for line in data:
            rx = re.search('\s+powerState\s=\s"(\w+)",', line)
            if rx:
                status = re.match('\s+powerState\s=\s"(\w+)"', line).group(1)
                if status == "poweredOff":
                    return "PW"
                elif status == "poweredOn":
                    return "RN"
                elif status == "suspended":
                    return "PA"


    elif option == "vm_mem":
        for line in data:
            rx = re.search('\s+(\w+)\s=\s(.+),', line)
            if rx:
                regex = re.sub('"', '', re.match('\s+(\w+)\s=\s(.+),', line).group(2))
                return regex

    elif option == "vm_ncpu":
        for line in data:
            rx = re.search('\s+(\w+)\s=\s(.+),', line)
            if rx:
                regex = re.sub('"', '', re.match('\s+(\w+)\s=\s(.+),', line).group(2))
                return regex


    #elif option == "vm_nic":
     #   pass

    elif option == "vm_vrde":
        rem_adm = {}
        for line in data:
            rx = re.search('RemoteDisplay\.vnc\.(\w+)\s=\s(.+)',line)
            if rx:
                property = re.match('RemoteDisplay\.vnc\.(\w+)\s=\s(.+)',line).group(1)
                value = re.match('RemoteDisplay\.vnc\.(\w+)\s=\s(.+)',line).group(2)
                if property == "enabled":
                    rem_adm['enabled'] = True
                elif property == "port":
                    rem_adm['port'] = re.sub('"','',value)
                elif property == "password":
                    rem_adm['passwd'] = re.sub('"','',value)
        print (rem_adm)
        return rem_adm

    elif option == "vm_os":
        for line in data:
            print (line)
            rx = re.search('guestOS\s=\s"(.+)"', line)
            if rx:
                regex = re.match('guestOS\s=\s"(.+)"', line).group(1)
                return regex


    elif option == "vm_nic":
        for line in data:
            rx = re.search('ethernet0.networkName\s=\s"(.+)"', line)
            if rx:
                regex = re.match('ethernet0.networkName\s=\s"(.+)"', line).group(1)
                return regex

    elif option == "vm_path":
        for line in data:
            return "/vmfs/volumes/" + re.sub('\n','',line)

    elif option == "vm_cfg":
        for line in data:
            rx = re.search('^\[(.+)\]\s(.+)',line)
            if rx:
                return "/vmfs/volumes/" + re.match('^\[(.+)\]\s(.+)',line).group(1) + "/" + re.match ('^\[(.+)\]\s(.+)',line).group(2)


    # Contol Snapshots


    elif option == "snap_list":
        snaplist = []
        currentid = ""
        snapname = ""
        snapid = ""
        current = False
        for line in data:
            rx1 = re.search("^\s+currentSnapshot\s=\s'vim.vm.Snapshot:\d+-snapshot-(\d+)',",line)
            rx2 = re.search('^\s+name\s=\s"(.+)",',line)
            rx3 = re.search('^\s+id\s=\s(\d+),',line)
            rx4 = re.search('^\s+createTime\s=\s"(.+)",',line)
            if rx1:
                currentid = re.match("^\s+currentSnapshot\s=\s'vim.vm.Snapshot:\d+-snapshot-(\d+)',",line).group(1)
            elif rx2:
                snapname = re.match('^\s+name\s=\s"(.+)",',line).group(1)
            elif rx3:
                snapid = re.match('^\s+id\s=\s(\d+),',line).group(1)
                if currentid == snapid:
                    current = True
            elif rx4:
                snapdata = {
                    'uuid' : snapid,
                    'name': snapname + "_" + re.match('^\s+createTime\s=\s"(.+)",',line).group(1),
                }
                if current:
                    snapdata['current'] = current
                    current = ""
                else:
                    snapdata['current'] = False
                snaplist.append(snapdata)
        return snaplist

def esx_info(option,**kwargs):


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

    if kwargs.get('vmdisk'):
        vmdisk = kwargs['vmdisk']

    if kwargs.get('portgroup'):
        portgroup = kwargs['portgroup']

    # COMMANDS Virtual Hosts
    
    if option == "list_all":
        cmdCLI = "vim-cmd vmsvc/getall | awk '{print $1," + '";"' +",$2}' | grep -v Vmid"
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vswitch-portgroup":
        cmdCLI = 'vim-cmd  hostsvc/net/vswitch_info | egrep "name|PortGroup-"'
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vswitch-nic":
        cmdCLI = 'esxcfg-vswitch -l | egrep -v "^ |^$|Uplink" |' + "awk '{print $1," + '";"' +",$6}'"
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))


    elif option == "vswitch":
        cmdCLI = 'vim-cmd  hostsvc/net/vswitch_info | egrep "name"'
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))


    elif option == "port_groups":
        cmdCLI = 'vim-cmd  hostsvc/net/vswitch_info | egrep "PortGroup-"'
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "port_group_exists":
        cmdCLI = 'vim-cmd  hostsvc/net/vswitch_info | egrep "PortGroup-"'

        for port in esx_parser(option="port_groups",data=execCMD(vhost=vhost,cmd=cmdCLI)):
            vhost_port = re.sub('\s','_',port)
            port_form = re.sub('\s','_',portgroup)
            if str(vhost_port) == str(port_form):
                return True
        return False

    elif option == "ifaces":
        cmdCLI = "esxcfg-nics  -l | grep -v MAC| awk '{print $1}'"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))


    elif option == "ostypes":
        filename = BASE_DIR + "/console/toolset/cfg/esx_os_guest.csv"
        return esx_parser(option=option,data=filename)

    elif option == "datastore":
        cmdCLI = "esxcli storage filesystem list | grep  -v UUID | grep -v -e  ----- | awk '{print $1," +'";",$2,";",$5,";",$6,";",$7}' + "'"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))


    
    # COMMANDS Virtual Machines Data
    
    elif option == "vm_run":
        cmdCLI = "vim-cmd vmsvc/power.getstate " + vuuid + "| grep -v Retrieved"
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "get_uuid" or option == "get_name":
        print (vmname)
        cmdCLI = "vim-cmd vmsvc/getall | awk '{print $1," +'";"'+ ",$2}' | grep -v Vmid| grep -i " + vmname
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmname=vmname)

    elif option == "vm_dir":
        cmdCLI = "ls  -d " + vmdir
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmdir=vmdir)

    elif option == "vm_file":
        cmdCLI = "ls " + vmdir + "/" + vmfile
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmdir=vmdir,vmfile=vmfile)

    elif option == "vm_disk":
        cmdCLI = "ls " + vmdisk
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI),vmdisk= vmdisk)

    elif option == "vm_uptime":
        cmdCLI = "vim-cmd vmsvc/get.runtime " + vuuid + "| grep boot"
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_state":
        cmdCLI = "vim-cmd vmsvc/get.runtime " + vuuid + "| grep powerState"
        return esx_parser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_mem":
        cmdCLI = "vim-cmd vmsvc/get.config " + vuuid +" | grep -i memoryMB"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_ncpu":
        cmdCLI = "vim-cmd vmsvc/get.config " + vuuid + " | grep -i numCPU "
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_vrde":
        cfgfile = esx_info(option="vm_cfg", vhost=vhost, vmname=vmname)
        cmdCLI = "cat " + cfgfile + "| grep vnc"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_os":

        cfgfile = esx_info(option="vm_cfg", vhost=vhost, vmname=vmname)
        print (cfgfile)
        cmdCLI = "cat " + cfgfile + "| grep guestOS"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_nic":
        cfgfile = esx_info(option="vm_cfg", vhost=vhost, vmname=vmname)
        cmdCLI = "cat " + cfgfile + "| grep ethernet0.networkName"
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_path":
        cmdCLI = "vim-cmd vmsvc/getall | grep " + vmname + " | awk '{print $3}' | cut -d'[' -f2| cut -d']' -f1"
        return esx_parser(option=option, data=execCMD(vhost=vhost,cmd=cmdCLI), vmname=vmname)

    elif option == "vm_cfg":
        cmdCLI = "vim-cmd vmsvc/getall | grep "  + vmname + " | awk '{print $3,$4}'"
        return esx_parser(option="vm_cfg",data=execCMD(vhost=vhost,cmd=cmdCLI),vmname=vmname)
    
    # Contol Snapshots
    
    elif option == "snap_list":
        cmdCLI = "vim-cmd vmsvc/get.snapshotinfo " + vuuid # ADD ESX command
        return esx_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))
    
    elif option == "current_snap":
        print ("buuid", vuuid)
        snaplist = esx_info(option="snap_list",vhost=vhost,vuuid=vuuid)
        print (snaplist)
        for snap in snaplist:
            print (snap)
            if snap['current'] == True:
                return snap['uuid']

def esx_control(option,**kwargs):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vm variable
    :return:
    '''

    # COMMANDS Virtual Hosts


    if kwargs.get('vm'):
        vmachine = kwargs['vm']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']


    if option=="start_vm":
        cmdCLI = "vim-cmd vmsvc/power.on "+ vmachine.vuuid
        execCMD(vhost=vhost, cmd=cmdCLI)
        if esx_info(option="vm_run", vhost=vhost, vuuid=vmachine.vuuid) == "RN":
            vmachine.state = esx_info(option="vm_state", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.uptime = esx_info(option="vm_uptime", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.save()
            return True

    elif option=="stop_vm":
        cmdCLI = "vim-cmd vmsvc/power.off " + vmachine.vuuid
        execCMD(vhost=vhost, cmd=cmdCLI)
        vmachine.state = esx_info(option="vm_state", vhost=vhost, vuuid=vmachine.vuuid)
        vmachine.uptime = esx_info(option="vm_uptime", vhost=vhost, vuuid=vmachine.vuuid)
        vmachine.save()


        if esx_info(option="vm_run",vhost=vhost,vuuid=vmachine.vuuid) == "PW":
            return True

    elif option =="pause_vm":
        if esx_info(option="vm_state",vhost=vhost,vuuid=vmachine.vuuid) == 'PA':
            cmdCLI = "vim-cmd vmsvc/power.suspendResume " + vmachine.vuuid
            execCMD(vhost=vhost, cmd=cmdCLI)
            vmachine.state = esx_info(option="vm_state", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.uptime = esx_info(option="vm_uptime", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.save()
            return "resumed"
        else:
            cmdCLI = "vim-cmd vmsvc/power.suspend " + vmachine.vuuid
            execCMD(vhost=vhost, cmd=cmdCLI)
            vmachine.state = esx_info(option="vm_state", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.uptime = esx_info(option="vm_uptime", vhost=vhost, vuuid=vmachine.vuuid)
            vmachine.save()
            return "paused"

    elif option == "add_iso":
        #http://www.vm-help.com/esx40i/manage_without_VI_client_1.php
        #https://communities.vmware.com/thread/420294?start=0&tstart=0

        #Disconect CRDROM
        cmdCLI = "vim-cmd vmsvc/device.connection " + vmid + " 3002 false"

        #Modify

        pass

    elif option == "rm_iso":

        pass


    pass

def esx_create_vm(vhost,vm):

    #Load Env Variables
    file_tmp = "/tmp"

    if not VMachine.objects.filter(name=vm['name']).exists():

        vm_dir = vm['datastore'] + "/" + vm['name']
        cmdCLI = "mkdir " + vm_dir
        execCMD(vhost=vhost, cmd=cmdCLI)

        if esx_info(option="vm_dir", vhost=vhost, vmdir=vm_dir):

            #VMX File Creation

            print("Creating VWARE File")
            line = []

            line.append('config.version = "8"')
            line.append('virtualHW.version = "11"')
            line.append('vmci0.present = "TRUE"')
            line.append('displayName = "' + vm['name'] + '"')
            line.append('floppy0.present = "FALSE"')
            line.append('numvcpus = "' + str(vm['cpu']) + '"')
            line.append('scsi0.present = "TRUE"')
            line.append('scsi0.sharedBus = "none"')
            line.append('scsi0.virtualDev = "lsilogic"')
            line.append('memsize = "' + str(vm['mem']) + '"')
            line.append('scsi0:0.present = "TRUE"')
            line.append('scsi0:0.fileName = "' + vm['name'] + '.vmdk"')
            line.append('scsi0:0.deviceType = "scsi-hardDisk"')
            line.append('ide1:0.present = "TRUE"')
            line.append('ide1:0.fileName = ')
            line.append('ide1:0.deviceType = "cdrom-image"')
            line.append('ethernet0.virtualDev ="' + str(vm['driver']) +'"')
            line.append('ethernet0.networkName = "' + str(vm['net']) + '"')
            line.append('ethernet0.addressType = "generated"')
            line.append('ethernet0.uptCompatibility = "TRUE"')
            line.append('ethernet0.present = "TRUE"')
            line.append('pciBridge0.present = "TRUE"')
            line.append('pciBridge4.present = "TRUE"')
            line.append('pciBridge4.virtualDev = "pcieRootPort"')
            line.append('pciBridge4.functions = "8"')
            line.append('pciBridge5.present = "TRUE"')
            line.append('pciBridge5.virtualDev = "pcieRootPort"')
            line.append('pciBridge5.functions = "8"')
            line.append('pciBridge6.present = "TRUE"')
            line.append('pciBridge6.virtualDev = "pcieRootPort"')
            line.append('pciBridge6.functions = "8"')
            line.append('pciBridge7.present = "TRUE"')
            line.append('pciBridge7.virtualDev = "pcieRootPort"')
            line.append('pciBridge7.functions = "8"')
            line.append('guestOS = "' + vm['ostype'] + '"')
            line.append('RemoteDisplay.vnc.enabled = True')
            line.append('RemoteDisplay.vnc.port = "'+ vm['rdpport'] +'"')
            line.append('RemoteDisplay.vnc.password = "'+ vm['rdppass'] +'"')

            vm_file = vm['name'] + ".vmx"
            filename = file_tmp + "/" + vm_file
            target = open(filename, 'w')

            target.truncate()

            rpath = vm_dir + "/" + vm_file

            for data in line:

                target.write(data)
                target.write("\n")

            target.close()
            # Load File in ES
            execSFTP(vhost=vhost,remote_path=rpath,local_path=filename,method="PUT")
            # Create Disk
            dpath = vm['datastore'] + "/" + vm['name'] + "/" + vm['name'] + ".vmdk"''
            cmdCLI = "vmkfstools -c " + str(vm['dsize']) + "M " + dpath + " -a lsilogic"
            execCMD(vhost=vhost, cmd=cmdCLI)

            cmdCLI = "vim-cmd solo/registervm " + vm_dir + "/" + vm_file
            x = execCMD(vhost=vhost, cmd=cmdCLI)
            for line in x:
                print (line)

            vuuid = esx_info(option="get_uuid",vhost=vhost,vmname=vm['name'])

            if vuuid:
                if esx_info(option="vm_dir",vhost=vhost,vmdir=vm_dir):
                    if esx_info(option="vm_file", vhost=vhost, vmfile=vm_file, vmdir=vm_dir):
                        if esx_info(option="vm_disk", vhost=vhost, vmdisk=dpath,vuuid=vuuid):
                            if vm['rdpport']:
                                new_vm = VMachine(
                                    vuuid=vuuid,
                                    name=vm['name'],
                                    cpu=vm['cpu'],
                                    mem=vm['mem'],
                                    VHost_id=vhost.id,
                                    OsType_id=OsType.objects.get(name=vm['ostype']).id,
                                    Datastore_id=Datastore.objects.get(dpath=vm['datastore']).id,
                                    rdport=vm['rdpport'],
                                    rdppass=vm['rdppass']
                                )
                            else:
                                new_vm = VMachine(
                                    vuuid=vuuid,
                                    name=vm['name'],
                                    cpu=vm['cpu'],
                                    mem=vm['mem'],
                                    VHost_id=vhost.id,
                                    OsType_id=OsType.objects.get(name=vm['ostype']).id,
                                    Datastore_id=Datastore.objects.get(dpath=vm['datastore']).id,
                                )


                            new_vm.save()

                            new_dsk = VDisk(
                                name=vm['name'] + ".vmdk",
                                VMachine_id=new_vm.id,
                                size=vm['dsize'],
                            )

                            new_dsk.save()

                            Add_Client(name=new_vm.name, protocol="vnc", port = new_vm.rdport, username = new_vm.rdpuser, password = new_vm.rdppass, hostname = vhost.ipaddr)

                            return "OK"

                        else:
                            return "KO-DISK"
                    else:
                        return "KO-VMFILE"
                else:
                    return "KO-VMDIR"
            else:
                return "KO-VM_NOT_REGISTER"

def esx_create_net(vhost,pg_name,vswitch):

    cmdCLI = "vim-cmd hostsvc/net/portgroup_add " + vswitch + " " + pg_name
    execCMD(vhost=vhost, cmd=cmdCLI)

    if esx_info(option="port_group_exists",vhost=vhost,portgroup=pg_name):
        return True
    else:
        return False

def esx_delete_net(vhost_id,pg_name,vswitch):

    vhost = VHost.objects.get(id=vhost_id)
    cmdCLI = "vim-cmd hostsvc/net/portgroup_remove " + vswitch + " " + pg_name
    execCMD(vhost=vhost, cmd=cmdCLI)

    if esx_info(option="port_group_exists",vhost=vhost,portgroup=pg_name):
        return False
    else:
        return True

def esx_modify(vhost,vm,data):


    ssh = sshSession(hostip=vhost.ipaddr, hostuser=vhost.user, userkey=vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    file_tmp = "/tmp"



    #Uregister
    cmdCLI = "vim-cmd vmsvc/unregister " + str(vm.vuuid)
    ssh.addCommand(cmdCLI)

    #Delete Old Config:
    old_dir = vm.Datastore.dpath + "/" + vm.name
    old_cfg = old_dir + "/" + vm.name + ".vmx"
    cmdCLI = "mv " + old_cfg + " " + old_cfg + ".old"
    ssh.addCommand(cmdCLI)

    #Rename Directory
    mod_dir = vm.Datastore.dpath + "/" + data['name']
    cmdCLI = "mv " + old_dir + " " + mod_dir
    ssh.addCommand(cmdCLI)
    ssh.execCMD()


    old_file = vm.name + ".vmx"
    mod_file = data['name'] + ".vmx"
    mod_cfg = mod_dir + "/" + mod_file

    if esx_info(option="vm_dir", vhost=vhost, vmdir=mod_dir):

        # VMX File Creation

        line = []

        line.append('config.version = "8"')
        line.append('virtualHW.version = "11"')
        line.append('vmci0.present = "TRUE"')
        line.append('displayName = "' + data['name'] + '"')
        line.append('floppy0.present = "FALSE"')
        line.append('numvcpus = "' + str(data['cpu']) + '"')
        line.append('scsi0.present = "TRUE"')
        line.append('scsi0.sharedBus = "none"')
        line.append('scsi0.virtualDev = "lsilogic"')
        line.append('memsize = "' + str(data['mem']) + '"')
        line.append('scsi0:0.present = "TRUE"')
        line.append('scsi0:0.fileName = "' + vm.name + '.vmdk"')
        line.append('scsi0:0.deviceType = "scsi-hardDisk"')
        line.append('ide1:0.present = "TRUE"')
        line.append('ide1:0.fileName = ')
        line.append('ide1:0.deviceType = "cdrom-image"')
        line.append('ethernet0.virtualDev ="' + str(data['driver']) + '"')
        line.append('ethernet0.networkName = "' + str(data['net']) + '"')
        line.append('ethernet0.addressType = "generated"')
        line.append('ethernet0.uptCompatibility = "TRUE"')
        line.append('ethernet0.present = "TRUE"')
        line.append('pciBridge0.present = "TRUE"')
        line.append('pciBridge4.present = "TRUE"')
        line.append('pciBridge4.virtualDev = "pcieRootPort"')
        line.append('pciBridge4.functions = "8"')
        line.append('pciBridge5.present = "TRUE"')
        line.append('pciBridge5.virtualDev = "pcieRootPort"')
        line.append('pciBridge5.functions = "8"')
        line.append('pciBridge6.present = "TRUE"')
        line.append('pciBridge6.virtualDev = "pcieRootPort"')
        line.append('pciBridge6.functions = "8"')
        line.append('pciBridge7.present = "TRUE"')
        line.append('pciBridge7.virtualDev = "pcieRootPort"')
        line.append('pciBridge7.functions = "8"')
        line.append('guestOS = "' + data['osname'] + '"')
        line.append('RemoteDisplay.vnc.enabled = True')
        line.append('RemoteDisplay.vnc.port = "' + data['rdpport'] + '"')
        line.append('RemoteDisplay.vnc.password = "' + data['rdppass'] + '"')

        filename = file_tmp + "/" + mod_file
        target = open(filename, 'w')

        target.truncate()

        for item in line:
            target.write(item)
            target.write("\n")
        target.close()

        # Load File in ES
        execSFTP(vhost=vhost, remote_path=mod_cfg, local_path=filename, method="PUT")

        # Register NewMachine
        cmdCLI = "vim-cmd solo/registervm " + mod_cfg
        ssh.addCommand(cmdCLI)

        ssh.execCMD()
        ssh.closeSession()

        vuuid = esx_info(option="get_uuid", vhost=vhost,vmname=data['name'])
        if vuuid:
            mod_vm = VMachine.objects.get(id=vm.id)
            mod_vm.vuuid = vuuid
            mod_vm.name = data['name']
            mod_vm.OsType.id = data['osid']
            mod_vm.cpu = data['cpu']
            mod_vm.mem = data['mem']
            mod_vm.VSwitch.id = data['vswid']
            mod_vm.rdport = data['rdpport']
            mod_vm.rdppass = data['rdppass']
            mod_vm.save()

            Remove_Client(name=vm.name)
            Add_Client(name=mod_vm.name, protocol="vnc", port=mod_vm.rdport,password=mod_vm.rdppass, hostname=vhost.ipaddr)

            return True

        else:
            return False

def esx_delete_vm(vhost,vm):

    cmdCLI="vim-cmd vmsvc/destroy " + vm.vuuid
    execCMD(vhost=vhost, cmd=cmdCLI)
    if not esx_info(option="get_uuid",vhost=vhost,vmname=vm.name):
        vmdel = VMachine.objects.get(id=vm.id)
        dstore = Datastore.objects.get(id=vmdel.Datastore.id)
        cmdCLI ="rm -rf "+ dstore.dpath + "/" + vm.name
        execCMD(vhost=vhost, cmd=cmdCLI)
        vmdel.delete()

        Remove_Client(name=vm.name)

        return True
    else:
        return False

def esx_clone(vhost,vm,clone_name):

    #https://communities.vmware.com/message/2412308
    #http://virtuallyhyper.com/2012/04/cloning-a-vm-from-the-command-line/
    #http://collisionresistanthashfunction.blogspot.com.es/2013/10/clone-vm-from-command-line-in-vmware.html


    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()


    # GET Original
    ori_cfg = esx_info(option="vm_cfg",vhost=vhost,vmname=vm.name)


    # Create CLone Path
    vm_dir = vm.Datastore.dpath + "/" + clone_name
    cmdCLI = "mkdir " + vm_dir
    ssh.addCommand(cmdCLI)


    # Copy VMX File
    cl_file = clone_name + ".vmx"
    cl_cfg = vm_dir + "/" + clone_name + ".vmx"
    cmdCLI = "cp " + ori_cfg + " " + ori_cfg + ".old"
    ssh.addCommand(cmdCLI)


    # Modify
    # SUBstitute olonave with clone_name
    cmdCLI ="sed -e s/" + vm.name + "/" + clone_name + "/g " + ori_cfg + ">>" + cl_cfg
    ssh.addCommand(cmdCLI)

    # Create DISK
    ori_disk = vm.Datastore.dpath + "/" + vm.name + "/" + vm.name + ".vmdk"
    new_disk = vm_dir + "/" + clone_name + ".vmdk"
    cmdCLI = "vmkfstools -i " + ori_disk + " " + new_disk
    ssh.addCommand(cmdCLI)


    #Register NewMachine
    cmdCLI = "vim-cmd solo/registervm " + cl_cfg
    ssh.addCommand(cmdCLI)

    ssh.execCMD()
    ssh.closeSession()

    print("OS id", vm.OsType.id)

    vuuid = esx_info(option="get_uuid", vhost=vhost, vmname=clone_name)

    if vuuid:
        if esx_info(option="vm_dir", vhost=vhost, vmdir=vm_dir):
            if esx_info(option="vm_file", vhost=vhost, vmfile=cl_file, vmdir=vm_dir):
                if esx_info(option="vm_disk", vhost=vhost, vmdisk=new_disk):


                    new_vm = VMachine(
                        vuuid=vuuid,
                        name=clone_name,
                        cpu=vm.cpu,
                        mem=vm.mem,
                        VHost_id=vhost.id,
                        OsType_id=vm.OsType.id,
                        Datastore_id=vm.Datastore.id,
                        VSwitch_id=vm.VSwitch.id,
                        rdport=vm.rdport,
                        rdpass=vm.rdppass,
                    )

                    new_vm.save()


                    new_dsk = VDisk(
                        name=clone_name + ".vmdk",
                        VMachine_id=new_vm.id,
                        size="1",
                    )

                    new_dsk.save()

                    Add_Client(name=new_vm.name, protocol="vnc", port=new_vm.rdport, username=new_vm.rdpuser,
                               password=new_vm.rdppass, hostname=vhost.ipaddr)

                    return True

                else:
                    print("KO-DISK")
                    return False
            else:
                print("KO-VMFILE")
                return False
        else:
            print("KO-VMDIR")
            return False
    else:
        print("KO-VM_NOT_REGISTER")
        return False

def esx_snapshots(option,vhost,vm,**kwargs):

    '''
    :param option:
    :param kwargs:
        - suuid = varaible

    :return:
    '''
    #http://blog-lrivallain.rhcloud.com/2015/02/26/play-vm-snapshots-esxi-command-line-tools/
    if kwargs.get('suuid'):
        suuid = kwargs['suuid']

    vuuid = esx_info(option="get_uuid", vhost=vhost, vmname=vm.name)


    if option == "snap_list":
        return esx_info(option=option, vhost=vhost, vuuid=vm.vuuid)

    elif option == "snap_create":
        cmdCLI = "vim-cmd vmsvc/snapshot.create " + vm.vuuid + " " + vm.name
        print (cmdCLI)
        execCMD(vhost=vhost, cmd=cmdCLI)
        return esx_info(option="current_snap", vhost=vhost, vuuid=vm.vuuid)

    elif option == "snap_delete":
        cmdCLI = "vim-cmd vmsvc/snapshot.remove " + vm.vuuid + " " + suuid
        execCMD(vhost=vhost, cmd=cmdCLI)
        print (cmdCLI)
        for snap in esx_info(option="snap_list", vhost=vhost, vuuid=vm.vuuid):
            if snap['uuid'] == suuid:
                return False
            else:
                snap = Snapshot.objects.get(suuid=suuid)
                snap.delete()
                return True

    elif option == "snap_restore":
        cmdCLI = "vim-cmd vmsvc/snapshot.revert " + vm.vuuid + " " + suuid + " 0"
        execCMD(vhost=vhost, cmd=cmdCLI)
        if suuid == esx_info(option="current_snap", vhost=vhost, vuuid=vm.vuuid):
            return True
        else:
            return False

