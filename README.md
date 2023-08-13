# 使用 Docker Compose 部署 Telegram Bot

本仓库包含了使用 Docker Compose 部署 `tg-bot` 的设置。

## 前提条件

在开始之前，请确保您的系统已安装以下内容：

- Docker：https://docs.docker.com/get-docker/
- Docker Compose：https://docs.docker.com/compose/install/

## 入门指南

1. 克隆此仓库：

    ```bash
    git clone https://github.com/your-username/tg-bot.git
    cd tg-bot
    ```

2. 编辑 `docker-compose.yml` 文件并在 `environment` 部分中配置 `MYSQL_URL` 地址：
    ```yaml
    services:
      db:
        image: mysql:latest
        environment:
          MYSQL_URL: "mysql://user:password@hostname:port/database"
    ```
   
3. 使用 Docker Compose 部署 Telegram Bot：

    ```bash
    docker-compose up -d --build
    ```

4. 您的 Telegram Bot 现已部署并运行！您可以检查日志以查看是否有任何问题：

    ```bash
    docker-compose logs -f
    ```
## 后台入口

您可以使用以下地址访问管理后台：
```url
http://your-server-ip:port/login.html
```

## 使用方法

要与您部署的 Telegram Bot 进行交互，请在 Telegram 应用中打开对话并开始发送消息。

## 清理

要停止并移除部署的容器：

```bash
docker-compose down
```

