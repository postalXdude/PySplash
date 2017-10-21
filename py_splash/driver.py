try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


class Driver(object):
    def __init__(self, splash_url='http://localhost:8050/execute', headers=None):
        """
        :param splash_url:  Url to target running splash container. It can be on local or external machine.
                            Defaults to local machine.
        :param headers:     Custom headers in form of dictionary that will be always used through whole session.
        (optional)          Except, if they are overridden in some functions bellow.
        """
        self.splash_url = splash_url
        self.headers = headers

    def wait_for_condition(self, url=None, condition=None, timeout=10, wait=0.5, post=None, cookies=None, headers=None,
                           full_info=False, custom_js=None):
        # Todo url as condition (it should be possible if I understood it correctly from splash docs)
        """
        :param url:         Url for splash to target desired resource.
        :param condition:   List of xpath expressions ["//td[@class='splash']", etc.] or url, on which splash will wait.
                            If never fulfilled, timeout occurs.
        :param timeout:     Amount of time in seconds, until splash stops loading page.
        :param wait:        Amount of time in seconds, for how long will splash wait and
                            check if condition is fulfilled.
        :param post:        Post data to be sent for POST request. List of tuples [(user, bla),(pass, bla)]
        (optional)
        :param cookies:     Custom cookies in form of dictionary that will be used in request.
        (optional)
        :param headers:     Custom headers in form of dictionary that will be used in request.
        (optional)          If sent, they will override headers set up in __init__ .
        :param full_info:   If set to True, function will return html, cookies, headers, current url, etc.
        :param custom_js:   Custom js code that will be executed by lua script on splash machine.
        (optional)          It needs to return True or False.
        :return:            It can return html or full_info.
        """

        condition_piece = '''
                                    "{}",
                                    document,
                                    null,
                                    XPathResult.BOOLEAN_TYPE,
                                    null
                                ).booleanValue || document.evaluate('''

        js_start = ''
        condition_source = ''

        if custom_js:
            condition_source = custom_js

        if type(condition) is str:
            # ToDo
            pass
        elif type(condition) is list:
            js_start = '\t\t\t\t\t\tdocument.evaluate('
            condition_source = [condition_piece.format(xpath.replace('[', '\\[').replace(']', '\\]')).strip('\n')
                                for xpath in condition]
            condition_source = '\n'.join(condition_source)
            condition_source = '{}{}'.format(condition_source[:condition_source.rfind('booleanValue')], 'booleanValue')

        get_all_data = '''
                    local entries = splash:history()
                    local last_response = entries[#entries].response
                    local url = splash:url()
                    local headers = last_response.headers
                    local http_status = last_response.status
                    local cookies = splash:get_cookies()
        '''

        return_data = '\t\t\t\t\treturn html'
        if full_info:
            return_data = '''
                    return {
                        url = splash:url(),
                        headers = last_response.headers,
                        http_status = last_response.status,
                        cookies = splash:get_cookies(),
                        html = splash:html(),
                    }
            '''

        lua_source = '''
                function main(splash)
                    splash.resource_timeout = splash.args.timeout
                    splash.images_enabled = false

                    splash:go(splash.args.url)

                    local condition = false

                    while not condition do
                        splash:wait(splash.args.wait)
                        condition = splash:evaljs([[
{}
{}
                        ]])
                    end

                    local html = splash:html()
{}

                    splash:runjs("window.close()")

{}

                end
                '''.format(
            js_start,
            condition_source,
            get_all_data if full_info else '',
            return_data
        )

        return '{}?lua_source={}&url={}&timeout={}&wait={}{}{}{}'.format(
            self.splash_url,
            quote_plus(lua_source),
            quote_plus(url),
            quote_plus(str(timeout)),
            quote_plus(str(wait)),
            quote_plus(post if post else ''),
            quote_plus(cookies if cookies else ''),
            quote_plus(headers if headers else '')
        )

    # ToDo Check for errors ... if there is condition, custom script must be None etc,etc.
    def check_for_errors(self):
        pass
