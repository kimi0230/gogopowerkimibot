# Fly.io
https://fly.io/

## install
**MAC**
```
brew install flyctl
```

## singup login
```sh
flyctl auth signup
flyctl auth login
```

##
```sh
flyctl launch
flyctl deploy 
flyctl ssh console 
fly status --all
```

## Postgre
```sh
flyctl postgres create
flyctl postgres db list gogopowerkimi -a gogopowerkimibot-db
```

```sh
CREATE DATABASE name
\+
```

## Redis
```sh
flyctl redis create 
flyctl redis list
flyctl redis status gogopowerkimi-redis
fly redis connect
fly redis delete {ID}
```

## Secrets
```sh
flyctl secrets import < .env.flyio
```

## 
* https://rajasimon.io/blog/deploy-django-flyio/
* https://fly.io/docs/reference/redis/