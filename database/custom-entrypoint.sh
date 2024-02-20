#!/bin/bash
set -e

# Start MySQL server in the background
/usr/local/bin/docker-entrypoint.sh mysqld &
MYSQL_PID=$!

# Wait for MySQL to start
echo "Waiting for MySQL to start..."
sleep 10

# Set innodb_fast_shutdown to 0
mysql -uroot -e "SET GLOBAL innodb_fast_shutdown = 0;"

# Wait for MySQL process to finish
wait $MYSQL_PID
