import threading
from flask_app.Backend.Webscraping.HebrewMorphologyEngine.morphology_engine_worker import MorphologyEngineWorker


class MorphologyWorkersOrchestrator:
    @classmethod
    def worker_func(cls, worker):
        worker.start_consumption()

    def run_orchestrator(self, num_workers, word_dict):
        worker_list = []

        for i in range(num_workers):
            worker_list.append(MorphologyEngineWorker(word_dict))

        worker_threads = list()
        for worker in worker_list:
            x = threading.Thread(target=self.worker_func, args=(worker,))
            worker_threads.append(x)
            x.start()
