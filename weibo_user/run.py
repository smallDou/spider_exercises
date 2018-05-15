from spider import Spider

def main():
    s = Spider.verify_cookie()
    s.get_weibo_info()

#设置定时任务
if __name__ == '__main__':
    main()