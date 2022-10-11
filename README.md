# webVPN-mitm

webVPN_mitm, A Good Man In the Middle of You and webVPN.

webVPN_mitm 是一个基于 [mitmproxy](https://mitmproxy.org) 的插件，实现利用 webVPN 进行任意数据转发。

## 目录：

1. [安装指南](#安装指南)
2. [开始使用](#开始使用)
3. [开发手册](#开发手册)
4. [关于 webVPN 的安全性讨论](#关于 webVPN 的安全性讨论)
5. [鸣谢](#鸣谢)

**重要提醒：**

⚠️ 本项目具有一定程度的危险性（可能为爬虫、渗透工具提供可用的接口），本项目仅被允许在 wenVPN 提供者制定的规章制度、法律允许的范围内为学习、研究提供帮助，造成的任何后果与开发者无关；

💰 严格禁止任何组织或个人通过此项目进行盈利行为；使用本项目及其衍生版本必须在发行版本中附带此***重要提醒***；

👀 在 webVPN 通道传输任意`最外层`基于 TLS 加密的数据对 webVPN 提供者是透明的，webVPN 提供者有能力对传输内容进行任意程度的审查或篡改；

💊 本项目针对中国药科大学 webVPN 开发，理论上可适用于任何 webVPN 提供商，详见 [开发手册](#开发手册)、[关于 webVPN 的安全性讨论](#关于 webVPN 的安全性讨论)；

🐧 本指南中安装方法适用于 `Unix/macOS`，`Windows` 用户请按实际情况酌情修改。


## 安装指南

 1. 安装要求

    任意操作系统，**[Python](https://www.python.org/downloads/) 3.9 版本以上**，[Pypi](https://pypi.org/)。

2. 安装流程

   2.1 获取源代码

   通过 git 获取：

   ```bash
     git clone https://github.com/Metaphorme/webVPN-mitm.git
   ```
    
   或者直接下载 [zip 包](https://github.com/Metaphorme/webVPN-mitm/archive/refs/heads/master.zip)。
    
   2.2 设置虚拟环境

   ```bash
    cd webVPN-mitm                      # 进入项目目录
    python3 -m venv env                 # 创建虚拟环境，请不要更改虚拟环境名
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

   [图]
   
   **请注意，之后每次启动前都需要先激活虚拟环境。**


## 开始使用
// To be continued


## 开发手册
// To be continued


## 关于 webVPN 的安全性讨论
// To be continued


## 鸣谢
// To be continued

