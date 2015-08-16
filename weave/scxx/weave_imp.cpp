/******************************************** 
  copyright 1999 McMillan Enterprises, Inc.
  www.mcmillan-inc.com

  modified for weave by eric jones.
*********************************************/
#include "object.h"

using namespace py;

//---------------------------------------------------------------------------
// object
//
// !! Wish I knew how to get these defined inline in object.h...
//---------------------------------------------------------------------------

std::ostream& operator <<(std::ostream& os, py::object& obj)
{
    os << obj.repr();
    return os;
}

//---------------------------------------------------------------------------
// Fail method for throwing exceptions with a given message.
//---------------------------------------------------------------------------

void py::fail(PyObject* exc, const char* msg)
{
  PyErr_SetString(exc, msg);
  throw 1;
}
