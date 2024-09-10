#ifndef OSRM_NB_TABLEPARAMETER_H
#define OSRM_NB_TABLEPARAMETER_H

#include "engine/api/table_parameters.hpp"

#include <nanobind/nanobind.h>

#include <unordered_map>

using osrm::engine::api::TableParameters;

void init_TableParameters(nanobind::module_& m);

static const std::unordered_map<std::string, TableParameters::FallbackCoordinateType> fallback_map {
    { "input", TableParameters::FallbackCoordinateType::Input },
    { std::string(), TableParameters::FallbackCoordinateType::Input },
    { "snapped", TableParameters::FallbackCoordinateType::Snapped }
};

static const std::unordered_map<std::string, TableParameters::AnnotationsType> table_annotations_map {
    { "none", TableParameters::AnnotationsType::None },
    { std::string(), TableParameters::AnnotationsType::None },
    { "duration", TableParameters::AnnotationsType::Duration },
    { "distance", TableParameters::AnnotationsType::Distance },
    { "all", TableParameters::AnnotationsType::All }
};

#endif //OSRM_NB_TABLEPARAMETER_H
