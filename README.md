內網才可正常顯示操作步驟&版本狀態

### AzureDevopsPipeline自動佈署腳本

### 簡介

`自動化雲端佈署`python，免去`人工建置`的困擾

### 專案結構
```
MyPython
├─ azure-pipelines.yml
├─ python
│  ├─ .env
│  ├─ docker-compose.yml
│  ├─ mypython
│  │  ├─ apache
│  │  │  ├─ 000-default.conf
│  │  │  ├─ apache2.conf
│  │  │  ├─ conf-available
│  │  │  │  ├─ charset.conf
│  │  │  │  ├─ javascript-common.conf
│  │  │  │  ├─ localized-error-pages.conf
│  │  │  │  ├─ other-vhosts-access-log.conf
│  │  │  │  ├─ security.conf
│  │  │  │  └─ serve-cgi-bin.conf
│  │  │  ├─ conf-enabled
│  │  │  │  ├─ charset.conf
│  │  │  │  ├─ javascript-common.conf
│  │  │  │  ├─ localized-error-pages.conf
│  │  │  │  ├─ other-vhosts-access-log.conf
│  │  │  │  ├─ security.conf
│  │  │  │  └─ serve-cgi-bin.conf
│  │  │  ├─ envvars
│  │  │  ├─ letsencrypt
│  │  │  │  └─ live
│  │  │  │     └─ markweb.idv.tw
│  │  │  │        ├─ cert.pem
│  │  │  │        ├─ chain.pem
│  │  │  │        ├─ fullchain.pem
│  │  │  │        ├─ privkey.pem
│  │  │  │        └─ README
│  │  │  ├─ magic
│  │  │  ├─ mods-available
│  │  │  ├─ mods-enabled
│  │  │  ├─ ports.conf
│  │  │  ├─ sites-available
│  │  │  │  ├─ 000-default.conf
│  │  │  │  └─ default-ssl.conf
│  │  │  └─ sites-enabled
│  │  │     └─ 000-default.conf
│  │  ├─ DigiCertGlobalRootCA.crt.pem
│  │  ├─ Dockerfile
│  │  ├─ letsencrypt
│  │  │  └─ live
│  │  │     └─ markweb.idv.tw
│  │  │        ├─ cert.pem
│  │  │        ├─ chain.pem
│  │  │        ├─ fullchain.pem
│  │  │        ├─ privkey.pem
│  │  │        └─ README
│  │  ├─ main.py
│  │  ├─ requirements.txt
│  │  └─ serve-cgi-bin.conf
│  └─ phpmyadmin
│     ├─ Dockerfile
│     └─ php.ini
└─ README.md
```

