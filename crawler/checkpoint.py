import pickle
import logger
import os.path
import multiprocessing as mp
import sys


class Checkpoint():
    def __init__(self, location, db_location):
        self.location = location
        self.db_location = db_location

    def urls_seen_checkpoint(self):
        print('[i] Backtracking to last url_seen...')
        log = logger.Logger(self.db_location + '/url_seen')
        seen = set()
        for row in log.fetch_all_seen():
            seen.add(row[1])
        return seen

    def store(self, list_to_save, filename):
        with open(self.location + filename, mode='wb') as f:
            pickle.dump(list_to_save, f)
        return

    def recover(self, filename):
        if os.path.isfile(self.location + filename) and os.path.getsize(self.location + filename) > 0:
            with open(self.location + filename, mode='rb') as f:
                return pickle.load(f)
        else:
            return []
