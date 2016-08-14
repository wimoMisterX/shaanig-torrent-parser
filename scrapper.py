import urllib2
import hashlib
import os
import sys
import settings
from bs4 import BeautifulSoup

def clear_lines(num):
    for x in range(num):
        print '\x1b[1A' + '\x1b[2K' + '\x1b[1A'

def get_html(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page, 'lxml')

def save_torrent_to_disk(thread_title, thread_link):
    soup = get_html(thread_link)
    torrent = urllib2.urlopen(
        soup.body.find('div', {'class': 'attachments'}).find('a', {'class': 'downloadbutton_attachments'})['href']
    )
    sha1_hash = hashlib.sha1()
    sha1_hash.update(thread_title)
    torrent_filename_location = settings.TORRENT_FILE_DOWNLOAD_DIR + "/" + sha1_hash.hexdigest() + '.torrent'
    with open(torrent_filename_location, 'w') as f:
        f.write(torrent.read())
    return torrent_filename_location

def get_movie_choices(current_list):
    movie_choice = ''
    while movie_choice != 'q':
        movie_choice = raw_input("Please enter your choice (q/#): ")
        if movie_choice.isdigit() and int(movie_choice) > 0 and int(movie_choice) < len(current_list):
            os.system(
                "transmission-remote -n " + '\'' + settings.TRANSMISSION_USERNAME + ':' + settings.TRANSMISSION_PASSWORD + '\'' + " -a " +
                save_torrent_to_disk(current_list.keys()[int(movie_choice)-1], current_list[current_list.keys()[int(movie_choice)-1]])
            )
        else:
            print 'Invalid response - "q" to exit choice / enter a number to download'
        clear_lines(2)

def scrape_page(CURRENT_PAGE_NO):
    soup = get_html(settings.SHAANIG_URL + str(CURRENT_PAGE_NO)  + '.html')
    return {
        thread.find('a', {'class': 'title'}).string: thread.find('a', {'class': 'title'})['href']
        for thread in soup.body.find('ol', {'id': 'threads'}).find_all('li', {'class': 'threadbit'})
    }

def main():
    USER_RESPONSE = ''
    CURRENT_PAGE_NO = 1
    THREAD_LIST = {}

    # Make download dir if it doesn't exist
    if not os.path.exists(settings.TORRENT_FILE_DOWNLOAD_DIR):
        os.makedirs(settings.TORRENT_FILE_DOWNLOAD_DIR)

    # Run program until user wants to quit
    while USER_RESPONSE != 'q':
        current_list = THREAD_LIST[CURRENT_PAGE_NO] if THREAD_LIST.has_key(CURRENT_PAGE_NO) else scrape_page(CURRENT_PAGE_NO)
        if not THREAD_LIST.has_key(CURRENT_PAGE_NO):
            THREAD_LIST.update({
                CURRENT_PAGE_NO:current_list
            })
        for movie in current_list.keys():
            print '[' + str(current_list.keys().index(movie)+1) + '] ' + movie
        get_movie_choices(current_list)
        USER_RESPONSE = ''
        while USER_RESPONSE not in ['n', 'p', 'q'] and not USER_RESPONSE.isdigit():
            USER_RESPONSE = raw_input("What page? (n/p/#/q): ")
            if USER_RESPONSE in ['n', 'p']:
                CURRENT_PAGE_NO += 1 if USER_RESPONSE == 'n' else -1
            elif USER_RESPONSE.isdigit():
                CURRENT_PAGE_NO = int(USER_RESPONSE)
            elif USER_RESPONSE != 'q':
                print 'Invalid response - "n" next page/ "p" previous page/ enter a page number/ "q" to exit program'
            clear_lines(2)
        clear_lines(len(current_list))

if __name__ == "__main__":
    sys.exit(main())
