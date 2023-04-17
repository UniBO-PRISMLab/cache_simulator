
from parameters import TIME_WINDOW_SIZE, HIT_RATE


class CacheManager:
    def __init__(self, hit_rate=HIT_RATE):
        self.time_window_size = TIME_WINDOW_SIZE
        self.hit_rate = hit_rate
        return

    def epoch_passed(self, current_time):
        if current_time % self.time_window_size != 0:
            return
        return self.generate_caching_orders()

    def generate_caching_orders(self):
        pass
