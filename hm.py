import random, requests, time
people_to_join = list(range(15))

while people_to_join:
    user_id = random.choice(people_to_join)
    r= requests.post(f"http://localhost:5100/queue/event/1/user/{user_id+1}/join")
    print(f"added user {user_id} to queue")
    time.sleep(1)

    if r.status_code not in range(200,300):
        print(r.text)
        break

    people_to_join.remove(user_id)


input("Check got 15 people for event 1 or not")


