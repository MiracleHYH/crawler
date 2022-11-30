from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
from tqdm import tqdm
from utils import mkup
import reg


def get_res(base_url: str, data: dict, require_json: bool = False, max_times: int = 3,
            sep_time: float = 0.5) -> dict | BeautifulSoup | int:
    res = {}
    url = base_url + '?' + urllib.parse.urlencode(data)
    req = urllib.request.Request(url=url, headers=mkup.headers, method='GET')
    error_code = 0
    for i in range(max_times):
        try:
            time.sleep(sep_time)
            res = urllib.request.urlopen(req)
            if res.getcode() == 200:
                if require_json is True:
                    return json.loads(res.read())
                else:
                    return BeautifulSoup(res.read().decode('utf-8'), 'lxml')
        except urllib.error.HTTPError as e:
            error_code = e.code
        except urllib.error.URLError as e:
            return -1
    if error_code != 0:
        return error_code
    else:
        return res.getcode()


def load_news_list(file_path: str) -> dict:
    with open(file_path, encoding='utf-8') as f:
        news_list = json.load(f)
    return news_list


def get_news_list(keyword: str, save_dir: str, use_local: bool = True) -> dict:
    file_path = os.path.join(save_dir, keyword + '.json')
    if use_local is True:
        print('use_local=True, Try to use local url storage')
        if os.path.exists(file_path):
            return load_news_list(file_path)
        print('Can not find ' + file_path)

    print('Downloading urls from website')
    news_list = {}

    base_url = 'https://so.news.cn/getNews'
    data = {
        'keyword': keyword,
        'curPage': 1,
        'sortField': 0,
        'searchFields': 1,
        'lang': 'jp'
    }

    res = get_res(base_url=base_url, data=data, require_json=True)
    if type(res) is dict:
        content = res.get('content')
        total_page = content.get('pageCount')
        total_news = content.get('resultCount')
        print('Searching success, total_news=%d, total_page=%d' % (total_news, total_page))
        print("Getting news's URLs ...")
        with tqdm(total=total_page, desc='Processing', unit='Page', leave=True) as pbar:
            for page in range(1, total_page + 1):
                data.update(curPage=page)
                res = get_res(base_url=base_url, data=data, require_json=True)
                if type(res) is not dict:
                    print('search error, code=%d, page=%d, skipping ...' % (res, page))
                else:
                    content = res.get('content')
                    if content is None:
                        print('response has no content, page=%d, skipping ...' % page)
                    elif content.get('results') is None:
                        print('content has no results, page=%d, skipping ...' % page)
                    else:
                        for news in content.get('results'):
                            news_list.update({
                                news.get('url'): (
                                    reg.parse_title(news.get('title')),
                                    reg.parse_time(news.get('pubtime'))
                                )
                            })
                        pbar.update(1)
        print("Saving %d unique URLs to %s" % (len(news_list), keyword + '.json'))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False)
    else:
        print('search error, code=%d' % res)

    return news_list


def get_page_detail(news_list: dict, save_dir: str):
    print("Getting news's contents ...")
    with tqdm(total=len(news_list), desc='Processing', unit='News', leave=True) as pbar:
        for (news_url, (title, pub_time)) in news_list.items():
            res = get_res(news_url, {})
            if type(res) is BeautifulSoup:
                try:
                    content = reg.parse_content(res.select('#detail')[0].get_text())
                    file_path = os.path.join(save_dir, title + ' ' + pub_time + '.txt')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(pub_time + '\n' + content)
                except Exception as e:
                    print('search error, error=%s, url=%s, skipping ...' % (e, news_url))
            else:
                print('search error, code=%d, url=%s, skipping ...' % (res, news_url))
            pbar.update(1)


def main(keyword):
    save_dir = os.path.join(os.getcwd(), 'downloads', keyword)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    news_list = get_news_list(keyword=keyword, save_dir=save_dir, use_local=True)
    get_page_detail(news_list, save_dir=save_dir)


if __name__ == '__main__':
    main("習近平")
