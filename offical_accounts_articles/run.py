from spider import Spider

def main():
    s = Spider.verify_cookie()
    s.get_details()

if __name__ == '__main__':
    main()