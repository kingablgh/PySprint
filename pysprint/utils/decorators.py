import sys
import time
import threading
import re
from itertools import cycle
from functools import wraps, lru_cache
from copy import copy

import numpy as np

from pysprint.utils.misc import run_from_ipython


__all__ = [
    '_progress',
    'inplacify',
    '_mutually_exclusive_args',
    '_lazy_property',
    'pprint_disp',
]


_inplace_doc = """\n\tinplace : bool, optional
            Whether to apply the operation on the dataset in an "inplace" manner.
            This means if inplace is True it will apply the changes directly on
            the current dataset and returns None. If inplace is False, it will
            leave the current object untouched, but returns a copy of it, and
            the operation will be performed on the copy. It's useful when
            chaining operations on a dataset.\n\n\t"""


def _has_parameter_section(method):
    try:
        return "Parameters" in method.__doc__
    except TypeError:
        return False


def _update_doc(method, doc):
    if _has_parameter_section(method):
        newdoc = _build_doc(method, doc)
        method.__doc__ = newdoc
    else:
        newdoc = """\n\tParameters
        ----------\n\tinplace : bool, optional
            Whether to apply the operation on the dataset in an "inplace" manner.
            This means if inplace is True it will apply the changes directly on
            the current dataset and returns None. If inplace is False, it will
            leave the current object untouched, but returns a copy of it, and
            the operation will be performed on the copy. It's useful when
            chaining operations on a dataset.\n\n\t"""

        nodoc_head = (f"Docstring automatically created for {method.__name__}. "
                      "Parameter list may not be complete.\n")
        if method.__doc__ is not None:
            method.__doc__ += newdoc
        else:
            method.__doc__ = nodoc_head + newdoc
        return


def _build_doc(method, param):
    patt = r"(\w+(?=\s*[-]{4,}[^/]))"  # finding sections
    splitted_doc = re.split(patt, method.__doc__)
    try:
        target = splitted_doc.index("Parameters") + 1
    except ValueError:
        return method.__doc__

    splitted_doc[target] = splitted_doc[target].rstrip() + param

    return ''.join(_ for _ in splitted_doc if _ is not None)


def inplacify(method):
    """
    Decorator used to allow a class function to be called
    as `inplace` as well.
    """
    _update_doc(method, _inplace_doc)

    @wraps(method)
    def wrapper(self, *args, **kwds):
        inplace = kwds.pop("inplace", True)
        if inplace:
            method(self, *args, **kwds)
        else:
            return method(copy(self), *args, **kwds)

    return wrapper


def _progress(func):
    active = threading.Lock()

    def spinning_pbar_printer():
        symbols = ['|', '/', '-', '\\', '\\']
        cursor = cycle(symbols)
        while active.locked():
            sys.stdout.write("\r")
            sys.stdout.write("Working... " + next(cursor))
            sys.stdout.flush()
            time.sleep(0.1)

    def wrapper(*args, **kwargs):
        t = threading.Thread(target=spinning_pbar_printer)
        active.acquire()
        t.start()
        try:
            res = func(*args, **kwargs)
        finally:
            active.release()
        return res

    return wrapper


# https://stackoverflow.com/a/54487188/11751294
def _mutually_exclusive_args(keyword, *keywords):
    """
    Decorator to restrict the user to specify exactly one of the given parameters.
    Often used for std and fwhm for Gaussian windows.
    """
    keywords = (keyword,) + keywords

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if sum(k in keywords for k in kwargs) != 1:
                raise TypeError(
                    "You must specify exactly one of {}.".format(" and ".join(keywords))
                )
            return func(*args, **kwargs)

        return inner

    return wrapper


def _lazy_property(f):
    return property(lru_cache()(f))


def pprint_disp(f):
    """
    Pretty print the dispersion results from returned arrays.
    """
    @wraps(f)
    def wrapping(*args, **kwargs):
        disp, disp_std, stri = f(*args, **kwargs)
        labels = ("GD", "GDD", "TOD", "FOD", "QOD", "SOD")
        disp = np.trim_zeros(disp, "b")
        disp_std = disp_std[: len(disp)]
        for i, (label, disp_item, disp_std_item) in enumerate(
                zip(labels, disp, disp_std)
        ):
            if run_from_ipython():
                from IPython.display import display, Math # noqa

                display(
                    Math(f"{label} = {disp_item:.5f} ± {disp_std_item:.5f} fs^{i + 1}")
                )
            else:
                print(f"{label} = {disp_item:.5f} ± {disp_std_item:.5f} fs^{i + 1}")
        return disp, disp_std, stri

    return wrapping