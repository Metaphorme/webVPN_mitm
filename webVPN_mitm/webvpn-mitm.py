from mitmproxy import ctx
from mitmproxy.script import concurrent
import url_conversion
import cpu_webvpn as instCookie
import re
from cpu_webvpn import read_credentials


class Modify:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.d = url_conversion.WebvpnUrl("webvpn.cpu.edu.cn")
        self.cookie = ''

    def running(self) -> None:
        self.__getCookie()
        return None

    def __getCookie(self) -> None:
        self.cookie = instCookie.login(username=self.username, password=self.password)
        ctx.log("Get cookie: {wengine_vpn_ticketwebvpn_cpu_edu_cn: " + self.cookie + "}")
        return None

    def done(self) -> None:
        instCookie.logout(cookie=self.cookie)
        return None

    def reformat(self, match: re.match) -> str:
        return "//" + self.d.url_decode(match.group()[:-1]).split("//")[1] + '"'

    @concurrent
    def request(self, flow) -> None:
        if flow.request.url.startswith("https://webvpn.cpu.edu.cn/"):
            ctx.log("Skip " + flow.request.url)
        else:
            ctx.log("Encode " + flow.request.url)
            flow.request.url = self.d.url_encode(flow.request.url)

        flow.request.cookies["wengine_vpn_ticketwebvpn_cpu_edu_cn"] = self.cookie
        return None

    @concurrent
    def response(self, flow) -> None:
        content = flow.response.get_text()
        if content == '<a href="https://webvpn.cpu.edu.cn/login">Found</a>.\n\n':
            ctx.log("Cookie invalid. Try to get a fresh cookie...")
            self.__getCookie()
        else:
            content = re.sub(
                pattern=r'\/\/webvpn\.cpu\.edu\.cn\/\S*"',
                repl=self.reformat,
                string=content
            )
            flow.response.set_text(content)
        return None


addons = [
    # 请在此处输入学号/密码
    Modify(username=read_credentials()[0], password=read_credentials()[1])
]
