from __future__ import division, absolute_import, print_function

import sys
import subprocess
import pkgutil
import types
import importlib

import numpy as np
import numpy
import pytest

try:
    import ctypes
except ImportError:
    ctypes = None


def check_dir(module, module_name=None):
    """Returns a mapping of all objects with the wrong __module__ attribute."""
    if module_name is None:
        module_name = module.__name__
    results = {}
    for name in dir(module):
        item = getattr(module, name)
        if (hasattr(item, '__module__') and hasattr(item, '__name__')
                and item.__module__ != module_name):
            results[name] = item.__module__ + '.' + item.__name__
    return results


@pytest.mark.skipif(
    sys.version_info[0] < 3,
    reason="NumPy exposes slightly different functions on Python 2")
def test_numpy_namespace():
    # None of these objects are publicly documented.
    undocumented = {
        'Tester': 'numpy.testing._private.nosetester.NoseTester',
        '_add_newdoc_ufunc': 'numpy.core._multiarray_umath._add_newdoc_ufunc',
        'add_docstring': 'numpy.core._multiarray_umath.add_docstring',
        'add_newdoc': 'numpy.core.function_base.add_newdoc',
        'add_newdoc_ufunc': 'numpy.core._multiarray_umath._add_newdoc_ufunc',
        'byte_bounds': 'numpy.lib.utils.byte_bounds',
        'compare_chararrays': 'numpy.core._multiarray_umath.compare_chararrays',
        'deprecate': 'numpy.lib.utils.deprecate',
        'deprecate_with_doc': 'numpy.lib.utils.<lambda>',
        'disp': 'numpy.lib.function_base.disp',
        'fastCopyAndTranspose': 'numpy.core._multiarray_umath._fastCopyAndTranspose',
        'get_array_wrap': 'numpy.lib.shape_base.get_array_wrap',
        'get_include': 'numpy.lib.utils.get_include',
        'int_asbuffer': 'numpy.core._multiarray_umath.int_asbuffer',
        'mafromtxt': 'numpy.lib.npyio.mafromtxt',
        'ndfromtxt': 'numpy.lib.npyio.ndfromtxt',
        'recfromcsv': 'numpy.lib.npyio.recfromcsv',
        'recfromtxt': 'numpy.lib.npyio.recfromtxt',
        'safe_eval': 'numpy.lib.utils.safe_eval',
        'set_string_function': 'numpy.core.arrayprint.set_string_function',
        'show_config': 'numpy.__config__.show',
        'who': 'numpy.lib.utils.who',
    }
    # These built-in types are re-exported by numpy.
    builtins = {
        'bool': 'builtins.bool',
        'complex': 'builtins.complex',
        'float': 'builtins.float',
        'int': 'builtins.int',
        'long': 'builtins.int',
        'object': 'builtins.object',
        'str': 'builtins.str',
        'unicode': 'builtins.str',
    }
    whitelist = dict(undocumented, **builtins)
    bad_results = check_dir(np)
    # pytest gives better error messages with the builtin assert than with
    # assert_equal
    assert bad_results == whitelist


@pytest.mark.parametrize('name', ['testing', 'Tester'])
def test_import_lazy_import(name):
    """Make sure we can actually use the modules we lazy load.

    While not exported as part of the public API, it was accessible.  With the
    use of __getattr__ and __dir__, this isn't always true It can happen that
    an infinite recursion may happen.

    This is the only way I found that would force the failure to appear on the
    badly implemented code.

    We also test for the presence of the lazily imported modules in dir

    """
    exe = (sys.executable, '-c', "import numpy; numpy." + name)
    result = subprocess.check_output(exe)
    assert not result

    # Make sure they are still in the __dir__
    assert name in dir(np)


def test_numpy_linalg():
    bad_results = check_dir(np.linalg)
    assert bad_results == {}


def test_numpy_fft():
    bad_results = check_dir(np.fft)
    assert bad_results == {}


@pytest.mark.skipif(ctypes is None,
                    reason="ctypes not available in this python")
