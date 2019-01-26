from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.common.keys import Keys
import time
import sys

# driver = webdriver.Firefox()
# driver.get("http://www.facebook.com")
# assert "Facebook" in driver.title
# elem = driver.find_element_by_id("email")
# elem.send_keys(user)
# elem = driver.find_element_by_id("pass")
# elem.send_keys(pwd)
# elem.send_keys(Keys.RETURN)
# time.sleep(10)
# driver.close()

# myProxy = "localhost"
# myProxyPort = 9090

# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'httpProxyPort': myProxyPort,
#     'sslProxy': myProxy,
#     'sslProxyPort': myProxyPort
#     })

    # ,
    # 'noProxy': '' # set this value as desired

# profile = webdriver.FirefoxProfile() 
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", "54.213.66.208")
# profile.set_preference("network.proxy.http_port", 80)
# profile.update_preferences() 
# driver = webdriver.Firefox(profile)
PROXY = 'localhost:9090'
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
