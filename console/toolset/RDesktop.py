from console.models import VHost,VType, VMachine,   Datastore, OsType, Snapshot, Remote_Admin, VSwitch, Medium


def Rdesktop(option,vhost,**kwargs):

    if kwargs['port']:
        remote_port = kwargs.get('port')

    if option == "enable":
        OK_port = False
        while not OK_port:
            remote_port = random.randint (60000, 65000)
            if not Remote_Admin.objects.filter(vhost_id=vhost.id, rdport=remote_port).exists():
                new_port = Remote_Admin(
                    vhost=vhost,
                    rdport=remote_port
                )
                new_port.save()
            return new_port
    elif option == "disable":
        dis_port = Remote_Admin.objects.get(vhost_id=vhost.id, rdport=remote_port)
        dis_port.delete()
        return True
    pass
