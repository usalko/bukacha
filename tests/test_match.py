import pytest
import osrm
import constants
import math

data_path = constants.data_path
mld_data_path = constants.mld_data_path
three_test_coordinates = constants.three_test_coordinates
two_test_coordinates = constants.two_test_coordinates

class TestMatch:
    py_osrm = osrm.OSRM(
        storage_config = data_path, 
        use_shared_memory = False
    )

    def test_match(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            timestamps = [1424684612, 1424684616, 1424684620]
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        for m in res["matchings"]:
            assert(m["distance"] 
                   and m["duration"] 
                   and isinstance(m["legs"], osrm.Array)
                   and m["geometry"] 
                   and m["confidence"] > 0)
        assert(len(res["tracepoints"]) == 3)
        for t in res["tracepoints"]:
            assert(t["hint"] 
                   and not math.isnan(t["matchings_index"])
                   and not math.isnan(t["waypoint_index"])
                   and t["name"])
            
    def test_match_no_timestamps(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["tracepoints"]) == 3)
        assert(len(res["matchings"]) == 1)

    def test_match_no_geometrycompression(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            geometries = "geojson"
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(isinstance(res["matchings"][0]["geometry"], osrm.Object))
        assert(isinstance(res["matchings"][0]["geometry"]["coordinates"], osrm.Array))

    def test_match_geometrycompression(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(isinstance(res["matchings"][0]["geometry"], str))

    def test_match_speedannotations(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            timestamps = [1424684612, 1424684616, 1424684620],
            radiuses = [4.07, 4.07, 4.07],
            steps = True,
            annotations = ["speed"],
            overview = "false",
            geometries = "geojson"
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(res["matchings"][0]["confidence"] > 0)
        for l in res["matchings"][0]["legs"]:
            assert(len(l["steps"]) > 0
                   and l["annotation"] 
                   and l["annotation"]["speed"])
        for l in res["matchings"][0]["legs"]:
            assert(not l["annotation"]["weight"] 
                   and not l["annotation"]["datasources"]
                   and not l["annotation"]["duration"] 
                   and not l["annotation"]["distance"] 
                   and not l["annotation"]["nodes"])
        assert(not "geometry" in res["matchings"][0])

    def test_match_severalannotations(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            timestamps = [1424684612, 1424684616, 1424684620],
            radiuses = [4.07, 4.07, 4.07],
            steps = True,
            annotations = ["duration", "distance", "nodes"],
            overview = "false",
            geometries = "geojson"
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(res["matchings"][0]["confidence"] > 0)
        for l in res["matchings"][0]["legs"]:
            assert(len(l["steps"]) > 0 
                   and l["annotation"] 
                   and l["annotation"]["distance"] is not None
                   and l["annotation"]["duration"] is not None
                   and l["annotation"]["nodes"] is not None)
            assert(not l["annotation"]["weight"]
                   and not l["annotation"]["datasources"]
                   and not l["annotation"]["speed"])
        assert(not "geometry" in res["matchings"][0])

    def test_match_alloptions(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            timestamps = [1424684612, 1424684616, 1424684620],
            radiuses = [4.07, 4.07, 4.07],
            steps = True,
            annotations = ["all"],
            overview = "false",
            geometries = "geojson",
            gaps = "split",
            tidy = False
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(res["matchings"][0]["confidence"] > 0)
        for l in res["matchings"][0]["legs"]:
            assert(len(l["steps"]) > 0
                   and l["annotation"] 
                   and l["annotation"]["distance"] is not None
                   and l["annotation"]["duration"] is not None)
        assert(not "geometry" in res["matchings"][0])

    def test_match_missing_arg(self):
        with pytest.raises(Exception):
            self.py_osrm.Match(osrm.MatchParameters())

    def test_match_nonobj_arg(self):
        with pytest.raises(TypeError):
            osrm.MatchParameters(None)

    def test_match_invalidcoords(self):
        match_params = osrm.MatchParameters(
            coordinates = []
        )
        with pytest.raises(Exception):
            self.py_osrm.Match(match_params)
        with pytest.raises(Exception):
            match_params.coordinates = [three_test_coordinates[0]]
            self.py_osrm.Match(match_params)
        with pytest.raises(TypeError):
            match_params.coordinates = three_test_coordinates[0]
        with pytest.raises(TypeError):
            match_params.coordinates = [three_test_coordinates[0][0], three_test_coordinates[0][1]]

    def test_match_invalidtimestamps(self):
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates
        )
        with pytest.raises(Exception):
            match_params.timestamps = [1424684612, 1424684616]
            self.py_osrm.Match(match_params)

    def test_match_without_motorways(self):
        py_osrm = osrm.OSRM(
            storage_config = mld_data_path, 
            algorithm = "MLD",
            use_shared_memory = False
        )
        match_params = osrm.MatchParameters(
            coordinates = three_test_coordinates,
            exclude = ["motorway"]
        )
        res = py_osrm.Match(match_params)
        assert(len(res["tracepoints"]) == 3)
        assert(len(res["matchings"]) == 1)

    # TODO: Would require custom validation bindings side
    # def test_match_invalidwaypoints_needtwo(self):
    #     match_params = osrm.MatchParameters(
    #         steps = True,
    #         coordinates = three_test_coordinates,
    #         waypoints = [0]
    #     )
    #     with pytest.raises(Exception):
    #         self.py_osrm.Match(match_params)

    # TODO: Would require custom validation bindings side
    # def test_match_invalidwaypoints_needcoordindices(self):
    #     match_params = osrm.MatchParameters(
    #         steps = True,
    #         coordinates = three_test_coordinates,
    #         waypoints = [1, 2]
    #     )
    #     with pytest.raises(Exception):
    #         self.py_osrm.Match(match_params)

    # TODO: Would require custom validation bindings side
    # def test_match_invalidwaypoints_ordermatters(self):
    #     match_params = osrm.MatchParameters(
    #         steps = True,
    #         coordinates = three_test_coordinates,
    #         waypoints = [2, 0]
    #     )
    #     with pytest.raises(Exception):
    #         self.py_osrm.Match(match_params)

    def test_match_invalidwaypoints_mustcorrespond(self):
        match_params = osrm.MatchParameters(
            steps = True,
            coordinates = three_test_coordinates,
            waypoints = [0, 3, 2]
        )
        with pytest.raises(Exception):
            self.py_osrm.Match(match_params)

    def test_match_error_on_splittrace(self):
        match_params = osrm.MatchParameters(
            steps = True,
            coordinates = three_test_coordinates+[(7.41902,43.73487)],
            timestamps = [1700, 1750, 1424684616, 1424684620],
            waypoints = [0,3]
        )
        with pytest.raises(RuntimeError) as ex:
            res = self.py_osrm.Match(match_params)
        assert("NoMatch" in str(ex.value))

    def test_match_waypoints(self):
        match_params = osrm.MatchParameters(
            steps = True,
            coordinates = three_test_coordinates,
            waypoints = [0,2]
        )
        res = self.py_osrm.Match(match_params)
        assert(len(res["matchings"]) == 1)
        assert(len(res["matchings"][0]["legs"]) == 1)
        for m in res["matchings"]:
            assert(m["distance"] 
                   and m["duration"] 
                   and isinstance(m["legs"], osrm.Array)
                   and m["geometry"] 
                   and (m["confidence"] > 0))
        assert(len(res["tracepoints"]) == 3)
        for t in res["tracepoints"]:
            assert(t["hint"]
                   and not math.isnan(t["matchings_index"])
                   and t["name"])
