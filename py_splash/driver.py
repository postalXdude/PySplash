try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from .static import (
    LUA_SOURCE,
    GET_ALL_DATA,
    RETURN_ALL_DATA,
    PREPARE_COOKIES,
    JS_PIECE,
    SET_PROXY,
    GO
)


class Driver(object):
    def __init__(self, splash_url='http://127.0.0.1:8050', proxy=None, proxy_user_pass=None, proxy_type=None):
        """
        :param splash_url:      Url to target running splash container. It can be on local or external machine.
                                Defaults to local machine.
        :param proxy:           Proxy server that will be used by splash ('example.com:8080').
        (optional)
        :param proxy_user_pass: If the proxy server requires authentication, send username and password in this
        (optional)              format - 'user:pass'. If there is no password - 'user:'.
        :param proxy_type:      Type of proxy server. It can be 'HTTP' or 'SOCKS5'. This param is ignoring lower case.
        (optional)              It can be 'http' or 'HtTp'. Defaults to 'HTTP'.
        """
        self.splash_url = '{}/execute'.format(splash_url)
        self.proxy = proxy
        self.proxy_user_pass = proxy_user_pass
        self.proxy_type = proxy_type

    def wait_for_condition(self, url=None, condition='no_condition', timeout=20, wait=0.5, backup_wait=None,
                           post=None, cookies=None, headers=None, full_info=False):
        """
        :param url:         Url for splash to target desired resource.
        :param condition:   List of xpath expressions ["//td[@class='splash']", etc.] on which splash will wait.
        (optional)          Or it can be custom js code. It needs to return True or False.
                            If never fulfilled, timeout occurs.
                            If not set, defaults to True.
        :param timeout:     Amount of time in seconds, until splash stops loading page and throws timeout error.
        :param wait:        Amount of time in seconds, for how long will splash wait and
                            check if condition is fulfilled.
        :param backup_wait: If condition is fulfilled, and data is still not there (Tested this with really slow
        (optional)          proxies) use this param to add extra seconds to wait after condition is fulfilled.
        :param post:        Post data to be sent for POST request. Dictionary {'user': 'bla', 'pass': 'bla'}.
        (optional)          Or it can be just JSON string or any other string format. In this case headers must be
                            set up to match string type. If JSON - headers={["content-type"]="application/json"}, etc.
        :param cookies:     Custom cookies in form of dictionary that will be used in request.
        (optional)
        :param headers:     Custom headers in form of dictionary that will be used in request.
        (optional)
        :param full_info:   If set to True, function will return html, cookies, headers, current url, and status code.
        (optional)
        :return:            It can return page content or full_info.
        """

        prepared_data = self._prepare_data_for_request(post, headers, cookies)

        condition_piece = JS_PIECE

        if type(condition) is list and condition:
            condition_source = [condition_piece.format(xpath.replace('[', '\\[').replace(']', '\\]')).strip('\n')
                                for xpath in condition]
            condition_source = ' '.join(condition_source)[:-22]
        elif type(condition) is str and condition:
            if condition == 'no_condition':
                condition_source = 'return true;'
            else:
                condition_pieces = condition.split('\n')
                condition_pieces = [piece.strip() for piece in condition_pieces]
                condition_source = ' '.join(condition_pieces).replace("'", "\\'")
        else:
            raise ValueError("Function must receive a list of xpath expressions or custom js code!")

        return_data = '{}return html'.format('\t' * 5)
        if full_info:
            return_data = RETURN_ALL_DATA

        js_start = 'document.evaluate(' if type(condition) is list else '(function(){'
        js_end = '' if type(condition) is list else '})();'

        lua_source = LUA_SOURCE.format(
            prepared_data,
            '\'' if type(condition) is str else '[[',
            '{} {} {}'.format(js_start, condition_source, js_end),
            '\'' if type(condition) is str else ']]',
            '{}splash:wait({})'.format('\t' * 5, backup_wait) if backup_wait else '',
            GET_ALL_DATA if full_info else '{}local html = splash:html()'.format('\t' * 5),
            return_data
        )

        return '{}?lua_source={}&url={}&timeout={}&wait={}'.format(
            self.splash_url,
            quote_plus(lua_source),
            quote_plus(url),
            quote_plus(str(timeout)),
            quote_plus(str(wait))
        )

    def _prepare_data_for_request(self, post, headers, cookies, images_enabled=False):
        prepared_data = []
        form_data = True

        if images_enabled:
            prepared_data.append('{}splash.images_enabled = true\n'.format('\t' * 5))
        else:
            prepared_data.append('{}splash.images_enabled = false\n'.format('\t' * 5))

        if self.proxy:
            proxy_init = []
            host = self.proxy[:self.proxy.rfind(':')]
            port = self.proxy[self.proxy.rfind(':') + 1:]
            proxy_init.append('{}host = "{}",\n{}port = {},'.format('\t' * 7, host, '\t' * 7, port))

            if self.proxy_user_pass:
                username = self.proxy_user_pass[:self.proxy_user_pass.find(':')]
                password = self.proxy_user_pass[self.proxy_user_pass.find(':') + 1:]
                proxy_init.append('{}username = "{}",\n{}password = "{}",'.format(
                    '\t' * 7, username, '\t' * 7, password.replace('"', '\\"')))

            if self.proxy_type:
                proxy_init.append('{}type = "{}",'.format('\t' * 7, self.proxy_type.upper()))

            proxy_init[-1] = proxy_init[-1].rstrip(',')

            prepared_data.append(SET_PROXY.format('{', '\n'.join(proxy_init), '}'))

        if type(post) is dict and post:
            post = Driver._prepare_lua_table('post', post)
            prepared_data.append(post)
        elif type(post) is str and post:
            form_data = False
            body = '''
                    local body = '{}'
            '''.format(post.replace("'", "\\'"))
            prepared_data.append(body)

        if type(headers) is dict and headers:
            headers = Driver._prepare_lua_table('headers', headers)
            prepared_data.append(headers)

        if type(cookies) is dict and cookies:
            table_values = ["{}{}name='{}', value='{}'{},".format(
                '\t' * 6,
                '{',
                name.replace("'", "\\'"),
                str(value).replace("'", "\\'") if value else '',
                '}'
            )
                for name, value in cookies.items()]

            table_values[-1] = table_values[-1].rstrip(',')
            cookies = PREPARE_COOKIES.format('{', '\n'.join(table_values), '}')
            prepared_data.append(cookies)

        prepared_data.append(GO.format(
            '{',
            'headers' if headers else 'nil',
            'POST' if post else 'GET',
            'body' if post and not form_data else 'nil',
            'post' if post and form_data else 'nil',
            '}'
        ))

        return '\n'.join(prepared_data)

    @staticmethod
    def _prepare_lua_table(data_type, data):
        table_skeleton = '''
                    local {} = {}
{}
                    {}
                    '''

        table_values = ["{}['{}'] = '{}',".format(
            '\t' * 6,
            name.replace("'", "\\'"),
            str(value).replace("'", "\\'") if value else '',
        )
            for name, value in data.items()]

        table_values[-1] = table_values[-1].rstrip(',')

        return table_skeleton.format(data_type, '{', '\n'.join(table_values), '}')
