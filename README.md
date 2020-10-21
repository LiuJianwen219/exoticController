# exoticController
该项目是Exotic远程实验测试系统项目的子项目，该项目用于部署树莓派控制系统。
## 部署方法
### 1、创建 python3.5 以上的虚拟环境，并启动
```shell script
cd work_dir
python3 -m venv venv_dir
source ./venv_dir/bin/activate
```
### 2、安装 python3版本的 WiringPi
```shell script
# 快速安装
pip install wiringpi

# 手动安装
git clone --recursive https://github.com/WiringPi/WiringPi-Python.git ## 下载源码
cd WiringPi-Python
sudo apt-get install python-dev python-setuptools swig wiringpi ## 安装依赖
sudo python3 setup.py install ## 安装
gpio -v ## 检查安装
```

> 安装步骤参考1 https://github.com/WiringPi/WiringPi-Python

> 安装步骤参考2 https://www.icxbk.com/article/detail/1707.html

### 3、下载源码
```shell script
cd work_dir
git clone https://github.com/LiuJianwen219/exoticController.git
cd exoticController
vi settings.ini
  -- WEBIP = 10.14.30.15 ## 网页服务器 IP地址
  -- WEBPORT = 8000 ## 网页服务器端口
  -- HOST = 10.14.30.15 ## 通信服务器 IP地址
  -- PORT = 20200 ## 通信服务器端口
  --DEVICE_NUM = 1 ## 设备识别号（部署的系统中需要唯一）
```

### 4、安装 FPGA控制下载组件
```shell script
cd  work_dir/exoticController
sudo dpkg -i ./requirements/digilent.adept.runtime_2.20.1-armhf.deb
sudo dpkg -i ./requirements/digilent.adept.utilities_2.3.2-armhf.deb
ditgcfg enum ## 查看已经连接的 FPGA型号
```

### 5、安装其他依赖
```shell script
cd  work_dir/exoticController
pip install -r requirement.txt
```

## 6、启动
```shell script
python main.py
```
