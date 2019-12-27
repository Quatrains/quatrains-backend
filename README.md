# quatrains-backend

---
## 生产环境 启动说明
本服务期望运行在docker容器环境中，请提前装好docker环境

### 1.拉取镜像
```
docker pull quatrains/mysql
docker pull quatrains/quatrains_bk
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
--restart=always quatrains/mysql
```

### 4.启动flask
```
docker run -d \
--net=quatrains_net \
--link=mysql:mysql \
-e APP_SECRET='THE_APP_SECRET' \
-e APP_ID='THE_APP_ID' \
-e FLASK_ENV='production' \
-p 8888:5000 \
--name quatrains quatrains/quatrains_bk
```
