#ifndef OSRM_NB_MATCHPARAMETER_H
#define OSRM_NB_MATCHPARAMETER_H

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/unordered_map.h>

#include "engine/api/match_parameters.hpp"

#include <unordered_map>

using osrm::engine::api::MatchParameters;

void init_MatchParameters(nanobind::module_& m);

static const std::unordered_map<std::string, MatchParameters::GapsType> gaps_map {
    { "split", MatchParameters::GapsType::Split },
    { std::string(), MatchParameters::GapsType::Split },
    { "ignore", MatchParameters::GapsType::Ignore }
};

#endif //OSRM_NB_MATCHPARAMETER_H
