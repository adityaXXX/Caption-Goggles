import meetup.api
key = '39742216187936612d1055305074549'


def grouping(name):
    client = meetup.api.Client(key)

    name = name.replace(" ","-")
    group_info = client.GetGroup({'urlname': name})

    result = {
        'Name': group_info.name,
        'Organizer': group_info.organizer['name'],
        'City': group_info.city,
        'Upcoming Event': {
            'Event Name': group_info.next_event['name'],
            'RSVP': group_info.next_event['yes_rsvp_count'],
            'Time': group_info.next_event['time']
        },
        'Link': group_info.link
    }
    return result

#x = "GDG Ranchi"
#zz = grouping(x)
#print(zz["Upcoming Event"]["RSVP"])