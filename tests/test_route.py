import pytest
import osrm
import constants

data_path = constants.data_path
mld_data_path = constants.mld_data_path
three_test_coordinates = constants.three_test_coordinates
two_test_coordinates = constants.two_test_coordinates

class TestRoute:
    py_osrm = osrm.OSRM(
        storage_config = data_path, 
        use_shared_memory = False
    )

    def test_route(self):
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates
        )
        res = self.py_osrm.Route(route_params)
        assert(res["waypoints"])
        assert(res["routes"])
        assert(res["routes"][0]["geometry"])

    def test_route_mld(self):
        py_osrm = osrm.OSRM(
            algorithm = "MLD",
            storage_config = mld_data_path,
            use_shared_memory = False
        )
        route_params = osrm.RouteParameters(
            coordinates = [(13.43864,52.51993),(13.415852,52.513191)]
        )
        res = py_osrm.Route(route_params)
        assert(res["waypoints"])
        assert(res["routes"])
        assert(res["routes"][0]["geometry"])

    def test_route_alternatives(self):
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates
        )
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) == 1)
        
        route_params.alternatives = True
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) > 1)

        route_params.number_of_alternatives = 3
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) > 1)

    def test_route_badparams(self):
        route_params = osrm.RouteParameters(
            coordinates = []
        )
        with pytest.raises(Exception):
            self.py_osrm.Route(route_params)
        with pytest.raises(Exception):
            route_params.coordinates = None
            self.py_osrm.Route(route_params)
        with pytest.raises(Exception):
            route_params.coordinates = [[three_test_coordinates[0], three_test_coordinates[1]]]
            self.py_osrm.Route(route_params)
        with pytest.raises(Exception):
            route_params.coordinates = [(213.43864,252.51993),(413.415852,552.513191)]
            res = self.py_osrm.Route(route_params)


    def test_route_shmem(self):
        py_osrm = osrm.OSRM()
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates
        )
        res = py_osrm.Route(route_params)
        assert(isinstance(res["routes"][0]["geometry"], str))

    def test_route_geometrycompression(self):
        py_osrm = osrm.OSRM()
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            geometries = "geojson"
        )
        res = py_osrm.Route(route_params)
        assert(isinstance(res["routes"][0]["geometry"]["coordinates"], osrm.Array))
        assert(res["routes"][0]["geometry"]["type"] == "LineString")

    def test_route_polyline6(self):
        py_osrm = osrm.OSRM()
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            continue_straight = False,
            overview = "false",
            geometries = "polyline6",
            steps = True
        )
        res = py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) == 1)
        assert(not res["routes"][0]["geometry"])
        assert(res["routes"][0]["legs"][0])
        assert(isinstance(res["routes"][0]["legs"][0]["geometry"], str))

    def test_route_speedannotations(self):
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            continue_straight = False,
            overview = "false",
            geometries = "polyline",
            steps = True,
            annotations = ["speed"],            
        )
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) == 1)
        assert(not res["routes"][0]["geometry"])
        assert(res["routes"][0]["legs"][0])
        for l in res["routes"][0]["legs"]:
            assert(len(l["steps"]) > 0
                   and l["annotation"] 
                   and l["annotation"]["speed"])
            assert(not l["annotation"]["weight"] 
                   and not l["annotation"]["datasources"]
                   and not l["annotation"]["duration"] 
                   and not l["annotation"]["distance"] 
                   and not l["annotation"]["nodes"])
            
        route_params.overview = "full"
        full_res = self.py_osrm.Route(route_params)

        route_params.overview = "simplified"
        simplified_res = self.py_osrm.Route(route_params)
        
        assert(full_res["routes"][0]["geometry"] != simplified_res["routes"][0]["geometry"])

    def test_route_severalannotations(self):
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            continue_straight = False,
            overview = "false",
            geometries = "polyline",
            steps = True,
            annotations = ["duration", "distance", "nodes"],            
        )
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) == 1)
        assert(not res["routes"][0]["geometry"])
        assert(res["routes"][0]["legs"][0])
        for l in res["routes"][0]["legs"]:
            assert(len(l["steps"]) > 0)
            assert(l["annotation"]
                   and l["annotation"]["distance"] 
                   and l["annotation"]["duration"] 
                   and l["annotation"]["nodes"])
            assert(not l["annotation"]["weight"]
                   and not l["annotation"]["datasources"] 
                   and not l["annotation"]["speed"])
            
        route_params.overview = "full"
        full_res = self.py_osrm.Route(route_params)

        route_params.overview = "simplified"
        simplified_res = self.py_osrm.Route(route_params)
        
        assert(full_res["routes"][0]["geometry"] != simplified_res["routes"][0]["geometry"])

    def test_route_options(self):
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            continue_straight = False,
            overview = "false",
            geometries = "polyline",
            steps = True,
            annotations = ["all"],            
        )
        res = self.py_osrm.Route(route_params)
        assert(res["routes"])
        assert(len(res["routes"]) == 1)
        assert(not res["routes"][0]["geometry"])
        assert(res["routes"][0]["legs"][0])
        for l in res["routes"][0]["legs"]:
            assert(len(l["steps"]) > 0)
            assert(l["annotation"]
                   and l["annotation"]["distance"] 
                   and l["annotation"]["duration"] 
                   and l["annotation"]["nodes"]
                   and l["annotation"]["weight"]
                   and l["annotation"]["datasources"] 
                   and l["annotation"]["speed"])
            
        route_params.overview = "full"
        full_res = self.py_osrm.Route(route_params)

        route_params.overview = "simplified"
        simplified_res = self.py_osrm.Route(route_params)
        
        assert(full_res["routes"][0]["geometry"] != simplified_res["routes"][0]["geometry"])

    # def test_route_validbearings(self):
    #     route_params = osrm.RouteParameters(
    #         coordinates = two_test_coordinates,
    #         bearings = [(200, 180), (250, 180)]       
    #     )
    #     res = self.py_osrm.Route(route_params)
    #  
    #     assert(res["routes"][0])

    #     route_params.bearings = [None, (200, 180)]
    #     res = self.py_osrm.Route(route_params)
    #  
    #     assert(res["routes"][0])

    # def test_route_validradius(self):
    #     route_params = osrm.RouteParameters(
    #         coordinates = two_test_coordinates,
    #         radiuses = [100, 100]       
    #     )
    #     res = self.py_osrm.Route(route_params)
    #  

    #     route_params.radiuses = [None, None]
    #     res = self.py_osrm.Route(route_params)
    #  

    #     route_params.radiuses = [100, None]
    #     res = self.py_osrm.Route(route_params)
    #  

    # def test_route_validapproaches(self):
    #     route_params = osrm.RouteParameters(
    #         coordinates = two_test_coordinates,
    #         approaches = [None, osrm.Approach.CURB]
    #     )
    #     res = self.py_osrm.Route(route_params)
    #  

    #     route_params.approaches = [osrm.Approach.UNRESTRICTED, None]
    #     res = self.py_osrm.Route(route_params)
    #  

    def test_route_customlimitsmld(self):
        py_osrm = osrm.OSRM(
            algorithm = "MLD",
            storage_config = mld_data_path,
            max_alternatives = 10,
            use_shared_memory = False
        )
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            number_of_alternatives = 10
        )
        res = py_osrm.Route(route_params)
        assert(isinstance(res["routes"], osrm.Array))

        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            number_of_alternatives = 11
        )
        with pytest.raises(RuntimeError) as ex:
            res = py_osrm.Route(route_params)
        assert("TooBig" in str(ex.value))

    def test_route_nomotorways(self):
        py_osrm = osrm.OSRM(
            algorithm = "MLD",
            storage_config = mld_data_path,
            use_shared_memory = False
        )
        route_params = osrm.RouteParameters(
            coordinates = two_test_coordinates,
            exclude = ["motorway"]
        )
        res = py_osrm.Route(route_params)
        assert(len(res["waypoints"]) == 2)
        assert(len(res["routes"]) == 1)

    def test_route_invalidwaypoints(self):
        route_params = osrm.RouteParameters(
            steps = True,
            coordinates = three_test_coordinates,
            waypoints = [0]
        )
        with pytest.raises(RuntimeError) as ex:
            res = self.py_osrm.Route(route_params)
        assert("InvalidValue" in str(ex.value))

        route_params = osrm.RouteParameters(
            steps = True,
            coordinates = three_test_coordinates,
            waypoints = [1,2]
        )
        with pytest.raises(RuntimeError) as ex:
            res = self.py_osrm.Route(route_params)
        assert("InvalidValue" in str(ex.value))

        route_params = osrm.RouteParameters(
            steps = True,
            coordinates = three_test_coordinates,
            waypoints = [2, 0]
        )
        with pytest.raises(RuntimeError) as ex:
            res = self.py_osrm.Route(route_params)
        assert("InvalidValue" in str(ex.value))

    def test_route_snapping(self):
        route_params = osrm.RouteParameters(
            coordinates = [(7.448205209414596,43.754001097311544),
                           (7.447122039202185,43.75306156811368)],
            snapping = "any"
        )
        res = self.py_osrm.Route(route_params)
        assert(round(res["routes"][0]["distance"] * 10) == 1315)
