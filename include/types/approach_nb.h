#ifndef OSRM_NB_APPROACH_H
#define OSRM_NB_APPROACH_H

#include <nanobind/nanobind.h>

#include "engine/approach.hpp"

NB_MAKE_OPAQUE(osrm::engine::Approach)

#include <unordered_map>
#include <string>

using osrm::engine::Approach;

void init_Approach(nanobind::module_& m);

static const std::unordered_map<std::string, Approach> approach_map {
    { "curb", Approach::CURB },
    { std::string(), Approach::CURB },
    { "unrestricted", Approach::UNRESTRICTED }
};

#endif //OSRM_NB_APPROACH_H
