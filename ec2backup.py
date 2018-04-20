import boto3
import time
import datetime
import os

if not(os.path.exists('logs')):
    os.makedirs('logs')
log = open('logs/aws_backup_' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), 'w')

def output(t):
    print(t)
    log.write(t+"\r\n")

def deleteOldSnapshots(snapshots):
    limit = 7
    total = 0
    snaps = []

    for s in snapshots:
        snaps.append({'id': s.id, 'start_time': s.start_time})
        #output("\t"+s.id + " - " + s.start_time.strftime("%d-%m-%Y %H:%M"))
        
    snaps = sorted(snaps, key=lambda k: k['start_time'], reverse = True)

    total = len(snaps)

    if(total > limit):
        output("\tHay que borrar " + str(total-limit))
        for s in snaps[limit:total]:            
            output("\t\tSnapshot: " + s['id'] + " - " + s['start_time'].strftime("%d-%m-%Y %H:%M"))
            amis = ec2.images.filter(Filters=[{'Name': 'block-device-mapping.snapshot-id', 'Values': [s['id']]}]).limit(1)
            #print(str(amis))
            for ami in amis:
                output("\t\tAmi: " + ami.id + " - " + ami.creation_date)
                #ami.deregister()
                output("\t\tEsperando para eliminar snap")
                time.sleep(15)                
                #ec2.Snapshot(s['id']).delete()
            # output("\t\t" + res)
    else:
        output("\tNada que eliminar")


output("--------- COMIENZO - " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M")+"---------")
servers = ["NODO1", "SRV_CITRIX01", "SRV_CITRIX02", "SRV_CITRIX03", "SRV_CITRIX04",
           "SRV_CITRIX05", "SRV_CITRIX06", "SRV_CITRIX07", "SRV_CITRIX08", "SRV_CITRIX09", "SRV_PERFILES", "FTP", "DCAWS", "META4", "WEBSERVER"]
#servers = ["SRV_CITRIX02"]

ec2 = boto3.resource('ec2')


instances = ec2.instances.all()

for i in instances:    
    try:
        instanceName = i.tags[0]['Value']
        #Solo realizo copias de las intancias que esten en el array
        if(instanceName in servers):
            output(instanceName + " - " + i.state['Name'] + " - ")
            
            #Creamos la imagen para la copia de seguridad
            fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            description = "Copia de seguridad de la maquina " + \
                instanceName + " del dia " + fecha
            backupName = "BAK_" + instanceName + "_" + fecha

            output("\tCreando imagen ...")
            image = i.create_image(
                Description=description, NoReboot=True, Name=backupName, DryRun=False)
            image.wait_until_exists()
            time.sleep(2)
            
            #busco la snap asociada al volumen para ponerle la etiqueta con el nombre
            snapshot_id = image.block_device_mappings[0]['Ebs']['SnapshotId']
            if(snapshot_id != ""):
                #Las marco con la etiqueta para luego en la limpieza solo borrar las DBACKUP
                snapshot = ec2.Snapshot(snapshot_id)
                snapshot.create_tags(
                    Tags=[{'Key': 'Name', 'Value': backupName},{'Key': 'Type' , 'Value' : 'DBACKUP'}])
                image.create_tags(
                    Tags=[{'Key': 'Name', 'Value': backupName}, {'Key': 'Type', 'Value': 'DBACKUP'}])

            for v in i.volumes.all():
                snapshots = v.snapshots.filter(Filters =[{ 'Name':'tag:Type', 'Values':['DBACKUP'] }])
                output("\tVolumen ------------> "+v.id)
                output("\tTotal de Snaps: " + str(sum(1 for _ in snapshots)))
                output("\tTotal AMIs: " + str(sum(1 for _ in ec2.images.filter(
                    Filters=[{'Name': 'name', 'Values': ['*'+instanceName+'*']}, {'Name': 'tag:Type', 'Values': ['DBACKUP']} ]))))
                #Borramos la/s ami/s antigua/s y sus respectivas snapshot/s
                
                deleteOldSnapshots(snapshots)
            print("Esperando ...")

            time.sleep(120)
    except Exception:
        output("Error en la copia de la instancia: "+i.id)
    

output("--------- FIN - "+datetime.datetime.now().strftime(" %d-%m-%Y %H:%M") +"---------")





    




#image = instance.create_image(Description="Test from python10", NoReboot=True, Name="NameTestFromPython10", DryRun = False)
#image_id = ec2.create_image(Description="Test from python",NoReboot=True,Name="NameTestFromPython",InstanceID="i-008e0533073e4e73a", DryRun=False)
# print(image.id)
# images = ec2.images.filter(Owners=['self'])
# print("Comienza la Espera")
# waiter = image.wait_until_exists()
#while(image.state == "pending"):
#    print(image.name + " - " + image.state)
#    time.sleep(5)
#    image = ec2.Image(image.id)

# print(image.state)
# print(waiter)

