/********************************************
  copyright 1999 McMillan Enterprises, Inc.
  www.mcmillan-inc.com

  modified for weave by eric jones
*********************************************/
#if !defined(SEQUENCE_H_INCLUDED_)
#define SEQUENCE_H_INCLUDED_

#include <string>
#include <complex>

#include "object.h"

namespace py {

//---------------------------------------------------------------------------
// !! This isn't being picked up out of object.h for some reason, so I'll
// !! redeclare it.
//---------------------------------------------------------------------------
void fail(PyObject*, const char* msg);

//---------------------------------------------------------------------------
// base class for list and tuple objects.
//---------------------------------------------------------------------------
class sequence : public object
{
private:
  // since we override this virtual method, make it private
  using object::set_item;
public:
  //-------------------------------------------------------------------------
  // constructors
  //-------------------------------------------------------------------------
  sequence(const sequence& other) : object(other) {};
  sequence(PyObject* obj) : object(obj) {
    _violentTypeCheck();
  };

  //-------------------------------------------------------------------------
  // destructors
  //-------------------------------------------------------------------------
  virtual ~sequence() {}

  //-------------------------------------------------------------------------
  // operator=
  //-------------------------------------------------------------------------
  virtual sequence& operator=(const sequence& other) {
    grab_ref(other);
    return *this;
  };
  /*virtual*/ sequence& operator=(const object& other) {
    grab_ref(other);
    _violentTypeCheck();
    return *this;
  };

  //-------------------------------------------------------------------------
  // type checking.
  //-------------------------------------------------------------------------
  virtual void _violentTypeCheck() {
    if (!PySequence_Check(_obj)) {
      grab_ref(0);
      fail(PyExc_TypeError, "Not a sequence");
    }
  };

  //-------------------------------------------------------------------------
  // operator+ -- concatenation
  //-------------------------------------------------------------------------
  sequence operator+(const sequence& rhs) const {
    PyObject*  rslt = PySequence_Concat(_obj, rhs);
    if (rslt==0)
      fail(PyExc_TypeError, "Improper rhs for +");
    return lose_ref(rslt);
  };

  //-------------------------------------------------------------------------
  // count -- count the number of objects in a sequence.
  //-------------------------------------------------------------------------
  template<class T>
  int count(T value) const {
    int rslt = PySequence_Count(_obj, object(value));
    if (rslt == -1)
      fail(PyExc_RuntimeError, "failure in count");
    return rslt;
  };

  //-------------------------------------------------------------------------
  // set_item -- virtual so that set_item for tuple and list use
  //             type specific xxx_SetItem function calls.
  //-------------------------------------------------------------------------
  virtual void set_item(int ndx, object& val) {
    int rslt = PySequence_SetItem(_obj, ndx, val);
    if (rslt==-1)
      fail(PyExc_IndexError, "Index out of range");
  };


  //-------------------------------------------------------------------------
  // operator[] -- non-const version defined in list and tuple sub-types.
  //-------------------------------------------------------------------------
  object operator [] (int i) {
    PyObject* o = PySequence_GetItem(_obj, i);
    // don't throw error for when [] fails because it might be on left hand
    // side (a[0] = 1).  If the sequence was just created, it will be filled
    // with NULL values, and setting the values should be ok.  However, we
    // do want to catch index errors that might occur on the right hand side
    // (obj = a[4] when a has len==3).
    if (!o) {
      if (PyErr_ExceptionMatches(PyExc_IndexError))
        throw 1;
    }
    return lose_ref(o);
  };

  //-------------------------------------------------------------------------
  // slice -- handles slice operations.
  // !! NOT TESTED
  //-------------------------------------------------------------------------
  sequence slice(int lo, int hi) const {
    PyObject* o = PySequence_GetSlice(_obj, lo, hi);
    if (o == 0)
      fail(PyExc_IndexError, "could not obtain slice");
    return lose_ref(o);
  };

  //-------------------------------------------------------------------------
  // in -- find whether a value is in the given sequence.
  //       overloaded to handle the standard types used in weave.
  //-------------------------------------------------------------------------
  template<class T>
  bool in(T value) const {
    int rslt = PySequence_In(_obj, object(value));
    if (rslt==-1)
      fail(PyExc_RuntimeError, "problem in in");
    return (rslt==1);
  };

  //-------------------------------------------------------------------------
  // index -- find whether a value is in the given sequence.
  //          overloaded to handle the standard types used in weave.
  //-------------------------------------------------------------------------
  template<class T>
  int index(T value) const {
    int rslt = PySequence_Index(_obj, object(value));
    if (rslt==-1)
      fail(PyExc_IndexError, "value not found");
    return rslt;
  };

  //-------------------------------------------------------------------------
  // len, length, size -- find the length of the sequence.
  //                      version inherited from py::object ok.
  //-------------------------------------------------------------------------

  //-------------------------------------------------------------------------
  // operator* -- repeat a list multiple times.
  //-------------------------------------------------------------------------
  sequence operator * (int count) const {
    PyObject* rslt = PySequence_Repeat(_obj, count);
    if (rslt==0)
      fail(PyExc_RuntimeError, "sequence repeat failed");
    return lose_ref(rslt);
  };
};

//---------------------------------------------------------------------------
// indexed_ref -- return reference obj when operator[] is used as an lvalue.
//
// list and tuple objects return this for non-const calls to operator[].
// It is similar to object::keyed_ref, except that it stores an integer
// index instead of py::object key.
//---------------------------------------------------------------------------
class indexed_ref : public object
{
  sequence& _parent;
  int _ndx;
public:
  indexed_ref(PyObject* obj, sequence& parent, int ndx)
    : object(obj), _parent(parent), _ndx(ndx) { };
  virtual ~indexed_ref() {};

  indexed_ref& operator=(const object& other) {
    grab_ref(other);
    _parent.set_item(_ndx, *this);
    return *this;
  };
  indexed_ref& operator=( const indexed_ref& other ) {
    object oth = other;
    return operator=( oth );
  }
};


} // namespace py

#endif // SEQUENCE_H_INCLUDED_
