import numpy as np
from svgpathtools import svg2paths


class SVG_Handler():
    
    
    def __init__(self, svg_path : str):
        self.path = svg_path
        
        # load svg file to process as parametrized function
        self._load_svg()
        
        
    
    
    def _load_svg(self):
        tmp_paths, tmp_attributes = svg2paths(self.path)
        self.all_functions = [] # here we will safe all callable saved curves
        self.all_paths = []
        for path in tmp_paths: # iterate through all paths
            tmp_paths = []
            
            for path_obj in path:
                #print(path_obj)
                numpy_poly = path_obj.poly() # every curve ranges from 0 to 1
                
                self.all_functions += [numpy_poly] # append curve to internal array of curves
                tmp_paths += [numpy_poly]
                
            self.all_paths += [tmp_paths]
               
        self.line_count = len(self.all_functions) # total number of lines
        #self._sort_functions() # kind of sorts the distinct paths --> does not really work if you used a "free hand drawing" in the svg
        
        
    def _get_next_func(self, prev_func, left_funcs): # returns index of next function
        end_point = prev_func(1)
        left_beginnings = np.array([func_t(0) for func_t in left_funcs], dtype=complex)
        
        nearest_index = np.argmin(np.abs(np.conjugate(left_beginnings - end_point)))
        return nearest_index
        
        
    def _sort_functions(self): # should sort functions such that the curve is mostly "steady"
        #print(self.all_functions)
        tmp_funcs = self.all_functions
        
        new_functions = [tmp_funcs[0]]
        tmp_funcs.pop(0)
        
        for i in range(1, self.line_count): # here add next function and remove if from list
            next_ind = self._get_next_func(new_functions[-1], tmp_funcs)
            new_functions += [tmp_funcs[next_ind]]
            tmp_funcs.pop(next_ind)
            
        self.all_functions = new_functions
    
    
    
    
    def get_whole_image(self, N_per_curve=50): # returns all data points for the whole image (takes into account that discontinuities should not be connected)
        t_param = np.linspace(0, 1, N_per_curve)        
        
        ret_path = [] 
        #print(points_to_plot)
        for i, path in enumerate(self.all_paths):
            points_to_plot = [] # self.get_point(t_param)
            
            for func in path:
                points_to_plot += [func(t_t) for t_t in t_param]
            
            ret_path += [points_to_plot]
        
        #print(ret_path)
        #ret_path = np.array(ret_path, dtype=complex)
        real_part = [[points_t.real for points_t in path] for path in ret_path]
        imag_part = [[-points_t.imag for points_t in path] for path in ret_path]
        #print(ret_path)
        #print(real_part)
        #print(imag_part)
        #print(real_part)
        return real_part, imag_part # minus because of some weired normalization?!
    
    
    def _get_parameter_func(self, t):
        func_index = int(t * self.line_count)
        
        if func_index == self.line_count: # means we are at the end
            return 1, self.all_functions[func_index-1]
        
        lower_bound = func_index/self.line_count
        upper_bount = lower_bound + 1/self.line_count
        
        new_ret_t = t/(upper_bount-lower_bound) - lower_bound/(upper_bount-lower_bound)
        
        return new_ret_t, self.all_functions[func_index]
    
    
    def _single_points(self, t, reverse): # t is between zero and one
        if reverse:
            t = -t + 1 # reverse for T \in [0, 1] 
        use_t, use_func = self._get_parameter_func(t)
        return use_func(use_t)
    
    
    def get_point(self, t, reverse=False):
        if isinstance(t, float):
            t = [t]
            
        t = np.array(t)
        
        assert np.all(0 <= t) and np.all(t <= 1), "t has to be between 0 and 1"
        return np.array([self._single_points(t_t, reverse) for t_t in t])
    
        #if isinstance(t, float):
        #    return self._single_points(t)
        #elif isinstance(t, list):
        #assert False, "Parameter t has to be an instance of list (containing floats) or float"
        
            
            



