import threading
from flask_app.Backend.webscrapers_orchestrator import WebscrapersOrchestrator
from flask_app.Backend.Clustering.Graphs.networkx_graph import GraphConnections


class BackendOrchestrator:
    def __init__(self):
        self.webscrapers = WebscrapersOrchestrator()
        self.graph_connections = GraphConnections()

    def stop_thread(self, thread):
        thread.stop()

    def run_orchestrator(self):
        finished_graphing = False
        # graph_thread = threading.Thread(target=self.graph_connections.run_clustering, args=())
        # graph_thread.start()
        thread_list = self.webscrapers.run_orchestrator()
        graph_thread = threading.Thread(target=self.graph_connections.start_consumption, args=())
        graph_thread.start()
        thread_list.append(graph_thread)
        [t.join() for t in thread_list]
        return


orchestrator = BackendOrchestrator()
orchestrator.run_orchestrator()
