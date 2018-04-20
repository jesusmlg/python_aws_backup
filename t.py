import boto3

ec2 = boto3.resource('ec2')

v = ec2.Volume('vol-08ca7f43ae64ca5a8')

for s in v.snapshots.filter(Filters=[{'Name': 'tag:Type', 'Values': ['DBACKUP']}]) :
    print(s.id)
