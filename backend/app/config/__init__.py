from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv("backend/.env "))

youtube_api_keys = config('YOUTUBE_API_KEY').strip('][').split(', ')
youtube_api_keys = dict.fromkeys(youtube_api_keys, 10000)

mongodb_url = config('MONGODB_URL')

database_name = config('DATABASE_NAME')
