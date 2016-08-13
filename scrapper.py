import urllib2
from bs4 import BeautifulSoup

page = urllib2.urlopen('https://www.shaanig.org/f30/index1.html')
soup = BeautifulSoup(page, 'lxml')

threads = soup.body.find('ol', {'id': 'threads'})
movie_list = {thread.find('a', {'class': 'title'}).string: thread.find('a', {'class': 'title'})['href'] for thread in threads.find_all('li', {'class': 'threadbit'})}
for movie in movie_list.keys():
    print '[' + str(movie_list.keys().index(movie)+1) + '] ' + movie
movie_choice = raw_input("Please enter your choice: ")
print movie_list[movie_list.keys()[int(movie_choice)-1]]
