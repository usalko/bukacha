#ifndef OSRM_NB_APPROACH_H
#define OSRM_NB_APPROACH_H

#include <nanobind/nanobind.h>

#include "engine/approach.hpp"

#include <nanobind/stl/string.h>
#include <nanobind/stl/unordered_map.h>

#include <unordered_map>
#include <string>

using osrm::engine::Approach;

namespace nb = nanobind;

void init_Approach(nanobind::module_& m);

static const std::unordered_map<std::string, Approach> approach_map {
    { "curb", Approach::CURB },
    { std::string(), Approach::CURB },
    { "unrestricted", Approach::UNRESTRICTED }
};

#endif //OSRM_NB_APPROACH_H
