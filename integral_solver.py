import time
import numpy as np
import scipy.optimize


class IS():
    
    #Implemented integral function-strings
    Z_SIMPSON_QUAD = "zSQR" # Zusammengesetzte Simpson Quadraturregel
    Z_GAUSS_QUAD = "zGQ" # Zusammengesetzte Gauß Quadratur (Ordnung wird beim Aufrufen bestimmt)
    Z_TRAPEZOIDAL = "zTR" # Zusammengesetzte Trapezregel
    Z_MIDPOINT = "zMID" # Zusammengesetzte Mittelpunktsregel
    
    @staticmethod
    def get_all_method_strings():
        '''
        Returns
        -------
        Numpy-String-Array
            Array with every possible method-string
        '''
        return np.array([IS.Z_SIMPSON_QUAD, IS.Z_GAUSS_QUAD, IS.Z_TRAPEZOIDAL, IS.Z_MIDPOINT])
    
    def _get_integration_method(self):
        if self.method==self.Z_SIMPSON_QUAD:
            return self._simpson, False
        elif self.method==self.Z_GAUSS_QUAD:
            return self._gauss_legendre, True
        elif self.method==self.Z_TRAPEZOIDAL:
            return self._trapezoidal, False
        elif self.method==self.Z_MIDPOINT:
            return self._midpoint, False
        return None, None
    
    
    def __init__(self, f, integration_time, method_string=Z_GAUSS_QUAD):
        '''
        Parameters
        ----------
        f                   : callable function (one parameter) to integrate
        integration_time    : [left, right] array for boundaries
        method_string       : Member-String that indicates integration method
        '''
        assert isinstance(method_string, str), 'method_string of wrong type, must be a Member-String!'
        self.method, self.rhs, self.T_integrate = method_string, f, integration_time
        
    
    def get_approximation(self, n_steps, integration_time=None, n_gauss_param=4, show_needed_time=False, return_needed_time=False): # if integration time is set, Standard-Gauss-order 4
        '''
        Parameters
        ----------
        n_steps : int that represents the number of subinterval (for integration)
        integration_time : optional, if a specific (other than the initialized one) integration-time is needed
        n_gauss_param : optional, if specified order of gauss-quadrature. The default is 4.

        Returns
        -------
        integral : float-type number that represents the value of the given integral
        '''
        if not (integration_time == None): self.T_integrate = np.array(integration_time) # for custom integration boundaries
        
        integral = None
        method, needs_gauss_param = self._get_integration_method()
        assert not(method == None), "Integration-method-string does not exist!"
        
        start_time = time.perf_counter()
        if needs_gauss_param: integral = method(n_steps, n_gauss_param) # Gauß-Quadratur
        else: integral = method(n_steps) # Sonstige Quadratur
        end_time = time.perf_counter()
        
        if show_needed_time: print(self.method + " integration calculated in " + str( end_time - start_time ) + "s")
        
        if return_needed_time: return integral, end_time-start_time
        else: return integral
        
        
        
        
        
        
    # Simpson-rule integration
    def _simpson(self, N):
        """Integrate f, over [left, right], using Simpson quadrature.
        N     : number of subintervals
        """
        integral = 0 #Rückgabewert des Integrals
        x_n, h = np.linspace(self.T_integrate[0], self.T_integrate[1], N + 1, retstep=True) #Die Intervallrandwerte und -breite    
        integral = (h/6) * ( self.rhs(self.T_integrate[0]) + 2 * sum(self.rhs(x_n[1:-1])) + 4 * sum(self.rhs((x_n[:-1] + x_n[1:]) / 2)) + self.rhs(self.T_integrate[1]) )
        return integral
    
    
    # Gauß-Legendre integration (chained)
    def _gauss_legendre_step(self, left, right, x_n, w_n):
        '''
        Integrate self.rhs, over [left, right], using Gauss-Legendre quadrature.
        n       : degree of the quadrature rule
        x_n     : node-parameters
        w_n     : weight-parameters
        '''
        f_ref = lambda x: ((right - left) / 2) * self.rhs( (left/2.0) * (1 - x) + (right/2.0) * (1 + x) ) # Fkt. auf neuem Referenzintervall, damit x_n und w_n passen
        integral = 0
        for n in range(len(x_n)):
            integral += w_n[n] * f_ref(x_n[n])
        return integral
    
    def _gauss_legendre(self, N, n):
        '''
        Integrate self.rhs, over self.T_integrate, using the chained Gauss-Legendre quadrature.
        n       : degree of the quadrature rule per subinterval
        N       : number of subintervals
        '''
        x_n, h = np.linspace(self.T_integrate[0], self.T_integrate[1], N + 1, retstep=True) #Die Intervallrandwerte und -breite 
        nodes, weights = scipy.special.roots_legendre(n) # Punkte x_n und Gewichte w_n der Gauß-Quadratur
        integral = sum(self._gauss_legendre_step(x_n[:-1], x_n[1:], nodes, weights))
        return integral
    
    # chained trapezoidal rule
    def _trapezoidal(self, N):
        """
        Trapezoidal quadrature of function f from left to right with N subintervals.
        N:            Number of subintervals
        """
        x_n, h = np.linspace(self.T_integrate[0], self.T_integrate[1], N + 1, retstep=True) #Die Werte x_k für später und Intervallbreite h
        integral = h/2 * self.rhs(x_n[0]) + h * sum(self.rhs(x_n[1:-1])) + h/2 * self.rhs(x_n[-1]) #Integral Berechnung:
        return integral

    # chained midpoint rule
    def _midpoint(self, N):
        """
        Integrate self.rhs, over self.T_integrate, using the midpoint rule.
        N     : number of subintervals
        """
        x_n, h = np.linspace(self.T_integrate[0], self.T_integrate[1], N + 1, retstep=True) #Die Intervallgrenzwerte und Intervallbreiten
        integral = h * sum(self.rhs((x_n[:-1] + x_n[1:]) / 2))
        return integral

    
    
    
    