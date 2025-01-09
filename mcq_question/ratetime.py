import datetime
class RateLimit:
    def _init_(self):
        self.requests = deque()
        self.window = 60  # seconds
        self.token_limit = 6000

    def check_limit(self, tokens):
        now = datetime.now()
        while self.requests and (now - self.requests[0][0]).total_seconds() > self.window:
            self.requests.popleft()

        current_tokens = sum(r[1] for r in self.requests)
        return current_tokens + tokens <= self.token_limit

    def add_request(self, tokens):
        self.requests.append((datetime.now(), tokens))