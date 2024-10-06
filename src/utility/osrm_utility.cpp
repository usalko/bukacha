#include "utility/osrm_utility.h"

#include "osrm/osrm.hpp"
#include "osrm/engine_config.hpp"
#include "osrm/status.hpp"

#include "engineconfig_nb.h"
#include "utility/param_utility.h"

#include <unordered_map>
#include <stdexcept>

#define UNLIMITED -1

namespace nb = nanobind;

using osrm::engine::EngineConfig;

template <typename T>
void assign_val(T &to_assign, const std::pair<nb::handle, nb::handle> &val)
{
    try
    {
        to_assign = nb::cast<T>(val.second);
    }
    catch (const nb::cast_error &ex)
    {
        throw std::runtime_error("Invalid type passed for argument: " + nb::cast<std::string>(val.first));
    }
}

namespace osrm_nb_util
{

    std::string string_value_to_string(osrm::util::json::Value &value)
    {
        if (const auto stringValue(std::get_if<osrm::util::json::String>(&value)); stringValue)
        {
            return (*stringValue).value;
        }
        return "";
    }

    void check_status(osrm::engine::Status status, osrm::util::json::Object &res)
    {
        if (status == osrm::engine::Status::Ok)
        {
            return;
        }

        const std::string code = string_value_to_string(res.values["code"]);
        const std::string msg = string_value_to_string(res.values["message"]);

        throw std::runtime_error(code + " - " + msg);
    }

    void populate_cfg_from_kwargs(const nb::kwargs &kwargs, EngineConfig &config)
    {
        std::unordered_map<std::string, std::function<void(const std::pair<nb::handle, nb::handle> &)>> assign_map{
            {"storage_config", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 std::string str;
                 assign_val(str, val);
                 config.storage_config = osrm::storage::StorageConfig(str);
             }},
            {"max_locations_trip", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_locations_trip, val);
             }},
            {"max_locations_viaroute", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_locations_viaroute, val);
             }},
            {"max_locations_distance_table", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_locations_distance_table, val);
             }},
            {"max_locations_map_matching", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_locations_map_matching, val);
             }},
            {"max_radius_map_matching", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_radius_map_matching, val);
             }},
            {"max_results_nearest", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_results_nearest, val);
             }},
            {"default_radius", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 try
                 {
                     const std::string rad_val = nb::cast<std::string>(val.second);

                     if (!(rad_val == "unlimited" || rad_val == "UNLIMITED"))
                     {
                         throw std::runtime_error("default_radius must be a float value or 'unlimited'");
                     }

                     config.default_radius = UNLIMITED;
                 }
                 catch (const nb::cast_error)
                 {
                     assign_val(config.default_radius, val);
                 }
             }},
            {"max_alternatives", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.max_alternatives, val);
             }},
            {"use_shared_memory", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.use_shared_memory, val);
             }},
            {"memory_file", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 std::string str;
                 assign_val(str, val);
                 config.memory_file = std::filesystem::path(str);
             }},
            {"use_mmap", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.use_mmap, val);
             }},
            {"algorithm", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 std::string str;
                 assign_val(str, val);
                 config.algorithm = osrm_nb_util::str_to_enum(str, "Algorithm", algorithm_map);
             }},
            {"verbosity", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.verbosity, val);
             }},
            {"dataset_name", [&config](const std::pair<nb::handle, nb::handle> &val)
             {
                 assign_val(config.dataset_name, val);
             }}};

        for (auto kwarg : kwargs)
        {
            const std::string arg_str = nb::cast<std::string>(kwarg.first);
            auto itr = assign_map.find(arg_str);

            if (itr == assign_map.end())
            {
                throw std::invalid_argument(arg_str);
            }

            itr->second(kwarg);
        }
    }

    std::string format_config_parameters_error(std::string error_header, osrm::engine::EngineConfig engine_config)
    {
        std::stringstream ss;

        ss << error_header << ": ";

        const bool all_path_are_empty = engine_config.storage_config.GetPath("").empty();

        const auto unlimited_or_more_than = [](const auto v, const auto limit)
        { return v == -1 || v > limit; };

        const bool limits_valid = unlimited_or_more_than(engine_config.max_locations_distance_table, 2) &&
                                  unlimited_or_more_than(engine_config.max_locations_map_matching, 2) &&
                                  unlimited_or_more_than(engine_config.max_radius_map_matching, 0) &&
                                  unlimited_or_more_than(engine_config.max_locations_trip, 2) &&
                                  unlimited_or_more_than(engine_config.max_locations_viaroute, 2) &&
                                  unlimited_or_more_than(engine_config.max_results_nearest, 0) &&
                                  unlimited_or_more_than(engine_config.default_radius, 0) && engine_config.max_alternatives >= 0;

        if (!limits_valid)
        {
            ss << " limits invalid;";
        }
        if (!engine_config.storage_config.IsValid())
        {
            ss << " storage config is invalid:";
            for (auto &fileName : engine_config.storage_config.GetMissingFiles())
            {

                ss << " missing/broken file: " << engine_config.storage_config.base_path.string()
                   << fileName;
            }
            ss << ";";
        }

        ss << std::endl;
        return ss.str();
    }

} // namespace osrm_nb_util
