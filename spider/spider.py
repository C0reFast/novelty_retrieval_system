import Queue
import threading
import requests


class Request(object):
    """Url Request"""
    def __init__(self, url, parser=None):
        super(Request, self).__init__()
        self.url = url
        self.parser = parser


class BaseSpider(object):
    """Base class for spiders"""
    def __init__(self, thread_number=8, fetcher=None):
        super(BaseSpider, self).__init__()
        self.queue = Queue.Queue(maxsize=0)
        self.thread_pool = []
        self.thread_number = thread_number
        self.fetcher = fetcher or (lambda url: (requests.get(url).text))

    def parser(self, req):
        if req.parser:
            result = req.parser(req.url, self.fetcher(req.url))
            if result:
                for res in result:
                    if isinstance(res, Request):
                        self.queue.put(res)

    def work(self):
        while True:
            req = self.queue.get()
            self.parser(req)
            self.queue.task_done()

    def crawl(self, seed_requests):
        for req in seed_requests:
            self.queue.put(req)
        for _ in xrange(self.thread_number):
            thread = threading.Thread(target=self.work)
            thread.setDaemon(True)
            self.thread_pool.append(thread)
            thread.start()
        self.queue.join()
