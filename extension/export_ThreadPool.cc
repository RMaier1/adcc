//
// Copyright (C) 2018 by the adcc authors
//
// This file is part of adcc.
//
// adcc is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// adcc is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with adcc. If not, see <http://www.gnu.org/licenses/>.
//

#include <sstream>

#include <adcc/ThreadPool.hh>
#include <pybind11/pybind11.h>

namespace adcc {
namespace py_iface {

namespace py = pybind11;

static std::string ThreadPool___repr__(const ThreadPool& self) {
  std::stringstream ss;
  ss << "ThreadPool("
     << "n_cores = " << self.n_cores() << ", n_threads = " << self.n_threads() << ")";
  return ss.str();
}

void export_ThreadPool(py::module& m) {
  // Once we switch to C++14, this can be handled by the py::overload_cast
  // function
  void (ThreadPool::*reinit_1)(size_t)         = &ThreadPool::reinit;
  void (ThreadPool::*reinit_2)(size_t, size_t) = &ThreadPool::reinit;

  py::class_<ThreadPool, std::shared_ptr<ThreadPool>>(
        m, "ThreadPool",
        "Class providing access to the thread pool and the adcc parallelisation.")
        .def(py::init<>())
        .def(py::init<size_t>(),
             "Initialise the parallelisation by providing the number of cores to use.")
        .def(py::init<size_t, size_t>(),
             "Initialise the parallelisation by providing the number of cores and the "
             "number of threads to use.")
        .def("reinit", reinit_1,
             "Reinitialise the parallelisation by providing the number of cores to use. "
             "Default number of threads is 2 * "
             "n_cores - 1.")
        .def("reinit", reinit_2,
             "Reinitialise the parallelisation by providing the number of cores and "
             "number of threads to use.")
        .def_property_readonly("n_cores", &ThreadPool::n_cores)
        .def_property_readonly("n_threads", &ThreadPool::n_threads)
        .def("__repr__", &ThreadPool___repr__)
        //
        ;
}

}  // namespace py_iface
}  // namespace adcc