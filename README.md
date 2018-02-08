# PySplash

- Small interface for splash written in python.<br />
*https://github.com/scrapinghub/splash*

- Idea is to look similar to Ghost.py and Dryscrape.<br />
https://github.com/jeanphix/Ghost.py<br />
https://github.com/niklasb/dryscrape

## Usage examples
``` python
from py_splash.driver import Driver

splash_driver = Driver()

url_to_go = splash_driver.load_url(url=url, wait=5)
```

Rendering page for 5 seconds and returns result.

---
``` python
from py_splash.driver import Driver

splash_driver = Driver()

url = 'random_url'
condition = [
    "//div[@class='splash']",
    "//a[@href='PySplash']"
]

url_to_go = splash_driver.load_url(url=url, condition=condition)
```

In example above lua script is generated and added to url_to_go as query param.
That url contains all info needed for splash to wait for desired html tags that are added in condition.

---
``` python
from py_splash.driver import Driver

splash_driver = Driver()

url = 'random_url'
condition = '''
link = document.getElementsByClassName("icon-flight-bookings").item('icon-flight-bookings');
if (link !== null) {
    link.click();
    return true;
}

return false;
'''

url_to_go = splash_driver.load_url(url=url, condition=condition)
```

Same as the second example, except in this case javascript is used as condition.
This can be used for specific cases when it is impossible to wait for tags in html.
For example, wait for certain cookie to initialize, header, etc.

## Requirements
Latest splash version and any version of python after 2.7 .

## Installation
```pip install py-splash```

## ToDo
- take screenshot

## Docs
For now there is no docs. <br />
For detailed info go to [here](./py_splash/driver.py) .

## [Changelog](./CHANGELOG.md)
