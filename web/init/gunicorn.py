accesslog='/var/log/gunicorn/access.log'
errorlog='/var/log/gunicorn/error.log'
loglevel='debug'
bind='unix:/var/www/hacker_news/gunicorn.sock'
backlog=1000
workers=2
timeout=30
keepalive=7