def test_NPY_NO_EXPORT():
    cdll = ctypes.CDLL(np.core._multiarray_tests.__file__)
    # Make sure an arbitrary NPY_NO_EXPORT function is actually hidden
    f = getattr(cdll, 'test_not_exported', None)
    assert f is None, ("'test_not_exported' is mistakenly exported, "
                      "NPY_NO_EXPORT does not work")


PUBLIC_MODULES = [
    "ctypeslib",
    "distutils",
    "distutils.cpuinfo",
    "distutils.exec_command",
    "distutils.misc_util",
    "distutils.log",
    "distutils.system_info",
    "doc",
    "doc.basics",
    "doc.broadcasting",
    "doc.byteswapping",
    "doc.constants",
    "doc.creation",
    "doc.dispatch",
    "doc.glossary",
    "doc.indexing",
    "doc.internals",
    "doc.misc",
    "doc.structured_arrays",
    "doc.subclassing",
    "doc.ufuncs",
    "dual",
    "f2py",
    "fft",
    "lib",
    "lib.format",
    "lib.mixins",
    "lib.npyio",
    "lib.recfunctions",
    "lib.scimath",
    "linalg",
    "ma",
    "ma.extras",
    "ma.mrecords",
    "matlib",
    "polynomial",
    "polynomial.chebyshev",
    "polynomial.hermite",
    "polynomial.hermite_e",
    "polynomial.laguerre",
    "polynomial.legendre",
    "polynomial.polynomial",
    "polynomial.polyutils",
    "random",
    "testing",
    "version",
]


PUBLIC_ALIASED_MODULES = [
    "char",
    "emath",
    "rec",
]


PRIVATE_BUT_PRESENT_MODULES = [
    "compat",
    "compat.py3k",
    "conftest",
    "core",
    "core.arrayprint",
    "core.code_generators",
    "core.code_generators.genapi",
    "core.code_generators.generate_numpy_api",
    "core.code_generators.generate_ufunc_api",
    "core.code_generators.generate_umath",
    "core.code_generators.numpy_api",
    "core.code_generators.ufunc_docstrings",
    "core.cversions",
    "core.defchararray",
    "core.einsumfunc",
    "core.fromnumeric",
    "core.function_base",
    "core.getlimits",
    "core.info",
    "core.machar",
    "core.memmap",
    "core.multiarray",
    "core.numeric",
    "core.numerictypes",
    "core.overrides",
    "core.records",
    "core.shape_base",
    "core.umath",
    "core.umath_tests",
    "distutils.ccompiler",
    "distutils.command",
    "distutils.command.autodist",
    "distutils.command.bdist_rpm",
    "distutils.command.build",
    "distutils.command.build_clib",
    "distutils.command.build_ext",
    "distutils.command.build_py",
    "distutils.command.build_scripts",
    "distutils.command.build_src",
    "distutils.command.config",
    "distutils.command.config_compiler",
    "distutils.command.develop",
    "distutils.command.egg_info",
    "distutils.command.install",
    "distutils.command.install_clib",
    "distutils.command.install_data",
    "distutils.command.install_headers",
    "distutils.command.sdist",
    "distutils.compat",
    "distutils.conv_template",
    "distutils.core",
    "distutils.extension",
    "distutils.fcompiler",
    "distutils.fcompiler.absoft",
    "distutils.fcompiler.compaq",
    "distutils.fcompiler.environment",
    "distutils.fcompiler.g95",
    "distutils.fcompiler.gnu",
    "distutils.fcompiler.hpux",
    "distutils.fcompiler.ibm",
    "distutils.fcompiler.intel",
    "distutils.fcompiler.lahey",
    "distutils.fcompiler.mips",
    "distutils.fcompiler.nag",
    "distutils.fcompiler.none",
    "distutils.fcompiler.pathf95",
    "distutils.fcompiler.pg",
    "distutils.fcompiler.sun",
    "distutils.fcompiler.vast",
    "distutils.from_template",
    "distutils.info",
    "distutils.intelccompiler",
    "distutils.lib2def",
    "distutils.line_endings",
    "distutils.mingw32ccompiler",
    "distutils.msvc9compiler",
    "distutils.msvccompiler",
    "distutils.npy_pkg_config",
    "distutils.numpy_distribution",
    "distutils.pathccompiler",
    "distutils.unixccompiler",
    "f2py.auxfuncs",
    "f2py.capi_maps",
    "f2py.cb_rules",
    "f2py.cfuncs",
    "f2py.common_rules",
    "f2py.crackfortran",
    "f2py.diagnose",
    "f2py.f2py2e",
    "f2py.f2py_testing",
    "f2py.f90mod_rules",
    "f2py.func2subr",
    "f2py.info",
    "f2py.rules",
    "f2py.use_rules",
    "fft.helper",
    "fft.info",
    "fft.pocketfft",
    "fft.pocketfft_internal",
    "lib.arraypad",  # TODO: figure out which numpy.lib submodules are public
    "lib.arraysetops",
    "lib.arrayterator",
    "lib.financial",
    "lib.function_base",
    "lib.histograms",
    "lib.index_tricks",
    "lib.info",
    "lib.nanfunctions",
    "lib.polynomial",
    "lib.shape_base",
    "lib.stride_tricks",
    "lib.twodim_base",
    "lib.type_check",
    "lib.ufunclike",
    "lib.user_array",
    "lib.utils",
    "linalg.info",
    "linalg.lapack_lite",
    "linalg.linalg",
    "ma.bench",
    "ma.core",
    "ma.testutils",
    "ma.timer_comparison",
    "ma.version",
    "matrixlib",
    "matrixlib.defmatrix",
    "random.bit_generator",
    "random.bounded_integers",
    "random.common",
    "random.entropy",
    "random.generator",
    "random.info",
    "random.mt19937",
    "random.mtrand",
    "random.pcg64",
    "random.philox",
    "random.sfc64",
    "testing.decorators",
    "testing.noseclasses",
    "testing.nosetester",
    "testing.print_coercion_tables",
    "testing.utils",
]


