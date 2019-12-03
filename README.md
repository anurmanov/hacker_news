# hacker_news

Service for scrappying news from https://news.ycombinator.com/news. The service has end-point /posts/ for represent news in json format. The service is implemented via Django framework, using Django Rest Framework and deployed via Docker Compose.

Service can be installed via Linux Systemd subsystem. File setup.sh has bash script .

The source codes of the django project is located in ./web/src/hacker_news path.

Fetching mechanism is implemented in the module updater/tasks.py
End-point /posts/ is implemented in the module updater/views.py
All configs for fetching are located in the end of the module settings.py

All significant parts of the code are provided by comments.

P.S.: Docker containers postgres, web, redis works on special internal network in case of enhancement of the security of system. These containers have static ip-addresses for implementing unit test.  There is variable hn_postgres_ipv4_address in the configuration module settings.py. The value of this variable must be equal to ip address of the postgres service in the docker-compose.yml.
