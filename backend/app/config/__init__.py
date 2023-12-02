from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv(r"YoutubeAnalytics\backend\.env"))

mongodb_ip = config('MONGODB_IP')
mongodb_port = config('MONGODB_PORT', cast=int)
database_name = config('DATABASE_NAME')

ssh_connection = config('SSH_CONNECTION')
ssh_ip = config('SSH_IP')
ssh_username = config('SSH_USERNAME')
ssh_password = config('SSH_PASSWORD')


# youtube_api_keys = config('YOUTUBE_API_KEY').strip('][').split(', ')
# youtube_api_keys = dict.fromkeys(youtube_api_keys, 10000)

# mongodb_url = config('MONGODB_URL')

# database_name = config('DATABASE_NAME')