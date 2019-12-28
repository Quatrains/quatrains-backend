# quatrains-backend

---
## 生产环境 启动说明
本服务期望运行在docker容器环境中，请提前装好docker环境

### 1.拉取镜像
```
docker pull mysql:5.7
docker pull quatrains/quatrains_bk:[最新tag]
```

### 2.创建network
```
docker network create quatrains_net
```


### 3.启动mysql（数据持久化到docker宿主机）
```
docker run -d \
--net=quatrains_net \
--name mysql \
-e MYSQL_ROOT_PASSWORD=root_quatrains \
-v /var/container_data/mysql:/var/lib/mysql \
--restart=always mysql:5.7
```

### 4.创建数据库
```
docker exec -it mysql bash
mysql -uroot -proot_quatrains
create database quatrains character set utf8mb4 collate utf8mb4_unicode_ci;
exit
exit
```

### 5.启动flask
```
docker run -d \
--net=quatrains_net \
--link=mysql:mysql \
-e APP_SECRET='THE_APP_SECRET' \
-e APP_ID='THE_APP_ID' \
-e FLASK_ENV='production' \
-p 8888:5000 \
--name quatrains quatrains/quatrains_bk:[最新tag]
```

### 6.访问api
```
- 自动创建数据:
    http://127.0.0.1:8888/auto_create_data

- api文档:
    http://127.0.0.1:8888/apidocs
```
