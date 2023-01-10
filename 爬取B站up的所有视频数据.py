import math, requests,time                   # 导入网络请求模块
from datetime import datetime           # 导入时间解析模块

def getTime(time):                      # 将时间戳解析成人们看得懂的时间
    return datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")


def getallvideos():                     # 爬虫的主函数
    mid = input("请输入B站up主的mid:（默认:661047235）")                          # 输入up的mid
    if mid=="":
        mid='661047235'
    url = 'https://api.bilibili.com/x/space/wbi/arc/search?mid=' + mid      # 拼接请求地址
    response = requests.get(url=url, headers=headers)                       # 发起网络请求
    try:                                        # 如果用户输入up的mid不正确，这里就无法获取数据，
        list = response.json()['data']          # 获取数据
        count = list['page']['count']           # 获取up的视频总数
        page = math.ceil(count / 30)            # 分页数
        if page==0:                             # 如果page=0，说明这个up还没发布作评
            print("这个up没有投稿的作品，无法获取数据！")
            return                              # 结束函数
        print(f'这个up主的视频总数:{count}')
        print('序号', 'up主昵称', '视频标题', '视频的评论数', '视频地址', '视频封面图片的地址', 'up的mid', '视频发布时间', '视频时长', '视频的弹幕数')
        i = 1                                  # 计数变量
        for currentpage in range(1, page + 1):      # 遍历每一页
            url = 'https://api.bilibili.com/x/space/wbi/arc/search?mid=' + str(mid) + '&pn=' + str(currentpage)
            response = requests.get(url=url, headers=headers)       # 发起网络请求
            list = response.json()['data']['list']['vlist']         # 获取视频数据
            for li in list:                             # 遍历每一个视频
                author = li['author']                   # 作者
                title = li['title']                     # 视频标题
                comment = li['comment']                 # 评论
                post = li['pic']                        # 视频封面
                description = li['description']         # 视频简介
                mid = li['mid']                         # 作者的mid
                created = getTime(li['created'])        # 视频发布时间
                length = li['length']                   # 视频时长
                video_review = li['video_review']       # 弹幕数
                src = 'https://www.bilibili.com/video/' + li['bvid']  # 视频链接
                print(i, author, title, comment, src, post, mid, created, length, video_review)
                i = i + 1                               # 计数 +1
        time.sleep(0.3)          # 由于爬虫的速度太快了，这里等待一下下，防止被服务器抓到
    except Exception as error:   # 程序出错了
        print(f"呜呜呜，程序出错了:{error}，请检查up的mid是否输入正确，或者是我们的爬虫遭到了拦截，更多帮助，请添加微信：safeseaa  ")

if __name__ == '__main__':      # 主函数
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }               # headers 反反爬虫
    getallvideos()          # 调用函数
