import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.youtube

requests_collection = database.scraper_requests
collection_videos = database.videos
collection_channels = database.channels
collection_analysis = database.analysis
