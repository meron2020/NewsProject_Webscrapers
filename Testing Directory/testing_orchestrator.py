import threading

from flask_app.Backend.Webscraping.HebrewMorphologyEngine.morphology_workers_orchestrator import MorphologyWorkersOrchestrator
from flask_app.Backend.Webscraping.QueueWorkers.workers_orchestrator import WorkersOrchestrator
from flask_app.Backend.Databases.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from testing_urls_file import TestingUrlsSender


class TestingOrchestrator:
    def run_orchestrator(self):
        handler = DatabaseHandlerOrchestrator()
        score_thread = threading.Thread(target=handler.create_score_db)
        score_thread.start()
        cache_thread = threading.Thread(target=handler.create_cache_db)
        cache_thread.start()
        word_dict = handler.get_all_rows_from_cache()
        handler_thread = threading.Thread(target=handler.run_orchestrator)
        handler_thread.start()
        morphology_workers = MorphologyWorkersOrchestrator()
        morphology_workers.run_orchestrator(1, word_dict)
        workers = WorkersOrchestrator()
        workers.run_orchestrator(1)
        TestingUrlsSender.send_urls()


orchestrator = TestingOrchestrator()
orchestrator.run_orchestrator()
