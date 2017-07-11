import re
from console.models import OsType, Datastore, VHost, VMachine, VDisk, Snapshot, VSwitch
from .guacamole import Add_Client, Remove_Client, Console_Port
from .ssh import execCMD, sshSession
from .PyPass import PyPass
from .RDesktop import Rdesktop

def vbox_paser(option,data,**kwargs):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vmname variable
        - dstore variable
    :return:
    '''

    if kwargs.get('vmname'):
        vmname = kwargs['vmname']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']

    if kwargs.get('datastore'):
        datastore = kwargs['datastore']

    # Commands VHIST



    # COMMANDS Virtual Hosts

    if option == "list_all":
        list_machines = []
        for line in data:
            rx = re.search('^"(.+)" {(.+)}', line)
            if rx:
                machine = {
                'name' : re.match('^"(.+)" {(.+)}', line).group(1),
                'uuid':  re.match('^"(.+)" {(.+)}', line).group(2),
                }
                list_machines.append(machine)
        return list_machines

    elif option == "intnet":
        vminets = []
        for line in data:
            rx = re.search('^(Name):.*$', line)
            if rx:
                data = re.match('^Name:\s*(\S*).*$', line).group(1)
                vminets.append(data)
        return vminets

    elif option == "ifaces":
        vhifaces = []
        for line in data:
            rx = re.search('^(\w+\s)', line)
            if rx:
                iface = re.match('^(\w+\s)', line).group(1)
                vhifaces.append(iface)
        return vhifaces

    elif option == "ostypes":
        vmostype = []
        block = 0
        for line in data:
            rx = re.search('^(ID|Description):.*$', line)
            if rx:
                if re.match('^(ID|Description):\s*(.+).*$', line).group(1) == "ID" and block == 0:

                    id = re.match('^(ID|Description):\s*(.+).*$', line).group(2)
                    block =1

                elif re.match('^(ID|Description):\s*(.+).*$', line).group(1) == "Description" and block == 1:

                    desc = re.match('^(ID|Description):\s*(.+).*$', line).group(2)
                    block = 0

                    os = { "id" : id, "desc": desc}
                    vmostype.append(os)

        return vmostype    

    # COMMANDS Virtual Machines  Control

    elif option == "vm_run":
        for line in data:
            rx = re.search('^"(.+)" {(.+)}', line)
            if re.match('^"(.+)" {(.+)}', line).group(1) == vmname:
                return True
            else:
                return False

    elif option == "get_name":
        for line in data:
            rx = re.search('^"(.+)" {(.+)}', line)
            if rx:
                if re.match('^"(.+)" {(.+)}', line).group(1) == vmname:
                    return re.match('^"(.+)" {(.+)}', line).group(1)

    elif option == "get_uuid":
        for line in data:
            rx = re.search('^"(.+)" {(.+)}', line)
            if rx:
                if re.match('^"(.+)" {(.+)}', line).group(1) == vmname:
                    return re.match('^"(.+)" {(.+)}', line).group(2)

    elif option == "datastore":
        for line in data:
            return re.sub('\\n', "", line)

    # COMMANDS Virtual Machines  Data

    elif option == "vm_uptime":
        for line in data:
            if line.split('=')[0] == "VMStateChangeTime":
                bad_chars ='"'
                return re.sub(bad_chars,"",line.split('=')[1])
                 
    elif option == "vm_state":
        for line in data:
            regex = re.search('^VMState="(.+)"', line)
            if regex:
                status = re.match('^VMState="(.+)"', line).group(1)
                if status == "poweroff":
                    return "PW"
                elif status == "running":
                    return "RN"
                elif status == "paused":
                    return "PA"

                
        return "Error_NO_STATE"

    elif option == "vm_mem":
        for line in data:
            if line.split('=')[0] == "memory":
                return line.split('=')[1]

    elif option == "vm_ncpu":
        for line in data:
            if line.split('=')[0] == "cpus":
                return line.split('=')[1]

    elif option == "vm_cfg":
        for line in data:
            rx = re.search('CfgFile="(.+)"',line)
            if rx:
                cfg_file = re.match('CfgFile="(.+)"', line).group(1)
                return  re.match('CfgFile="(.+)"', line).group(1)  # cfg File

    elif option == "vm_vdisk":
        for line in data:
            regex = re.search(r'<(HardDisk uuid).*',line, re.M|re.I )
            if regex.group(1) == "HardDisk":
                regex = re.match(r'(.*)location="(.*)" forma.*',line, re.M|re.I )
                return regex.group(2) 

    elif option == "vm_nic":
        for line in data:
            rx = re.search('^NIC\s(\d):[\w\s]+:\s(.{12}),[\w\s]+:\s(.+),\sCable.+Type:\s([\w\d]+),', line)
            if rx:
                reg = re.match('^NIC\s(\d):[\w\s]+:\s(.{12}),[\w\s]+:\s(.+),\sCable.+Type:\s([\w\d]+),', line)

                data = {
                    'nic': reg.group(1),
                    'mac': reg.group(2),
                    'driver': reg.group(4),

                }

                if reg.group(3) == "NAT":

                    data['type'] = "nat"

                else:

                    if re.search("^(Internal).+'(.+)'", reg.group(3)):

                        if re.match("^(Internal|Bridged).+'(.+)'", reg.group(3)).group(1) == "Internal":
                            data['type'] = "intnet"
                            data['name'] = re.match("^(Internal).+'(.+)'", reg.group(3)).group(2)

                        else:
                            data['type'] = re.match("^(Internal).+'(.+)'", reg.group(3)).group(1).lower()
                            data['iface'] = re.match("^(Internal).+'(.+)'", reg.group(3)).group(2)

        return data

    elif option == "vm_rdport":
        for line in data:
            regex = re.search('.+="TCP\/Ports"\svalue="(\d+)',line)
            if regex:
                return int(re.match(r'.+="TCP\/Ports"\svalue="(\d+)',line,).group(1))

    elif option == "rdppass":
        for line in data:
            return line


    elif option == "vm_os":
        for line in data:
            regex = re.search('.+OSType="(.*?)"\s',line, re.M|re.I)

            if regex:
                return re.match('.+OSType="(.*?)"\s',line, re.M|re.I).group(1)

            if line.split('=')[0] == "ostype":
                bad_chars ='"'
                return re.sub(bad_chars,"",line.split('=')[1])

    elif option == "vm_path":
        regex = '^(.+)\/' + vmname + '\/'
        rx = re.search(regex, data)
        if rx:
            return re.match(regex, data).group(1)


    # Control VM

    # NO OK

    # Snapshots
    
    elif option == "snap_list":
        vmsnaplist = []
        current = ""
        for line in data:
            if  re.search('^SnapshotName.*="(.+)"',line):
                snap_name = re.match('^SnapshotName.*="(.+)"',line).group(1)
            elif re.search('^SnapshotUUID.*="(.+)"',line):
                vmsnap ={
                    'name': snap_name,
                    'uuid': re.match('^SnapshotUUID.*="(.+)"',line).group(1),
                    'current': False,
                }
                snap_name = ""
                vmsnaplist.append(vmsnap)

            elif re.search('^CurrentSnapshotUUID="(.+)"',line):
                current = re.match('^CurrentSnapshotUUID="(.+)"',line).group(1)

        for snap in vmsnaplist:

            if snap['uuid'] == current:
                snap['current'] = True
        return vmsnaplist
        
    elif option == "current_snap":
        for line in data:
            if re.search('^CurrentSnapshotUUID="(.+)"',line):
                return re.match('^CurrentSnapshotUUID="(.+)"',line).group(1)

def vbox_info(option,**kwargs):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vmname variable
        - dstore valirable
    :return:
    '''

    if kwargs.get('vmname'):
        vmname = kwargs['vmname']

    if kwargs.get('vhost'):
        vhost = kwargs['vhost']

    if kwargs.get('datastore'):
        datastore = kwargs['datastore']

    # COMMANDS Virtual Hosts

    if option == "list_all":
        cmdCLI = "vboxmanage list vms"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "intnet":
        cmdCLI = "vboxmanage list intnets"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "ostypes":
        print ("Querz OS")
        cmdCLI = "vboxmanage list ostypes"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "ifaces":
        cmdCLI = 'netstat -i | egrep -vi "Tabl|kernel|Iface"'
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "datastore":
        cmdCLI = 'ls -d ' + datastore
        return vbox_paser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))


    # COMMANDS Virtual Machines  Control
    elif option == "vm_run":
        cmdCLI = "vboxmanage list runningvms"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmname=vmname)

    elif option == "get_name":
        cmdCLI = "vboxmanage list vms"
        return vbox_paser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI), vmname=vmname)

    elif option == "get_uuid":
        cmdCLI = "vboxmanage list vms"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmname=vmname)

    # COMMANDS Virtual Machines  Data

    elif option == "vm_uptime":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI),vmname=vmname)

    elif option == "vm_state":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_mem":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_ncpu":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_vdisk":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        cfgfile = vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))
        cmdCLI = "cat" + cfgfile
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_nic":
        cmdCLI = "vboxmanage showvminfo " + vmname
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_rdport":
        print ("VRDE_info", vmname)
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        cfgfile = vbox_paser(option = "vm_cfg", data = execCMD(vhost=vhost,cmd=cmdCLI))
        print("FIchero config",cfgfile)
        cmdCLI = "cat " + cfgfile
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

    elif option == "vm_os":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        cfgfile = vbox_paser(option = "vm_cfg", data = execCMD(vhost=vhost,cmd=cmdCLI))
        cmdCLI = "cat " + cfgfile
        return vbox_paser(option=option,data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "vm_path":
        cmdCLI = "vboxmanage showvminfo " + vmname + " --machinereadable"
        data = vbox_paser(option = "vm_cfg", data=execCMD(vhost=vhost,cmd=cmdCLI))
        return vbox_paser(option=option,data=data,vmname=vmname)


    # Contol Snapshots
    
    elif option == "snap_list":
        cmdCLI = "vboxmanage snapshot " + vmname + " list  --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))
        
    elif option == "current_snap":
        cmdCLI = "vboxmanage snapshot " + vmname + " list  --machinereadable"
        return vbox_paser(option=option,data=execCMD(vhost=vhost,cmd=cmdCLI))

def vbox_control(option,**kwargs):

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

        cmdCLI = "vboxmanage startvm " + vmachine.name + " --type headless"
        execCMD(vhost=vhost, cmd=cmdCLI)
        if vbox_info(option="vm_run",vhost=vhost,vmname=vmachine.name):
            vmachine.state = vbox_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
            vmachine.uptime = vbox_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
            vmachine.save()
            return True


    elif option=="stop_vm":

        cmdCLI = "vboxmanage controlvm " + vmachine.name + " poweroff"
        execCMD(vhost=vhost, cmd=cmdCLI)
        vmachine.state = vbox_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
        vmachine.uptime = vbox_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
        vmachine.save()

        if not vbox_info(option="vm_run",vhost=vhost,vmname=vmachine.name):
            return "OK"

    elif option =="pause_vm":

        if vbox_info(option="vm_state",vhost=vhost,vmname=vmachine.name) == 'PA':
            cmdCLI = "vboxmanage controlvm " + vmachine.name + " resume"
            execCMD(vhost=vhost, cmd=cmdCLI)
            vmachine.state = vbox_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
            vmachine.uptime = vbox_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
            vmachine.save()
            return "resumed"
        else:
            cmdCLI = "vboxmanage controlvm " + vmachine.name + " pause"
            execCMD(vhost=vhost, cmd=cmdCLI)
            vmachine.state = vbox_info(option="vm_state", vhost=vhost, vmname=vmachine.name)
            vmachine.uptime = vbox_info(option="vm_uptime", vhost=vhost, vmname=vmachine.name)
            vmachine.save()
            return "paused"

    elif option == "add_iso":




        pass

    elif option == "rm_iso":
        #http://www.vm-help.com/esx40i/manage_without_VI_client_1.php
        #https://communities.vmware.com/thread/420294?start=0&tstart=0

        pass

def vbox_create(vhost,vm):  #Decidir si lista o clase para mandar los parametros de la maquina virtual

    pypass = PyPass()
    remote_pass = pypass.run()
    remote_user = "consoleVM"
    remote_port = Console_Port(option="enable",vhost=vhost)

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    ##Define VM
    cmdCLI="VBoxManage createvm --name " + vm['name'] + " --ostype " + vm['ostype'] + " --basefolder " + vm['datastore'] + " --register" #Coomand return an UUID
    ssh.addCommand(cmdCLI)

    ##Add Controlers
    cmdCLI="VBoxManage storagectl " + vm['name']  + " --name " + vm['name'] +"_SATA --add sata"
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage storagectl " + vm['name'] + " --name " + vm['name'] + "_IDE --add ide"
    ssh.addCommand(cmdCLI)

    ##Create DISK
    dpath = vm['datastore']  + "/" + vm['name'] + "/" + vm['name'] + "_HD.vdi"
    cmdCLI="VBoxManage createhd --filename " + dpath + " --size " + vm['dsize'] ##DISK Size en MB.  this command giveback  the his uuid after creating it
    ssh.addCommand(cmdCLI)

    ##add controller DISK
    cmdCLI = "VBoxManage storageattach " + vm['name'] +" --storagectl " + vm['name'] +"_SATA --type hdd --medium " + dpath + " --port 0"
    ssh.addCommand(cmdCLI)

    #Add ISO
    cmdCLI = "VBoxManage storageattach " + vm['name'] +" --storagectl " +  vm['name'] +"_IDE --type dvddrive --port 0 --device 0 --medium " + vm['image']
    ssh.addCommand(cmdCLI)

    ##ADD cpu
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --cpus" + vm['cpu']
    ssh.addCommand(cmdCLI)

    ##ADD mem
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --memory " + vm['mem']
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --vram 128"
    ssh.addCommand(cmdCLI)

    ##Add Network

    nic = vm['iface']

    if vm['type'] == 'intnet':
        ntype = "intnet --intnet1 " + vm['net']
    elif vm['iface'] == 'bridged':
        ntype = "bridged --bridgeadapter1 " + vm['iface']
    else:
        ntype = "nat"

    cmdCLI = "VBoxManage modifyvm " + vm['name'] + "--nic1 " + ntype + " --nictype1 " + vm['driver']
    ssh.addCommand(cmdCLI)

    ##ADD cpboot parameters
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --ioapic on --boot1 dvd --boot2 disk --boot3 none --boot4 none"
    ssh.addCommand(cmdCLI)

    ##Enamble VRDE AUTH
    #cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --vrdeauthtype external"
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --vrdeauthtype null"
    ssh.addCommand(cmdCLI)
    #Create pass
    print ("Password_ ",remote_pass)
    cmdCLI = "VBoxManage internalcommands passwordhash " + remote_pass
    passhash = vbox_paser(option="rdppass", data=execCMD(vhost=vhost, cmd=cmdCLI))
    print (passhash)
    #ADD Console_Port VRDE USER and pass
    #cmdCLI = "VBoxManage setextradata " + vm['name'] + " VBoxAuthSimple/users/" + remote_user + " " + passhash
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --vrde on"
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + vm['name'] + " --vrdeport " + str(remote_port)
    ssh.addCommand(cmdCLI)

    log = ssh.execCMD()
    ssh.closeSession()


    vm_uuid =vbox_info(option="get_uuid", vhost=vhost, vmname=vm['name'])



    if vm_uuid:

        new_vm = VMachine(
            vuuid=vm_uuid,
            name=vm['name'],
            cpu=vm['cpu'],
            mem=vm['mem'],
            VHost_id=vhost.id,
            OsType_id= OsType.objects.get(name=vm['ostype']).id,
            Datastore_id= Datastore.objects.get(dpath=vm['datastore']).id,
            rdport=remote_port,
            rdppass=remote_pass,
            rdpuser=remote_user,
        )

        new_vm.save()


        new_dsk = VDisk (
            name = vm['name'] + "_HD.vdi",
            VMachine_id= new_vm.id,
            size = vm['dsize'],
        )

        new_dsk.save()


        Add_Client(vm=new_vm,vhost=vhost)


        return True
    else:
        return False

def vbox_modify(vhost,vm,data):

    '''
    :param option:
    :param kwargs:
        - vhost object
        - vmname variable
    :return:
    '''


    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    cmdCLI = "vboxmanage modifyvm " + vm.name + " --ncpu " + data['cpu']
    ssh.addCommand(cmdCLI)
    cmdCLI = "vboxmanage modifyvm " + vm.name + " --mem " + data['mem']
    ssh.addCommand(cmdCLI)

    cmdCLI = "vboxmanage modifyvm " + vm.name + " --ostype " + data['osname']
    ssh.addCommand(cmdCLI)


    nic = data['iface']
    if data['type'] == 'intnet':
        ntype = "inetnet --intnet1 " + data['net']
    elif data['iface'] == 'bridged':
        ntype = "bridged --bridgeadapter1 " + data['iface']
    else:
        ntype = "nat"

    cmdCLI = "VBoxManage modifyvm " + vm.name + " --nic1 " + ntype + " --nictype1 " + data['driver']
    ssh.addCommand(cmdCLI)
    cmdCLI = "vboxmanage modifyvm " + vm.name + " --name " + data['name']
    ssh.addCommand(cmdCLI)

    #Add ISO
    cmdCLI = "VBoxManage storageattach " + vm.name +" --storagectl " +  vm.name +"_IDE --type dvddrive --port 0 --device 0 --medium " + data['image']
    ssh.addCommand(cmdCLI)



    log = ssh.execCMD()
    ssh.closeSession()

    if vbox_info(option="get_uuid", vhost=vhost, vmname=data['name']):
        mod_vm = VMachine.objects.get(id=vm.id)
        mod_vm.name = data['name']
        mod_vm.OsType = OsType.objects.get(id=data['osid'])
        mod_vm.cpu = data['cpu']
        mod_vm.mem = data['mem']
        mod_vm.VSwitch = VSwitch.objects.get(id=data['vswid'])
        mod_vm.save()

        print ("Cambios", mod_vm.OsType.name, mod_vm.cpu, " ", mod_vm.mem)


        return True

    else:
        return False

def vbox_delete_vm(vhost,vm):

    cmdCLI="vboxmanage unregistervm " + vm.name + " --delete"

    execCMD(vhost=vhost, cmd=cmdCLI)
    print (vbox_info(option="get_uuid",vhost=vhost,vmname=vm.name))
    if not vbox_info(option="get_uuid",vhost=vhost,vmname=vm.name):
        vmdel = VMachine.objects.get(id=vm.id)
        print("MAquina",vmdel.name, "Puerto",vmdel.rdport)
        Console_Port(option="disable",vhost=vhost,rdport=vmdel.rdport)
        vmdel.delete()

        Remove_Client(name=vm.name)

        return True
    else:
        return False

def vbox_clone(vhost,vm,clone_name):

    pypass = PyPass()
    remote_pass = pypass.run()
    remote_user = "consoleVM"
    remote_port = Console_Port(option="enable",vhost=vhost)

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()
    
    cmdCLI = "vboxmanage clonevm " + vm.vuuid + " --mode machine --name " + clone_name + " --basefolder " + vm.Datastore.dpath  + " --register"
    ssh.addCommand(cmdCLI)
    ##Enamble VRDE AUTH
    cmdCLI = "VBoxManage modifyvm " + clone_name + " --vrdeauthtype external"
    ssh.addCommand(cmdCLI)
    # Create pass
    print("PASSOED",remote_pass)
    cmdCLI = "VBoxManage internalcommands passwordhash " + remote_pass
    passhash = vbox_paser(option="rdppass", data=execCMD(vhost=vhost, cmd=cmdCLI))
    print(passhash)
    # ADD Console_Port VRDE USER and pass
    cmdCLI = "VBoxManage setextradata " + clone_name + " VBoxAuthSimple/users/" + remote_user + " " + passhash
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + clone_name + " --vrde on"
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + clone_name + " --vrdeport " + str(remote_port)
    ssh.addCommand(cmdCLI)

    log = ssh.execCMD()
    ssh.closeSession()



    os = OsType.objects.filter(VType__id=vhost.VType.id).get(name=vbox_info(option="vm_os", vhost=vhost, vmname=clone_name))
    dpath = vbox_info(option="vm_path", vhost=vhost, vmname=clone_name)
    ds = Datastore.objects.filter(VHost__id=vhost.id).get(dpath=dpath)

    new_vm = VMachine(
        vuuid=vbox_info(option="get_uuid", vhost=vhost, vmname=clone_name),
        name=clone_name,
        cpu=vbox_info(option="vm_ncpu", vhost=vhost, vmname=clone_name),
        mem=vbox_info(option="vm_mem", vhost=vhost, vmname=clone_name),
        VHost_id=vhost.id,
        OsType_id=os.id,
        Datastore_id=ds.id,
        rdport=remote_port,
        VSwitch_id = vm.VSwitch.id,
        rdppass= remote_pass,
        rdpuser = remote_user,
    )
    new_vm.save()

    Add_Client(name=new_vm.name, protocol="rdp", port=new_vm.rdport, username=new_vm.rdpuser, password=new_vm.rdppass,
               hostname=vhost.ipaddr)

    if VMachine.objects.get(vuuid=vbox_info(option="get_uuid",vhost=vhost,vmname=clone_name)):
        return True
    else:
        return False

def vbox_create_dstore(vhost,dname,dpath):


    cmdCLI = "mkdir -p " + dpath
    execCMD(vhost=vhost, cmd=cmdCLI)

    if vbox_info(option="datastore", vhost=vhost, datastore=dpath) == dpath:
        return True
    else:
        return False

def vbox_delete_dstore(vhost, dpath):

    if not dpath == "/":
        cmdCLI = "rm -rf " + dpath
        execCMD(vhost=vhost, cmd=cmdCLI)

    if vbox_info(option="datastore", vhost=vhost, datastore=dpath) == dpath:
        return False
    else:
        return True

def vbox_snapshots(option,vhost,vm,**kwargs):
    
    '''
    :param option:
    :param kwargs:
        - suuid = varaible
        
    :return:
    '''

    if kwargs.get('suuid'):
        suuid = kwargs['suuid']
    
    if option == "snap_list":
        return vbox_info(option=option, vhost=vhost, vmname=vm.name)
        
    elif option == "snap_create":
        cmdCLI = "vboxmanage snapshot " + vm.vuuid + "  take snap_" + vm.name + "_ --uniquename Timestamp --live"
        execCMD(vhost=vhost, cmd=cmdCLI)
        return vbox_info(option="current_snap", vhost=vhost, vmname=vm.name)

    elif option == "snap_delete":
        cmdCLI = "vboxmanage snapshot " + vm.vuuid + "  delete " + suuid 
        data = execCMD(vhost=vhost, cmd=cmdCLI)

        print (cmdCLI)

        snaplist = vbox_info(option="snap_list", vhost=vhost, vmname=vm.name)
        if not snaplist:
            snap = Snapshot.objects.get(suuid=suuid)
            snap.delete()
            return True
        else:
            for snap in vbox_info(option="snap_list", vhost=vhost, vmname=vm.name):

                if snap['uuid'] == suuid:
                    return False
                else:
                    snap = Snapshot.objects.get(suuid=suuid)
                    snap.delete()
                    return True
        
    elif option == "snap_restore":
        cmdCLI = "vboxmanage snapshot " + vm.vuuid + " restore " + suuid
        print(cmdCLI)
        execCMD(vhost=vhost, cmd=cmdCLI)
        if suuid == vbox_info(option="current_snap", vhost=vhost, vmname=vm.name):
            return True
        else:
            return False

def vbox_vrde(vmname,vhost):

    pypass = PyPass()
    remote_pass = pypass.run()
    remote_user = "consoleVM"
    remote_port = Console_Port(option="enable",vhost=vhost)

    ssh = sshSession(hostip = vhost.ipaddr, hostuser = vhost.user, userkey = vhost.sshkey, port=vhost.sshport)
    ssh.openSession()

    ##Enamble VRDE AUTH
    cmdCLI = "VBoxManage modifyvm " + vmname + " --vrdeauthtype external"
    ssh.addCommand(cmdCLI)
    # Create pass
    cmdCLI = "VBoxManage internalcommands passwordhash " + remote_pass
    passhash = vbox_paser(option="rdppass", data=execCMD(vhost=vhost, cmd=cmdCLI))

    # ADD Console_Port VRDE USER and pass
    cmdCLI = "VBoxManage setextradata " + vmname + " VBoxAuthSimple/users/" + remote_user + " " + passhash
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + vmname + " --vrde on"
    ssh.addCommand(cmdCLI)
    cmdCLI = "VBoxManage modifyvm " + vmname + " --vrdeport " + str(remote_port)
    ssh.addCommand(cmdCLI)

    log = ssh.execCMD()
    ssh.closeSession()

    vrde_data={
        'user' : remote_user,
        'pass' : remote_pass,
        'port' : remote_port
    }

    return vrde_data