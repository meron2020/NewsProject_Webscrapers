import time

from flask_app.Backend.Webscraping.QueueWorkers.workers_orchestrator import WorkersOrchestrator
from flask_app.Backend.Webscraping.News_Crawlers.CrawlersHandler import CrawlersHandler
import threading
from flask_app.Backend.Databases.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from flask_app.Backend.Webscraping.HebrewMorphologyEngine.morphology_workers_orchestrator import MorphologyWorkersOrchestrator
from googleapiclient import discovery


class WebscrapersOrchestrator:
    def run_orchestrator(self):
        compute = discovery.build('compute', 'v1')
        request = compute.instances().start(project="sonic-shuttle-322109", zone="europe-west6-a",
                                            instance="instance-1")
        request.execute()
        status = ''
        while status != "RUNNING":
            request = compute.instances().get(project="sonic-shuttle-322109", zone="europe-west6-a",
                                              instance="instance-1")
            json = request.execute()
            status = json['status']
            continue
        thread_list = []
        time.sleep(90)
        handler = DatabaseHandlerOrchestrator()
        score_thread = threading.Thread(target=handler.create_score_db)
        score_thread.start()
        cache_thread = threading.Thread(target=handler.create_cache_db)
        cache_thread.start()
        word_dict = handler.get_all_rows_from_cache()
        handler_thread = threading.Thread(target=handler.run_orchestrator, args=())
        handler_thread.start()
        morphology_workers = MorphologyWorkersOrchestrator()
        morphology_workers.run_orchestrator(3, word_dict)
        workers = WorkersOrchestrator()
        workers.run_orchestrator(3)

        crawler_handler = CrawlersHandler()
        crawler_thread = threading.Thread(target=crawler_handler.crawl_links, args=())
        crawler_thread.start()
        thread_list.append(score_thread)
        thread_list.append(cache_thread)
        thread_list.append(handler_thread)
        thread_list.append(crawler_thread)
        # [t.join() for t in thread_list]
        return thread_list


if __name__ == "__main__":
    orchestrator = WebscrapersOrchestrator()
    orchestrator.run_orchestrator()
