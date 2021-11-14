"""
Trafficbot is a tool to rapidly improve traffic for website.
"""
import os
from argparse import ArgumentParser
from time import sleep

from browser import Browser
from taskqueue import TaskQueue


class Views(Browser):
    """
        Requirement: 
            Tor installed in your machine
            Firefox updated last
            Run as Admin
    """
    def __init__(self, urllist, visits, min, max, hidden=False):
        super().__init__()

        self.targets = {}
        self.alive = True
        self.ip = None
        self.count = 0
        self.queue = TaskQueue(3)
        self.binpath = os.path.join(os.environ["ProgramFiles"], r"Firefox Developer Edition\firefox.exe")
        self.headless = hidden
        self.min = int(min)
        self.max = int(max)
        self.visits = int(visits)

        if not os.path.isfile(urllist):
            exit('Error: Unable to locate `{}`'.format(urllist))

        with open(urllist, 'r') as f:
            try:
                for url in [_ for _ in f.read().split('\n') if _]:
                    self.targets[url] = 0
            except Exception as e:
                exit('Error: {}'.format(e))

    def visit(self, url):
        try:
            if self.watch(url):
                views = self.targets[url]
                self.targets[url] = views + 1
        except:
            pass
        finally:
            self.count -= 1

    def clear_screen(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def display(self, url):
        print('')
        print('[+] URL: {}'.format(url))
        print('[+] Proxy IP: {}'.format(self.ip))
        print('[+] Views: {}'.format(self.targets[url]))

    def exit(self):
        self.alive = False
        self.tor.stop()

    def run(self):
        closed_ip = list()

        while all([self.alive, len(self.targets)]):
            self.restart_tor()
            self.ip = self.get_ip()

            if any([not self.ip, self.ip in closed_ip]):
                continue

            urls = [_ for _ in self.targets.keys()]

            for url in urls:
                views = self.targets[url]
                if views < self.visits:
                    self.queue.add_task(self.visit, url)
                    self.count += 1
                else:
                    del self.targets[url]

            while self.count > 0:
                sleep(1)
                self.clear_screen()
                for url in self.targets:
                    self.display(url)

            closed_ip.append(self.ip)

        self.queue.join()
        self.exit()
        print('')
        print('Completed')


if __name__ == '__main__':

    args = ArgumentParser(description=__doc__)
    args.add_argument('--visits', help='The amount of visits (default=5)', type=int, default=5)
    args.add_argument('urllist', help='path of url list')
    args.add_argument('--min', help='Minimum watch time in seconds (default=20)', type=int, default=20)
    args.add_argument('--max', help='Maximum watch time in seconds (default=40)', type=int, default=40)
    args.add_argument('--hidden', help='the browser is running in background', action='store_true')

    args = args.parse_args()

    views = Views(args.urllist, args.visits, args.min, args.max, args.hidden)
    try:
        views.run()
    except Exception as e:
        import sys

        sys.exit('ERROR: {}'.format(e))
