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

url = 'random_url'
condition = [
    "//div[@class='splash']",
    "//a[@href='PySplash']"
]

url_to_go = splash_driver.wait_for_condition(url=url, condition=condition)
```

In example above lua script is generated and added to splash_url as query param.
That url contains all info needed for splash to wait for desired html tags that are added in condition.

---
``` python
from py_splash.driver import Driver

splash_driver = Driver()

url = 'random_url'
condition = '''
var table = document.getElementById("forecast-table");
var cells = table.getElementsByTagName("td");

condition = false;

for (var i = 0; i < cells.length; i++) {
    var status = cells[i].getAttribute("data-status");
    if ( status == "open" ) {
        // check if something exists, if exists set condition to true
        condition = true;
        break;
    }
}

return condition;
'''

url_to_go = splash_driver.wait_for_condition(url=url, condition=condition)
```

Same as first example, except in this case javascript is used as condition.
This can be used for specific cases when it is impossible to wait for tags in html.
For example, wait for certain cookie to initialize, header, etc.

## Requirements
Latest splash version and any version of python after 2.7 .

## Installation
```pip install py-splash```

## ToDo
- add an option to wait for certain url (if possible)
- add methods for get and post request that will not load page content into browser

## Docs
For now there is no docs. <br />
For detailed info go to [here](./py_splash/driver.py) .

## Changelog
[click_me_baby xD](./CHANGELOG.md)
