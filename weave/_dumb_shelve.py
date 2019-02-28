from shelve import Shelf
import collections
try:
    import zlib
except ImportError:
    zlib = None

class ZlibMapping(collections.MutableMapping):
    """Mapping adapter that applies zlib compression.
    """

    def __init__(self, dict):
        self.dict = dict
        if hasattr(dict, 'close'):
            self.close = dict.close
        if hasattr(dict, 'sync'):
            self.sync = dict.sync
        if hasattr(dict, 'keys'):
            self.keys = dict.keys

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __contains__(self, key):
        return key in self.dict

    def __getitem__(self, key):
        return zlib.decompress(self.dict[key])

    def __setitem__(self, key, value):
        self.dict[key] = zlib.compress(value)

    def __delitem__(self, key):
        del self.dict[key]


def open(filename, flag='c'):
    """Open a persistent dictionary for reading and writing.

    The filename parameter is the base filename for the underlying
    database.  As a side-effect, an extension may be added to the
    filename and more than one file may be created.  The optional flag
    parameter has the same interpretation as the flag parameter of
    dbm.open().
    """
    writeback = False

    from . import _dumbdbm_patched
    d = _dumbdbm_patched.open(filename, flag)
    return Shelf(ZlibMapping(d) if zlib is not None else d)
