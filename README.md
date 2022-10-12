# webVPN_mitm

webVPN_mitm, A Good Man In the Middle of You and webVPN.

webVPN_mitm 是一个基于 [mitmproxy](https://mitmproxy.org) 的插件，实现利用 webVPN 进行 HTTP/HTTPS/WebSocket 数据转发。

适用于网瑞达科技的资源访问控制系统（WebVPN），并为穿透其他资源访问控制系统提供思路。

## 目录：

1. [安装指南](#安装指南)
2. [功能介绍](#功能介绍)
3. [开发手册](#开发手册)
4. [关于webVPN的安全性讨论](#关于webvpn的安全性讨论)
5. [参考和鸣谢](#参考和鸣谢)

**重要提醒：**

⚠️ 本项目具有一定程度的危险性（可能为爬虫、渗透工具提供可用的接口），本项目仅被允许在 wenVPN 提供者制定的规章制度、法律允许的范围内为学习、研究提供帮助，造成的任何后果与开发者无关；

💰 严格禁止任何组织或个人通过此项目进行盈利行为；使用本项目及其衍生版本必须在发行版本中附带此***重要提醒***；

👀 在 webVPN 通道传输任意`最外层`基于 TLS 加密的数据对 webVPN 提供者是透明的，webVPN 提供者有能力对传输内容进行任意程度的审查或篡改；

💊 本项目针对中国药科大学 webVPN 开发，理论上可适用于任何 webVPN 提供商，详见 [开发手册](#开发手册)、[关于webVPN的安全性讨论](#关于webvpn的安全性讨论)；

🐧 本指南中安装方法适用于 `Unix/macOS`，`Windows` 用户请按实际情况酌情修改。


## 安装指南

1. 安装要求

   任意操作系统，**[Python](https://www.python.org/downloads/) 3.9 版本以上**，[Pypi](https://pypi.org/)。

2. 安装流程

   2.1 获取源代码

   通过 git 获取：

   ```bash
     git clone https://github.com/Metaphorme/webVPN_mitm.git
   ```
    
   或者直接下载 [zip 包](https://github.com/Metaphorme/webVPN_mitm/archive/refs/heads/master.zip)。
    
   2.2 设置虚拟环境

   ```bash
    cd webVPN_mitm                      # 进入项目目录
    python3 -m venv env                 # 创建虚拟环境
    source env/bin/activate             # 激活虚拟环境
   ```
   
   Windows 用户请参考 [Installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments)。

   2.3 安装所需包

   ```bash
   python3 -m pip install -r requirements.txt
   ```
   
   2.4 进入工具菜单
   
   ```bash
   python3 menu.py
   ```
   
   如果你顺利看到了下图，那么恭喜🎉，你已经配置成功了！

   ![menu](https://metaphorme.github.io/webVPN_mitm/img/menu.png)
   
   **请注意，之后每次启动前都需要激活虚拟环境。**


## 功能介绍

1. 创建凭证文件
   输入学号、密码（不会被显示）后，将在根目录创建 credentials.txt 存储加密后的学号/密码。

2. 验证凭证文件有效性  
   使用 credentials.txt 中保存的学号/密码进行登录，如果返回有效 cookie，则凭证有效。

3. 普通 URL -> webVPN 加密 URL  
   将普通 URL 转换为 webVPN 加密后的 URL。

4. webVPN 加密 URL -> 普通 URL
   将 webVPN 加密后的 URL 转换为普通 URL。

5. 获取有效 Cookie
   使用 credentials.txt 中保存的学号/密码进行登录，获取有效 cookie。

6. 开启 HTTP/HTTPS 代理服务器  
   使用 credentials.txt 中保存的学号/密码进行登录，在指定端口（默认 8080）开启 HTTP/HTTPS服务器。  
   由于 webVPN 使用 HTTPS 通信，需要安装证书以允许 mitmproxy 解密 HTTPS 流量。安装方法详见 [mitmproxy docs](https://docs.mitmproxy.org/stable/overview-getting-started/#configure-your-browser-or-device)。


## 开发手册
// To be continued


## 关于webvpn的安全性讨论
// To be continued


## 参考和鸣谢
- [ESWZY/webvpn-dlut](https://github.com/ESWZY/webvpn-dlut)
- [mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy)
