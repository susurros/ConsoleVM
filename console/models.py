import uuid
from django.db import models
from django.utils import timezone

# Models Vendor

class VType(models.Model):

    VBOX = 'VB'
    ZONES = 'ZN'
    ESX = 'VW'

    VENDOR_CHOICES = (
        (VBOX, 'Oracle Virtualbox'),
        (ZONES, 'Oracle Solaris'),
        (ESX, 'Vmware ESXi'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    vendor = models.CharField(max_length=2, choices=VENDOR_CHOICES,default=VBOX)

    def __str__(self):
        return self.name

# Models Virtual Hosts

class VHost(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    ipaddr = models.GenericIPAddressField (protocol='ipv4')
    VType = models.ForeignKey(VType)  # Lista de Vbox,ESXi, Zones
    user = models.CharField(max_length=10)
    sshkey = models.CharField(max_length=255)   # Mirar si existe un modelo especifco
    sshport = models.PositiveIntegerField(blank=True)
    isopath = models.CharField(max_length=100)



    def __str__(self):
        return self.name

class OsType(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    VType = models.ForeignKey(VType)

    def __str__(self):
        return self.name

class Datastore(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    dpath = models.CharField(max_length=100, null=False)
    VHost = models.ForeignKey(VHost)

    def __str__(self):
        return self.name

class VSwitch(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    VHost = models.ForeignKey(VHost)
    type = models.CharField(max_length=30, blank=True, null=True)
    phy_iface = models.CharField(max_length=7, blank=True, null=True)

class Medium(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    dpath = models.CharField(max_length=100)
    VHost = models.ForeignKey(VHost)

    def __str__(self):
        return self.name

'''
class Mediums(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
'''

# Models Virtual Machines

class VMachine(models.Model):



    RUNNING = 'RN'
    POWEROFF = 'PW'
    PAUSE = 'PA'

    STATE_CHOICES = (
        (RUNNING, 'running'),
        (POWEROFF, 'poweroff'),
        (PAUSE, 'paused'),
    )


    INSTALLED_CHOICES = (
        ('OK', 'OK'),
        ('KO', 'KO'),
    )

    id = models.AutoField(primary_key=True)
    vuuid = models.CharField(max_length=36) #change name to UUID
    name = models.CharField(max_length=30)
    cpu = models.PositiveIntegerField()
    mem = models.PositiveIntegerField() # EN MB
    VHost = models.ForeignKey(VHost)
    uptime = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES,default='PW')
    OsType = models.ForeignKey(OsType,models.SET_NULL,blank=True,null=True)
    Datastore = models.ForeignKey(Datastore, models.SET_NULL, blank=True, null=True)
    rdport = models.PositiveIntegerField(blank=True, null=True)
    rdpuser = models.CharField(max_length=15,blank=True, null=True)
    rdppass = models.CharField(max_length=50,blank=True, null=True)
    installed = models.CharField(max_length=2, choices=INSTALLED_CHOICES,default='KO')
    VSwitch = models.ForeignKey(VSwitch, models.SET_NULL, blank=True, null=True,)


    #Remote_Admin = models.ForeignKey(Remote_Admin)  #TODO


    def __str__(self):
        return self.name

class VDisk(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    VMachine = models.ForeignKey(VMachine)
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Snapshot(models.Model):

    id = models.AutoField(primary_key=True)
    suuid = models.CharField(max_length=36)
    name = models.CharField(max_length=30)
    VMachine = models.ForeignKey(VMachine)
    current = models.BooleanField(default=False)


class Remote_Admin(models.Model):

    id = models.AutoField(primary_key=True)
    VHost = models.ForeignKey(VHost)
    rdport = models.PositiveIntegerField(null=True)
    used = models.BooleanField(default=False)

# Model Logs

class Log(models.Model):

    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=255, blank=True, null=True)


'''
Borrar si no se usa

class VBOX_IFACE(models.Model): #TEST

    NAT = 'NT'
    INTNET = 'IT'
    BRIGED = 'BR'

    TYPE_CHOICES = (
        (NAT, 'Nat Network'),
        (INTNET, 'Internal Network'),
        (BRIGED, 'Bridged Network'),
    )


    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES,default=NAT)
    VMachine = models.ForeignKey(VMachine)
    driver = models.CharField(max_length=30)
    int_net = models.CharField(max_length=30, blank=True, null=True)
    phy_iface = models.CharField(max_length=7, blank=True, null=True)


class Ifaces(models.Model):  #Borrar si no usasda

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    VHost = models.ForeignKey(VHost)







'''
