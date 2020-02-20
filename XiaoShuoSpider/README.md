@[TOC](mm131.com的全站图片爬取crawlspider爬虫)

## hello 大家好,我是W

项目介绍：本项目为CrawlSpider实战，目标是爬取一个网站全站的图片，其中包含crawlspider项目创建、**网站分析**、xpath获取数据、**使用ImagesPipeline自动下载图片**、**自定义pipeline实现文件夹分类**以及**下载中间件实现User-Agent**和IP（了解）设置。

## 网站分析

本次选择的布标网站是有很多妹子图片的mm131.net 接下来需要进入网站对其进行分析。

 1. [进入www.mm131.net](http://www.mm131.net)
 进入首页我们可以看到首页带有几大分区如xx校花等，可以清晰知道该站点的图片主要分为以下这几大类型，所以只要将几这几个大类的图片抓取下来就能够实现全站爬取。
 2. [点击进入校花页www.mm131.net/xiaohua/](https://www.mm131.net/xiaohua/)
1.首先通过url我们可以**猜测到.net后面跟什么就是什么类的大相册了**，这为我们后续爬取其他大相册提供了依据，不相信的话我们可以继续点击其他大相册试试。
	[https://www.mm131.net/xinggan/](https://www.mm131.net/xinggan/)
	[https://www.mm131.net/qingchun/](https://www.mm131.net/qingchun/)
	[https://www.mm131.net/xiaohua/](https://www.mm131.net/xiaohua/)
	[https://www.mm131.net/chemo/](https://www.mm131.net/chemo/)
	[https://www.mm131.net/qipao/](https://www.mm131.net/qipao/)
	[https://www.mm131.net/mingxing/](https://www.mm131.net/mingxing/)
2.接下来我们进入校花页，可以看到有整齐排列的小相册，同时在最下方翻页处**随意点击几页观察url可以知道url的变化规律**[https://www.mm131.net/xiaohua/list_2_3.html](https://www.mm131.net/xiaohua/list_2_3.html)**要实现翻页只需要更改html前面的最后一个数字即可，即上面url的3的位置**。若不信我们可以改一改2，[https://www.mm131.net/xiaohua/list_1_3.html](https://www.mm131.net/xiaohua/list_1_3.html)很显然服务器返回404。

3. F12打开检查点选图片可以看到相册的名称和相册地址
多选择几个其他相册我们可以得到规律：**进入不同相册是通过改变/xiaohua/\*\*\*.html的\*\*实现的**，如[https://www.mm131.net/xiaohua/608.html](https://www.mm131.net/xiaohua/608.html)
[https://www.mm131.net/xiaohua/611.html](https://www.mm131.net/xiaohua/611.html)找到这些规律对我们写crawl的rules的时候很关键



## CrawlSpider的创建
1. 打开cmd，cd进入自己的project文件夹

	```
	cd D:\project
	```
2. 生成scrapy项目
	```
	scrapy startproject crawl_spider
	```
3. **cd进入scrapy的spider文件夹**生成crawlSpider模板的py文件
	```
	scrapy genspider -t crawl mm131 www.mm131.net
	```
	这一行命令的意思是scrapy 生成爬虫 使用crawl模板 爬虫名称mm131 爬取的范围是www.mm131.net
4. 进入项目我们可以看到项目的文件结构，并且本次项目需要用到的文件有mm131.py、items.py、pipelines.py、middlewares.py、settings.py，并且我们要再新建一个run.py驱使项目启动。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020012821533688.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsaWFuX1c=,size_16,color_FFFFFF,t_70)
run.py 没有什么技术含量,请放心复制粘贴，创建完成后右键运行文件出现下方红字即项目正常启动

## 使用xpath获取数据

1. 在操作前配置settings文件
	```python
	ROBOTSTXT_OBEY = True -> ROBOTSTXT_OBEY = False
	
	DEFAULT_REQUEST_HEADERS = {
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
	}
	```
2. 编写Rule
网站分析部分可知只要爬取所有相册我们就能实现全站爬取，所以设置初始url为其中一个大相册
	```start_urls = ['https://www.mm131.net/xinggan/']```并且知道每个小相册的url规则，所以设置Rule
	```python
	rules = (
        Rule(LinkExtractor(allow=r'.+/xiaohua/(.+).html'), callback='parse_page', follow=True),
    )```
	# rule的规则使用正则表达式

3. 编写xpath获取小相册的title和url
	```python
	# 因为在写rules的时候直接解析的是大相册（校花）下的小相册的入口URL，所以下方callback函数写的是针对相册的xpath
	# 同时由页面分析也知道翻页的url也符合上面定义rule的规则
	# 但是需要注意的是，由于相册太多，所以导致需要解析的url队列太长，所以需要很久才能看到翻页下载的效果
	def parse_page(self, response):
			title = response.xpath("//div[@class='content']/h5/text()").get()
	        url = response.xpath("//div[@class='content-pic']/a/img/@src").get()
	        url_list = []
	        # image_urls必须接受list对象 所以需要将xpath返回对象改成list
	        url_list.append(url)
	        yield MM131SpiderItem(title=title, image_urls=url_list)
	```
	同时到Items.py编写MM131SpiderItem：
	```python
	class MM131SpiderItem(scrapy.Item):
	    title = scrapy.Field() # 小相册中每一页的title
	    image_urls = scrapy.Field() # 图片地址
	    iamges = scrapy.Field() # None
	```
## 使用ImagesPipeline自动下载图片
1. 在settings中配置scrapy自带的图片下载pipeline，无需对pipelines.py进行任何操作，scrapy会自动在项目根目录下生成images/full/文件路径并将文件保存其中[注意:此时的文件名是uuid生成的所以无序]
	```python
	ITEM_PIPELINES = {
	    'scrapy.pipelines.images.ImagesPipeline' : 300,
	}
	```
2. 同时在settings文件中配置IMAGES_STORE
	```python
	IMAGES_STORE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
	# 这是os模块的操作，不了解的可以看https://blog.csdn.net/xxlovesht/article/details/80913193
	```
3. 同时担心爬虫爬取速度太快了，我们将delay打开
	```python
	DOWNLOAD_DELAY = 1 # 1秒请求1次
	```
4. 执行run.py 发现image文件夹生成了，但是**文件夹为空**，**因为有的网站需要有Referer，所以需要在headers里面添加Referer**
	```python
	DEFAULT_REQUEST_HEADERS = {
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
	    'Referer': 'https://www.mm131.net/xiaohua/',
	}
	```
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200128224150100.png)
这样就完美解决相片无法下载问题，并且不会被反爬查出并返回垃圾资源

至此使用ImagesPipeline自动下载图片完成

## 自定义pipeline实现文件夹分类
1. 要实现文件按小相册名称归类需要重写ImagesPipeline的get_media_requests、file_path两个方法，先上代码
	```python
	class MMSpiderPipeline(ImagesPipeline):
	
	    def get_media_requests(self, item, info):
	        request_objs = super(MMSpiderPipeline, self).get_media_requests(item, info)
	        for obj in request_objs:
	            obj.item = item
	        return request_objs
		# 在ImagesPipeline中的request没有item，所以在spider里爬取到的title无法取出
		# 所以需要用到get_media_request方法获取request对象列表，因为get_media_requests方法可以获取spider的item所以可以将item放入其中
		# 并且get_media_requests方法在file_path之前调用，request对象在file_path里已经有item了，所以可以获取title并且改写path
	    def file_path(self, request, response=None, info=None):
	        path = super(MMSpiderPipeline, self).file_path(request, response, info) # 就不需要调用父类的file_path获取uuid定义的path
	        title = request.item.get("title")
	        # 本来相片的path是由ImagesPipeline的file_path生成uuid生成的 现在用相册名(页码数)自己定义imagepath
	        path = title + ".jpg"
	        print('[文件名] '+path)
	        image_store = settings.IMAGES_STORE
	
	        # 取消文件夹定义 让其放再image下
	        # category_path = os.path.join(image_store, title)
	        # if not os.path.exists(category_path):
	        #     os.mkdir(category_path)
	
	        # 取消full文件夹 直接放再image文件夹下
	        image_path = path.replace("full/", "")
	        image_path = os.path.join(image_store, path)
	        return image_path
			# 直接运行的效果是所有相册的图片都放在images文件夹下，且没有full文件夹
			# 各位少侠可以自行想办法把title后不一样的文字取出使其同一小相册的图片放再一个文件夹中
	```


## 下载中间件实现User-Agent和IP（了解）设置

1. 自己上网查一下UA大全
	```python
	class UserAgentDownloadMiddleware(object):
	    USER_AGENTS = [
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
	        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)",
	        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
	        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5;",
	        "Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)",
	        "Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)",
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
	        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	    ]
	
	    def process_request(self, request, spider):
	    	# 使用random从中随机选择UA
	        user_agent = random.choice(self.USER_AGENTS)
	        request.headers['User-Agent'] = user_agent
		# 使用下载器中间件需要了解的是不同方法的走向，process_request是从core走向pipeline，所以中间件对request进行处理的时候可以提取出headers并且对ua或者ip进行修改，达到反反爬虫的目的。

	```
2. 记得在settings里面开启下载器中间件
	```python
		DOWNLOADER_MIDDLEWARES = {
	   'XiaoShuoSpider.middlewares.UserAgentDownloadMiddleware': 543,
	}
	```

## 效果
![](https://i.imgur.com/ElMVE32.png)


## 写在最后
研究生考试结束后花了两天把庆余年刷完了，然后就开始看python了，从python基础、高级、网络、mysql、mongodb、redis再到现在的爬虫，中间又出去玩，还要过年所以进度拖沓了。不过还好以前有Java基础，在学校学的东西也比较扎实，在实际应用中真的会联想运用其中，也算是可喜。不管考试结果如何，人生还是不断地战斗，既然选择做程序员，那就必须做好像马一样奔跑一生的准备，加油吧各位少年！
