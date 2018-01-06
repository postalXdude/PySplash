class SplashError(Exception):
    pass

class SplashTimeoutError(SplashError):
    pass


class SplashRenderError(SplashError):
    pass


class SplashInternalError(SplashError):
    pass


class SplashUnsupportedContentTypeError(SplashError):
    pass


class SplashBadRequestError(SplashError):
    pass


class SplashSyntaxError(SplashError):
    pass