def is_unexpected(name):
    """Check if this needs to be considered."""
    if '._' in name or '.tests' in name or '.setup' in name:
        return False

    if name.startswith("numpy."):
        name = name[6:]

    if name in PUBLIC_MODULES:
        return False

    if name in PUBLIC_ALIASED_MODULES:
        return False


    if name in PRIVATE_BUT_PRESENT_MODULES:
        return False

    return True


def test_all_modules_are_expected():
    """
    Test that we don't add anything that looks like a new public module by
    accident.  Check is based on filenames.
    """

    modnames = []
    for _, modname, ispkg in pkgutil.walk_packages(path=np.__path__,
                                                   prefix=np.__name__ + '.',
                                                   onerror=None):
        if is_unexpected(modname):
            # We have a name that is new.  If that's on purpose, add it to
            # PUBLIC_MODULES.  We don't expect to have to add anything to
            # PRIVATE_BUT_PRESENT_MODULES.  Use an underscore in the name!
            modnames.append(modname)

    if modnames:
        raise AssertionError("Found unexpected modules: {}".format(modnames))


@pytest.mark.xfail(reason="missing __all__ dicts are messing this up, "
                          "needs work")
def test_all_modules_are_expected_2():
    """
    Method checking all objects. The pkgutil-based method in
    `test_all_modules_are_expected` does not catch imports into a namespace,
    only filenames.  So this test is more thorough, and checks this like:

        import .lib.scimath as emath

    """
    modnames = []

    def check(modname):
        module = importlib.import_module(modname)
        if hasattr(module, '__all__'):
            objnames = module.__all__
        else:
            objnames = dir(module)

        for objname in objnames:
            if not objname.startswith('_'):
                fullobjname = modname + '.' + objname
                if isinstance(eval(fullobjname), types.ModuleType):
                    if is_unexpected(fullobjname):
                        modnames.append(fullobjname)

    check("numpy")
    for modname in PUBLIC_MODULES:
        check("numpy." + modname)

    if modnames:
        raise AssertionError("Found unexpected object(s) that look like "
                             "modules: {}".format(modnames))
