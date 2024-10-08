#ifndef OSRM_NB_OSRM_UTIL_H
#define OSRM_NB_OSRM_UTIL_H

#include <nanobind/nanobind.h>

#include "osrm/engine_config.hpp"
#include "osrm/status.hpp"
#include "util/json_container.hpp"

namespace osrm_nb_util {

void check_status(osrm::engine::Status status, osrm::util::json::Object& res);

void populate_cfg_from_kwargs(const nanobind::kwargs& kwargs, osrm::engine::EngineConfig& config);

std::string format_config_parameters_error(std::string error_header, osrm::engine::EngineConfig engine_config);

} //namespace osrm_nb_util

#endif //OSRM_NB_OSRM_UTIL_H
