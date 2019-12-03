#!bin/bash
cp /tmp/postgresql.conf /var/lib/postgresql/data
cp /tmp/pg_hba.conf /var/lib/postgresql/data
cd /docker-entrypoint-initdb.d
psql -c "create database hacker_news" postgres
psql -c "create database test_hacker_news" postgres
