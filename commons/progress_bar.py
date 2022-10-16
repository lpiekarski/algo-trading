import logging
import time
import numpy as np

LOGGER = logging.getLogger(__name__)

class ProgressBar:
    def __init__(self, num_updates, bar_length=50):
        self.count = 0
        self.length = num_updates
        self.bar_length = bar_length
        self.last_completed_num = None
        self.first_update_time = None

    def update(self, count=1):
        if self.first_update_time is None:
            self.first_update_time = time.time()
        self.count += count
        completed_percent = self.count / self.length
        completed_num = int(np.ceil(self.bar_length * completed_percent))
        remaining_num = int(np.floor(self.bar_length * (1 - completed_percent)))
        if self.last_completed_num != completed_num or self.count == self.length:
            self.last_completed_num = completed_num
            elapsed = time.time() - self.first_update_time
            estimated = elapsed / completed_percent * (1 - completed_percent)
            LOGGER.info(f"|{completed_num * '='}{remaining_num * '-'}| {100 * completed_percent:.2f}%, Estimated: {estimated:.2f} seconds left")