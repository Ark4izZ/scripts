# weibo爬虫

## 目前功能
- 根据用户名列表获取uid
- 获取用户基本信息(粉丝数、关注数、总发帖数等)
- 根据用户列表爬取微博(可配置爬取含有特定内容的帖子)
- 保存爬虫任务状态(如果中途退出，下次运行可以从上次进度开始)

## 配置
配置文件为`config.json`,需要手动配置。
### config.json
`wait`：等待时间=每次请求的间隔

`last_status`：上次运行的状态；name=用户名，page=爬取到了第几页，uid=用户的uid

`key_word`：爬取含有指定内容的帖子，如果为空则获取全部。

`uid_list`：需要爬取的用户uid列表，可以手动添加，也可以运行`uid_Collector.py`批量获取（根据username_list.txt获取，用户名使用`、`间隔）。最终会更新到此处

`headers`：配置请求头，headers和cookie。获取方法：登录`https://weibo.com`，打开F12开发者工具，刷新之后在network工具里选中weibo.com这个请求，右击复制=>以cURL格式复制所有内容(bash或者cmd都可)，然后打开`https://curlconverter.com/` 粘贴进去，这样就快速构造了headers和cookie字典。

`start_time`&`end_time`：爬取的时间范围。

`model`：爬取模式，0：爬取全部；1：原创微博；2：热门微博；3：赞过的微博；按时间搜索

## 接口

weibo在请求用户页面时会请求几个接口，均以json格式返回数据，对于批量获取数据十分方便，这里介绍几个见到的。

个人信息
`https://weibo.com/ajax/profile/info?uid={}`

信誉、学校、生日等
`https://weibo.com/ajax/profile/detail?uid={}`

side: 粉丝群、关注推荐
`https://weibo.com/ajax/profile/sidedetail?uid={}`

帖子
`https://weibo.com/ajax/statuses/mymblog?uid=1669879400&page=1&feature=0`
`https://weibo.com/ajax/statuses/mymblog?uid=5720474518&page=1&feature=0&displayYear=2022&curMonth=4&stat_date=202204`

访问下一页会有一个新的参数：
data=>since_id=上一页mymblog的id，访问第一页以后每页都要加上 

data=>list=>{index}=>user=>screen_name=发帖用户名

data=>list=>{index}=>created_at=时间

data=>list=>{index}=>text_raw=文字内容

data=>list=>{index}=>reposts_count=转发数

data=>list=>{index}=>comments_count=评论数

data=>list=>{index}=>attitudes_count=点赞数

data=>list=>{index}=>retweeted_status=转发的内容

data=>list=>{index}=>repost_type=是否转发(1是0否)?share_repost_type

发帖历史，如果当月有发就会显示在里面
`https://weibo.com/ajax/profile/mbloghistory?uid={uid}`

返回的 json一般比较乱，可以用json美化工具格式化一下，推荐一个浏览器拓展：[FeHelper](https://github.com/zxlie/FeHelper)


