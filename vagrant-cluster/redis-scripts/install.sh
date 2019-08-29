#!/usr/bin/env bash

yum install git gcc memkind-devel tcl vim -y

wget https://github.com/antirez/redis/archive/5.0.5.tar.gz
tar xf 5.0.5.tar.gz
mv redis-5.0.5 redis

cd redis

make

mkdir /etc/redis

cp src/redis-server /usr/bin/
cp src/redis-sentinel /usr/bin/
cp src/redis-cli /usr/bin/
cp redis.conf /etc/redis/
cp sentinel.conf /etc/redis/


cp /home/vagrant/redis-scripts/redis-shutdown /usr/libexec/
cp /home/vagrant/redis-scripts/redis_sentinel@.service /etc/systemd/system/
cp /home/vagrant/redis-scripts/redis@.service /etc/systemd/system/

cd /etc/redis


useradd redis
mkdir -p /var/lib/redis
mkdir -p /var/log/redis

chown redis: /var/lib/redis
chown redis: /var/log/redis

sed -i 's/protected-mode yes/protected-mode no/g' redis.conf
sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' redis.conf

sed -i 's/protected-mode yes/protected-mode no/g' sentinel.conf
sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' sentinel.conf

function redis_instance {
 name=$1
 port=$2
 cluster=$3
    mkdir -p /var/lib/redis/${name}
    chown redis: /var/lib/redis/${name}
    cp redis.conf redis_${name}.conf
    chown redis: redis_${name}.conf
    sed -i "s/port 6379/port ${port}/g" redis_${name}.conf
    sed -i "s/supervised no/supervised auto/g" redis_${name}.conf
    sed -i "s/pidfile \/var\/run\/redis_6379.pid/pidfile \/var\/run\/redis_${name}.pid/g" redis_${name}.conf
    echo 'maxmemory 64mb' >> redis_${name}.conf
    echo "logfile /var/log/redis/${name}.log" >> redis_${name}.conf
    echo "dir /var/lib/redis/${name}" >> redis_${name}.conf
    echo "requirepass P4ssW0rd" >> redis_${name}.conf
    echo "masterauth P4ssW0rd" >> redis_${name}.conf
    if [[ "${cluster}" = "yes" ]]
    then
        echo "cluster-enabled yes"  >> redis_${name}.conf
    fi
    systemctl enable redis@${name}
    systemctl start redis@${name}
}

function sentinel_instance {
 name=$1
 port=$2
    mkdir -p /var/lib/redis/${name}
    chown redis: /var/lib/redis/${name}
    cp sentinel.conf sentinel_${name}.conf
    chown redis: sentinel_${name}.conf
    sed -i "s/port 26379/port ${port}/g" sentinel_${name}.conf
    sed -i "s/pidfile \/var\/run\/redis-sentinel.pid/pidfile \/var\/run\/redis_${name}.pid/g" sentinel_${name}.conf
    echo "logfile /var/log/redis/${name}.log" >> sentinel_${name}.conf
    systemctl enable redis_sentinel@${name}
    systemctl start redis_sentinel@${name}
}

for i in 0 1 2
do
    name=sentinel${i}
    port=400${i}
    sentinel_instance ${name} ${port}
done

sleep 2

redis-cli -p 4000 sentinel remove mymaster
redis-cli -p 4001 sentinel remove mymaster
redis-cli -p 4002 sentinel remove mymaster

for i in 0 1 2
do
    name=standalone${i}
    port=500${i}
    redis_instance ${name} ${port}
done

sleep 2

redis-cli -p 5001 slaveof localhost 5000
redis-cli -p 5002 slaveof localhost 5000

redis-cli -p 4000 sentinel monitor standalone 127.0.0.1 5000 2
redis-cli -p 4000 sentinel auth-pass standalone P4ssW0rd
redis-cli -p 4001 sentinel monitor standalone 127.0.0.1 5000 2
redis-cli -p 4001 sentinel auth-pass standalone P4ssW0rd
redis-cli -p 4002 sentinel monitor standalone 127.0.0.1 5000 2
redis-cli -p 4002 sentinel auth-pass standalone P4ssW0rd

for i in 0 1 2
do
    for j in 0 1
    do
      name=bucket${i}_replica${j}
      port=60${i}${j}
      redis_instance ${name} ${port}
    done
done

sleep 2

redis-cli -p 6001 slaveof localhost 6000

redis-cli -p 6011 slaveof localhost 6020

redis-cli -p 6021 slaveof localhost 6020

redis-cli -p 4000 sentinel monitor bucket0 127.0.0.1 6000 2
redis-cli -p 4000 sentinel auth-pass bucket0 P4ssW0rd
redis-cli -p 4000 sentinel monitor bucket1 127.0.0.1 6010 2
redis-cli -p 4000 sentinel auth-pass bucket1 P4ssW0rd
redis-cli -p 4000 sentinel monitor bucket2 127.0.0.1 6020 2
redis-cli -p 4000 sentinel auth-pass bucket2 P4ssW0rd

redis-cli -p 4001 sentinel monitor bucket0 127.0.0.1 6000 2
redis-cli -p 4001 sentinel auth-pass bucket0 P4ssW0rd
redis-cli -p 4001 sentinel monitor bucket1 127.0.0.1 6010 2
redis-cli -p 4001 sentinel auth-pass bucket1 P4ssW0rd
redis-cli -p 4001 sentinel monitor bucket2 127.0.0.1 6020 2
redis-cli -p 4001 sentinel auth-pass bucket2 P4ssW0rd

redis-cli -p 4002 sentinel monitor bucket0 127.0.0.1 6000 2
redis-cli -p 4002 sentinel auth-pass bucket0 P4ssW0rd
redis-cli -p 4002 sentinel monitor bucket1 127.0.0.1 6010 2
redis-cli -p 4002 sentinel auth-pass bucket1 P4ssW0rd
redis-cli -p 4002 sentinel monitor bucket2 127.0.0.1 6020 2
redis-cli -p 4002 sentinel auth-pass bucket2 P4ssW0rd

for i in 0 1 2
do
    for j in 0 1
    do
      name=cluster${i}_replica${j}
      port=70${i}${j}
      redis_instance ${name} ${port} yes
    done
done

sleep 2

printf 'yes\n' | redis-cli -a P4ssW0rd --cluster-replicas 1 --cluster create  127.0.0.1:7000 127.0.0.1:7010 127.0.0.1:7020 127.0.0.1:7001 127.0.0.1:7011 127.0.0.1:7021
