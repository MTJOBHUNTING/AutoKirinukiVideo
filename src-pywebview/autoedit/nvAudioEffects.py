"""
以下のコードは ctypesgen を使用して生成されました。

そのため、コメント文がありません。
"""
__docformat__ = "restructuredtext"

import ctypes, os, sys
from ctypes import *
from autoedit.settings import S_NVAFX_DIR_PATH

_int_types = (c_int16, c_int32)
if hasattr(ctypes, "c_int64"):
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types


class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, Union):

    _fields_ = [("raw", POINTER(c_char)), ("data", c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        elif isinstance(obj, String):
            return obj

        elif isinstance(obj, bytes):
            return cls(obj)

        elif isinstance(obj, str):
            return cls(obj.encode())

        elif isinstance(obj, c_char_p):
            return obj

        elif isinstance(obj, POINTER(c_char)):
            return obj

        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        elif isinstance(obj, c_char * len(obj)):
            return obj

        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return c_void_p

class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

_libs = {}
_libdirs = []

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util


def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []


import win32api
import win32con
class LibraryLoader(object):
    name_formats = ["%s"]

    class Lookup(object):
        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            dll_handle = None
            if os.path.isfile(path):
                dll_handle = win32api.LoadLibraryEx(path, 0, win32con.LOAD_WITH_ALTERED_SEARCH_PATH)
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode, handle=dll_handle))

        def get(self, name, calling_convention="cdecl"):
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        paths = self.getpaths(libname)

        for path in paths:
            try:
                return self.Lookup(path)
            except:
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        if os.path.isabs(libname):
            yield libname
        else:
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    yield os.path.join(dir_i, fmt % libname)

            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            for path in self.getplatformpaths(libname):
                yield path

            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, libname):
        return []

