import requests
import json


def get_tickets(deport='45'):
    lpu = None
    resault = []
    heraders = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': 'Mozilla / 5.0(X11;Ubuntu;Linuxx86_64;rv: 106.0)Gecko/20100101Firefox / 106.0'
    }
    url = f'https://uslugi.mosreg.ru/zdrav/doctor_appointment/api/doctors?lpuCode=&departmentId={deport}&doctorId=&days=14'
    data = requests.get(url=url, headers=heraders)
    json_data = json.loads(data.text)
    items = json_data.get('items')

    # находим по коду, поликлинику в Мытищах
    for i in items:
        if i.get('lpu_code') == '2801011':
            lpu = i
    # берем всех врачей из поликлиники пишем их именна и количество билетовtest
    doctors = lpu.get('doctors')
    for doctor in doctors:
        resault.append({
            'name': doctor.get('displayName'),
            'family': doctor.get('family'),
            'room': doctor.get('room'),
            'count_tickets': doctor.get('count_tickets'),
        })

    return resault


if __name__ == '__main__':
    get_tickets()
