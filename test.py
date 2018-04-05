import datetime

snaps = []

snaps.append({'id': '1', 'fecha': datetime.datetime.now() + datetime.timedelta(days=4)})
snaps.append({'id': '2', 'fecha': datetime.datetime.now() + datetime.timedelta(days=1)})
snaps.append({'id': '3', 'fecha': datetime.datetime.now() + datetime.timedelta(days=9)})
snaps.append({'id': '4', 'fecha': datetime.datetime.now() + datetime.timedelta(days=4)})
snaps.append({'id': '5', 'fecha': datetime.datetime.now() + datetime.timedelta(days=2)})
snaps.append({'id': '6', 'fecha': datetime.datetime.now() + datetime.timedelta(days=8)})
snaps.append({'id': '7', 'fecha': datetime.datetime.now() + datetime.timedelta(days=-5)})
snaps.append({'id': '8', 'fecha': datetime.datetime.now() + datetime.timedelta(days=3)})


# for s in snaps:
#     print(s['fecha'].strftime("%d-%m-%Y"))

ordered = sorted(snaps, key=lambda k: k['fecha'], reverse=True)

for s in ordered:
    print(s['fecha'].strftime("%d-%m-%Y"))

if(len(ordered) > 6):
    print("hay que borrar")
    for s in ordered[6: len(snaps)]:
        print("voy a borrar esta -> "+s['id']+ " - " + s['fecha'].strftime("%d-%m-%Y"))
else:
    print("no tenemos demasiadas")
        


