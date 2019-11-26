from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.gis.geos import LineString, Point
from api.models import Climb
from api.serializers import ClimbListSerializer, ClimbOneSerializer, AltimeterSerializer
from api.views import ClimbViewSet, AltimeterViewSet
import json

class ClimbTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.climb_data = {
            'id':1,
            'climb_name':"Villanueva", 
            'peak_name':"El Torcal",
            'location':Point([-4.523481,36.916911,415]),
            'start':Point([-4.523481,36.916911,415]),
            'summit':Point([-4.544574,36.952726,1209]),
            'path':LineString([[-4.523481,36.916911,415],[-4.523508,36.916945,415],[-4.523554,36.916961,415],[-4.523925,36.917046,415],[-4.524041,36.917095,415],[-4.524154,36.917161,415],[-4.524259,36.917249,417],[-4.524477,36.917564,430],[-4.524744,36.918163,430],[-4.52479,36.918287,430],[-4.524843,36.918545,433],[-4.524881,36.91863,433],[-4.524967,36.918668,433],[-4.525035,36.91866300000001,437],[-4.525602,36.918433,437],[-4.525726,36.918429,437],[-4.5258,36.918474,437],[-4.525821,36.918526,437],[-4.525804,36.918606,437],[-4.52559,36.918935,437],[-4.525506,36.919153,437],[-4.525489,36.919266,447],[-4.525520000000001,36.919639,447],[-4.525509,36.919855,447],[-4.525434,36.920353,460],[-4.525441,36.920467,460],[-4.525498,36.920642,460],[-4.525552,36.920725,460],[-4.525686,36.92087300000001,466],[-4.525914,36.921068,470],[-4.525991000000001,36.92117,470],[-4.526031,36.921283,470],[-4.526057,36.921481,470],[-4.526058,36.92208500000001,477],[-4.526116,36.922992,488],[-4.526117,36.923247,488],[-4.526096,36.92339,497],[-4.526046,36.923521,497],[-4.525933,36.923673,497],[-4.525416,36.924247,498],[-4.525372,36.924325,498],[-4.525358,36.924494,498],[-4.525435,36.924608,498],[-4.525658,36.924758,498],[-4.525776,36.924859,498],[-4.525855,36.924952,505],[-4.526045,36.925281,514],[-4.526548,36.925813000000005,514],[-4.526703,36.925922,528],[-4.526797,36.925943,528],[-4.52688,36.925900000000006,528],[-4.527081,36.92550700000001,522],[-4.527145,36.925414,522],[-4.527211,36.92535,522],[-4.527325,36.925306,522],[-4.52738,36.925313,522],[-4.527415,36.925335,522],[-4.52771,36.925668,526],[-4.527815,36.925765,526],[-4.527924,36.925862,534],[-4.52828,36.926101,534],[-4.528388,36.926198,540],[-4.528427,36.926256,540],[-4.528437,36.92633,540],[-4.528424,36.926426,540],[-4.528219,36.92719,543],[-4.528199,36.927411,543],[-4.528204,36.927481,543],[-4.528241,36.927579,550],[-4.528455,36.927914,557],[-4.528427,36.928253,557],[-4.52845,36.928416,568],[-4.52862,36.928779,568],[-4.528654,36.928911,568],[-4.528624,36.929114,568],[-4.528583,36.929251,577],[-4.528533,36.929339,577],[-4.528383,36.929479,577],[-4.528255,36.92956,565],[-4.527457,36.929888,563],[-4.527442,36.930021,579],[-4.52746,36.930372,579],[-4.527517,36.930623000000004,580],[-4.527623,36.930877,593],[-4.527867,36.931312,593],[-4.528036,36.93145,593],[-4.528364,36.931652,595],[-4.528580000000001,36.931764,602],[-4.528744,36.931887,602],[-4.528882,36.932044,602],[-4.528997,36.932256,602],[-4.529006,36.932308,602],[-4.528957,36.932363,602],[-4.527889,36.933139,611],[-4.527813,36.93321900000001,611],[-4.527799,36.933294,611],[-4.527832,36.933371,619],[-4.527873,36.933413,619],[-4.528153,36.933502,619],[-4.528322,36.933578,619],[-4.528393,36.933632,620],[-4.528474,36.933736,620],[-4.528531000000001,36.933864,620],[-4.528556,36.93473500000001,630],[-4.528584,36.934856,630],[-4.528622,36.934899,630],[-4.528692,36.934925,630],[-4.528802000000001,36.934927,630],[-4.529084,36.934884,630],[-4.529339,36.934872,635],[-4.529561,36.934924,635],[-4.529661,36.934982,635],[-4.529753,36.93506,649],[-4.530133,36.93558,646],[-4.530227,36.93575,646],[-4.530251,36.935822,646],[-4.53025,36.935914,664],[-4.530175,36.936077,664],[-4.530103,36.936161,664],[-4.529632,36.936598,666],[-4.529527,36.936767,675],[-4.529477,36.937044,675],[-4.529504,36.937202,675],[-4.529584,36.9373,675],[-4.5298,36.937432,675],[-4.530641,36.937845,690],[-4.530765,36.937933,690],[-4.530916,36.938076,694],[-4.5311200000000005,36.938307,694],[-4.531724,36.9388,700],[-4.531953,36.938972,700],[-4.532668,36.939408,714],[-4.532796,36.939548,714],[-4.532884,36.939764,714],[-4.532901,36.939889,714],[-4.532889,36.940019,725],[-4.532851,36.940126,725],[-4.532785,36.940217,725],[-4.532564,36.94045,725],[-4.532486,36.940561,720],[-4.532439,36.940833,735],[-4.532459,36.940935,735],[-4.5325,36.941022000000004,735],[-4.532583,36.941083,741],[-4.532823,36.94116,741],[-4.53517,36.941777,766],[-4.535471,36.941863,766],[-4.535675,36.941943,766],[-4.535722,36.941978,766],[-4.535753,36.942056,766],[-4.53574,36.942105,766],[-4.535689,36.942144,766],[-4.535616,36.942169,766],[-4.535106,36.942206,766],[-4.535017,36.942224,766],[-4.534888,36.942285,766],[-4.534833,36.942351,766],[-4.534804,36.942423,766],[-4.534777,36.942623000000005,782],[-4.534765,36.943128,782],[-4.534792,36.943334,782],[-4.534826,36.943423,788],[-4.534928,36.943545,788],[-4.535023,36.943603,797],[-4.535112,36.943637,797],[-4.5352250000000005,36.943661,797],[-4.53534,36.943663,797],[-4.535814,36.943619000000005,797],[-4.535946,36.943629,800],[-4.536183000000001,36.943715,800],[-4.536331,36.943825,800],[-4.536371,36.943943,800],[-4.536365,36.94403,800],[-4.536332,36.944178,817],[-4.536131,36.944798,817],[-4.536125,36.944919000000006,817],[-4.536159,36.944961,817],[-4.536267,36.94499,817],[-4.536689,36.944987,820],[-4.536746,36.945004,838],[-4.536798,36.945079,838],[-4.536778,36.945167,838],[-4.53625,36.945917,848],[-4.536137,36.946022,848],[-4.53573,36.946299,839],[-4.535475,36.946439,839],[-4.534504,36.946916,846],[-4.534247,36.947104,846],[-4.534134,36.947279,834],[-4.533981,36.947726,851],[-4.533949,36.947789,851],[-4.533894,36.947845,851],[-4.533816,36.9479,851],[-4.533706,36.947949,851],[-4.533004,36.948139,845],[-4.532802,36.94824,845],[-4.53273,36.948314,845],[-4.532531,36.94872800000001,856],[-4.532366,36.948943,855],[-4.532004,36.949356,860],[-4.531783,36.949566,860],[-4.531573,36.949731,860],[-4.531385000000001,36.949851,860],[-4.531107,36.94998,860],[-4.530817,36.950101,866],[-4.530003,36.950391,866],[-4.529809000000001,36.950497,871],[-4.529733,36.95056,871],[-4.529673,36.950645,871],[-4.529641,36.950801,871],[-4.529646,36.95124,874],[-4.529596,36.951384,874],[-4.529125,36.95183,887],[-4.528533,36.952366,887],[-4.528412,36.952459000000005,887],[-4.528260000000001,36.952535,894],[-4.527703,36.952688,894],[-4.526991,36.952952,891],[-4.526555,36.953212,887],[-4.526266,36.953351,899],[-4.52572,36.953527,900],[-4.525196,36.953622,900],[-4.524857,36.953736,898],[-4.52457,36.953903,898],[-4.524088,36.954321,907],[-4.523946,36.954426,907],[-4.523592,36.954648,907],[-4.523131,36.954899,898],[-4.522212,36.955432,909],[-4.522053,36.955562,909],[-4.52162,36.95598,913],[-4.521386,36.956181,913],[-4.520915,36.956493,913],[-4.519989,36.957008,919],[-4.519805,36.957138,919],[-4.51968,36.957255,919],[-4.519585,36.957376,919],[-4.519442,36.957624,934],[-4.519392,36.95784,934],[-4.519361,36.958237,934],[-4.519333,36.958314,934],[-4.51925,36.958423,948],[-4.519147,36.958508,933],[-4.518985,36.958583,933],[-4.518563,36.958653000000005,933],[-4.51842,36.958699,933],[-4.518321,36.958755,930],[-4.518176,36.958917,930],[-4.518118,36.959007,930],[-4.518083,36.959099,930],[-4.518048,36.959281,945],[-4.517968,36.959415,945],[-4.517845,36.959496,945],[-4.517524,36.959592,945],[-4.517345,36.959683,936],[-4.517128,36.959959,936],[-4.516824,36.960301,954],[-4.516302,36.960636,933],[-4.515938,36.960838,947],[-4.515858,36.96090300000001,947],[-4.515789,36.960973,937],[-4.515407,36.961557,937],[-4.515265,36.961725,952],[-4.515164,36.961814,952],[-4.513859,36.962604,949],[-4.512727,36.963258,940],[-4.511704,36.963794,952],[-4.510848,36.964291,960],[-4.511094,36.964316,960],[-4.511236,36.964288,960],[-4.511371,36.964242000000006,960],[-4.513316,36.963539,964],[-4.513819,36.963425,983],[-4.51411,36.963331,949],[-4.51439,36.963224,968],[-4.514674,36.963088,968],[-4.514855,36.96297,968],[-4.515195,36.962784,986],[-4.51533,36.962727,986],[-4.515571,36.962655,986],[-4.516765,36.962414,990],[-4.517036,36.962377,990],[-4.517615,36.962259,1003],[-4.517855,36.962223,1003],[-4.518378,36.962195,1006],[-4.518754,36.962239,1006],[-4.518919,36.962278,1006],[-4.519376,36.962443,1006],[-4.519723,36.962524,1033],[-4.520249,36.962532,1046],[-4.520776,36.96248,1016],[-4.521183,36.962416,1031],[-4.521283,36.962388,1031],[-4.522991000000001,36.961846,1069],[-4.524807,36.961461,1065],[-4.525485,36.961242,1087],[-4.527049,36.960506,1095],[-4.527731,36.960138,1119],[-4.528696,36.959527,1110],[-4.53033,36.958715,1123],[-4.530534,36.958621,1123],[-4.530903000000001,36.958499,1135],[-4.531264,36.958447,1135],[-4.532259,36.958413,1145],[-4.532368,36.958381,1145],[-4.532846,36.958138,1173],[-4.532981,36.958114,1173],[-4.533089,36.958124,1173],[-4.533189,36.958166,1173],[-4.533472,36.958343,1171],[-4.533867,36.958638,1171],[-4.534071,36.958725,1171],[-4.534189,36.958718,1177],[-4.534401,36.958669,1177],[-4.534632,36.958673,1177],[-4.535197,36.958718,1185],[-4.53531,36.958715,1185],[-4.535423,36.958697,1185],[-4.536213,36.958447,1191],[-4.536309,36.958388,1191],[-4.53637,36.958329,1183],[-4.536561,36.958031,1183],[-4.536622,36.957982,1183],[-4.538408,36.957187,1217],[-4.538499,36.957121,1217],[-4.538838,36.956652,1205],[-4.538986,36.956513,1205],[-4.539081,36.956451,1205],[-4.540707,36.9556,1213],[-4.540846000000001,36.955551,1213],[-4.541006,36.955524,1213],[-4.541371,36.95552,1213],[-4.542184,36.955551,1211],[-4.542332,36.955541,1211],[-4.542471,36.955503,1211],[-4.543288,36.955121,1211],[-4.543414,36.955003,1207],[-4.544127,36.953771,1206],[-4.544574,36.952726,1209],[-4.544574,36.952726,1209]])
        }

        self.climb = Climb.objects.create(**self.climb_data)
        self.listSerializer = ClimbListSerializer(instance=self.climb)
        self.oneSerializer = ClimbOneSerializer(instance=self.climb)
        self.altimeterSerializer = AltimeterSerializer(instance=self.climb)
        self.climbView = ClimbViewSet.as_view(actions={'get': 'retrieve'})
        self.altimeterView = AltimeterViewSet.as_view(actions={'get': 'retrieve'})

    def test_climb_peak_name(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.peak_name, "El Torcal")

    def test_climb_virtual_name(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.name, "El Torcal por Villanueva")

    def test_climb_virtual_altitude(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.altitude, 1209.0)

    def test_climb_virtual_extent(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.extent, (-4.544574, 36.916911, -4.510848, 36.964316))

    def test_climb_virtual_gradient(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.gradient, 6.872228387112019)

    def test_climb_virtual_gain(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.gain, 794.0)

    def test_climb_virtual_distance(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.distance, 11.553748730019581)

    def test_climb_virtual_center(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.center, {
            "type": "Point",
            "coordinates": [
                -4.527561588740162,
                36.94760397652403
            ]
        })

    def test_climb_virtual_kilometers_points(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(len(climb.kilometers),13)
        self.assertEqual(climb.kilometers[1], {
            "altitude": 498.0,
            "distance": 1.0,
            "kmGradient": 8.3
        })
        self.assertEqual(climb.kilometers[12],{
            "altitude": 1209.0,
            "distance": 11.553748730019581,
            "kmGradient": 1.494247273854261
        })

    def test_climb_virtual_area(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(len(climb.area),340)
        self.assertEqual(climb.area[0],{
            'altitude': 415, 
            'distance': 0, 
            'x': 0, 
            'y': 0
        })
        self.assertEqual(climb.area[150],{
            'altitude': 766, 
            'distance': 3.854531285827735, 
            'x': 3.854531285827735, 
            'y': 351
        })
        self.assertEqual(climb.area[339],{
            "altitude": 1209.0,
            "distance": 11.553748730019585,
            "x": 11.553748730019585,
            "y": 794.0
        })

    def test_list_serializer_contains_expected_geo_fields(self):
        data = self.listSerializer.data
        self.assertEqual(set(data.keys()), set(['id','type','geometry','properties']))

    def test_properties_contains_expected_in_list_serializer(self):
        data = self.listSerializer.data
        self.assertEqual(data['properties'],{ 'name': 'El Torcal por Villanueva' })

    def test_list_serializer_contains_geojson_point(self):
        data = self.listSerializer.data
        self.assertEqual(data['geometry']['coordinates'],[-4.523481, 36.916911, 415.0])
        self.assertEqual(data['geometry']['type'], 'Point')

    def test_one_serializer_contains_expected_geo_fields(self):
        data = self.oneSerializer.data
        self.assertEqual(set(data.keys()), set(['id','type','geometry','properties']))

    def test_properties_contains_expected_in_one_serializer(self):
        data = self.oneSerializer.data
        self.assertEqual(set(data['properties'].keys()), set(['name', 'location', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center']))

    def test_one_serializer_contains_geojson_point(self):
        data = self.oneSerializer.data
        self.assertEqual(data['geometry']['type'], 'LineString')
        self.assertEqual(len(data['geometry']['coordinates']),340)

    def test_altimeter_serializer_contains_expected_fields(self):
        data = self.altimeterSerializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'kilometers', 'area']))

    def test_climb_viewset_list_route(self):
        request = self.factory.get('/api/climb')
        view = ClimbViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['type'],"FeatureCollection")
        self.assertEqual(len(response.data['features']),1)
    
    def test_climb_viewset_one_route(self):
        request = self.factory.get('/api/climb')
        view = ClimbViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id','type','geometry','properties']))