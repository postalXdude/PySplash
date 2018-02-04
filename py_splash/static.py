LUA_SOURCE = '''
function main(splash)
    splash.resource_timeout = splash.args.timeout

{}

    local condition = false

    while not condition do
        splash:wait(splash.args.wait)
        condition = splash:evaljs({}{}{})
    end

{}

{}

    splash:runjs("window.close()")

{}

end
'''

GO = '\tassert(splash:go{}splash.args.url, baseurl=nil, headers={}, http_method="{}", body={}, formdata={}{})' \
    .format(*['{}'] * 6)

JS_PIECE = '`{}`, document, null, XPathResult.BOOLEAN_TYPE, null).booleanValue || document.evaluate('

USER_AGENT = '\tsplash:set_user_agent(\'{}\')'

GET_HTML_ONLY = '\tlocal html = splash:html()'

RETURN_HTML_ONLY = '\treturn html'

GET_ALL_DATA = '''
    local entries = splash:history()
    local last_response = entries[#entries].response
    local url = splash:url()
    local headers = last_response.headers
    local http_status = last_response.status
    local cookies = splash:get_cookies()
'''

RETURN_ALL_DATA = '''
    return {
        url = splash:url(),
        headers = last_response.headers,
        http_status = last_response.status,
        cookies = splash:get_cookies(),
        html = splash:html(),
    }
'''

PREPARE_COOKIES = '''
    splash:init_cookies({}
{}
    {})
'''

SET_PROXY = '''
    splash:on_request(function(request)
        request:set_proxy{}
{}
        {}
    end)
'''
