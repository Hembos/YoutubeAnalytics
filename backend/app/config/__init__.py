from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv("backend/.env "))

youtube_api_keys = config('YOUTUBE_API_KEY').strip('][').split(', ')
