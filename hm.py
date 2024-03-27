import random, requests, time
people_to_join = list(range(15))

while people_to_join:
    user_id = random.choice(people_to_join)
    r= requests.post("http://localhost:5004/queue",json= {
        "eid": 1,
        "uid": user_id+1
    })
    print(f"added user {user_id} to queue")
    time.sleep(1)

    if r.status_code not in range(200,300):
        print(r.text)
        break

    people_to_join.remove(user_id)


input("Check got 15 people for event 1 or not")


