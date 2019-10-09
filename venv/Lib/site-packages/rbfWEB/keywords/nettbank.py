# Copyright 2019-     DNB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import types
import requests

from selenium import webdriver

from rbfWEB.base import keyword, LibraryComponent
from rbfWEB.locators import WindowManager
from rbfWEB.utils import (is_truthy, is_noney, secs_to_timestr,
                                   timestr_to_secs)

from .webdrivertools import WebDriverCreator
from .waiting import WaitingKeywords
from .element import ElementKeywords

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class NettbankKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._window_manager = WindowManager(ctx)

       
    @keyword
    def DNB_get_OTP_for_Uten_BankID(self, serialNumber, url=None):
        
        """Generates a new OTP for Uten Bank ID Authentication for GO3 & DP250 devices for the given ``serialNumber``. 
        
        ``url`` & ``alias`` are Optional 
        
        Examples:
        | `DNBGet Otp With Gogo` | 24299558 |
        | `Get Otp With Gogo` | 24299558 | http://e41ap027.erf01.net:8080/getOtp/jsp/getCode.servlet |
        | `Get Otp With Gogo` | 24299558 | http://e41ap027.erf01.net:8080/getOtp/jsp/getCode.servlet | getOTP |    
        
        """
        if url is None:
            formattedURL="http://e41ap027.erf01.net:8080/getOtp/jsp/getCode.servlet"+"?"+"serialNumber="+serialNumber+"&GoGo=GoGo"
        if url is not None:
            formattedURL=url+"?"+"serialNumber="+serialNumber+"&GoGo=GoGo"
        # browser='headlesschrome'
        # self.info("Opening browser '%s' to base url '%s'." % (browser, formattedURL))
        # driver = self._make_driver(browser)
        # try:
            # driver.get(formattedURL)
        # except Exception:
            # self.ctx.register_driver(driver, alias)
            # self.debug("Opened browser with session id %s but failed "
                       # "to open url '%s'." % (driver.session_id, formattedURL))
            # raise
        # self.debug('Opened browser with session id %s.' % driver.session_id)
        # self.ctx.register_driver(driver, alias)
        # self.generatedText=self.find_element('//*[text()[contains(., \'OTP Code\')]]').text
        # self.otp=self._get_substring(self.generatedText, -6)
        # self.formattedOTP=self._format_OTP(self.otp)
        # self.close_browser()
        # return self.formattedOTP
        
        self.info("Making a POST call to '%s'." % (formattedURL))
        response = requests.post(url = formattedURL)
        responseString = str(response.text)
        self.otp = responseString.partition("OTP Code ")[2][:6]
        self.formattedOTP=self._format_OTP(self.otp)
        return self.formattedOTP
        
    @keyword
    def open_browser(self, url, browser='firefox', alias=None,
                     remote_url=False, desired_capabilities=None,
                     ff_profile_dir=None):
        """Opens a new browser instance to the given ``url``.

        The ``browser`` argument specifies which browser to use, and the
        supported browser are listed in the table below. The browser names
        are case-insensitive and some browsers have multiple supported names.

        |    = Browser =    |        = Name(s) =       |
        | Firefox           | firefox, ff              |
        | Google Chrome     | googlechrome, chrome, gc |
        | Headless Firefox  | headlessfirefox          |
        | Headless Chrome   | headlesschrome           |
        | Internet Explorer | internetexplorer, ie     |
        | Edge              | edge                     |
        | Safari            | safari                   |
        | Opera             | opera                    |
        | Android           | android                  |
        | Iphone            | iphone                   |
        | PhantomJS         | phantomjs                |
        | HTMLUnit          | htmlunit                 |
        | HTMLUnit with Javascript | htmlunitwithjs    |

        To be able to actually use one of these browsers, you need to have
        a matching Selenium browser driver available. Headless Firefox and
        Headless Chrome require Selenium 3.8.0 or newer.

        Optional ``alias`` is an alias given for this browser instance and
        it can be used for switching between browsers. An alternative
        approach for switching is using an index returned by this keyword.
        These indices start from 1, are incremented when new browsers are
        opened, and reset back to 1 when `Close All Browsers` is called.
        See `Switch Browser` for more information and examples.

        Optional ``remote_url`` is the URL for a
        [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid].

        Optional ``desired_capabilities`` can be used to configure, for example,
        logging preferences for a browser or a browser and operating system
        when using [http://saucelabs.com|Sauce Labs]. Desired capabilities can
        be given either as a Python dictionary or as a string in format
        ``key1:value1,key2:value2``.
        [https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities|
        Selenium documentation] lists possible capabilities that can be
        enabled.

        Optional ``ff_profile_dir`` is the path to the Firefox profile
        directory if you wish to overwrite the default profile Selenium
        uses. 

        Examples:
        | `Open Browser` | http://example.com | Chrome  |
        | `Open Browser` | http://example.com | Firefox | alias=Firefox |
        | `Open Browser` | http://example.com | Edge    | remote_url=http://127.0.0.1:4444/wd/hub |

        If the provided configuration options are not enough, it is possible
        to use `Create Webdriver` to customize browser initialization even
        more.

        Applying ``desired_capabilities`` argument also for local browser is
        
        """
        if is_truthy(remote_url):
            self.info("Opening browser '%s' to base url '%s' through "
                      "remote server at '%s'." % (browser, url, remote_url))
        else:
            self.info("Opening browser '%s' to base url '%s'." % (browser, url))
        driver = self._make_driver(browser, desired_capabilities,
                                   ff_profile_dir, remote_url)
        try:
            driver.get(url)
        except Exception:
            self.ctx.register_driver(driver, alias)
            self.debug("Opened browser with session id %s but failed "
                       "to open url '%s'." % (driver.session_id, url))
            raise
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return self.ctx.register_driver(driver, alias)


    
    def _wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until ``text`` appears on current page.

        Fails if ``timeout`` expires before the text appears. See
        the `Timeouts` section for more information about using timeouts
        and their default value.

        ``error`` can be used to override the default error message.
        """
        self._wait_until(lambda: self.is_text_present(text),
                         "Text '%s' did not appear in <TIMEOUT>." % text,
                         timeout, error)
    
    
    def _wait_until(self, condition, error, timeout=None, custom_error=None):
        timeout = self.get_timeout(timeout)
        if is_noney(custom_error):
            error = error.replace('<TIMEOUT>', secs_to_timestr(timeout))
        else:
            error = custom_error
        self._wait_until_worker(condition, timeout, error)
    
    
    def _wait_until_worker(self, condition, timeout, error):
        max_time = time.time() + timeout
        not_found = None
        while time.time() < max_time:
            try:
                if condition():
                    return
            except ElementNotFound as err:
                not_found = str(err)
            except StaleElementReferenceException as err:
                self.info('Suppressing StaleElementReferenceException from Selenium.')
                not_found = err
            else:
                not_found = None
            time.sleep(0.2)
        raise AssertionError(not_found or error)
        
    
    def _make_driver(self, browser, desired_capabilities=None,
                     profile_dir=None, remote=None):
        driver = WebDriverCreator(self.log_dir).create_driver(
            browser=browser, desired_capabilities=desired_capabilities,
            remote_url=remote, profile_dir=profile_dir)
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        if self.ctx.speed:
            self._monkey_patch_speed(driver)
        return driver

    def _monkey_patch_speed(self, driver):
        def execute(self, driver_command, params=None):
            result = self._base_execute(driver_command, params)
            speed = self._speed if hasattr(self, '_speed') else 0.0
            if speed > 0:
                time.sleep(speed)
            return result
        if not hasattr(driver, '_base_execute'):
            driver._base_execute = driver.execute
            driver.execute = types.MethodType(execute, driver)
        driver._speed = self.ctx.speed
        
    def _get_substring(self, string, start, end=None):
        """Returns a substring from ``start`` index to ``end`` index.

        The ``start`` index is inclusive and ``end`` is exclusive.
        Indexing starts from 0, and it is possible to use
        negative indices to refer to characters from the end.

        Examples:
        | ${ignore first} = | Get Substring | ${string} | 1  |    |
        | ${ignore last} =  | Get Substring | ${string} |    | -1 |
        | ${5th to 10th} =  | Get Substring | ${string} | 4  | 10 |
        | ${first two} =    | Get Substring | ${string} |    | 1  |
        | ${last two} =     | Get Substring | ${string} | -2 |    |
        """
        start = self._convert_to_index(start, 'start')
        end = self._convert_to_index(end, 'end')
        return string[start:end]
    
    def _convert_to_index(self, value, name):
        if value == '':
            return 0
        if value is None:
            return None
        return self._convert_to_integer(value, name)

    
    def _convert_to_integer(self, value, name):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Cannot convert '%s' argument '%s' to an integer."
                             % (name, value))
    
    

    def _format_OTP(self, otp):
        formattedOTP = ''
        for i in otp:
            if i in '0123456789':
                formattedOTP+=i
    
        while (len(formattedOTP)<6):
            num = '0'+formattedOTP        
        return formattedOTP   
    
    
    def close_browser(self):
        """Closes the current browser."""
        if self.drivers.current:
            self.debug('Closing browser with session id {}.'
                       .format(self.driver.session_id))
            self.drivers.close()

