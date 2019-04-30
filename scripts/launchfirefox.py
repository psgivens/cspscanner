from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import sys

PROXY = 'localhost:9090'
PROXY = 'ubu-bb-psgivens:9090'

webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "proxyType":"MANUAL"
}

driver = webdriver.Firefox()
driver.get("http://mitm.it")    

print ("Press enter to close proxied firefox session.")
sys.stdin.readline()
driver.quit ()
