import redis, json

class RedisClient:
    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        decode_responses: bool = True
    ):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=decode_responses)


    def PushToQueue(self, queue_name: str = "scan_queue", data: dict = {}):
        self.redis.lpush(queue_name, json.dumps(data))

    def PopFromQueue(self, queue_name: str = "scan_queue"):
        return self.redis.brpop(queue_name)  