class DarwinLibraryLoader(LibraryLoader):
    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir, name)

    def getdirs(self, libname):
        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser("~/lib"), "/usr/local/lib", "/usr/lib"]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        if hasattr(sys, "frozen") and sys.frozen == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    class _Directories(dict):
        def __init__(self):
            self.order = 0

        def add(self, directory):
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            if not os.path.exists(directory):
                return
            o = self.setdefault(directory, self.order)
            if o == self.order:
                self.order += 1

        def extend(self, directories):
            for d in directories:
                self.add(d)

        def ordered(self):
            return (i[0] for i in sorted(self.items(), key=lambda D: D[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        try:
            with open(conf) as f:
                for D in f:
                    D = D.strip()
                    if not D:
                        continue

                    m = self._include.match(D)
                    if not m:
                        dirs.add(D)
                    else:
                        for D2 in glob.glob(m.group("pattern")):
                            self._get_ld_so_conf_dirs(D2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",
            "LIBPATH",
            "LIBRARY_PATH",
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            if bitage.startswith("32"):
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                unix_lib_dirs_list += ["/lib/x86_64-linux-gnu", "/usr/lib/x86_64-linux-gnu"]
            else:
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        ext_re = re.compile(r"\.s[ol]$")
        for dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            yield i

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    for F in other_dirs:
        if not os.path.isabs(F):
            F = os.path.abspath(F)
        load_library.other_dirs.append(F)


del loaderclass

add_library_search_dirs([str(S_NVAFX_DIR_PATH.absolute())])
_libs["NVAudioEffects"] = load_library('NVAudioEffects')

enum_anon_3 = c_int

NVAFX_STATUS_SUCCESS = 0

NVAFX_STATUS_FAILED = 1

NVAFX_STATUS_INVALID_HANDLE = 2

NVAFX_STATUS_INVALID_PARAM = 3

NVAFX_STATUS_IMMUTABLE_PARAM = 4

NVAFX_STATUS_INSUFFICIENT_DATA = 5

NVAFX_STATUS_EFFECT_NOT_AVAILABLE = 6

NVAFX_STATUS_OUTPUT_BUFFER_TOO_SMALL = 7

NVAFX_STATUS_MODEL_LOAD_FAILED = 8

NVAFX_STATUS_32_SERVER_NOT_REGISTERED = 9

NVAFX_STATUS_32_COM_ERROR = 10

NVAFX_STATUS_GPU_UNSUPPORTED = 11

NvAFX_Status = enum_anon_3

NvAFX_Bool = c_char

NvAFX_EffectSelector = String

NvAFX_ParameterSelector = String

NvAFX_Handle = POINTER(None)

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetEffectList", "cdecl"):
        continue
    NvAFX_GetEffectList = _lib.get("NvAFX_GetEffectList", "cdecl")
    NvAFX_GetEffectList.argtypes = [POINTER(c_int), POINTER(POINTER(NvAFX_EffectSelector))]
    NvAFX_GetEffectList.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_CreateEffect", "cdecl"):
        continue
    NvAFX_CreateEffect = _lib.get("NvAFX_CreateEffect", "cdecl")
    NvAFX_CreateEffect.argtypes = [NvAFX_EffectSelector, POINTER(NvAFX_Handle)]
    NvAFX_CreateEffect.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_CreateChainedEffect", "cdecl"):
        continue
    NvAFX_CreateChainedEffect = _lib.get("NvAFX_CreateChainedEffect", "cdecl")
    NvAFX_CreateChainedEffect.argtypes = [NvAFX_EffectSelector, POINTER(NvAFX_Handle)]
    NvAFX_CreateChainedEffect.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_DestroyEffect", "cdecl"):
        continue
    NvAFX_DestroyEffect = _lib.get("NvAFX_DestroyEffect", "cdecl")
    NvAFX_DestroyEffect.argtypes = [NvAFX_Handle]
    NvAFX_DestroyEffect.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetU32", "cdecl"):
        continue
    NvAFX_SetU32 = _lib.get("NvAFX_SetU32", "cdecl")
    NvAFX_SetU32.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, c_uint]
    NvAFX_SetU32.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetU32List", "cdecl"):
        continue
    NvAFX_SetU32List = _lib.get("NvAFX_SetU32List", "cdecl")
    NvAFX_SetU32List.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(c_uint), c_uint]
    NvAFX_SetU32List.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetString", "cdecl"):
        continue
    NvAFX_SetString = _lib.get("NvAFX_SetString", "cdecl")
    NvAFX_SetString.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, String]
    NvAFX_SetString.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetStringList", "cdecl"):
        continue
    NvAFX_SetStringList = _lib.get("NvAFX_SetStringList", "cdecl")
    NvAFX_SetStringList.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(POINTER(c_char)), c_uint]
    NvAFX_SetStringList.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetFloat", "cdecl"):
        continue
    NvAFX_SetFloat = _lib.get("NvAFX_SetFloat", "cdecl")
    NvAFX_SetFloat.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, c_float]
    NvAFX_SetFloat.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_SetFloatList", "cdecl"):
        continue
    NvAFX_SetFloatList = _lib.get("NvAFX_SetFloatList", "cdecl")
    NvAFX_SetFloatList.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(c_float), c_uint]
    NvAFX_SetFloatList.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetU32", "cdecl"):
        continue
    NvAFX_GetU32 = _lib.get("NvAFX_GetU32", "cdecl")
    NvAFX_GetU32.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(c_uint)]
    NvAFX_GetU32.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetString", "cdecl"):
        continue
    NvAFX_GetString = _lib.get("NvAFX_GetString", "cdecl")
    NvAFX_GetString.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, String, c_int]
    NvAFX_GetString.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetStringList", "cdecl"):
        continue
    NvAFX_GetStringList = _lib.get("NvAFX_GetStringList", "cdecl")
    NvAFX_GetStringList.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(POINTER(c_char)), POINTER(c_int), c_uint]
    NvAFX_GetStringList.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetFloat", "cdecl"):
        continue
    NvAFX_GetFloat = _lib.get("NvAFX_GetFloat", "cdecl")
    NvAFX_GetFloat.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(c_float)]
    NvAFX_GetFloat.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetFloatList", "cdecl"):
        continue
    NvAFX_GetFloatList = _lib.get("NvAFX_GetFloatList", "cdecl")
    NvAFX_GetFloatList.argtypes = [NvAFX_Handle, NvAFX_ParameterSelector, POINTER(c_float), c_uint]
    NvAFX_GetFloatList.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_Load", "cdecl"):
        continue
    NvAFX_Load = _lib.get("NvAFX_Load", "cdecl")
    NvAFX_Load.argtypes = [NvAFX_Handle]
    NvAFX_Load.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_GetSupportedDevices", "cdecl"):
        continue
    NvAFX_GetSupportedDevices = _lib.get("NvAFX_GetSupportedDevices", "cdecl")
    NvAFX_GetSupportedDevices.argtypes = [NvAFX_Handle, POINTER(c_int), POINTER(c_int)]
    NvAFX_GetSupportedDevices.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_Run", "cdecl"):
        continue
    NvAFX_Run = _lib.get("NvAFX_Run", "cdecl")
    NvAFX_Run.argtypes = [NvAFX_Handle, POINTER(POINTER(c_float)), POINTER(POINTER(c_float)), c_uint, c_uint]
    NvAFX_Run.restype = NvAFX_Status
    break

for _lib in _libs.values():
    if not _lib.has("NvAFX_Reset", "cdecl"):
        continue
    NvAFX_Reset = _lib.get("NvAFX_Reset", "cdecl")
    NvAFX_Reset.argtypes = [NvAFX_Handle]
    NvAFX_Reset.restype = NvAFX_Status
    break

