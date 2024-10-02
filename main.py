from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类

import requests

from mirai import Image
import logging
import traceback


# 注册插件
@register(name="News60s", description="Hello News60s", version="0.1", author="max")
class News60sPlugin(BasePlugin):

    # API URL
    image_api_url = "https://api.andeer.top/API/60s.php"

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def _(self, event: EventContext):
        try:
            text = event.event.text_message
            if text == "news60s" or text == "60s":
                event.prevent_default()
                event.prevent_postorder()
                # 发送图片
                response = requests.get(self.image_api_url)
                if response.ok:  # 使用 response.ok 来检查请求是否成功
                    event.add_return("reply", [Image(url=response.url)])
                else:
                    event.add_return("reply", ["图片获取失败，请稍后再试。"])
                logging.info("News60s!")
        except Exception as e:
            logging.error(traceback.format_exc())

    # 插件卸载时触发
    def __del__(self):
        pass
