#!/bin/bash

echo "( ) rabbit setup awaiting server init..."
sleep 1
rabbitmqctl await_startup
echo "rabbit setup detected server init complete"
rabbitmqctl add_user ratatosk $RABBIT_PASSWORD
rabbitmqctl set_permissions -p "/" ratatosk ".*" ".*" ".*"
rabbitmqctl delete_user guest
echo "(*) rabbit setup finished configuring auth"
