#!/usr/bin/env bash

source /home/vagrant/redis-scripts/redis_vars.sh

for port in $REDIS_SENTINEL_INSTANCES; do
    PROCESS_NAME=redis_$port
    echo "======================================"
    echo "INSTALLING REDIS SERVER: $PROCESS_NAME"
    echo "======================================"

    # base config
    mkdir -p $REDIS_CONF_DIR
    cp $REDIS_BUILD_DIR/sentinel.conf $REDIS_CONF_DIR/$PROCESS_NAME.conf
    # override config values from file
    cat $VAGRANT_REDIS_CONF_DIR/redis_sentinel.conf >> $REDIS_CONF_DIR/$PROCESS_NAME.conf
    sed -i "s/PORTNUM/$port/g" $REDIS_CONF_DIR/$PROCESS_NAME.conf

    # replace placeholder variables in init.d script
    cp $VAGRANT_DIR/sentinel_init_script /etc/init.d/$PROCESS_NAME
    sed -i "s/PORTNUM/$port/g" /etc/init.d/$PROCESS_NAME
    chmod 755 /etc/init.d/$PROCESS_NAME

    # and tell update-rc.d about it
    update-rc.d $PROCESS_NAME defaults 98

    # start redis
    /etc/init.d/$PROCESS_NAME start
done

for port in $REDIS_INSTANCES_STANDALONE; do
    PROCESS_NAME=redis_$port
    echo "======================================"
    echo "INSTALLING REDIS SERVER: $PROCESS_NAME"
    echo "======================================"

    # base config
    mkdir -p $REDIS_CONF_DIR
    cp $REDIS_BUILD_DIR/redis.conf $REDIS_CONF_DIR/$PROCESS_NAME.conf
    # override config values from file
    cat $VAGRANT_REDIS_CONF_DIR/redis_standalone.conf >> $REDIS_CONF_DIR/$PROCESS_NAME.conf
    sed -i "s/PORTNUM/$port/g" $REDIS_CONF_DIR/$PROCESS_NAME.conf

    # replace placeholder variables in init.d script
    cp $VAGRANT_DIR/redis_init_script /etc/init.d/$PROCESS_NAME
    sed -i "s/PORTNUM/$port/g" /etc/init.d/$PROCESS_NAME
    chmod 755 /etc/init.d/$PROCESS_NAME

    # and tell update-rc.d about it
    update-rc.d $PROCESS_NAME defaults 98

    # start redis
    /etc/init.d/$PROCESS_NAME start
done

sleep 1
/home/vagrant/redis/bin/redis-cli -p 8001 slaveof localhost 8000
sleep 1
/home/vagrant/redis/bin/redis-cli -p 8003 slaveof localhost 8002
sleep 1
/home/vagrant/redis/bin/redis-cli -p 8005 slaveof localhost 8004

sleep 1
/home/vagrant/redis/bin/redis-cli -p 9000 sentinel monitor bucket-1 127.0.0.1 8000 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9000 sentinel monitor bucket-2 127.0.0.1 8002 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9000 sentinel monitor bucket-3 127.0.0.1 8004 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9001 sentinel monitor bucket-1 127.0.0.1 8000 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9001 sentinel monitor bucket-2 127.0.0.1 8002 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9001 sentinel monitor bucket-3 127.0.0.1 8004 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9002 sentinel monitor bucket-1 127.0.0.1 8000 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9002 sentinel monitor bucket-2 127.0.0.1 8002 2
sleep 1
/home/vagrant/redis/bin/redis-cli -p 9002 sentinel monitor bucket-3 127.0.0.1 8004 2

for port in $REDIS_INSTANCES; do
    PROCESS_NAME=redis_$port
    echo "======================================"
    echo "INSTALLING REDIS SERVER: $PROCESS_NAME"
    echo "======================================"

    # base config
    mkdir -p $REDIS_CONF_DIR
    cp $REDIS_BUILD_DIR/redis.conf $REDIS_CONF_DIR/$PROCESS_NAME.conf
    # override config values from file
    cat $VAGRANT_REDIS_CONF_DIR/redis.conf >> $REDIS_CONF_DIR/$PROCESS_NAME.conf
    sed -i "s/PORTNUM/$port/g" $REDIS_CONF_DIR/$PROCESS_NAME.conf

    # replace placeholder variables in init.d script
    cp $VAGRANT_DIR/redis_init_script /etc/init.d/$PROCESS_NAME
    sed -i "s/PORTNUM/$port/g" /etc/init.d/$PROCESS_NAME
    chmod 755 /etc/init.d/$PROCESS_NAME

    # and tell update-rc.d about it
    update-rc.d $PROCESS_NAME defaults 98

    # start redis
    /etc/init.d/$PROCESS_NAME start
done

printf 'yes\n' | redis/bin/redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005