libc = cdll.msvcrt

malloc = libc.malloc
malloc.argtypes = [ctypes.c_size_t]
malloc.restype = ctypes.c_void_p

calloc = libc.calloc
calloc.argtypes = [ctypes.c_size_t, ctypes.c_size_t]
calloc.restype = ctypes.c_void_p

free = libc.free
free.argtypes = [ctypes.c_void_p]
free.restype = None

try:
    NVAFX_TRUE = 1
except:
    pass

try:
    NVAFX_FALSE = 0
except:
    pass

try:
    NVAFX_EFFECT_DENOISER = 'denoiser'
except:
    pass

try:
    NVAFX_EFFECT_DEREVERB = 'dereverb'
except:
    pass

try:
    NVAFX_EFFECT_DEREVERB_DENOISER = 'dereverb_denoiser'
except:
    pass

try:
    NVAFX_EFFECT_AEC = 'aec'
except:
    pass

try:
    NVAFX_EFFECT_SUPERRES = 'superres'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_DENOISER_16k_SUPERRES_16k_TO_48k = 'denoiser16k_superres16kto48k'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_DEREVERB_16k_SUPERRES_16k_TO_48k = 'dereverb16k_superres16kto48k'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_DEREVERB_DENOISER_16k_SUPERRES_16k_TO_48k = 'dereverb_denoiser16k_superres16kto48k'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_SUPERRES_8k_TO_16k_DENOISER_16k = 'superres8kto16k_denoiser16k'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_SUPERRES_8k_TO_16k_DEREVERB_16k = 'superres8kto16k_dereverb16k'
except:
    pass

try:
    NVAFX_CHAINED_EFFECT_SUPERRES_8k_TO_16k_DEREVERB_DENOISER_16k = 'superres8kto16k_dereverb_denoiser16k'
except:
    pass

try:
    NVAFX_PARAM_NUM_STREAMS = 'num_streams'
except:
    pass

try:
    NVAFX_PARAM_USE_DEFAULT_GPU = 'use_default_gpu'
except:
    pass

try:
    NVAFX_PARAM_USER_CUDA_CONTEXT = 'user_cuda_context'
except:
    pass

try:
    NVAFX_PARAM_DISABLE_CUDA_GRAPH = 'disable_cuda_graph'
except:
    pass

try:
    NVAFX_PARAM_ENABLE_VAD = 'enable_vad'
except:
    pass

try:
    NVAFX_PARAM_MODEL_PATH = 'model_path'
except:
    pass

try:
    NVAFX_PARAM_INPUT_SAMPLE_RATE = 'input_sample_rate'
except:
    pass

try:
    NVAFX_PARAM_OUTPUT_SAMPLE_RATE = 'output_sample_rate'
except:
    pass

try:
    NVAFX_PARAM_NUM_INPUT_SAMPLES_PER_FRAME = 'num_input_samples_per_frame'
except:
    pass

try:
    NVAFX_PARAM_NUM_OUTPUT_SAMPLES_PER_FRAME = 'num_output_samples_per_frame'
except:
    pass

try:
    NVAFX_PARAM_NUM_INPUT_CHANNELS = 'num_input_channels'
except:
    pass

try:
    NVAFX_PARAM_NUM_OUTPUT_CHANNELS = 'num_output_channels'
except:
    pass

try:
    NVAFX_PARAM_INTENSITY_RATIO = 'intensity_ratio'
except:
    pass

try:
    NVAFX_PARAM_DENOISER_MODEL_PATH = NVAFX_PARAM_MODEL_PATH
except:
    pass


try:
    NVAFX_PARAM_DENOISER_NUM_SAMPLES_PER_FRAME = NVAFX_PARAM_NUM_SAMPLES_PER_FRAME
except:
    pass

try:
    NVAFX_PARAM_DENOISER_INTENSITY_RATIO = NVAFX_PARAM_INTENSITY_RATIO
except:
    pass

try:
    NVAFX_PARAM_NUM_CHANNELS = 'num_channels'
except:
    pass

try:
    NVAFX_PARAM_DENOISER_NUM_CHANNELS = NVAFX_PARAM_NUM_CHANNELS
except:
    pass

try:
    NVAFX_PARAM_SAMPLE_RATE = 'sample_rate'
except:
    pass

try:
    NVAFX_PARAM_DENOISER_SAMPLE_RATE = NVAFX_PARAM_SAMPLE_RATE
except:
    pass

try:
    NVAFX_PARAM_NUM_SAMPLES_PER_FRAME = 'num_samples_per_frame'
except:
    pass

