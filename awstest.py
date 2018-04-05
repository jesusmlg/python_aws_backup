import boto3
import time


def deleteOldSnapshots(snapshots):
    limit = 1
    total = 0
    snaps = []

    for s in snapshots:
        snaps.append({'id': s.id, 'start_time': s.start_time})
        print("           "+s.id + " - " + s.start_time.strftime("%d-%m-%Y %H:%M"))
        
    snaps = sorted(snaps, key=lambda k: k['start_time'], reverse = True)
     
    total = len(snaps)

    if(total > limit):
        print("           Hay que borrar " + str(total-limit))
        for s in snaps[limit:total]:
            print("                      "+s['id'] + " - " + s['start_time'].strftime("%d-%m-%Y %H:%M"))
    else:
        print("           Nada que eliminar")


def getSnapshotOfVolume(instance_id):
    volume = ec2.volumes.filter()


servers = ["SRV_CITRIX01", "SRV_CITRIX02", "SRV_CITRIX03", "SRV_CITRIX04" ]

ec2 = boto3.resource('ec2')
#instance = ec2.Instance('i-008e0533073e4e73a')

instances = ec2.instances.all()

for i in instances:
    #print(i.id + " - "+ i.tags[0]['Value'] +" - " + i.state['Name'])
    name = i.tags[0] ['Value']
    if(name in servers):
        print(name + " - " + i.state['Name'] + " - ")
        for v in i.volumes.all():
            print("           Volumen ------------> "+v.id)
            print("           Total de Snaps: " + str(sum(1 for _ in v.snapshots.all())))
            deleteOldSnapshots(v.snapshots.all())





    




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

