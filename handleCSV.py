import csv

def read_csv():
    alerts = []
    with open('alerts.csv',encoding='utf-8') as file:
        rows = csv.reader(file,delimiter=',')
        for row in rows:
            alerts.append({'title':row[0],'text':row[1],'time':row[2]})
    return alerts[1:]

def write_csv(data):
    #title,text,time
    with open('alerts.csv','w',encoding='utf-8') as file:
        fieldnames = ['title','text','time']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writerows(data)

