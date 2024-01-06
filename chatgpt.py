from hashlib import sha256
import requests
from time import time

class ChatGPT():
    @staticmethod
    def gensign(timestamp: int, msg: str, password: str):
        return sha256(("%d:%s:%s" % (timestamp, msg, password)).encode("utf-8")).digest().hex()

    def __init__(self, api: str, password: str="",
                 temperature: float = 0.6) -> None:
        self.api = api
        self.password = password
        self.temperature = temperature
        self.messages = []

    def ask(self, msg: str) -> str:
        """
        进行一轮对话, 并加入历史消息上下文
        """
        self.messages.append({"role": "user", "content": msg})
        timestamp = int(time())
        
        payload = {
            "pass": self.password,
            "time": timestamp,
            "messages": self.messages,
            "temperature": self.temperature,
            "sign": ChatGPT.gensign(timestamp, msg, self.password)
        }

        resp = requests.post(url = self.api, json = payload)
        if resp.status_code == 200:
            resp_msg = resp.content.decode("utf-8")
            self.messages.append({"role": "assistant", "content": resp_msg})
            return resp_msg
        else:
            return ""

    def nake_ask(self, msg: str, timeout: float = 3.0) -> str:
        """
        无消息上下文, 直接对话一轮
        """
        timestamp = int(time())
        payload = {
            "pass": self.password,
            "time": timestamp,
            "messages": [{"role": "user", "content": msg}],
            "temperature": self.temperature,
            "sign": ChatGPT.gensign(timestamp, msg, self.password)
        }
        resp = requests.post(url = self.api, json = payload, timeout=timeout)
        return resp.content.decode()

    def is_ok(self) -> bool:
        """
        判断当前api与key是否可用, 返回True可用, 否则不可用
        """
        try:
            n = self.nake_ask("你是谁？", timeout = 3.0)
            return n.find("error") == -1
        except:
            return False
    
