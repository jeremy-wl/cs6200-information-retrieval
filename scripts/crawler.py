import urllib.request
import re
import requests
import time
import sys
import os
import urllib.parse
from collections import deque

max_depth = 5


def crawl(seed_url, num_pages):
    visited = set()
    q = deque([
        seed_url
    ])

    depth = 0
    num_pages_crawled = 0
    min_page_size, max_page_size, avg_page_size, sum_size = float('inf'), 0, 0, 0

    for directory in ['outputs/html', 'outputs/stats']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    f_urls = open('outputs/stats/urls_crawled.txt', 'a')
    while depth <= max_depth and len(q) != 0 and num_pages_crawled < num_pages:
        qsize = len(q)
        depth += 1
        for i in range(qsize):
            top_url = urllib.parse.unquote(q.popleft())  # decode url
            if num_pages_crawled == num_pages:
                break
            if top_url not in visited:
                # 1. crawl url, save its content to file, and update size variables
                print('At depth {}, {} remaining in depth, Crawling {}'
                      .format(str(depth), qsize-i, top_url))
                res = requests.get(top_url)

                # construct html file path, with file name prepended with leading zeros
                file_path = "outputs/html/{}_{}.html".format(str(num_pages_crawled+1).zfill(3),
                                                             re.findall('.*/(.*)', top_url)[0])
                file_content = res.text
                with open(file_path, 'w') as html_file:
                    html_file.write(file_content)
                    file_size = html_file.tell()

                print("Size: {}, {} pages remaining in total\n"
                      .format(file_size, num_pages-num_pages_crawled))
                if file_size > max_page_size:
                    max_page_size = file_size
                if file_size < min_page_size:
                    min_page_size = file_size
                sum_size += file_size

                # 2. get urls from crawled content
                urls = re.compile('<a .*? href="([^#].*?)"').findall(file_content)
                base_url, protocol = re.findall('((.*?)://.*?\.\w+)/.*', top_url)[0]

                for url in urls:
                    # append site relative urls with base url
                    if url.startswith('//'):
                        url = protocol + ':' + url
                    if url.startswith('/'):
                        url = base_url + url

                    if 'en.wikipedia.org/wiki' not in url:
                        continue
                    if re.match('.*://.*:.*', url):  # Ignore links with a colon (‘:’) after the host name
                        continue
                    if '/wiki/Main_Page' in url:  # Ignore links to http://en.wikipedia.org/wiki/Main_Page
                        continue
                    if url not in visited:
                        q.append(url)
                f_urls.write(top_url + "\n")
                visited.add(top_url)
                num_pages_crawled += 1
            # time.sleep(1)
    f_urls.close()

    # 3. write stats to file
    min_str, max_str, avg_str, depth_str = str(min_page_size), str(max_page_size), \
                                           str(sum_size / num_pages_crawled), str(depth)
    print('Min size: {} bytes'.format(min_str))
    print('Max size: {} bytes'.format(max_str))
    print('Avg size: {} bytes'.format(avg_str))
    print('Max depth reached: ', depth_str)

    with open('outputs/stats/stats.txt', 'w') as f_stats:
        f_stats.write('Min size: {} bytes\n'.format(min_str))
        f_stats.write('Max size: {} bytes\n'.format(max_str))
        f_stats.write('Avg size: {} bytes\n'.format(avg_str))
        f_stats.write('Max depth reached: {}\n'.format(depth_str))


# crawl('https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)', 5)


if __name__ == '__main__':
    args = sys.argv
    crawl(args[1], int(args[2]))
