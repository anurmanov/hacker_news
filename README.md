# hacker_news

Service for scrappying news from https://news.ycombinator.com/news. The service has end-point /posts/ for represent news in json fromat. The service is implemented via Django framework, using Django Rest Framework and deployed via Docker Compose.

Service can be installed via Linux Systemd subsystem. File setup.sh has bash script .

Fetching mechanism is implemented in the module updater/tasks.py
End-point /posts/ is implemented in the module /updater/views.py

All significant parts of the code are provided by comments.
