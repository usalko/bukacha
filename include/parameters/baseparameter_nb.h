#ifndef OSRM_NB_BASEPARAMETER_H
#define OSRM_NB_BASEPARAMETER_H

#include "engine/api/base_parameters.hpp"

#include <nanobind/nanobind.h>

#include <unordered_map>

using osrm::engine::api::BaseParameters;

void init_BaseParameters(nanobind::module_& m);

static const std::unordered_map<std::string, BaseParameters::SnappingType> snapping_map {
    { "default", BaseParameters::SnappingType::Default },
    { std::string(), BaseParameters::SnappingType::Default },
    { "any", BaseParameters::SnappingType::Any }
};

static const std::unordered_map<std::string, BaseParameters::OutputFormatType> output_map {
    { "json", BaseParameters::OutputFormatType::JSON },
    { std::string(), BaseParameters::OutputFormatType::JSON },
    { "flatbuffers", BaseParameters::OutputFormatType::FLATBUFFERS }
};

#endif //OSRM_NB_BASEPARAMETER_H
