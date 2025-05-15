from faker import Faker
import json
     

fake = Faker()
users = []

for _ in range(1000):
    user = {
        "id": fake.random_int(),
        "name": fake.name(),
        "age": fake.random_int(18, 65),
        "email": fake.email(),
        "is_active": fake.boolean(),
        "registration_date": str(fake.date_this_decade()),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "zipcode": fake.zipcode()
        },
        "orders": []
    }
    users.append(user)


with open('data.json', 'w') as f:
    json.dump({"users": users}, f, indent=2)
