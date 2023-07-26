# My-Expenses
Easy and completely automatically control your expenses and track your SMS messages using iOS 17 and a python webserver.

## How to use

### Environment variables

| Variable | Description |
| --- | --- |
| DB_HOST | The host of the database |
| DB_PORT | The port of the database |
| DB_USERNAME | The username of the database |
| DB_PASSWORD | The password of the database |
| DB_DATABASE | The name of the database |
| DB_TABLE_NAME | The name of the table |

### Kubernetes
1. Install kubernetes and kubectl
2. Clone this repository
3. Fill the environment variables in the kubernetes.yml
4. Run `kubectl apply -f kubernetes.yml` in the root directory of this repository

### Docker
1. Install docker and docker-compose
2. Clone this repository
3. Fill the environment variables in the docker-compose.yml
4. Run `docker compose up -d ` in the root directory of this repository

### Python
1. Install python3
2. Setup a mariadb/mysql database
3. Clone this repository
4. Install the requirements with `pip install -r requirements.txt`
5. Fill the environment variables
6. Run `python3 main.py` in the root directory of this repository

### iOS:
1. Install the [Shortcuts App](https://apps.apple.com/us/app/shortcuts/id915249334)
2. Coming Soon: Download the Shortcut
3. Create an automation that runs the shortcut when you receive a message from your bank
4. Done!
