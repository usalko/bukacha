#ifndef OSRM_NB_ENGINECONFIG_H
#define OSRM_NB_ENGINECONFIG_H

#include <nanobind/nanobind.h>

#include "osrm/engine_config.hpp"

NB_MAKE_OPAQUE(osrm::engine::EngineConfig::Algorithm)

#include <unordered_map>

using osrm::engine::EngineConfig;

void init_EngineConfig(nanobind::module_& m);

static const std::unordered_map<std::string, EngineConfig::Algorithm> algorithm_map {
    { "CH", EngineConfig::Algorithm::CH },
    { std::string(), EngineConfig::Algorithm::CH },
    // { "CoreCH", EngineConfig::Algorithm::CoreCH },
    { "MLD", EngineConfig::Algorithm::MLD }
};

#endif //OSRM_NB_ENGINECONFIG_H
