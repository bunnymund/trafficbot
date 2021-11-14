import os
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from services import WinService


class Browser:
    def __init__(self):
        self.headless = False
        self.tor = WinService('tor')

    def create_browser(self):
        options = FirefoxOptions()
        # options.add_argument('-headless')
        options.headless = self.headless

        profile = FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference("general.useragent.override", self.useragent())
        profile.update_preferences()
        br = webdriver.Firefox(
            executable_path='drivers/geckodriver.exe',
            # firefox_binary=binary,
            firefox_profile=profile,
            firefox_options=options,
            service_log_path=os.devnull
        )

        if os.path.exists(self.binpath):
            br.binary = FirefoxBinary(self.binpath)

        return br

    def watch(self, url):
        if not self.alive:
            return

        try:
            br = self.create_browser()
            br.get(url)

            sleepTime = random.randint(self.min, self.max)
            [sleep(1) for _ in range(sleepTime) if self.alive]  # watching the video

            br.close()
            return True
        except:
            return

    def get_ip(self):
        ip = None
        try:
            br = self.create_browser()
            br.get('https://api.ipify.org/?format=text')
            sleep(0.5)

            ip = br.find_element_by_xpath('html').text
            br.close()
        except:
            pass
        finally:
            return ip

    def restart_tor(self):
        try:
            if not self.tor.restart():
                self.tor.start()
        except:
            print("ERROR: Tor Win32 Service Not Found")
            self.alive = False

        while not self.tor.running:
            sleep(0.5)

    def useragent(self):
        useragents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
            'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
            'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1']
        return random.choice(useragents)
