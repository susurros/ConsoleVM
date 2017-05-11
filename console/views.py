from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.http import Http404, HttpResponse, JsonResponse
from .models import VMachine, VHost, VType, Datastore, OsType, VSwitch # Borrar si no se usa Ifaces, VBOX_IFACE, VDisk
from .forms import VHForm, DSForm
from .toolset.vbox import vbox_info, vbox_create, vbox_modify, vbox_create_dstore, vbox_delete_vm
from .toolset.esx import esx_info, esx_create_vm, esx_create_net, esx_modify
from .toolset.zones import zone_info, zone_create_vm, zone_create_net, zone_create_dstore
from .toolset.vhost import vhost_info, update_model


# Create your views here.

def dash_vm(request):

    update_model(option="update_state")
    update_model(option="snap_shot")
    dbmachines = VMachine.objects.all()
    VV = VType.objects.order_by('name')

    return render(request, 'console/dash-vm.html', {'vm':dbmachines,'vv': VV})

def form_vm(request):

    if request.is_ajax() and request.POST:

        dstore  = Datastore.objects.get(id=int(request.POST.get('datastore')))
        os = OsType.objects.get(id=int(escape(request.POST.get('ostype'))))
        vsw = VSwitch.objects.get(id=int(escape(request.POST.get('vswitch'))))

        vmdata = {
            'name': escape(request.POST.get('name')),
            'vhost': int(escape(request.POST.get('vhost'))),
            'datastore' : dstore.dpath,
            'cpu' : escape(request.POST.get('cpu')),
            'mem' : escape(request.POST.get('mem')),
            'ostype' : os.name,
            'rdpport' : escape(request.POST.get('rdpport')),
            'dsize': escape(request.POST.get('dsize')),
            'driver': escape(request.POST.get('driver')),
            'net' : vsw.name,
        }

        vhost_id = vmdata['vhost']
        vmname = vmdata['name']


        if not VMachine.objects.filter(VHost_id=vhost_id,name=vmname).exists():

            VH = VHost.objects.get(id=vhost_id)

            if VH.VType.vendor == "VB":

                vmdata['type']=vsw.type
                vmdata['iface']=vsw.phy_iface
                vmdata['net']=vsw.name
                vmdata['rdpuser'] = escape(request.POST.get('rdpuser'))
                vmdata['rdppass'] = escape(request.POST.get('rdppass'))
                vmdata['image'] = escape(request.POST.get('image'))


                print(vmdata)
                if vbox_create(vhost=VH,vm=vmdata):
                    data = {
                        'msg': 'The Virtual Machine has been created. Please click close to continue',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'msg': 'Error: The Virtual Machine has not been created. Please contact with the administrator',
                    }
                    return JsonResponse(data)



            elif VH.VType.vendor == "VW":

                print(vmdata)

                msg = esx_create_vm(vhost=VH,vm=vmdata)

                print(msg)

                if msg == "OK":
                    data = {
                    'msg': 'The Virtual Machine has been created. Please click close to continue',
                    }
                    return JsonResponse(data)
                else:
                    print ("Error Creating the Virtual Machine: ", msg)
                    data = {
                    'msg': 'Error: The Virtual Machine has not been created. Please contact with the administrator',
                    }
                    return JsonResponse(data)


            elif VH.VType.vendor == "ZN":

                if zone_create_vm(vhost=VH,vm=vmdata):

                    data = {
                        'msg': 'The Virtual Machine has been created. Please click close to continue',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'msg': 'Error: The Virtual Machine has not been created. Please contact with the administrator',
                    }
                    return JsonResponse(data)
    else:

        VH = VHost.objects.all()

        return render(request, 'console/form_vmachine.html', {'VH': VH})

def dash_vhost(request):

    vhosts = VHost.objects.order_by('VType')
    VV = VType.objects.order_by('name')

    virtualhost=[]
    for item in vhosts:

        data={
            'id' : item.id,
            'name' : item.name,
            'VType': item.VType,
            'ipaddr': item.ipaddr,
            'cpu': vhost_info(option="cpu",vhost=item),
            'mem': vhost_info(option="mem",vhost=item),
            'uptime': vhost_info(option="uptime",vhost=item)
        }
        virtualhost.append(data)

    return render(request, 'console/dash-vh.html', {'vh': virtualhost, 'vv': VV})

def form_vhost (request):

    if request.is_ajax() and request.method == "POST":
        print(escape(request.POST.get('ipaddr')))
        print(request.POST.get('ipaddr'))

        ajax_id = int(escape(request.POST.get('vhostid')))
        VH = VHost.objects.get(id=ajax_id)
        VH.name = escape(request.POST.get('name'))
        VH.ipaddr = escape(request.POST.get('ipaddr'))
        VH.isopath = escape(request.POST.get('isopath'))
        VH.sshkey = escape(request.POST.get('sshkey'))
        VH.sshport = int(escape(request.POST.get('sshport')))
        VH.save()

        data = {
            'msg': 'The Virtual Host' + VH.name + ' has been modified',
            'URI': '/vhost/',
        }
        return JsonResponse(data)

    elif not request.is_ajax() and request.method == "POST":
        form = VHForm(request.POST)
        if form.is_valid():
            vh = form.save(commit=False)
            vh.save()
            return redirect('/vhost')

    else:
        form = VHForm()

    return render(request, 'console/form_vhost.html', {'form': form})

