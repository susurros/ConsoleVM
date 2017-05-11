import json
from .models import VMachine, VHost, Datastore,   OsType, VSwitch,  Snapshot, Medium
from console.toolset.vbox import vbox_info, vbox_create, vbox_control, vbox_snapshots, vbox_modify, vbox_delete_dstore, vbox_delete_vm, vbox_clone
from console.toolset.esx import esx_info, esx_create_vm, esx_control, esx_delete_vm, esx_modify, esx_snapshots, esx_delete_net, esx_clone
from console.toolset.zones import zone_info, zone_create_vm, zone_control, zone_delete_vm, zone_delete_net, zone_delete_dstore, zone_clone, zone_modify
from console.toolset.vhost import update_model
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.html import escape

# VMACHINES

def start_vm(request):

    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if str(ajax_id) == str(vm.id):

            VH = VHost.objects.get(id=vm.VHost.id)

            if VH.VType.vendor == "VB":
                if vbox_info(option="vm_state", vhost=VH, vmname=vm.name) == "PW":
                    if vbox_control(option="start_vm", vhost=VH, vm=vm):
                        data = {'msg': "The Virtual Machine %s has been initated" % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Internal Error starting %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)
                elif vbox_info(option="vm_state", vhost=VH, vmname=vm.name) == "PA":
                    data = {'msg': "The Virtual Machine %s is paused. Please press Resume if you want to change its state" % vm.name}
                    return JsonResponse(data)
                else:
                    data = {'msg': "The Virtual Machine %s is already started" % vm.name}
                    return JsonResponse(data)

            elif VH.VType.vendor == "VW":
                if not esx_info(option="vm_run", vhost=VH, vuuid=vm.vuuid) == "RN":
                    if esx_control(option="start_vm", vhost=VH,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been initated" % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Internal Error starting %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)
                else:
                    data = {'msg': "The Virtual Machine %s is already started" % vm.name}
                    return JsonResponse(data)

            elif VH.VType.vendor == "ZN":
                if not zone_info(option="list_run", vhost=VH, vmname=vm.name):

                    if zone_control(option="start_vm", vhost=VH,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been initated" % vm.name}
                        return JsonResponse(data)

                    else:
                        data = {'msg': "Internal Error starting %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s is already started" % vm.name}
                    return JsonResponse(data)

            else:
                return Http404

        else:
            data = {'msg': "The Virtual Machine %s does not Exist" % vm.name }
            return JsonResponse(data)

    else:
        raise Http404

def stop_vm(request):
    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if str(ajax_id) == str(vm.id):

            VH = VHost.objects.get(id=vm.VHost.id)

            if VH.VType.vendor == "VB":


                if not vbox_info(option="vm_state",vhost=VH,vmname=vm.name) == "PW":

                    if vbox_control(option="stop_vm", vhost=VH,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been stoped" % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Internal Error starting %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s is not running" % vm.name}
                    return JsonResponse(data)

            elif VH.VType.vendor == "VW":


                if not esx_info(option="vm_run", vhost=VH, vuuid=vm.vuuid) == "PW":

                    if esx_control(option="stop_vm", vhost=VH, vm=vm):
                        data = {'msg': "The Virtual Machine %s has been stoped" % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Internal Error starting %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s is not running" % vm.name}
                    return JsonResponse(data)

            elif VH.VType.vendor == "ZN":


                if zone_info(option="list_run", vhost=VH, vmname=vm.name):

                    test = zone_control(option="stop_vm", vhost=VH, vm=vm)
                    if test:

                        data = {'msg': "The Virtual Machine %s has been stoped" % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Internal Error stopping %s. Please report to the administrator" % vm.name}
                        return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s is not running" % vm.name}
                    return JsonResponse(data)


        else:
            data = {'msg': "The Virtual Machine %s does not Exist" % vm.name }
            return JsonResponse(data)

    else:
        raise Http404

def pause_vm(request):
    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)
        if str(ajax_id) == str(vm.id):

            VH = VHost.objects.get(id=vm.VHost.id)

            if VH.VType.vendor == "VB":

                state_pause = vbox_control(option="pause_vm", vhost=VH, vm=vm)

                print (state_pause)

                if state_pause == "paused":
                    data = {'msg': "The Virtual Machine %s has been paused" % vm.name}
                    return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s has been resumed" % vm.name}
                    return JsonResponse(data)

            elif VH.VType.vendor == "VW":

                state_pause = esx_control(option="pause_vm", vhost=VH, vm=vm)

                print (state_pause)

                if state_pause == "paused":
                    data = {'msg': "The Virtual Machine %s has been paused" % vm.name}
                    return JsonResponse(data)

                else:
                    data = {'msg': "The Virtual Machine %s has been resumed" % vm.name}
                    return JsonResponse(data)

        else:
            data = {'msg': "The Virtual Machine %s does not Exist" % vm.name }
            return JsonResponse(data)

    else:
        raise Http404

def mng_snap(request):


    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if int(ajax_id) == int(vm.id):

            SP = Snapshot.objects.filter(VMachine__id=vm.id)

            snaplist = []
            for snap in SP:
                data ={
                    'suuid': snap.suuid,
                    'name': snap.name,
                }
                if snap.current:
                    data['current']="True"
                else:
                    data['current']="False"

                snaplist.append(data)

            json_data = {
                'vm_id': vm.id,
                'vm_name': vm.name,
                'vm_vuuid': vm.vuuid,
                'snaplist':json.dumps(snaplist)
            }
            return JsonResponse(json_data)
        else:
            raise Http404
    else:
        raise Http404

def mk_snap(request):
    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if vm.VHost.VType.vendor == "VB":
            if int(ajax_id) == int(vm.id):
                suuid = vbox_snapshots(option="snap_create",vhost=vm.VHost,vm=vm)
                data = {'msg': "Snapshot with the UUID: %s has been created on the vm   %s " % (suuid,vm.name) }
                return JsonResponse(data)
            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)
        if vm.VHost.VType.vendor == "VW":
            if int(ajax_id) == int(vm.id):
                suuid = esx_snapshots(option="snap_create",vhost=vm.VHost,vm=vm)
                data = {'msg': "Snapshot with the UUID: %s has been created on the vm   %s " % (suuid,vm.name) }
                return JsonResponse(data)
            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)
    else:
        raise Http404

def rst_snap(request):
    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if vm.VHost.VType.vendor == "VB":
            if int(ajax_id) == int(vm.id):
                suuid = request.POST.get('suuid')
                if vbox_control(option="stop_vm", vhost=vm.VHost, vm=vm):
                    if vbox_snapshots(option="snap_restore", vhost=vm.VHost, vm=vm, suuid=suuid):
                        data = {'msg': "Snapshot with the UUID: %s has been recovered from  the vm   %s " % (suuid, vm.name)}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Snapshot with the UUID: %s does not exist on the vm   %s " % (suuid, vm.name)}
                        return JsonResponse(data)
                else:
                    raise Http404
            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)
        elif vm.VHost.VType.vendor == "VW":
            if int(ajax_id) == int(vm.id):
                suuid = request.POST.get('suuid')
                if esx_snapshots(option="snap_restore", vhost=vm.VHost, vm=vm, suuid=suuid):
                    data = {'msg': "Snapshot with the UUID: %s has been recovered from  the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)
                else:
                    data = {'msg': "Snapshot with the UUID: %s does not exist on the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)
            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)
    else:
        raise Http404

def del_snap(request):

    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)

        if vm.VHost.VType.vendor == "VB":
            if int(ajax_id) == int(vm.id):

                suuid = request.POST.get('suuid')
                if vbox_snapshots(option="snap_delete", vhost=vm.VHost, vm=vm,suuid=suuid):
                    data = {'msg': "Snapshot with the UUID: %s has been deleted from  the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)

                else:
                    data = {'msg': "Snapshot with the UUID: %s does not exist on the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)

            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)

        elif vm.VHost.VType.vendor == "VW":
            if int(ajax_id) == int(vm.id):

                suuid = request.POST.get('suuid')
                if esx_snapshots(option="snap_delete", vhost=vm.VHost, vm=vm, suuid=suuid):
                    data = {
                        'msg': "Snapshot with the UUID: %s has been deleted from  the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)

                else:
                    data = {'msg': "Snapshot with the UUID: %s does not exist on the vm   %s " % (suuid, vm.name)}
                    return JsonResponse(data)

            else:
                data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
                return JsonResponse(data)

    else:
        raise Http404

def recover_snap_vm(request):
    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)
        if ajax_id == vm.id:

            #cmdCLI = "vboxmanage startvm " +  vm.name + " --type headless"
            #exeCMD (vm.vhostid, cmdCLI)
            data = {'msg': "The Virtual Maachine %s has been initated" % vm.name }
            return JsonResponse(data)
        else:
            data = {'msg': "The Virtual Maachine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
            return JsonResponse(data)
    else:
        raise Http404

def delete_vm(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('vmid'))
        vm = VMachine.objects.get(id=ajax_id)
        if ajax_id == vm.id:

            if vm.VHost.VType.vendor == "VB":
                if vbox_info(option="vm_run", vhost=vm.VHost, vmname=vm.name):
                    if vbox_control(option="stop_vm", vhost=vm.VHost, vm=vm):
                        if vbox_delete_vm(vhost=vm.VHost,vm=vm):
                            data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                            return JsonResponse(data)
                        else:
                            data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                            return JsonResponse(data)
                else:
                    if vbox_delete_vm(vhost=vm.VHost,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                        return JsonResponse(data)
            elif vm.VHost.VType.vendor == "VW":
                if esx_info(option="list_run", vhost=vm.VHost, vmname=vm.name):
                    if esx_control(option="stop_vm", vhost=vm.VHost, vm=vm):
                        if esx_delete_vm(vhost=vm.VHost,vm=vm):
                            data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                            return JsonResponse(data)
                        else:
                            data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                            return JsonResponse(data)
                else:
                    if esx_delete_vm(vhost=vm.VHost,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                        return JsonResponse(data)
            elif vm.VHost.VType.vendor == "ZN":
                if zone_info(option="list_run", vhost=vm.VHost, vmname=vm.name):
                    if zone_control(option="stop_vm", vhost=vm.VHost, vm=vm):
                        if zone_delete_vm(vhost=vm.VHost,vm=vm):
                            data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                            return JsonResponse(data)
                        else:
                            data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                            return JsonResponse(data)
                else:
                    if zone_delete_vm(vhost=vm.VHost,vm=vm):
                        data = {'msg': "The Virtual Machine %s has been deleted " % vm.name}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "The Virtual Machine %s has not been deleted. Please remove it manually " % vm.name}
                        return JsonResponse(data)



        else:
            data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
            return JsonResponse(data)
    else:
        raise Http404

def modify_vm(request):

    print (request.POST.get('jqreq') )

    if request.is_ajax() and request.POST.get('jqreq') == "get_data":

        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)


        print (ajax_id)
        print (vm.id)
        if int(ajax_id) == int(vm.id):

            print ("Insde Mod Update")

            # Update OS
            os = OsType.objects.all().filter(VType_id=vm.VHost.VType)
            oslist =[]
            for item in os:
                ostype = {
                    "id": item.id,
                    "os" : item.name,
                }
                oslist.append(ostype)

            osname = OsType.objects.get(id=vm.OsType.id).name

            # Update Networking
            switchs = VSwitch.objects.all().filter(VHost_id=vm.VHost.id)

            vswlist = []
            for item in switchs:
                vswitch = {
                    "id": item.id,
                    "vsw": item.name,
                }
                vswlist.append(vswitch)
            if vm.VHost.VType.vendor == "VB":
                drivers = ["Am79C970A", "Am79C973", "82540EM", "82543GC", "82545EM"]
            elif vm.VHost.VType.vendor == "VW":
                drivers = ["E1000", "E1000e", "VMXNET"]
            else:
                drivers = ["default"]

            isos = Medium.objects.all().filter(VHost_id=vm.VHost.id)
            isolist = []
            for item in isos:
                iso = {
                    "id": item.id,
                    "name": item.name,
                }
                isolist.append(iso)

            data = {
                "vmname": vm.name,
                "vmid": vm.id,
                "osname": osname,
                "cpu": vm.cpu,
                "mem": vm.mem,
                "vhostid": vm.VHost.id,
                "vhostname": vm.VHost.name,
                "vswid":  vm.VSwitch.id,
                "oslist" : json.dumps(oslist),
                "vswlist": json.dumps(vswlist),
                "isolist": json.dumps(isolist),
                "drivers": drivers,
                "vendor": vm.VHost.VType.vendor,
                "rdpuser": vm.rdpuser,
                "rdppass": vm.rdppass,
                "rdpport": vm.rdport,
            }

            print ("VM DATA",data)
            return JsonResponse(data)
        else:
             raise Http404

    elif request.is_ajax() and request.POST.get('jqreq') == "modify":

        ajax_id = escape(int(request.POST.get('vmid')))
        vm = VMachine.objects.get(id=ajax_id)
        if int(ajax_id) == int(vm.id):

            vsw = VSwitch.objects.get(id=int(escape(request.POST.get('vswid'))))

            current_os = OsType.objects.get(id=int(escape(request.POST.get('osid'))))

            vmdata = {
                'name' : request.POST.get('name'),
                'vhostid' : request.POST.get('vhostid'),
                'vmid' : request.POST.get('vmid'),
                'cpu' : request.POST.get('cpu'),
                'mem' : request.POST.get('mem'),
                'vswid' : request.POST.get('vswid'),
                'osid': int(escape(request.POST.get('osid'))),
                'osname': current_os.name,
                'net': vsw.name,
                'rpduser': request.POST.get('rpduser'),
                'rdppass': request.POST.get('rdppass'),
                'rdpport': request.POST.get('rdpport'),
            }

            if vm.state == "PW":
                if vm.VHost.VType.vendor == "VB":
                    vmdata['driver'] = escape(request.POST.get('driver'))
                    vmdata['type']=vsw.type
                    vmdata['iface']=vsw.phy_iface

                    print (vmdata)
                    if vbox_modify(vhost=vm.VHost,vm=vm,data=vmdata):
                        data = {'msg': "The Virtual Machine " + vm.name + " has been modified"}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Error: There was a problem in the modification of the Virtual Machine: " + vm.name + ". Please contact de administrator"}
                        return JsonResponse(data)


                elif vm.VHost.VType.vendor == "VW":
                    vmdata['driver'] = escape(request.POST.get('driver'))
                    print (vmdata)
                    if esx_modify(vhost=vm.VHost,vm=vm,data=vmdata):
                        data = {'msg': "The Virtual Machine " + vm.name + " has been modified"}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Error: There was a problem in the modification of the Virtual Machine: " + vm.name + ". Please contact de administrator"}
                        return JsonResponse(data)

                elif vm.VHost.VType.vendor == "ZN":
                    print (vmdata)
                    if zone_modify(vhost=vm.VHost, vm=vm, data=vmdata):
                        data = {'msg': "The Virtual Machine " + vm.name + " has been modified"}
                        return JsonResponse(data)
                    else:
                        data = {'msg': "Error: There was a problem in the modification of the Virtual Machine: " + vm.name + ". Please contact de administrator"}
                        return JsonResponse(data)

            else:
                data = {'msg': "Please shutdown first the  Virtual Machine: " + vm.name}
                return JsonResponse(data)


    else:
        raise Http404

def clone_vm(request):

    print ("Clone")
    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('clid'))
        vm = VMachine.objects.get(id=ajax_id)
        if ajax_id == vm.id:
            clname = escape(request.POST.get('name'))
            if vm.VHost.VType.vendor == "VB":
                if vbox_clone(vhost=vm.VHost,vm=vm,clone_name=clname):
                    data = {'msg': "The Virtual Machine" + vm.name + " has been clonated"}
                    return JsonResponse(data)
            elif vm.VHost.VType.vendor == "VW":
                if esx_clone(vhost=vm.VHost,vm=vm,clone_name=clname):
                    data = {'msg': "The Virtual Machine" + vm.name + " has been clonated"}
                    return JsonResponse(data)
            elif vm.VHost.VType.vendor == "ZN":
                if zone_clone(vhost=vm.VHost,vm=vm,clone_name=clname):
                    data = {'msg': "The Virtual Machine" + vm.name + " has been clonated"}
                    return JsonResponse(data)
        else:
            data = {'msg': "The Virtual Machine does not Exist", 'console': vm.id, "ajax_id": ajax_id}
            return JsonResponse(data)
    else:
        raise Http404

def form_vm(request):


    if request.is_ajax():

        if request.POST.get('action') == "close":


            request.session['step'] = '0'
            data = {'URI' : '/vmachine/new/',}

            return JsonResponse(data)

        elif request.POST.get('action') == "back":

            if int(request.session['step']) < 1:

                request.session['step'] = '0'
                data = {'URI': '/vmachine/new/',}

                return JsonResponse(data)

            else:

                request.session['step'] = str(int(request.session['step']) -1)
                data = {'URI': '/vmachine/new/',}

                return JsonResponse(data)

        elif request.POST.get('vhid'):

            ajax_id = int(request.POST.get('vhid'))
            request.session['vhost'] = ajax_id
            request.session['step'] = '1'
            data = {'URI': '/vmachine/new/',}

            return JsonResponse(data)

        elif request.POST.get('step') == '1' and request.POST.get('name'):

            VH = VHost.objects.get(id=request.session['vhost'])


            request.session['vmname'] = escape(request.POST.get('name'))
            request.session['cpu'] = escape(request.POST.get('cpu'))
            request.session['mem'] = escape(request.POST.get('mem'))
            request.session['os'] = request.POST.get('os')
            request.session['dstore'] = (request.POST.get('dstore'))
            request.session['dsksz'] = (request.POST.get('dsksz'))
            request.session['step'] = '2'

            if VH.VType.vendor == "VB":
                request.session['ifaces'] = json.loads(request.POST.get('ifaces'))
                request.session['rdpuser'] = escape(request.POST.get('rdpuser'))
                request.session['rdppass'] = escape(request.POST.get('rdppass'))
                request.session['rdpport'] = escape(request.POST.get('rdpport'))
                request.session['meddpath'] = escape(request.POST.get('meddpath'))
            elif VH.VType.vendor == "VW":
                request.session['ifaces'] = json.loads(request.POST.get('ifaces'))
                request.session['rdppass'] = escape(request.POST.get('rdppass'))
                request.session['rdpport'] = escape(request.POST.get('rdpport'))
                request.session['meddpath'] = escape(request.POST.get('meddpath'))
            elif VH.VType.vendor == "ZN":
                request.session['ifaces'] = escape(request.POST.get('ifaces'))
                request.session['rdpuser'] = escape(request.POST.get('rdpuser'))
                request.session['rdppass'] = escape(request.POST.get('rdppass'))
                request.session['rdpport'] = escape(request.POST.get('rdpport'))
                request.session['meddpath'] = escape(request.POST.get('meddpath'))

            data = {'URI': '/vmachine/new/',}
            return JsonResponse(data)

        elif request.POST.get('step') == '2':

            VH = VHost.objects.get(id=request.session['vhost'])

            dstore = Datastore.objects.get(id=int(request.session['dstore']))
            os = OsType.objects.get(id=int(request.session['os']))

            data ={

                'name' : request.session['vmname'],
                'ostype' : os.name,
                'cpu' : request.session['cpu'],
                'mem': request.session['mem'],
                'datastore' : dstore.dpath ,
                'disksz': request.session['dsksz'],
                'ifaces': request.session['ifaces'],
                'meddpath': request.session['meddpath'],

            }


            if VH.VType.vendor == "VB":
                data['rdpuser'] = request.session['rdpuser']
                data['rdppass'] = request.session['rdppass']
                data['rdpport'] = request.session['rdpport']
                data['meddpath'] = request.session['meddpath']
                vm = vbox_create(vhost=VH,vm=data)
            elif VH.VType.vendor == "VW":
                data['rdppass'] = request.session['rdppass']
                data['rdpport'] = request.session['rdpport']
                data['meddpath'] = request.session['meddpath']
                vm = esx_create_vm(vhost=VH,vm=data)
                print (vm)
            elif VH.VType.vendor == "ZN":
                data['rdpuser'] = request.session['rdpuser']
                data['rdppass'] = request.session['rdppass']
                data['rdpport'] = request.session['rdpport']
                vm = zone_create_vm(vhost=VH,vm=data)

            print (vm)
            if vm == "OK":

                session_keys =['vhost', 'vmname', 'cpu','mem','os','dstore','dsksz','step']
                for key in session_keys:
                    print(request.session[key])
                    request.session[key] = ""
                    print (request.session[key])

                data = { 'msg': "Virtual Machine Created",
                         'URI': '/vmachine/',
                        }

            else:
                session_keys = ['vhost', 'vmname', 'cpu', 'mem', 'os', 'dstore', 'dsksz', 'step']
                for key in session_keys:
                    request.session[key] = ""
                data = {'msg': "There has been a problem with the VirtualMachine Creation. Please start the process again. If this happens again please contact with the administrator",
                        'URI': '/vmachine/new',
                        }

            return JsonResponse(data)

def vm_update_query(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('vhostid'))
        vh = VHost.objects.get(id=ajax_id)
        if ajax_id == vh.id:

            # Update OS
            os = OsType.objects.all().filter(VType_id=vh.VType)
            oslist =[]
            for item in os:
                ostype = {
                    "id": item.id,
                    "os" : item.name,
                }
                oslist.append(ostype)


            # Update Datastore

            datastore = Datastore.objects.all().filter(VHost_id=vh.id)

            dslist =[]
            for item in datastore:
                dsitm = {
                    "id": item.id,
                    "ds" : item.name,
                }
                dslist.append(dsitm)

            # Update Networking
            switchs = VSwitch.objects.all().filter(VHost_id=vh.id)

            vswlist = []
            for item in switchs:
                vswitch = {
                    "id": item.id,
                    "vsw": item.name,
                }
                vswlist.append(vswitch)

            if vh.VType.vendor == "VB":
                drivers = ["Am79C970A", "Am79C973", "82540EM", "82543GC", "82545EM"]
            elif vh.VType.vendor == "VW":
                drivers = ["E1000", "E1000e", "VMXNET"]
            else:
                drivers = ["default"]

            isos = Medium.objects.all().filter(VHost_id=vh.id)
            isolist = []
            for item in isos:
                iso = {
                    "id": item.id,
                    "name": item.name,
                }
                isolist.append(iso)

            data = {
                "oslist" : json.dumps(oslist),
                "dslist" : json.dumps(dslist),
                "vswlist": json.dumps(vswlist),
                "isolist": json.dumps(isolist),
                "drivers": drivers,
                "vendor": vh.VType.vendor,
            }
            return JsonResponse(data)
        else:
            return Http404
    else:
        return Http404

def remote(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('vmid'))
        vm = VMachine.objects.get(id=ajax_id)
        if ajax_id == vm.id:

            if vm.rdport:
                data = {
                    "name" : vm.name,
                    "cnx" : "c",
                    "athml" : "noauth",
                    "url" : "/guacamole/#/client/",
                    "remote" : "True"
                }
                return JsonResponse(data)

            else:
                data = {'msg': "Error: The Virtual Machines " + vm.name + " does not have a remote configuration defined. Please make the proper modifications or contact de administrator",
                        "remote": "False"}

            return JsonResponse(data)
        else:
            return Http404
    else:
        return Http404


# VHOST

def control_vh(request):

    if request.is_ajax() and request.POST:
        ajax_id = escape(int(request.POST.get('vhid')))
        cmd = escape(str(request.POST.get('command')))
        VH = VHost.objects.get(id=ajax_id)

        if str(ajax_id) == str(vm.id):

            if cmd == "shutdown":
                if VH.VType.vendor == "VB":
                    list_machines = VMachine.objects.get(VHost_id=VH.id)
                    for machine in list_machines:
                        vbox_control(option="stop_vm", vhost=VH,vm=machine)

                elif VH.VType.vendor == "VW":
                    list_machines = VMachine.objects.get(VHost_id=VH.id)
                    for machine in list_machines:
                        esx_control(option="stop_vm", vhost=VH,vm=machine)

                elif VH.VType.vendor == "ZN":
                    list_machines = VMachine.objects.get(VHost_id=VH.id)
                    for machine in list_machines:
                        zone_control(option="stop_vm", vhost=VH,vm=machine)

                data = {
                    'msg': "Maintenace Shutdown of the Virtual Host %s has started, this could take some time " % vm.name,
                    'URI': "/vhost",
                    'wait_time': '50'
                }

                return JsonResponse(data)

        else:
            data = {'msg': "The Virtual Host  %s does not Exist" % vm.name }
            return JsonResponse(data)

    else:
        raise Http404

def vhost_update_query(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(escape(request.POST.get('vhostid')))
        VH = VHost.objects.get(id=ajax_id)

        data = {
            'id': VH.id,
            'name': VH.name,
            'ipaddr': VH.ipaddr,
            'VType': VH.VType.name,
            'user': VH.user,
            'sshkey': VH.sshkey,
            'sshport': VH.sshport,
            'isopath': VH.isopath,
        }

        print (data)
        return JsonResponse(data)
    else:
        return Http404

def delete_vhost(request):

    if request.is_ajax() and request.POST:
        ajax_id = escape(request.POST.get('vhostid'))
        VH = VHost.objects.get(id=ajax_id)

        print ("SOME THING HAPPEND")
        data = {
            'URI': "/vhost/",
            "msg": "Virtual Host " + VH.name + " deleted. Remember that the other objects (Virtual Machines,Network and Datastores) asssociented with this Virtual Host also has been deleted from the Database",
        }
        VH.delete()
        return JsonResponse(data)

    else:
        return Http404

def dstore_update_query(request):

    if request.is_ajax() and request.POST.get('jq_req') == "vhost":
        VH = VHost.objects.all()
        vhost_list = []
        for item in VH:
            if not item.VType.vendor == "VW":
                vh_data = {
                    'id': item.id,
                    'name': item.name,
                }
                vhost_list.append(vh_data)
        data = {
            'vhosts': json.dumps(vhost_list),
        }
        return JsonResponse(data)

    elif request.is_ajax() and request.POST.get('jq_req') == "ds_type":
        VH = VHost.objects.get(id=int(escape(request.POST.get('vhostid'))))
        data = {
            'vendor' : VH.VType.vendor,
        }
        if VH.VType.vendor == "ZN":
            data['zpool_list'] = zone_info(option="zpool", vhost=VH)
        return JsonResponse(data)

def del_dstore(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('ds_id'))
        dstore = Datastore.objects.get(id=ajax_id)
        VH = VHost.objects.get(id=dstore.VHost.id)
        if ajax_id == dstore.id:

            if dstore.VHost.VType.vendor == "VB":
                if vbox_delete_dstore(vhost=VH,dpath=dstore.dpath):
                    data = {
                        'msg': 'The Datastore' + dstore.name + ' has been deleted',
                        'URI': '/vhost/datastore',
                    }
                    dstore.delete()
                else:
                    return Http404
            elif dstore.VHost.VType.vendor == "ZN":
                if zone_delete_dstore(vhost=VH,dpath=dstore.dpath):
                    data = {
                        'msg': 'The Datastore' + dstore.name + ' has been deleted',
                        'URI': '/vhost/datastore',
                    }
                    dstore.delete()
                else:
                    return Http404
            return JsonResponse(data)

        else:
            return Http404

    else:
        return Http404

def net_update_query(request):

    if request.is_ajax() and request.POST.get('jq_req') == "vsw_type":
        ajax_id = int(request.POST.get('vhostid'))
        vh = VHost.objects.get(id=ajax_id)
        if ajax_id == vh.id:
            data = {"vendor": vh.VType.vendor,}
            if vh.VType.vendor == "VW":
                data['vswlist'] = json.dumps(esx_info(option="vswitch-nic", vhost=vh))
            return JsonResponse(data)
        else:
            return Http404

    elif request.is_ajax() and request.POST.get('jq_req') == "vhost":
        VH = VHost.objects.all()
        vhost_list = []
        for item in VH:
            vh_data = {
                'id': item.id,
                'name': item.name,
            }
            vhost_list.append(vh_data)
        data = {
            'vhosts': json.dumps(vhost_list),
        }
        return JsonResponse(data)

    else:
        return Http404

def del_net(request):

    if request.is_ajax() and request.POST:
        ajax_id = int(request.POST.get('vsw_id'))
        vsw = VSwitch.objects.get(id=ajax_id)

        if ajax_id == vsw.id:

            data = {
                'msg': 'The Virtual Network ' + vsw.name + ' has been deleted',
                'URI': '/vhost/network',
            }

            if vsw.VHost.VType.vendor == "VB":
                vsw.delete();
                return JsonResponse(data)

            elif vsw.VHost.VType.vendor == "VW":
                if esx_delete_net(vhost_id=vsw.VHost.id, vswitch=vsw.type, pg_name=vsw.name):
                    vsw.delete();
                    return JsonResponse(data)
                else:
                    data = {
                        'msg': 'The Virtual Network ' + vsw.name + ' cannot been deleted. Please contact and Administrator',
                        'URI': '/vhost/network',
                    }
                    return JsonResponse(data)

            elif vsw.VHost.VType.vendor == "ZN":
                print (vsw.VHost.id)
                if zone_delete_net(vhost_id=vsw.VHost.id, pg_name=vsw.name):
                    vsw.delete();
                    return JsonResponse(data)
                else:
                    data = {
                        'msg': 'The Virtual Network ' + vsw.name + ' cannot been deleted. Please contact and Administrator',
                        'URI': '/vhost/network',
                    }
                    return JsonResponse(data)

            else:
                return Http404

        else:
            return Http404

    else:
        return Http404

def updatedb(request):
    if request.is_ajax() and request.POST:
        up_type = escape(request.POST.get('type'))

        if up_type == "vmachine":
            update_model(option="ostypes")
            update_model(option="ifaces")
            update_model(option="datastores")
            update_model(option="vswitch")
            update_model(option="vmachines")
            update_model(option="medium")
            update_model(option="remote")
            data = {'msg': "Database updated successfully" }
            return JsonResponse(data)

        elif up_type == "vswitch":
            update_model(option="ifaces")
            update_model(option="vswitch")
            data = {'msg': "Database updated successfully"}
            return JsonResponse(data)

        elif up_type == "vmachines":
            update_model(option="datastores")
            data = {'msg': "Database updated successfully"}
            return JsonResponse(data)

        else:
            data = {'msg': "Error: Update Database Failed. Please  contact de administrator" }
            return JsonResponse(data)
    else:
        return Http404










