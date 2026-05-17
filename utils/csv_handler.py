import csv
import time

def read_csv():
    alerts = []
    with open('utils/alerts.csv',encoding='utf-8') as file:
        rows = csv.reader(file,delimiter=',')
        for row in rows:
            if not row:
                break
            alerts.append({'id':row[0],'title':row[1],'text':row[2],'time':row[3],'level':row[4]})
    return alerts[1:]

def write_csv(data):
    with open('utils/alerts.csv','w',encoding='utf-8',newline='') as file:
        fieldnames = ['id','title','text','time','level']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def delete_row(id):
    rows = read_csv()
    new_rows = []
    for row in rows:
        #id es string, no es un numero
        if(row['id'] != id):
            new_rows.append(row)
    write_csv(new_rows)

def insert_row(reason):
        alerts = read_csv()
        now = time.localtime()
        if reason == 'Cara desconocida':
            data = {'id':int(alerts[0]['id']) + 1,
                    'title':reason,
                    'text':'Se detecto una persona no identificada en el vehiculo, se guardo una fotografia de su rostro en la galeria de fotos tomadas.',
                    'time':f'{now.tm_hour}:{now.tm_min}:{now.tm_sec}',
                    'level':2}
        if reason == 'Movimiento extraño detectado':
            data = {'id':int(alerts[0]['id']) + 1,
                    'title':reason,
                    'text':'Se detecto movimiento constante en el vehiculo, y se guardo una fotografia en la galeria de fotos tomadas.',
                    'time':f'{now.tm_hour}:{now.tm_min}:{now.tm_sec}',
                    'level':2}
        alerts.insert(0,data)
        write_csv(alerts)