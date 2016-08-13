import urllib2
import hashlib
import os
from bs4 import BeautifulSoup

user_response = ''
page_no = 1
movie_list = {}
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

sha1_hash = hashlib.sha1()
if not os.path.exists('../torrents'):
    os.makedirs('../torrents')
while user_response != 'n':
    page = urllib2.urlopen('https://www.shaanig.org/f30/index' + str(page_no)  + '.html')
    soup = BeautifulSoup(page, 'lxml')
    threads = soup.body.find('ol', {'id': 'threads'})
    current_list = {
        thread.find('a', {'class': 'title'}).string: thread.find('a', {'class': 'title'})['href']
        for thread in threads.find_all('li', {'class': 'threadbit'})
    }
    for movie in current_list.keys():
        print '[' + str(current_list.keys().index(movie)+1) + '] ' + movie
    movie_list.update(current_list)
    movie_choice = raw_input("Please enter your choice (-1 to stop): ")
    while int(movie_choice) > 0 and int(movie_choice) < 31:
        page = urllib2.urlopen(current_list[current_list.keys()[int(movie_choice)-1]])
        soup = BeautifulSoup(page, 'lxml')
        download_url = soup.body.find('div', {'class': 'attachments'}).find('a', {'class': 'downloadbutton_attachments'})['href']
        torrent = urllib2.urlopen(download_url)
        sha1_hash.update(movie_list.keys()[int(movie_choice)-1])
        torrent_filename = sha1_hash.hexdigest() + '.torrent'
        with open('../torrents/' + torrent_filename, 'w') as f:
            f.write(torrent.read())
        os.system("transmission-remote -n 'wimo:usmle26sas' -a /home/wimo/shaanig-torrent-parser/" + torrent_filename)
        print CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE
        movie_choice = raw_input("Please enter your choice: ")
    user_response = raw_input("Go to next page(y/n): ")
    page_no += 1
    for x in range(len(current_list)):
        print CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE
