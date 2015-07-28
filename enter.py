__author__ = 'yushiwei'

import sys
from magicyu.dianyingfm import movie

if __name__ == '__main__':
    cmd = sys.argv[0]
    param = sys.argv[1]

    if cmd == 'search':
        results = movie.search(param)
        movie.showSearch(results)
    elif cmd == 'detail':
        results = movie.movieDetail(param)
        movie.showDetail(results)