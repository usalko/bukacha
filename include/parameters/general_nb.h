#ifndef OSRM_NB_GENERAL_H
#define OSRM_NB_GENERAL_H

#include <nanobind/nanobind.h>

#include "engine/api/base_parameters.hpp"

NB_MAKE_OPAQUE(osrm::engine::api::BaseParameters::SnappingType)
NB_MAKE_OPAQUE(osrm::engine::api::BaseParameters::OutputFormatType)

#endif //OSRM_NB_GENERAL_H
