# aiqiyi_comment_crawler
爱奇艺视频下评论数据抓取

# 获取TVID
进入该剧集网页，F12进入开发者模式，搜索TVID，格式为16位纯数字。

# 替换至API
 url = "https://sns-comment.iqiyi.com/v3/comment/get_comments.action?agent_type=118&agent_version=9.11.5&authcookie=null&business_type=17&content_id=7222400481724500&page=&page_size=10&types=time&last_id="
的content_id字段即可。
