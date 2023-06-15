from __future__ import absolute_import, unicode_literals

from celery import Celery

from apps.instagram.scrape import web_scraping

app = Celery("tasks", broker="redis://localhost:6379/0")


@app.task
def scrape_instagram():
    print("\nbegin\n")
    web_scraping()
    print("\nend\n")
