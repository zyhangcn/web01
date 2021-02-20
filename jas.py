import argparse
import importlib
import os
import sys

from functools import wraps

from six.moves.urllib_parse import urlencode
from six.moves import urllib_parse as urlparse

def first(kk):
    def our(func):
        @wraps(func)
        def inner():
            func(kk)
            jss = "asdasd"
            return jss
        return inner
    return our

@first("kk")
def mainss(kk):
    print(kk)
    return "asdas"

print(mainss().upper())
print(dir(mainss))
print(type(mainss))
next_page = '/?kk=sadsa&as=asds'
next_page_decode = urlparse.unquote_plus(next_page)
next_host = urlparse.urlparse(next_page_decode).netloc

print(next_page)
print(next_host)
print(next_page_decode)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', help=u'方法指向的路径， 如 foo.bar  即 foo文件的bar函数')
parser.add_argument('args', nargs='*', help=u'函数的参数', default='')
parser = parser.parse_args()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
# This allows easy placement of apps within the interior
# datalake_backend directory.
# current_path = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(current_path, "apps"))
def import_module(dotted_path):
    dotted_path = dotted_path.replace('/', '.')
    module_parts = dotted_path.split('.')
    if len(module_parts) < 2:
        module_parts.append('main')  # 默认调用main函数
    if len(module_parts) == 2:
        module_parts.insert(0, 'utility')  # 默认调用utility/下的文件

    print(module_parts)
    module_path = ".".join(module_parts[:-1])
    print(module_path)
    module = importlib.import_module(module_path)
    return getattr(module, module_parts[-1])

def main():

    path,args =  parser.path,parser.args or []
    print(path,args)
    import_module(path)

if __name__ == '__main__':
    main()