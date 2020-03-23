# ComputerNeworkingProject
P2P flooding

## 一 开发环境与工具

本项目于Mac OSX与Ubuntu操作系统下、使用Python编程语言开发，开发工具为PyCharm以及Visual Studio Code。

## 二 设计架构

![image1](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture1.png)

项目文件结构如上图，共有四部分：

- P2P文件夹下是所有底层功能的代码实现，包括TCP（下载）、UDP（广播）、flooding、文件分享（以索引表形式记录分享文件）等。

- UI_design文件夹包含了UI的实现代码。UI的实现基于pyqt包，之所以设计UI，首先是为了方便用户使用，另一方面避免了在命令行下的多线程。

- SHOW文件夹为UI与P2P的封装，将P2P文件中的功能与UI控件捆绑。

- main.py是启动系统的接口。

系统架构如下图：

![image2](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture2.png)

## 三 安装与用户指南

因为本项目在Mac OSX与Ubuntu上开发，使用python socket等网络编程库，尚未在Windows系统上进行测试，因此强烈推荐用户在linux或者macOS上测试、使用，不要在Windows上使用，以防止出现版本、操作系统问题。本系统需要在2台以上的主机上使用。

如要运行代码、测试系统，请按照以下步骤进行：

安装相关python库：

```
pip3 install -r requirements.txt
```

运行系统：

```
python3 main.py
```

系统运行界面如下（在macOS下运行）：

![image3](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture3.png)

此界面为上传共享文件界面，用户可以选择添加单个共享文件（添加文件），或者添加共享文件夹（添加目录）。添加共享文件后，添加文件的信息会出现在下方文本框中。

如下图，添加了文件与文件目录后的界面：

![image4](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture4.png)

下图为下载共享文件界面（在macOS下运行）：

![image5](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture5.png)

在另一台主机上，用户可以搜索共享的文件，点击“搜索”按钮后，与检索文字相关的文件将会出现在下方的文本框中。

如果想要下载文件，则右键想要下载的文件，点击下载即可。如下图（在Ubuntu下运行）：

![image6](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture6.png)

点击下载后，在下方的文本框会出现下载文件的文件名、源IP与下载进度，下载完成后，会跳出“下载成功“提醒框。如下图（在Ubuntu下运行）：

![image7](https://github.com/Shiyuang-scu/ComputerNeworkingProject/raw/master/Picture7.png)

四 注意事项
本项目必然存在目前仍未发现的bug，因此在未来仍会持续更新。所以，您在测试系统时（请务必在macOS或者linux下测试），如果出现某些未预见的问题，也许在最新版本中已经得到解决。如问题仍未解决，请务必联系我。

```
git clone git@github.com:Shiyuang-scu/ComputerNeworkingProject.git
```