### 目錄
- [一、使用方式](#一使用方式)
  - [STEP1：設置git環境並產生金鑰](#step1設置git環境並產生金鑰)
  - [STEP2：拉取git存放庫目錄到本地](#step2拉取git存放庫目錄到本地)
- [二、執行步驟](#二執行步驟)
  - [STEP1：建立AZURE DEVOPS專案](#step1建立azure-devops專案)
  - [STEP2：建立Pipelinnes](#step2建立pipelinnes)
  - [STEP3：建立APP SERVICE](#step3建立app-service)
  - [STEP4：建立AZURE Container Registry 存放庫](#step4建立azure-container-registry-存放庫)
  - [STEP5：建立MYSQL資料庫](#step5建立mysql資料庫)
  - [STEP6：建立Pipelines環境變數](#step6建立pipelines環境變數)
  - [STEP7：開始撰寫腳本](#step7開始撰寫腳本)
    - [1. 建立`azure-pipelines.yml`，輸入以下指令](#1-建立azure-pipelinesyml輸入以下指令)
    - [2. 建立Python `DockerFile`，並輸入以下指令](#2-建立python-dockerfile並輸入以下指令)
    - [3. 建立`main.py`，並輸入以下指令](#3-建立mainpy並輸入以下指令)
    - [4. 建立`requirements.txt`，輸入以下指令](#4-建立requirementstxt輸入以下指令)
    - [5. 建立`docker-compose.yml`，並輸入以下指令](#5-建立docker-composeyml並輸入以下指令)
    - [6. 建立`.env`，並輸入以下指令](#6-建立env並輸入以下指令)
- [三、執行結果](#三執行結果)
  - [查看執行結果](#查看執行結果)
- [四、問題排除](#四問題排除)



## 一、使用方式

### STEP1：設置git環境並產生金鑰
1. 安裝好`git`環境
2. 開啟`cmd`,輸入以下指令
```shell
ssh keygan -b 4096 -c ['你的email']
```
3. 將產生的`金鑰`放在以下路徑 
```batch
C：\users\['你的使用者名稱']\.ssh
```
![image-20231018202934452](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018202934452.png)


4. 進入`AZURE DEVOPS` 的`使用者設定`，把剛剛產生的`public key 複製`到上面

![image-20231018203040256](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018203040256.png)


### STEP2：拉取git存放庫目錄到本地

1. 在windows`建立一個新目錄`，開啟`cmd`，輸入以下指令，成功畫面如下圖

```shell
git clone ['你的倉庫URL位址']
```
2. `倉庫的URL`可以在這邊找到

![image-20231019094128649](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231019094128649.png)

![image-20231018203309314](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018203309314.png)

<!--more-->


## 二、執行步驟

### STEP1：建立AZURE DEVOPS專案

輸入專案名稱、選擇私有專案，點選create

![image-20231018203636277](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018203636277.png)



### STEP2：建立Pipelinnes

點選`AZURE存放庫`

![image-20231018203929816](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018203929816.png)

選擇`mypython`
![image-20231018203959065](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018203959065.png)

建立一個`新的pipelines`
![image-20231018204044225](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018204044225.png)

開始撰寫`pipelines`
![image-20231018204347774](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018204347774.png)

### STEP3：建立APP SERVICE

點選建立`Web應用程式`
![image-20231018204551684](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018204551684.png)

填寫`紅框處`相關資訊
![image-20231018204743294](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018204743294.png)

選擇`定價方案`
![image-20231018204808282](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018204808282.png)

選擇`單一容器→快速入門`
![image-20231018205007447](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205007447.png)

點選`啟用公開存取`
![image-20231018205037346](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205037346.png)

點選`Application Insights`
![image-20231018205054750](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205054750.png)

看個人情況決定是否`建立標籤`
![image-20231018205126436](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205126436.png)

點選建立`Web應用程式`
![image-20231018205157355](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205157355.png)



### STEP4：建立AZURE Container Registry 存放庫

點選`Container Registry`
![image-20231018205242702](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205242702.png)

輸入`紅框處`相關內容
![image-20231018205413828](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205413828.png)

點選`下一步`
![image-20231018205435882](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205435882.png)

點選`下一步`
![image-20231018205448309](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205448309.png)

看個人情況決定是否`建立標籤`
![image-20231018205516050](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205516050.png)





AZURE Container Registry 存放庫設定

存放庫建立完成後，請先進入`設定`頁面，將`管理員權限`開啟
![image-20231018205728327](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205728327.png)


存放庫可查看推送上去的`映象檔`
![image-20231018205921457](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018205921457.png)

### STEP5：建立MYSQL資料庫

點選`建立`
![image-20231018210311672](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210311672.png)

選擇`彈性伺服器`
![image-20231018210339090](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210339090.png)

輸入`紅框處`相關資訊
![image-20231018210626261](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210626261.png)

點選只有`mysql驗證`，並輸入下方相關資訊
![image-20231018210736879](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210736879.png)

這邊`公用存取`選項一定要勾
![image-20231018210826611](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210826611.png)

`防火牆規則`建立(可全開也可不全開)
![image-20231018210921019](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018210921019.png)

點選`下一步`
![image-20231018211001017](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018211001017.png)

看個人情況決定是否`建立標籤`
![image-20231018211031391](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018211031391.png)

點選建立
![image-20231018211140671](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018211140671.png)

資料庫容器建置完成後，請`新增`一個`資料庫`
![image-20231018211304595](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018211304595.png)

這邊可以查看`連線相關帳密`
![image-20231018211738319](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018211738319.png)

### STEP6：建立Pipelines環境變數

![image-20231018212513993](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018212513993.png)

### STEP7：開始撰寫腳本

#### 1. 建立`azure-pipelines.yml`，輸入以下指令

```yaml
#git pipelines觸發
trigger:
- '*'

#定義變數群組
variables:
  - group: Azure Registry Login

#腳本執行進入點
stages:
- stage: AzureWebAppServiceBuild
  displayName: "AzureWebAppServiceBuild"
  jobs:
  - job: PythonImageBuild
    displayName: "PythonImageBuild"
    steps:   
    #DockerCompose
    - task: DockerCompose@0
      inputs:
        containerregistrytype: 'Azure Container Registry'
        azureSubscription: 'Azure subscription 1 (08f3d78b-9c30-4ff5-b097-5fb7283bafba)'
        azureContainerRegistry: '{"loginServer":"myrefistry.azurecr.io", "id" : "/subscriptions/08f3d78b-9c30-4ff5-b097-5fb7283bafba/resourceGroups/VM_12773033/providers/Microsoft.ContainerRegistry/registries/myrefistry"}'
        dockerComposeFile: 'python/docker-compose.yml'
        action: 'Run a Docker Compose command'
        dockerComposeCommand: --env-file python/.env up -d --build
        displayName: 'AZURE DOCKERCOMPOSE BUILD'
    #DockerImages
    - script: |
             docker images
      displayName: 'AZURE DOCKER IMAGE LIST'
    #DockerBuildAndPush
    - script: |
             docker login $(REGISTRY_HOST) -u $(REGISTRY_USER) -p $(REGISTRY_PASSWORD)
             docker tag mypythonweb:1.0 $(REGISTRY_IMAGE)
             docker push $(REGISTRY_IMAGE)
      displayName: 'AZURE DOCKER REGISTRY LOGIN AND PUSH IMAGE'
    #AzureWebAppContainer
    - task: AzureWebAppContainer@1
      displayName: 'AZURE WEB APP SERVICE BUILD'
      inputs:
        azureSubscription: 'Azure subscription 1 (08f3d78b-9c30-4ff5-b097-5fb7283bafba)'
        appName: 'testpython-1'
        containers: '$(REGISTRY_IMAGE)'
```
#### 2. 建立Python `DockerFile`，並輸入以下指令

```docker
FROM php:7.4-apache
COPY requirements.txt ./
RUN apt-get -y update \
&& apt-get install -y python3 python3-pip \
&& apt install vim -y \
&& a2enmod rewrite \
&& a2enmod ssl \
&& a2enmod headers \
&& a2enmod proxy \
&& a2enmod proxy_http \
&& a2enmod proxy_balancer \
&& a2enmod cgi \
&& apt-get install -y --no-install-recommends \
&& python3 -m pip install --upgrade pip \ 
&& pip install --no-cache-dir -r requirements.txt
COPY letsencrypt /etc/letsencrypt/
COPY apache/apache2.conf /etc/apache2/
COPY apache/000-default.conf /etc/apache2/sites-available/
COPY apache/ports.conf /etc/apache2/
COPY main.py /var/www/html
COPY DigiCertGlobalRootCA.crt.pem /var/www/html
WORKDIR /var/www/html
RUN chmod +X main.py && chmod 755 main.py 
EXPOSE 8000
```   

#### 3. 建立`main.py`，並輸入以下指令

```python
#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
app = Flask(__name__)

#這邊建立MYSQL連線資訊

@app.route("/")   
def index():
    # 建立資料庫連接
    db = pymysql.connect(
      host='[請在mysql server上查看]',
      user='[請在mysql server上查看]',
      password='[請在mysql server上查看]',
      database='[請在mysql server上查看]',
      ssl_disabled='True')
    
    cursor = db.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM student;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")

    # 印出資料
    for row in rows:
      print(row)

    # 釋放連線
    db.commit()
    cursor.close()
    db.close()

    return "Done"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)
```
#### 4. 建立`requirements.txt`，輸入以下指令
``` 
markdown==3.1.1
mysql-connector-python==8.0.17
protobuf==3.6.1
markupsafe==2.1.1
Jinja2==3.1.2
Flask == 2.0.1
Werkzeug==2.2.2
pymysql==1.1.0
```
#### 5. 建立`docker-compose.yml`，並輸入以下指令
```yaml
version: '3.3'
services:
  python:
    build: ./mypython
    container_name: mypythonweb
    image: mypythonweb:${BUILD_NUMBER}
    restart: always
    ports:
      - "${PYTHON_PORTS}:80"
    volumes:
      - $SourcesDirectory/etc/apache2:/etc/apache2/
      - $SourcesDirectory/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
      - $SourcesDirectory/var/www/html:/var/www/html
```
#### 6. 建立`.env`，並輸入以下指令
```
#MARIADB參數設定
MARIADB_ROOT_PASSWORD=[自行定義]
MARIADB_DATABASE=[自行定義]
MARIADB_USER=[自行定義]
MARIADB_PASSWORD=[自行定義]
MARIADB_PORTS=8088

#python參數設定
PYTHON_PORTS=80

#PHPMYADMIN參數設定
PHPMYADMIN_PORTS=8080
MYSQL_ROOT_PASSWORD=[自行定義]
BUILD_NUMBER=1.0
```


## 三、執行結果

### 查看執行結果

![image-20231018212224544](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018212224544.png)

![image-20231018212300671](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018212300671.png)

![image-20231018212335104](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231018212335104.png)

## 四、問題排除

1. 請到APP SERVICE的組態設定，檢查紅框處設定是否正確
![image-20231019094703760](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231019094703760.png)
2. 部署中心的設定可以檢查這個APP SERVICE目前和誰綁定，由此圖可以得知目前和DEVOPS做綁定
![image-20231019095015816](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231019095015816.png)

3. 部署中心的紀錄可以查看APP SERVICE的是否啟動，也可點選重新整理或是下載來查看紀錄
![image-20231019095240503](https://markweb.idv.tw:8443/markhsu/JoplinImageUpload/raw/branch/master/image-20231019095240503.png)