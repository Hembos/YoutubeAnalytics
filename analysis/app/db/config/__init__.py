from decouple import config

mongodb_ip = config('MONGODB_IP')
mongodb_port = config('MONGODB_PORT', cast=int)
database_name = config('DATABASE_NAME')

ssh_connection = config('SSH_CONNECTION')
ssh_ip = config('SSH_IP')
ssh_username = config('SSH_USERNAME')
ssh_password = config('SSH_PASSWORD')
