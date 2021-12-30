# SecretBox
A simple Encrypted IM chat software Server &amp; client based on Python3.

## Version 1.0 命令行版

## 安装步骤
### Server
运行`pip3 install -r requirements `安装依赖。
运行`python3 MyServer.py`启动服务端。

### Client
1. 安装依赖`pip3 install -r requirements.txt`
2. 配置 config.py，填写好服务器IP、端口即可。
3. 初始化用户`python3 register.py`，生成公私钥对，并且将公钥传到中继服务器。
4. 收消息：在一个单独的命令行窗口执行`python3 get.py`，执行完后没有反应（不用管），进程会在后台执行，有消息会打印出来
5. 发消息：打开一个新的命令行窗口执行`python3 post.py`，根据提示选择 1 查看用户列表，2 发送消息，先输入对方user id， 然后输入消息发送。
* 注意：这里的user id为初始化用户时生成的公钥的md5值，demo版本，以后可以增加一个nickname字段。
#### 另外，本项目纯粹是临时起意写着玩的，现在只有伊拉克战损版的服务端和客户端，均为命令行程序，因为还要做毕设，所以没时间增加图形界面等美化工作。并且架构设计得比较简单，现在账户信息和用户消息均直接存在内存中，数据库或者消息队列、缓存等暂不考虑。后续有时间再说吧，欢迎魔改。