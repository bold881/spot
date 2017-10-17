# spot

#环境需求
python2.7+scrapy+mongodb
具体平台安装下的安装方法查询各自官网。
使用方法：
1.repo_spider.py中的username和password为已知的新浪微博用户名和密码；
2.在settings.py修改Mongodb的连接方式，包括：ip, port, database, connection
3.在命令行中执行：
scrapy crawl repoweibo -a wurl="https://weibo.cn/u/2839685750" --'u/2839685750'为具体用户的页面，可修改

#已知问题
在一定量请求数据之后，微博会拒绝访问，现象是返回结果403，这种情况下只能更换账号访问，或者次日再访问。
如下：
2017-10-17 10:36:41 [scrapy.core.engine] DEBUG: Crawled (403) <GET https://weibo.cn/u/2839685750?page=376> (referer: https://weibo.cn/u/2839685750?page=375)
再可以再次请求数据的前提下，可以增量的抓取页面，命令scrapy crawl repoweibo -a wurl="https://weibo.cn/u/2839685750?page=376"

#示例数据见u2839685750.json

