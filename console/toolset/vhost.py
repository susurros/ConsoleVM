import re, math
from .ssh import execCMD, sshSession
from .vbox import vbox_info
from .esx import esx_info
from .zones import zone_info
from .guacamole import Update_Model
from console.models import VHost,VType, VMachine,   Datastore, OsType, Snapshot, Remote_Admin, VSwitch, Medium

def vhost_parser(option,data,**kwargs):


    if kwargs.get('os'):
        os = kwargs['os']

    if option == "cpu":

        cpu = 0
        for line in data:
            cpu += 1
        return cpu

    elif option == 'mem':

        if os == "Solaris":
            for line in data:
                rx = re.search('^Memory\ssize:\s(\d+)',line)
                if rx:
                    return re.match('^Memory\ssize:\s(\d+)',line).group(1) # MB

        if os == "VMWARE":
            for line in data:
                rx = re.search('^\s+Physical\sMemory:\s(\d+)\sBytes', line)
                if rx:
                    return math.floor(int(re.match('^\s+Physical\sMemory:\s(\d+)\sBytes',line).group(1))/1048576)  # Bytes to MB
        else:
            for line in data:
                rx = re.search('^MemTotal:\s+(\d+)', line)
                if rx:
                    return math.floor(int(re.match('^MemTotal:\s+(\d+)', line).group(1))/1024) # Kb to MB

    elif option == "uptime":
        for line in data:
            return line

    elif option == "ifaces":

        if os == "Solaris":
            vhifaces = []
            for line in data:
                vhifaces.append(line)
            pass

        elif os == "VMWARE":
            vhifaces = []
            for line in data:
                vhifaces.append(line)
            pass


        else:
            vhifaces = []
            for line in data:
                rx = re.search('^(\w+\s)', line)
                if rx:
                    iface = re.match('^(\w+\s)', line).group(1)
                    vhifaces.append(iface)
            return vhifaces

    elif option == "dstore_info":

        for line in data:
            rx = re.search('^.+\s+(\d+)\s+\d+\s+(\d+)\s+(\d+%)',line)
            if rx:
                rxm = re.match('^.+\s+(\d+)\s+\d+\s+(\d+)\s+(\d+%)',line)
                ds_info = {
                    'size': rxm.group(1),
                    'free': rxm.group(2),
                    'use': rxm.group(3),
                }
                return ds_info

    elif option == "images":
        print ("INSIDE IMAGES")
        images = []
        for iso in data:
            print (iso)
            images.append(iso)
        return images

def vhost_info(option,vhost,**kwargs):

    if kwargs.get('dpath'):
        dpath = kwargs['dpath']

    if option == "cpu":

        if vhost.VType.vendor == "ZN":
            cmdCLI='psrinfo'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))
        elif vhost.VType.vendor == "VW":
            cmdCLI='esxcli hardware cpu list | grep CPU:'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))
        else:
            cmdCLI='cat /proc/cpuinfo  | grep proc'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

        pass

    elif option == "mem":

        if vhost.VType.vendor == "ZN":
            cmdCLI='prtconf | grep Mem'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI),os="Solaris")
        elif vhost.VType.vendor == "VW":
            cmdCLI = 'esxcli hardware memory get | grep Phy'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI), os="VMWARE")
        else:
            cmdCLI='cat /proc/meminfo  | grep MemTotal'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI),os="Linux")

    elif option == "ifaces":

        if vhost.VType.vendor == "ZN":
            cmdCLI = 'ipadm show-if | cut -d " " -f1 | egrep -v "IFNAME|lo0" '
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI),os="Solaris")
        elif vhost.VType.vendor == "VW":
            cmdCLI='esxcli network nic list | grep vmnic'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI), os="VMWARE")
        else:
            cmdCLI = 'netstat -i | egrep -vi "Tabl|kernel|Iface"'
            return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI),os="Linux")

    elif option == "uptime":

        cmdCLI = 'uptime | cut -d "," -f1'
        return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))


    elif option == "dstore_info":

        cmdCLI = 'df -k ' + dpath + "| grep -v File"
        return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI), os="Linux")

    elif option == "images":

        cmdCLI = "ls -1 " + vhost.isopath +"/*.iso"
        return vhost_parser(option=option, data=execCMD(vhost=vhost, cmd=cmdCLI))

    elif option == "rem_adm_port":  # Not Implmeted

        VH = Remote_Admin.objects.all().filter(VHost__id=vhost.id)

        if not VH:
            new_port = 20000
        else:
            print (VH)
        rem_adm = Remote_Admin.objects.filter(VHost=vhost).latest(id)
        print ("remote %s", rem_adm)

        if rem_adm:
            new_port = rem_adm.port + 1
        else:
            new_port = 20000

        ports = Remote_Admin.objects.all()
        block = 0

        while block == 0:

            port_block = 0
            for port in ports:
                if port.rdport == new_port:
                    port_block = 1

            if port_block == 0:
                block = 1
                final_port = new_port

            else:
                new_port = rem_adm.port + 1

        return final_port

