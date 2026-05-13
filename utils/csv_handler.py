import csv

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