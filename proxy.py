import sys

from proxy import start_proxy

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {thread.name} | {message}",
    enqueue=True,
)
logger.add(
    "proxy.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {thread.name} | {message}",
    enqueue=True,
)


if __name__ == "__main__":
    host = "192.168.31.100"
    port = 2233

    logger.info("Server Init...")
    start_proxy(host, port)

    # try:
    #     with ThreadingTCPServer((host, port), Socks5Proxy) as server:
    #         print(f"[+] Listening on port: {host}:{port}")
    #         server.serve_forever()
    # except KeyboardInterrupt:
    #     print("[*] KeyboardInterrupt detected, proxy server will shutdown..")
    #     server.shutdown()