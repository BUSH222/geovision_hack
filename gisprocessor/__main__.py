from graph_processor import graph_preprocess, pil_convert
from digitizer import digitizer
from las_assembler import las_assembler


class GeneralConverter:
    def __init__(self, path) -> None:
        self.image = pil_convert(path)
        self.graph_data = dict()
        self.visible_scale = dict()
        self.graph_text = dict()
        self.well_info = []
        self.graph_data_loaded = False
        self.well_data_loaded = False
        self.preprocessed_graph_objects = dict()
        self.start_axis_coords = dict()

    def load_graph_data(self, graph_num, data, scale_type, graph_text_data):
        """Scale type can be
        0 = doesnt exist
        1 = exists, secondary (this graph only)
        2 = primary (for this graph and all 0 type graphs)

        Graph data is data that goes into graph_preprocess
        (color_range=[], use_hsv=False, approx_hue, delta_hue, denoise)

        Graph text data is a dict with a graph number and a list, which contains:
        mnemonyc (MNEM) acronym for the graph, e.g (PZ)
        unit, e.g (.Ohmm)
        curve description e.g (POTENTIAL RESISTIVITY BORE)
        """
        self.graph_data[graph_num] = data
        self.visible_scale[graph_num] = scale_type
        self.graph_text[graph_num] = graph_text_data
        self.graph_data_loaded = True

    def load_well_information(self, mnem, unit, data_type, information):
        """Well information: MNEM, UNIT, DATA TYPE, INFORMATION"""
        self.well_info.append([mnem, unit, data_type, information])
        self.well_data_loaded = True
    
    def load_start_axis_coords_and_values(self, coords1, coords2, value1, value2, axis):
        """Has to be repeated twice for the coordinates to work"""
        assert axis.lower() in ['x', 'y']
        self.start_axis_coords[axis] = [coords1, coords2, value1, value2]

    def _ensure_info_is_loaded(self):
        return bool(self.path) and self.graph_data_loaded and self.well_data_loaded

    def go(self):
        assert self._ensure_info_is_loaded()
        for key, value in self.graph_data.items():
            obj = graph_preprocess(self.image, color_range=value[0], use_hsv=value[1],
                                   approx_hue=value[2], delta_hue=value[3], denoise=value[4])
            self.preprocessed_graph_objects[key] = obj
        
        for graph in self.preprocessed_graph_objects:
            digitizer
