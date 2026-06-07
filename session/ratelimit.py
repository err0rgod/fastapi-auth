# redis based rate limitter
import time

class RateLimiter:
    def __init__(self, storage_client , max_requests: int =10, window : int  =60):
        self.storage =  storage_client
        self.maxRequests = max_requests
        self.window = window

    def check_limit(self, identifier : str, action : str = "login"):
        key = f"ratelimit:{action}:{identifier}"

        count = self.storage.incr(key)

        if count == 1:
            self.storage.expire(key, self.window)
        if count > self.maxRequests:
            raise ValueError(f"Rate limit exceeded. Try aagain in {self.window} seconds")
        return count