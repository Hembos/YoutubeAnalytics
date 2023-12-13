import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo_db/youtube')

database = client.youtube

requests_collection = database.scraper_requests
collection_videos = database.videos
collection_channels = database.channels
collection_analysis = database.analysis
