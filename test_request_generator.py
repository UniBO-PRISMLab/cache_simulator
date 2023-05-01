# 1. Initialize users
from models.provider import Provider
from models.request_generator import RequestGenerator
from models.user import User
from parameters import NUMBER_OF_PROVIDERS, NUMBER_OF_USERS


users = [User(i) for i in range(NUMBER_OF_USERS)]

# 2. Create providers
providers = [Provider(i) for i in range(NUMBER_OF_PROVIDERS)]


# 3. Assign requests to providers to each users (according to user category) for the experiment duration
request_generator = RequestGenerator(users, providers)
users = request_generator.users
for user in users:
    if(all(user.requests[i].execution_time <= user.requests[i + 1].execution_time for i in range(len(user.requests)-1))):
        print("list sorted")

