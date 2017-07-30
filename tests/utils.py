import sys
from cStringIO import StringIO
from yledl import download, StreamFilters, BackendFactory, IOContext, \
    StreamAction, RD_SUCCESS


# Context manager for capturing stdout output. See
# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def fetch_title(url):
    return fetch(url, StreamAction.PRINT_STREAM_TITLE)


def fetch_stream_url(url):
    return fetch(url, StreamAction.PRINT_STREAM_URL)


def fetch_episode_pages(url):
    return fetch(url, StreamAction.PRINT_EPISODE_PAGES)


def fetch(url, action):
    backends = [BackendFactory(BackendFactory.ADOBEHDSPHP)]
    basic_filters = StreamFilters(
        latest_only=False,
        audiolang='',
        sublang='all',
        hardsubs=False,
        maxbitrate=0,
        duration=None)
    io = IOContext(
        outputfilename=None,
        destdir='/tmp/',
        resume=False,
        ratelimit=None,
        excludechars='*/|',
        proxy = None)

    with Capturing() as output:
        res = download(url,
                       action,
                       io,
                       stream_filters = basic_filters,
                       backends = backends,
                       postprocess_command = None)
        assert res == RD_SUCCESS

    return output