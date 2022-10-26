from redis import StrictRedis
import pymongo

redis_db = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
mongo_db = pymongo.MongoClient("localhost", 27017)['anychat']