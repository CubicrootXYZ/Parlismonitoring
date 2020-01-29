import redis

conn = redis.Redis()

conn.set("hello", "world")

print(conn.get('hallo'))