def dash_datastore(request):


    ds = Datastore.objects.all()
    dstore = []

    for item in ds:

        print ("Nombre Datastore %s",item.dpath)


        VH = VHost.objects.get(id=item.VHost.id)

        dsize = vhost_info(option='dstore_info',vhost=VH,dpath=item.dpath)

        print (dsize)
        data = {
            'id' : item.id,
            'vhost': item.VHost.name,
            'vendor': item.VHost.VType.name,
            'name': item.name,
            'dpath': item.dpath,
            'dsize_total': int(int(dsize['size'])/1024),
            'dsize_free': int(int(dsize['free'])/1024),
            'dsize_use': dsize['use'],
        }
        dstore.append(data)

    # Parameter to be used in the web template
    VH = VHost.objects.order_by('name')


    return render(request, 'console/dash-dstore.html', {'dstore': dstore, 'vhosts': VH})

def form_datastore(request):

    if request.is_ajax() and request.POST:
        vhost_id = int(escape(request.POST.get('vhost')))
        ds_name = escape(request.POST.get('name'))
        VH = VHost.objects.get(id=vhost_id)

        if VH.VType.vendor == "VB":
            dpath = escape(request.POST.get('dpath'))
        elif VH.VType.vendor == "ZN":
            zpool = escape(request.POST.get('dpath'))
            dpath = "/" + zpool + "/" + ds_name

        else:
            return Http404

        if not Datastore.objects.filter(VHost__id=vhost_id,name=ds_name,dpath=dpath).exists():

            if VH.VType.vendor == "VB":
                if vbox_create_dstore(vhost=VH,dname=ds_name,dpath=dpath):

                    new_ds = Datastore(
                        name = ds_name,
                        VHost = VH,
                        dpath = dpath,
                    )
                    new_ds.save()
                    data = {
                        'msg': "The new Datastore has been created in the DB",
                        'URI': "/vhost/datastore",
                    }
                else:
                    data = {
                        'msg': "There is been an error creating the Datastore. Please contact de Administrator",
                        'URI': "/vhost/datastore",
                    }
            elif VH.VType.vendor == "ZN":
                if zone_create_dstore(vhost=VH, dname=ds_name, zpool=zpool):

                    new_ds = Datastore(
                        name=ds_name,
                        VHost=VH,
                        dpath=dpath,
                    )
                    new_ds.save()
                    data = {
                        'msg': "The new Datastore has been created in the DB",
                        'URI': "/vhost/datastore",
                    }
                else:
                    data = {
                        'msg': "There is been an error creating the Datastore. Please contact de Administrator",
                        'URI': "/vhost/datastore",
                    }
            else:
                return Http404

        else:
            data = {
                'msg': "The Datastore already exists",
                'URI': "/vhost/datastore",
            }
        return JsonResponse(data)

    else:
        return Http404

def dash_network(request):

    vsw = VSwitch.objects.all()
    VH = VHost.objects.order_by('name')

    return render(request, 'console/dash-network.html', {'vswitch': vsw, 'vhosts': VH})

def form_network(request):

    if request.is_ajax() and request.POST:
        vhost_id = int(escape(request.POST.get('vhost')))
        net_name = escape(request.POST.get('name'))
        VH = VHost.objects.get(id=vhost_id)

        if VH.VType.vendor == "VB":
            ntype = "intnet"
        elif VH.VType.vendor == "ZN":
            ntype = "portgroup"
        else:
            ntype = escape(request.POST.get('ntype'))

        if not VSwitch.objects.filter(VHost_id=vhost_id, name=net_name, type=ntype).exists():

            if VH.VType.vendor == "VB":
                new_net = VSwitch(
                    name=net_name,
                    VHost=VH,
                    type="intnet",
                )
                new_net.save()
                data = {
                    'msg' : "The new Virtual Box Network has been created in the DB",
                    'URI' : "/vhost/network",
                }
                return JsonResponse(data)

            elif VH.VType.vendor == "VW":


                if esx_create_net(vhost=VH,pg_name=net_name,vswitch=ntype):
                    new_net = VSwitch(
                        name=net_name,
                        VHost=VH,
                        type=ntype,
                    )
                    new_net.save()
                    data = {
                        'msg' : "The creation of the " + net_name + " has been made succesfully",
                        'URI' : "/vhost/network",
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'msg' : "The creation of the " + net_name +" portgroup has failed. Please contact with an Administrator",
                        'URI' : "/vhost/network",
                    }
                    return JsonResponse(data)

            elif VH.VType.vendor == "ZN":

                if zone_create_net(vhost=VH,pg_name=net_name):
                    new_net = VSwitch(
                        name=net_name,
                        VHost=VH,
                        type = "portgroup",
                    )
                    new_net.save()
                    data = {
                        'msg' : "The creation of the " + net_name + " has been made succesfully",
                        'URI' : "/vhost/network",
                    }
                    return JsonResponse(data)

                else:
                    data = {
                        'msg' : "The creation of the " + net_name +" portgroup has failed. Please contact with an Administrator",
                        'URI' : "/vhost/network",
                    }
                    return JsonResponse(data)

        else:
            print("Existe")
            print(VSwitch.objects.get(VHost_id=vhost_id, name=net_name, type=ntype))
            data = {'URI': '/vhost/network', 'msg': "Error: A network with this name already exits in the Virtual Host"}
            return JsonResponse(data)

    else:
        VH = VHost.objects.all()
        return render(request, 'console/form_network.html', {'VH': VH})

def dash_snap(request):

    if request.POST:
        ajax_id = int(request.POST.get('vmid'))
        vm = VMachine.objects.get(id=ajax_id)
    pass

