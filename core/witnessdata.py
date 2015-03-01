from naglib.startup import TOL, DPS
from naglib.exceptions import ExitSpaceError, WitnessDataException
from naglib.core.base import NAGobject, Point, AffinePoint, ProjectivePoint

class WitnessPoint(Point):
    """
    A single witness point for an algebraic set
    """
    def __init__(self, coordinates, component_id, is_projective=False):
        """
        Initialize the WitnessPoint object.

        Keyword arguments:
        point        -- AffinePoint or ProjectivePoint
        component_id -- int, the id of the component to which self belongs
        """
        super(WitnessPoint, self).__init__(coordinates)
        self._component_id = component_id
        self._is_projective = is_projective
        if isinstance(coordinates, AffinePoint):
            self._is_projective = False
        elif isinstance(coordinates, ProjectivePoint):
            self._is_projective = True
            
        # sanity check projective point
        if self._is_projective:
            summa = sum([abs(c) for c in self._coordinates])
            if summa < TOL:
                raise ExitSpaceError('{0} is not in projective space'.format(list(self._coordinates)))

    def __repr__(self):
        """
        x.__repr__() <==> repr(x)
        """
        coordinates = self._coordinates
        cid = self._component_id
        is_projective = self._is_projective
        
        if is_projective:
            coorstr = 'ProjectivePoint([' + ','.join([str(c) for c in coordinates]) + '])'
        else:
            coorstr = 'AffinePoint([' + ','.join([str(c) for c in coordinates]) + '])'
        repstr = 'WitnessPoint({0},{1})'.format(coorstr,cid)
        
        return repstr
    
    def __str__(self):
        """
        x.__str__() <==> str(x)
        """
        coordinates = self._coordinates
        is_projective = self._is_projective
        
        if is_projective:
            repstr = '[' + ' : '.join([str(c) for c in coordinates]) + ']'
        else:
            repstr = '[' + ', '.join([str(c) for c in coordinates]) + ']'
            
        return repstr
    
    def dehomogenize(self):
        """
        Dehomogenize the witness point
        
        Returns a new WitnessPoint object
        """
        component_id = self._component_id
        coordinates = self._coordinates
        is_projective = self._is_projective
        
        if is_projective:
            point = ProjectivePoint(coordinates)
        else:
            point = AffinePoint(coordinates)
            
        return WitnessPoint(point, component_id)
    
    @property
    def component_id(self):
        return self._component_id
    
    @property
    def point(self):
        coordinates = self._coordinates
        is_projective = self._is_projective
        if is_projective:
            return ProjectivePoint(coordinates)
        else:
            return AffinePoint(coordinates)

class WitnessSet(NAGobject):
    """
    A witness set for a component
    """
    def __init__(self, system, slice, witness_points):
        """Initialize the WitnessSet
        
        Keyword arguments:
        polynomials -- PolynomialSystem, system on which all the points vanish
        slice -- LinearSystem, system defining a generic linear space
        witness_points -- iterable of WitnessPoint objects,  witness point set, V(f) \cap V(L)
        """
        self._system = system
        self._slice = slice
        try:
            self._witness_points = list(witness_points)
        except TypeError:
            self._witness_points = [witness_points]
            
        wp = self._witness_points[0]
        self._component_id = wp._component_id
        for w in self._witness_points:
            if w._component_id != self._component_id:
                msg = 'WitnessPoint {0} and WitnessPoint {1} do not lie on the same component'.format(wp, w)
                raise WitnessDataException(msg)
    
    def __repr__(self):
        """
        x.__repr__() <==> repr(x)
        """
        sy = self._system
        sl = self._slice
        wp = self._witness_points
        repstr = 'WitnessSet({0},{1},{2})'.format(repr(sy), repr(sl), repr(wp))
        
        return repstr
    
    def __str__(self):
        """
        x.__str__() <==> str(x)
        """
        wp = self._witness_points
        repstr = '{' + ', '.join([str(p) for p in wp]) + '}'
        
        return repstr
        
    @property
    def system(self):
        return self._system
    @property
    def slice(self):
        return self._slice
    @property
    def witness_points(self):
        return self._witness_points