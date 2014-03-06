##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##  - Pierre ROULLON <proullon@aldebaran-robotics.com>
##
## Copyright (C) 2010 - 2013 Aldebaran Robotics
##

""" QiMessaging Python bindings

Provided features are very close to C++, Python style.
"""

import os
import sys
def load_lib_qipyessaging():
    """ Load _qipyessaging.so and its dependencies.

    This makes _qipyessaging usable from a relocatable
    SDK without having to set LD_LIBRARY_PATH
    """
    import ctypes
    deps = [
            "libboost_chrono.so.1.50.0",
            "libboost_date_time.so.1.50.0",
            "libboost_filesystem.so.1.50.0",
            "libboost_graph.so.1.50.0",
            "libboost_locale.so.1.50.0",
            "libboost_math_c99f.so.1.50.0",
            "libboost_math_c99l.so.1.50.0",
            "libboost_math_c99.so.1.50.0",
            "libboost_math_tr1f.so.1.50.0",
            "libboost_math_tr1l.so.1.50.0",
            "libboost_math_tr1.so.1.50.0",
            "libboost_prg_exec_monitor.so.1.50.0",
            "libboost_program_options.so.1.50.0",
            "libboost_python.so.1.50.0",
            "libboost_random.so.1.50.0",
            "libboost_regex.so.1.50.0",
            "libboost_serialization.so.1.50.0",
            "libboost_signals.so.1.50.0",
            "libboost_system.so.1.50.0",
            "libboost_thread.so.1.50.0",
            "libboost_timer.so.1.50.0",
            "libboost_unit_test_framework.so.1.50.0",
            "libboost_wave.so.1.50.0",
            "libboost_wserialization.so.1.50.0",
            "libqi.so",
            "libqitype.so",
            "libqimessaging.so",
    ]
    this_dir = os.path.abspath(os.path.dirname(__file__))
    for dep in deps:
        full_path = os.path.join(this_dir, "..", dep)
        try:
            ctypes.cdll.LoadLibrary(full_path)
        except Exception:
            pass


if sys.platform.startswith("linux"):
    load_lib_qipyessaging()


#######

from _qi import Application as _Application
from _qi import ApplicationSession as _ApplicationSession
from _qi import FutureState, FutureTimeout, Future, \
                Promise, Property, Session, Signal, \
                createObject, registerObjectFactory, async, PeriodicTask
import path

from _type import Void, Bool, Int8, UInt8, Int16, UInt16, Int32, UInt32, Int64, UInt64, Float, Double, String, List, Map, Struct, Object, Dynamic, Buffer, AnyArguments
from _type import typeof, _isinstance
from _binder import bind, nobind
from .logging import logSilent, logFatal, logError, logWarning, logInfo, logVerbose, logDebug, PyLogger, setLevel, setContext, setFilters, getLogger
from .translator import defaultTranslator, tr, Translator


#rename isinstance here. (isinstance should not be used in this file)
isinstance = _isinstance

_app = None


#we want to stop all thread before python start destroying
#module and the like. (this avoid callback calling python while
#it's destroying)
def _stopApplication():
    global _app
    if _app is not None:
        _app.stop()
        del _app
        _app = None

import atexit
atexit.register(_stopApplication)

#application is a singleton, it should live till the end of the program
#because it own eventloops
def ApplicationSession(args=None):
    global _app
    if _app is None:
        if args is None:
            _app = _ApplicationSession()
        else:
            _app = _ApplicationSession(args)
    else:
        raise Exception("Application was already initialized")
    return _app

def Application(args=None):
    global _app
    if _app is None:
        if args is None:
            _app = _Application()
        else:
            _app = _Application(args)
    else:
        raise Exception("Application was already initialized")
    return _app

__all__ = ["FutureState",
           "FutureTimeout",
           "Future",
           "Promise",
           "Property",
           "Session",
           "Signal",
           "createObject",
           "registerObjectFactory",
           "async",

           "Void", "Bool", "Int8", "UInt8", "Int16", "UInt16", "Int32", "UInt32", "Int64", "UInt64",
           "Float", "Double", "String", "List", "Map", "Struct", "Object", "Dynamic", "Buffer", "AnyArguments",
           "typeof", "isinstance",
           "bind", "nobind",
           "logSilent", "logFatal", "logError", "logWarning", "logInfo", "logVerbose", "logDebug",
           "setLevel", "setContext", "setFilters", "getLogger"
           "PyLogger",
           "defaultTranslator", "tr", "Translator"


]