def vhost_control(option,vhost):

    if option == "shutdown":
        if VHost.VType == "VW":
            cmdCLI="shutdown now"
        else:
            cmdCLI="shutdown.sh now"
        execCMD(vhost=vhost, cmd=cmdCLI)

def update_model(option, **kwargs):  # Mirar como acturalizar

    '''

    :param option:
    :param kwargs: vhost object
    :return:
    '''

    if 'vmname' in kwargs:
        vm = kwargs['vmname']
    elif 'vhost' in kwargs:
        vh = kwargs['vhost']

    if option == "vmachines":

        print("update vmachines")

        VH = VHost.objects.all()

        for item in VH:

            if item.VType.vendor == "VB":

                list_machines_local = vbox_info(option="list_all", vhost=item)

                for machine in list_machines_local:

                    if VMachine.objects.filter(vuuid=machine['uuid']).exists():

                        vmname = machine['name']
                        vnic= vbox_info(option="vm_nic",vhost=item,vmname=vmname)

                        print ("REDES VBOX")
                        print(vnic)

                        print("VNIC TYPE",vnic['type'])


                        if vnic['type'] == "intnet":
                            vsw = VSwitch.objects.get(VHost__id=item.id,type="inet",name=vnic['name'])
                        elif vnic['type'] == "bridged":
                            netname = vnic['type'] + "_" + vnic['iface']
                            vsw = VSwitch.objects.get(VHost__id=item.id,type="bridged",name=netname)
                        elif vnic['type'] == "nat":
                            vsw = VSwitch.objects.get(VHost__id=item.id, type="nat")
                        else:
                            vsw = None

                        vmachine = VMachine.objects.get(vuuid=machine['uuid'])
                        vmachine.name = vmname
                        vmachine.cpu = vbox_info(option="vm_ncpu", vhost=item, vmname=vmname)
                        vmachine.mem = vbox_info(option="vm_mem", vhost=item, vmname=vmname)
                        vmachine.rdport = vbox_info(option="vm_rdport", vhost=item, vmname=vmname)
                        vmachine.state = vbox_info(option="vm_state", vhost=item, vmname=vmname)
                        vmachine.uptime = vbox_info(option="vm_uptime", vhost=item, vmname=vmname)
                        vmachine.VSwitch = vsw
                        vmachine.save()

                    else:

                        vmname = machine['name']
                        os = OsType.objects.filter(VType__id=item.VType.id).get(name=vbox_info(option="vm_os", vhost=item, vmname=vmname))
                        dpath = vbox_info(option="vm_path", vhost=item, vmname=vmname)
                        ds = Datastore.objects.filter(VHost__id=item.id).get(dpath=dpath)
                        vnic= vbox_info(option="vm_nic",vhost=item,vmname=vmname)

                        print ("REDES VBOX", vmname)
                        print(vnic)

                        print("VNIC TYPE",vnic['type'])

                        if vnic['type'] == "intnet":
                            vsw = VSwitch.objects.get(VHost__id=item.id,type="inet",name=vnic['name'])
                        elif vnic['type'] == "bridged":
                            netname = vnic['type'] + "_" + vnic['iface']
                            vsw = VSwitch.objects.get(VHost__id=item.id,type="bridged",name=netname)
                        elif vnic['type'] == "bridged":
                            vsw = VSwitch.objects.get(VHost__id=item.id, type="nat")
                        else:
                            vsw = None

                        new_vm = VMachine(
                            vuuid=machine['uuid'],
                            name=vmname,
                            cpu=vbox_info(option="vm_ncpu", vhost=item, vmname=vmname),
                            mem=vbox_info(option="vm_mem", vhost=item, vmname=vmname),
                            VHost_id=item.id,
                            OsType_id=os.id,
                            Datastore_id=ds.id,
                            rdport=vbox_info(option="vm_rdport", vm=vmname),
                            VSwitch = vsw,
                        )
                        new_vm.save()

            elif item.VType.vendor == "VW":

                list_machines_local = esx_info(option="list_all", vhost=item)


                for machine in list_machines_local:


                    if VMachine.objects.filter(vuuid=machine['uuid']).exists():

                        vmname = machine['name']
                        vnic= esx_info(option="vm_nic",vhost=item,vmname=vmname)

                        if VSwitch.objects.filter(VHost__id=item.id, name=vnic).exists():
                            vsw =VSwitch.objects.get(VHost__id=item.id, name=vnic)
                        else:
                            vsw = None

                        vuuid = machine['uuid']
                        vmachine = VMachine.objects.get(vuuid=vuuid)
                        vmachine.name = vmname
                        vmachine.cpu = esx_info(option="vm_ncpu", vhost=item, vuuid=vuuid)
                        vmachine.mem = esx_info(option="vm_mem", vhost=item, vuuid=vuuid)
                        vmachine.rdport = esx_info(option="vm_rdport", vhost=item, vuuid=vuuid)
                        vmachine.state = esx_info(option="vm_state", vhost=item, vuuid=vuuid)
                        vmachine.uptime = esx_info(option="vm_uptime", vhost=item, vuuid=vuuid)
                        vmachine.VSwitch = vsw
                        vmachine.save()

                    else:

                        vmname = machine['name']
                        vuuid = machine['uuid']
                        os = OsType.objects.filter(VType__id=item.VType.id).get(name=esx_info(option="vm_os", vhost=item, vmname=vmname))
                        dpath = esx_info(option="vm_path", vhost=item, vmname=vmname)
                        ds = Datastore.objects.filter(VHost__id=item.id).get(dpath=dpath)
                        rem_data = esx_info(option="vm_vrde", vhost=item, vmname=vmname)

                        vnic = esx_info(option="vm_nic", vhost=item, vmname=vmname)

                        if VSwitch.objects.filter(VHost__id=item.id, name=vnic).exists():
                            vsw = VSwitch.objects.get(VHost__id=item.id, name=vnic)
                        else:
                            vsw = ""


                        if rem_data:
                            new_vm = VMachine(
                                vuuid=vuuid,
                                name=vmname,
                                cpu= esx_info(option="vm_ncpu", vhost=item, vuuid=vuuid),
                                mem= esx_info(option="vm_mem", vhost=item, vuuid=vuuid),
                                VHost_id=item.id,
                                OsType_id=os.id,
                                Datastore_id=ds.id,
                                rdport=int(rem_data['port']),
                                rdppass=rem_data['passwd'],
                                VSwitch=vsw,
                            )
                        else:
                            new_vm = VMachine(
                                vuuid=vuuid,
                                name=vmname,
                                cpu= esx_info(option="vm_ncpu", vhost=item, vuuid=vuuid),
                                mem= esx_info(option="vm_mem", vhost=item, vuuid=vuuid),
                                VHost_id=item.id,
                                OsType_id=os.id,
                                Datastore_id=ds.id,
                                VSwitch=vsw,
                            )

                        new_vm.save()

            elif item.VType.vendor == "ZN":

                list_machines_local = zone_info(option="list_all", vhost=item)

                for machine in list_machines_local:
                    if VMachine.objects.filter(vuuid=machine['uuid']).exists():

                        vmname = machine['name']
                        vnic = zone_info(option="vm_link", vhost=item, vmname=vmname)

                        if VSwitch.objects.filter(VHost__id=item.id, name=vnic).exists():
                            vsw = VSwitch.objects.get(VHost__id=item.id, name=vnic)
                        else:
                            print ("swith", machine)
                            vsw = None

                        vmachine = VMachine.objects.get(vuuid=machine['uuid'])
                        vmachine.name = vmname
                        vmachine.cpu = zone_info(option="vm_ncpu", vhost=item, vmname=vmname)
                        vmachine.mem = zone_info(option="vm_mem", vhost=item, vmname=vmname)
                        vmachine.rdport = zone_info(option="vm_rdport", vhost=item, vmname=vmname)
                        vmachine.state = zone_info(option="vm_state", vhost=item, vmname=vmname)
                        vmachine.uptime = zone_info(option="vm_uptime", vhost=item, vmname=vmname)
                        vmachine.VSwitch = vsw
                        vmachine.save()

                    else:
                        vmname = machine['name']

                        vnic = zone_info(option="vm_link", vhost=item, vmname=vmname)

                        if VSwitch.objects.filter(VHost__id=item.id, name=vnic).exists():
                            vsw = VSwitch.objects.get(VHost__id=item.id, name=vnic)
                        else:
                            print ("swith", machine)
                            vsw = None

                        os = OsType.objects.filter(VType__id=item.VType.id).get(name=zone_info(option="vm_os", vhost=item, vmname=vmname))
                        dpath = re.sub('/'+vmname,"",zone_info(option="vm_path", vhost=item, vmname=vmname))
                        ds = Datastore.objects.filter(VHost__id=item.id).get(dpath=dpath)


                        new_vm = VMachine(
                            vuuid=machine['uuid'],
                            name=vmname,
                            cpu=zone_info(option="vm_ncpu", vhost=item, vmname=vmname),
                            mem=zone_info(option="vm_mem", vhost=item, vmname=vmname),
                            VHost_id=item.id,
                            OsType_id=os.id,
                            Datastore_id=ds.id,
                            state=zone_info(option="vm_state", vhost=item, vmname=vmname),
                            VSwitch=vsw,
                        )
                        new_vm.save()

            db_machines = VMachine.objects.filter(VHost__id=item.id)
            for db_machine in db_machines:

                if item.VType.vendor == "VB":
                    if not vbox_info(option="get_uuid", vhost=item, vmname=db_machine.name) == db_machine.vuuid:
                        db_machine.delete()
                elif item.VType.vendor == "VW":
                    if not esx_info(option="get_uuid", vhost=item, vmname=db_machine.name) == db_machine.vuuid:
                        db_machine.delete()
                elif item.VType.vendor == "ZN":
                    if not zone_info(option="get_uuid", vhost=item, vmname=db_machine.name) == db_machine.vuuid:
                        db_machine.delete()

    elif option == "ostypes":

        VH = VHost.objects.all()

        for item in VH:
            if item.VType.vendor == "VB":
                for data in vbox_info(option="ostypes", vhost=item):

                    if not OsType.objects.filter(name=data['id'], VType=item.VType).exists():
                        os = OsType(name=data['id'], desc=data['desc'], VType=item.VType)
                        os.save()

            elif item.VType.vendor == "VW":
                for data in esx_info(option="ostypes", vhost=item):
                    if not OsType.objects.filter(name=data['id'], VType=item.VType).exists():
                        os = OsType(name=data['id'], desc=data['desc'], VType=item.VType)
                        os.save()

            else:
                for data in zone_info(option="ostypes", vhost=item):
                    if not OsType.objects.filter(name=data['id'], VType=item.VType).exists():
                        os = OsType(name=data['id'], desc=data['desc'], VType=item.VType)
                        os.save()

    elif option == "vswitch":

        VH = VHost.objects.all()

        for item in VH:
            if item.VType.vendor == "VB":
                intnet = vbox_info(option="intnet", vhost=item)
                for int_name in intnet:
                    if VSwitch.objects.filter(VHost_id=item.id,type="intnet",name=int_name).exists():
                        vnet = VSwitch.objects.get(VHost_id=item.id,type="intnet",name=int_name)
                        vnet.name = int_name
                        vnet.VHost = item
                        vnet.type = "intnet"
                        vnet.save()
                    else:
                        new_intnet= VSwitch(
                            name = int_name,
                            VHost = item,
                            type = "intnet",
                        )
                        new_intnet.save()

                if not VSwitch.objects.filter(VHost_id=item.id, type="nat").exists():
                    new_nat = VSwitch(
                        name="nat",
                        VHost=item,
                        type="nat",
                    )
                    new_nat.save()

                ndevices = vbox_info(option="ifaces",vhost=item)

                for ndev in ndevices:
                    if not VSwitch.objects.filter(VHost_id=item.id,type="bridged",phy_iface=ndev).exists():
                        new_bridged = VSwitch(
                            name="bridged_" + ndev,
                            VHost=item,
                            type="bridged",
                            phy_iface=ndev,
                        )
                        new_bridged.save()


            elif item.VType.vendor == "VW":

                network = esx_info(option="vswitch-portgroup",vhost=item)

                for net in network:

                    if VSwitch.objects.filter(VHost__id=item.id,type=net['vswitch'], name=net['portgroup']).exists():
                        vport = VSwitch.objects.get(VHost_id=item.id,type=net['vswitch'],name=net['portgroup'])
                        vport.name = net['portgroup']
                        vport.VHost = item
                        vport.type = net['vswitch']
                        vport.save()
                    else:
                        new_port = VSwitch(
                            name=net['portgroup'],
                            VHost=item,
                            type=net['vswitch'],
                        )
                        new_port.save()

            elif item.VType.vendor == "ZN":

                port_group = zone_info(option="port_groups", vhost=item)

                for port in port_group:

                    if VSwitch.objects.filter(VHost__id=item.id,type="portgroup", name=port).exists():
                        vport = VSwitch.objects.get(VHost_id=item.id,type="portgroup",name=port)
                        vport.name = port
                        vport.VHost = item
                        vport.type = "portgroup"
                        vport.save()
                    else:
                        new_port = VSwitch(
                            name=port,
                            VHost=item,
                            type="portgroup",
                        )
                        new_port.save()

    elif option == "datastores":

        VH = VHost.objects.all()
        for item in VH:

            if item.VType.vendor == "VB":

                list_machines_local = vbox_info(option="list_all", vhost=item)
                for machine in list_machines_local:

                    dpath = vbox_info(option="vm_path", vhost=item, vmname=machine['name'])

                    if not Datastore.objects.filter(dpath=dpath).exists():
                        ds_name = re.match('^.+/(.+$)', dpath).group(1)
                        ds = Datastore(name=ds_name, dpath=dpath, VHost_id=item.id)
                        ds.save()

            elif item.VType.vendor == "VW":
                dstore = esx_info(option="datastore",vhost=item)

                for ds in dstore:
                    if Datastore.objects.filter(dpath=ds['dpath']).exists():
                        current_ds = Datastore.objects.get(dpath=ds['dpath'])
                        current_ds.name = ds['dname']
                        current_ds.dpath = ds['dpath']
                        current_ds.save()
                    else:

                        new_ds = Datastore(
                            name = ds['dname'],
                            dpath = ds['dpath'],
                            VHost = item,
                        )
                        new_ds.save()


            elif item.VType.vendor == "ZN":
                dpath = zone_info(option="datastore", vhost=item)

                print (" LIST PATH", dpath)

                for ds in dpath:

                    if Datastore.objects.filter(dpath=ds['dpath']).exists():
                        print ("Exists")
                        current_ds = Datastore.objects.get(dpath=ds['dpath'])
                        current_ds.name = ds['dname']
                        current_ds.dpath = ds['dpath']
                        current_ds.save()
                    else:
                        new_ds = Datastore(
                            name=ds['dname'],
                            dpath=ds['dpath'],
                            VHost=item,
                        )
                        new_ds.save()

    elif option == "update_state":

        VH = VHost.objects.all()

        for item in VH:
            if item.VType.vendor == "VB":

                if VMachine.objects.filter(VHost__id=item.id).exists():
                    list_machines = VMachine.objects.filter(VHost__id=item.id)

                    for vmachine in list_machines:

                        vmachine.state = vbox_info(option="vm_state", vhost=item, vmname=vmachine.name)
                        vmachine.uptime = vbox_info(option="vm_uptime", vhost=item, vmname=vmachine.name)
                        vmachine.save()

            elif item.VType.vendor == "VW":

                if VMachine.objects.filter(VHost__id=item.id).exists():
                    list_machines = VMachine.objects.filter(VHost__id=item.id)

                    for vmachine in list_machines:

                        print ("Machine,state,id",vmachine,esx_info(option="vm_state", vhost=item, vuuid=vmachine.vuuid),vmachine.vuuid)
                        vmachine.state = esx_info(option="vm_state", vhost=item, vuuid=vmachine.vuuid)
                        vmachine.uptime = esx_info(option="vm_uptime", vhost=item, vuuid=vmachine.vuuid)

                        vmachine.save()

            elif item.VType.vendor == "ZN":

                if VMachine.objects.filter(VHost__id=item.id).exists():
                    list_machines = VMachine.objects.filter(VHost__id=item.id)

                    for vmachine in list_machines:
                        vmachine.state = zone_info(option="vm_state", vhost=item, vmname=vmachine.name)
                        vmachine.uptime = zone_info(option="vm_uptime", vhost=item, vmname=vmachine.name)
                        vmachine.save()

    elif option == "snap_shot":

        list_vhost = VHost.objects.all()

        for VH in list_vhost:

            if VH.VType.vendor == "VB":
                list_machines = VMachine.objects.filter(VHost__id=VH.id)
                for VM in list_machines:
                    snap_list = vbox_info(option="snap_list",vhost=VH,vmname=VM.name)
                    for snap in snap_list:
                        if Snapshot.objects.filter(suuid=snap['uuid'],VMachine__id=VM.id).exists():
                            snap_db = Snapshot.objects.get(suuid=snap['uuid'],VMachine__id=VM.id)
                            snap_db.current = snap['current']
                            snap_db.save()
                        else:
                            new_snap = Snapshot(
                                name = snap['name'],
                                suuid = snap['uuid'],
                                current = snap['current'],
                                VMachine = VM,
                            )
                            new_snap.save()

            elif VH.VType.vendor == "VW":
                list_machines = VMachine.objects.filter(VHost__id=VH.id)
                for VM in list_machines:
                    snap_list = esx_info(option="snap_list", vhost=VH, vuuid=VM.vuuid)
                    for snap in snap_list:
                        if Snapshot.objects.filter(suuid=snap['uuid'], VMachine__id=VM.id).exists():
                            snap_db = Snapshot.objects.get(suuid=snap['uuid'], VMachine__id=VM.id)
                            snap_db.current = snap['current']
                            snap_db.save()
                        else:
                            new_snap = Snapshot(
                                name=snap['name'],
                                suuid=snap['uuid'],
                                current=snap['current'],
                                VMachine=VM,
                            )
                            new_snap.save()

    elif option == "medium":

        list_vhost = VHost.objects.all()

        for VH in list_vhost:

            list_images = vhost_info(option="images",vhost=VH)

            for item in list_images:

                print (item)
                if not Medium.objects.filter(VHost__id=VH.id,dpath=item).exists():

                    iso_name = re.sub(VH.isopath + "/",'',item)
                    new_iso = Medium(
                        name=iso_name,
                        dpath=item,
                        VHost=VH,
                    )
                    new_iso.save()

    elif option == "remote":

        VM = VMachine.objects.all()

        Update_Model(list_machines=VM)
        #for item in VM:
         #   Update_Model(vm=item)

def update_db_init():
    #update_model(option="ostypes")
    #update_model(option="ifaces")
    #update_model(option="datastores")
    #update_model(option="vswitch")
    #update_model(option="vmachines")
    #update_model(option="medium")
    update_model(option="remote")



