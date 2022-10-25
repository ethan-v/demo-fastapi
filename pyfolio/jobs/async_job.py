from asyncio import tasks

from celery import Task

class Hello(Task):
    queue = 'hipri'

    def run(self, to):
        return 'hello {0}'.format(to)


tasks.register(Hello)
