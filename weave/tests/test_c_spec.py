

import os
import sys
import tempfile
import string
import time

from numpy.testing import TestCase, dec, assert_, run_module_suite

from weave import inline_tools, ext_tools, c_spec
from weave.build_tools import msvc_exists, gcc_exists
from weave.catalog import unique_file

from weave_test_utils import debug_print


def unique_mod(d,file_name):
    f = os.path.basename(unique_file(d,file_name))
    m = os.path.splitext(f)[0]
    return m


class IntConverter(TestCase):
    compiler = ''

    @dec.slow
    def test_type_match_string(self):
        s = c_spec.long_converter()
        assert_(not s.type_match('string'))

    @dec.slow
    def test_type_match_int(self):
        s = c_spec.long_converter()
        assert_(s.type_match(5))

    @dec.slow
    def test_type_match_float(self):
        s = c_spec.long_converter()
        assert_(not s.type_match(5.))

    @dec.slow
    def test_type_match_complex(self):
        s = c_spec.long_converter()
        assert_(not s.type_match(5.+1j))

    @dec.slow
    def test_var_in(self):
        mod_name = 'int_var_in' + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1
        code = "a=2;"
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'abc'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_int_return(self):
        mod_name = sys._getframe().f_code.co_name + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1
        code = """
               a=a+2;
               return_val = PyLong_FromLong(a);
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1
        c = test(b)

        assert_(c == 3)


class FloatConverter(TestCase):
    compiler = ''

    @dec.slow
    def test_type_match_string(self):
        s = c_spec.float_converter()
        assert_(not s.type_match('string'))

    @dec.slow
    def test_type_match_int(self):
        s = c_spec.float_converter()
        assert_(not s.type_match(5))

    @dec.slow
    def test_type_match_float(self):
        s = c_spec.float_converter()
        assert_(s.type_match(5.))

    @dec.slow
    def test_type_match_complex(self):
        s = c_spec.float_converter()
        assert_(not s.type_match(5.+1j))

    @dec.slow
    def test_float_var_in(self):
        mod_name = sys._getframe().f_code.co_name + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1.
        code = "a=2.;"
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1.
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'abc'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_float_return(self):
        mod_name = sys._getframe().f_code.co_name + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1.
        code = """
               a=a+2.;
               return_val = PyFloat_FromDouble(a);
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1.
        c = test(b)
        assert_(c == 3.)


class ComplexConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_type_match_string(self):
        s = c_spec.complex_converter()
        assert_(not s.type_match('string'))

    @dec.slow
    def test_type_match_int(self):
        s = c_spec.complex_converter()
        assert_(not s.type_match(5))

    @dec.slow
    def test_type_match_float(self):
        s = c_spec.complex_converter()
        assert_(not s.type_match(5.))

    @dec.slow
    def test_type_match_complex(self):
        s = c_spec.complex_converter()
        assert_(s.type_match(5.+1j))

    @dec.slow
    def test_complex_var_in(self):
        mod_name = sys._getframe().f_code.co_name + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1.+1j
        code = "a=std::complex<double>(2.,2.);"
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1.+1j
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'abc'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_complex_return(self):
        mod_name = sys._getframe().f_code.co_name + self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 1.+1j
        code = """
               a= a + std::complex<double>(2.,2.);
               return_val = PyComplex_FromDoubles(a.real(),a.imag());
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 1.+1j
        c = test(b)
        assert_(c == 3.+3j)


#----------------------------------------------------------------------------
# Callable object conversion tests
#----------------------------------------------------------------------------

class CallableConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_call_function(self):
        func = str.find
        search_str = "hello world hello"
        sub_str = "world"
        # * Not sure about ref counts on search_str and sub_str.
        # * Is the Py::String necessary? (it works anyways...)
        code = """
               py::tuple args(2);
               args[0] = search_str;
               args[1] = sub_str;
               return_val = func.call(args);
               """
        actual = inline_tools.inline(code,['func','search_str','sub_str'],
                                     compiler=self.compiler,force=1)
        desired = func(search_str,sub_str)
        assert_(desired == actual)


class SequenceConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_convert_to_dict(self):
        d = {}
        inline_tools.inline("",['d'],compiler=self.compiler,force=1)

    @dec.slow
    def test_convert_to_list(self):
        l = []
        inline_tools.inline("",['l'],compiler=self.compiler,force=1)

    @dec.slow
    def test_convert_to_string(self):
        s = 'hello'
        inline_tools.inline("",['s'],compiler=self.compiler,force=1)

    @dec.slow
    def test_convert_to_tuple(self):
        t = ()
        inline_tools.inline("",['t'],compiler=self.compiler,force=1)


class StringConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_type_match_string(self):
        s = c_spec.string_converter()
        assert_(s.type_match('string'))

    @dec.slow
    def test_type_match_int(self):
        s = c_spec.string_converter()
        assert_(not s.type_match(5))

    @dec.slow
    def test_type_match_float(self):
        s = c_spec.string_converter()
        assert_(not s.type_match(5.))

    @dec.slow
    def test_type_match_complex(self):
        s = c_spec.string_converter()
        assert_(not s.type_match(5.+1j))

    @dec.slow
    def test_var_in(self):
        mod_name = 'string_var_in'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 'string'
        code = 'a=std::string("hello");'
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)

        test = __import__(mod_name).test
        b = 'bub'
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 1
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_return(self):
        mod_name = 'string_return'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = 'string'
        code = """
               a= std::string("hello");
               return_val = PyUnicode_FromString(a.c_str());
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = 'bub'
        c = test(b)
        assert_(c == 'hello')


class ListConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_type_match_bad(self):
        s = c_spec.list_converter()
        objs = [{},(),'',1,1.,1+1j]
        for i in objs:
            assert_(not s.type_match(i))

    @dec.slow
    def test_type_match_good(self):
        s = c_spec.list_converter()
        assert_(s.type_match([]))

    @dec.slow
    def test_var_in(self):
        mod_name = 'list_var_in'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = [1]
        code = 'a=py::list();'
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = [1,2]
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'string'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_return(self):
        mod_name = 'list_return'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = [1]
        code = """
               a=py::list();
               a.append("hello");
               return_val = a;
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = [1,2]
        c = test(b)
        assert_(c == ['hello'])

    @dec.slow
    def test_speed(self):
        mod_name = 'list_speed'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = list(range(1000000))
        code = """
               int v, sum = 0;
               for(int i = 0; i < a.len(); i++)
               {
                   v = a[i];
                   if (v % 2)
                    sum += v;
                   else
                    sum -= v;
               }
               return_val = sum;
               """
        with_cxx = ext_tools.ext_function('with_cxx',code,['a'])
        mod.add_function(with_cxx)
        code = """
               long vv, sum = 0;
               PyObject *v;
               for(int i = 0; i < a.len(); i++)
               {
                   v = PyList_GetItem(py_a,i);
                   //didn't set error here -- just speed test
                   vv = PyLong_AsLong(v);
                   if (vv % 2)
                    sum += vv;
                   else
                    sum -= vv;
               }
               return_val = sum;
               """
        no_checking = ext_tools.ext_function('no_checking',code,['a'])
        mod.add_function(no_checking)
        mod.compile(location=test_dir, compiler=self.compiler)
        loaded_module = __import__(mod_name)
        with_cxx = loaded_module.with_cxx
        no_checking = loaded_module.no_checking
        t1 = time.time()
        sum1 = with_cxx(a)
        t2 = time.time()
        debug_print('speed test for list access')
        debug_print('compiler:', self.compiler)
        debug_print('scxx:', t2 - t1)
        t1 = time.time()
        sum2 = no_checking(a)
        t2 = time.time()
        debug_print('C, no checking:', t2 - t1)
        sum3 = 0
        t1 = time.time()
        for i in a:
            if i % 2:
                sum3 += i
            else:
                sum3 -= i
        t2 = time.time()
        debug_print('python:', t2 - t1)
        assert_(sum1 == sum2 and sum1 == sum3)


class TupleConverter(TestCase):

    compiler = ''

    @dec.slow
    def test_type_match_bad(self):
        s = c_spec.tuple_converter()
        objs = [{},[],'',1,1.,1+1j]
        for i in objs:
            assert_(not s.type_match(i))

    @dec.slow
    def test_type_match_good(self):
        s = c_spec.tuple_converter()
        assert_(s.type_match((1,)))

    @dec.slow
    def test_var_in(self):
        mod_name = 'tuple_var_in'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = (1,)
        code = 'a=py::tuple();'
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = (1,2)
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'string'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_return(self):
        mod_name = 'tuple_return'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = (1,)
        code = """
               a=py::tuple(2);
               a[0] = "hello";
               a.set_item(1,py::None);
               return_val = a;
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = (1,2)
        c = test(b)
        assert_(c == ('hello',None))


class DictConverter(TestCase):
    """Base Class for dictionary conversion tests."""

    # Default string specifying the compiler to use.  While this is set
    # in all sub-classes, this base test class is found by the test
    # infrastructure and run. Therefore, we give it a default value
    # so that it can run on its own.
    compiler = ''

    @dec.slow
    def test_type_match_bad(self):
        s = c_spec.dict_converter()
        objs = [[],(),'',1,1.,1+1j]
        for i in objs:
            assert_(not s.type_match(i))

    @dec.slow
    def test_type_match_good(self):
        s = c_spec.dict_converter()
        assert_(s.type_match({}))

    @dec.slow
    def test_var_in(self):
        mod_name = 'dict_var_in'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = {'z':1}
        code = 'a=py::dict();'  # This just checks to make sure the type is correct
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = {'y':2}
        test(b)
        try:
            b = 1.
            test(b)
        except TypeError:
            pass
        try:
            b = 'string'
            test(b)
        except TypeError:
            pass

    @dec.slow
    def test_return(self):
        mod_name = 'dict_return'+self.compiler
        mod_name = unique_mod(test_dir,mod_name)
        mod = ext_tools.ext_module(mod_name)
        a = {'z':1}
        code = """
               a=py::dict();
               a["hello"] = 5;
               return_val = a;
               """
        test = ext_tools.ext_function('test',code,['a'])
        mod.add_function(test)
        mod.compile(location=test_dir, compiler=self.compiler)
        test = __import__(mod_name).test
        b = {'z':2}
        c = test(b)
        assert_(c['hello'] == 5)


for _n in dir():
    if _n[-9:] == 'Converter':
        if msvc_exists():
            exec("class Test%sMsvc(%s):\n    compiler = 'msvc'" % (_n,_n))
        else:
            exec("class Test%sUnix(%s):\n    compiler = ''" % (_n,_n))
        if gcc_exists():
            exec("class Test%sGcc(%s):\n    compiler = 'gcc'" % (_n,_n))


def setup_location():
    test_dir = tempfile.mkdtemp()
    sys.path.insert(0,test_dir)
    return test_dir


test_dir = None


def setUpModule():
    global test_dir
    test_dir = setup_location()


def tearDownModule():
    import shutil
    if test_dir is not None:
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    run_module_suite()
