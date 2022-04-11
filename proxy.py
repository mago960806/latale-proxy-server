import configparser
import sys

from proxy.server import start_proxy

from loguru import logger

# LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {thread.name} | {message}"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

logger.remove()
logger.add(
    sys.stdout,
    format=LOG_FORMAT,
    enqueue=True,
)
logger.add(
    "proxy.log",
    format=LOG_FORMAT,
    enqueue=True,
)


if __name__ == "__main__":
    # 初始化配置
    config = configparser.ConfigParser()
    config.read("proxy.ini", encoding="utf-8")

    # 讀取配置
    port = int(config["LaTaleProxyServer"]["ListenPort"])

    logger.info("Server Init...")
    start_proxy("", port)

    # try:
    #     with ThreadingTCPServer((host, port), Socks5Proxy) as server:
    #         print(f"[+] Listening on port: {host}:{port}")
    #         server.serve_forever()
    # except KeyboardInterrupt:
    #     print("[*] KeyboardInterrupt detected, proxy server will shutdown..")
    #     server.shutdown()
