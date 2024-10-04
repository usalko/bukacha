#include <nanobind/nanobind.h>

#include "types/approach_nb.h"

#include "engine/approach.hpp"
#include "utility/param_utility.h"

namespace nb = nanobind;

void init_Approach(nb::module_& m) {
    using osrm::engine::Approach;

    nb::enum_<Approach>(m, "Approach", "enum-level docstring")
        .value("CURB", Approach::CURB, "CURB")
        .value("UNRESTRICTED", Approach::UNRESTRICTED, "UNRESTRICTED")
        .value("OPPOSITE", Approach::OPPOSITE, "OPPOSITE")
        .export_values();

    // nb::class_<Approach>(m, "Approach")
    //     .def("__init__", [](Approach* t, const std::string& str) {
    //         Approach approach = osrm_nb_util::str_to_enum(str, "Approach", approach_map);
    //         new (t) Approach(approach);
    //     })
    //     .def("__repr__", [](Approach type) {
    //         return osrm_nb_util::enum_to_str(type, "Approach", approach_map);
    //     });
    // nb::implicitly_convertible<std::string, Approach>();
}
