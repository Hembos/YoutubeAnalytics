import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.youtube

scraper_collection = database.scraper_requests
collection_videos = database.videos
collection_channels = database.channels
