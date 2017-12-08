"""
curved_distances.py
 
Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at
 
Created: Mon Nov 20 18:13:47 CET 2017
 
This is an ImageJ-pluging writen in Jython. Jython is the Python 
implementation to run the Java platform in ImageJ. Check
https://imagej.net/Jython_Scripting

It calculates the intersomatic distance between cells in the dentate gyrus.
The curvature of the dentate is accounted by plotting a circumference
around the area of the dentate gyrus where the recordings were made
similarly as in claw curvatures were measured in Feduccia 1993 [1].

The circumference is computed based on three points given by the user.
Its center will be used to estimate the arc-length between two somata.
It is made by computing the intersection between the bisector of line
between two cells and the parallel to this line with the center of the
circumference computed first.

To install the plugin use Plugins->Install Pluging... in Fiji and 
select this file.

Tested on ImageJ 1.51n, Java 1.8.0_66 (64-bit)

Reference:
----------
[1] Feduccia A (1993) Evidence from Claw Geometry Indicating Arboreal
Habits of Archaeopteryx. Science, Feb 5;259:790-793.
"""

from ij import WindowManager, IJ
from ij.plugin.frame import RoiManager

from ij.gui import WaitForUserDialog 
from ij.gui import Line, OvalRoi, PointRoi

from ij.measure import ResultsTable
 
from java.awt import Color
 
import math

__version__ = 0.2

class Circumference(object):
    """
    Calculates a circle based on the location of three points. The points
    are given as PointRoi objects containing x and y coordinates.

    """ 
    def __init__(self, pointlist = None):
        """
        Arguments:
        ----------
        pointlist: list
             a list with three PointRois containing the three points of
             a circle to be obtained.
        """
        
        A, B, C = pointlist
        # get slope and y-intercept from bisector lines
        line1 = self.get_bisector_equation( segment = (A,B) )
        line2 = self.get_bisector_equation( segment = (B,C) )

        # compute intersection from bisector lines
        self.center = self.get_intersect_from_param(line1, line2)
        
    def get_distance(self, segment):
        """
        Calculates the distance of a segment. 
        A segment is a tuple, like (A,B) where A and B are PointRoi objects.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        Returns:
        --------
        distance in pixels
        """
        A, B = segment # must be PointRoi

        x1, y1 = A.XBase, A.YBase
        x2, y2 = B.XBase, B.YBase
        
        dist = math.sqrt( math.pow(x1-x2,2) + math.pow(y1-y2,2) )
        return dist
        
    def get_midpoint(self, segment):
        """
        Computes the mid point of a segment
        A segment is a tuple, like (A,B) where A and B are PointRoi objects.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        Returns:
            Returns a tuple with the slope and the y-intercept of the line.
        """
        A, B = segment # must be PointRoi

        x1, y1 = A.XBase, A.YBase
        x2, y2 = B.XBase, B.YBase

        xmidpoint = ( x1 + x2 )/2
        ymidpoint = ( y1 + y2 )/2
        
        return PointRoi( int(xmidpoint), int(ymidpoint))
        
    def get_line_equation(self, segment):
        """
        Computes the line equation (slope,  m and the y-intercept,a )of the
        line crossing trought two points. Points are given as segment,
        from a tuple, like (A,B), where A and B are PointRoi objects.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        Returns:
            Returns a tuple with the slope and the y-intercept of the line.
        """

        A, B = segment # must be PointRoi

        x1, y1 = A.XBase, A.YBase
        x2, y2 = B.XBase, B.YBase

	    # slope (m) and y-intercept (a)
        try:
            m = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError: # undefined slope, e.g., x = 2
            m = (y2 - y1) / (x2 - (x1+1)) # move one pixel

        a = y1 - m * x1

        return (m, a)

    def get_bisector_equation(self, segment):
        """
        Computes the line equation (slope, m and y-intercept, a) of the
        perpendicular bisector of a segment. A segment is a tuple,
        like (A,B), where A and B are PointRoi objects.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        Returns:
            Returns a (m, a) tuple with the slope (m) and y-intercept (a)
            of the bisector line.
        """
        A, B = segment # must be PointRoi

        x1, y1 = A.XBase, A.YBase
        x2, y2 = B.XBase, B.YBase

        xmidpoint = ( x1 + x2 )/2
        ymidpoint = ( y1 + y2 )/2

        # avoid zero-division (undefined slope)
        if y1 == y2: 
            y2 +=1 # move one pixel

        # slope perpendicular -1/m
        m = -(x2 - x1) / (y2 - y1)
            
        a = ymidpoint - m * xmidpoint

        return(m, a)

    def get_intersect_from_param(self, param1, param2):
        """
        Calculates the point (x,y) from the intersection of two lines. 
        Form the equations for the lines, 

        y = m_1 * x + a_1

        and,
 
        y = m_2 * x + a_2

        the (x,y) coordinates of the intersection can be calculated as:
        x = (a_1 - a_2) / (m_2 - m_1)
        y = ( a_1 * m_2 - a_2 * m_1) / ( m_2 - m_1 )

        Arguments:
        ----------
        param1: tuple       
            the slope (m) and y-intercept of a line

        param1: tuple       
            the slope (m) and y-intercept of a line

        Returns:
        --------
        A PointRoi with the coordinates of the intersection.
        """

        m1, a1 = param1
        m2, a2 = param2

        try:
            x = (a1 - a2) / (m2 - m1)
        except ZeroDivisionError: #(m1 == m2)
            raise ZeroDivisionError("Lines are parallel")
            
        # now that lines are not parallel, we compute y
        y = ( a1 * m2 - a2 * m1) / ( m2 - m1 )

        return PointRoi( int(x), int(y) )

    def get_angle(self, segment, center = None):
        """
        Calculate the angle of the formed by the lines from the center
        of the circle (X) and the extreme points of the segment (A,B). 
        It is calculated using the law of cosines.

        c^2 = a^2 + b^2 - 2*a*b*cos(phi),

        where a, b and c are sides, and phi is the angle opposite side c
        
        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        center: a PointRoi 
            the center of a circle, if not, taken form the object

        """
        A, B = segment
        if center is None:
            C = self.center
        else:
            C = center

        a = self.get_distance(segment = (X,A))
        b = self.get_distance(segment = (X,B))
        c = self.get_distance(segment = (A,B))


        pow2 = lambda x: math.pow(x,2) 
        phi = math.acos( (pow2(a) + pow2(b) - pow2(c) ) / (2 * a * b) )

        return ( math.degrees(phi) ) # from radians to degrees


    def get_arclength(self, segment, center = None):
        """
        Calculates the arc length of an angle from the center of the
        circle.

        arc_length = (2* PI * r ) * (alpha/360)

        where r is the radius, and alpha is the angle between the two
        lines formed between AX and BX.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        center: a PointRoi 
            the center of a circle, if not, taken form the object
        """
        A, B = segment
        if center is None:
            X = self.center
        else:
            X = center

        PI = math.pi
    
        # radius can be calculated form AX, or BX
        ct = IJ.getImage().getCalibration()
        r =  self.get_distance( (A, X))
        angle = self.get_angle(segment, X)

        arc_length = 2*PI*r*(angle/360.)
        return arc_length 

    def get_parallel_equation(self, segment, point = None):
        """
        Calculate the line parallel to the segment passing through point.

        Arguments:
        ----------
        segment: tuple
            (A,B), where A and B are PointRoi objects with x,y coordinates.

        point: a PointRoi 
            if None, the center of a circle
        
        """
        m, a = self.get_line_equation(segment)

        if point is None:
            x, y  = self.center.XBase, self.center.YBase
        else:
            x, y  = point.XBase, point.YBase
        
        # to calculate the y-intercept, solve for b in y = b + m * x
        b = y - m * x

        return(m, b)
        
        
def set_circlepoints(RoiManager):
    """
    Sets three PointRois (A, B and C) in the current image and allow its
    manipulation within the ROI manager. It recalls its coordinates upon
    user-manipulation.

    Arguments:
    ----------
    Roimanager: RoiManager
        a RoiManager can be created with RoiManager().getInstance()

    Returns:
    --------
    A list with of PointRois with the (x,y) coordinates 
    of three points.
    """

    imp = WindowManager.getCurrentImage() # use current image 
    index = RoiManager.getCount() # number of items in the ROI

    # create points
    #A = PointRoi(imp.getWidth()/3, imp.getHeight()/2)
    A = PointRoi(722-100,512+100)
    A.setName('A')
    #B = PointRoi(imp.getWidth()/2, imp.getHeight()*1/5)
    B = PointRoi(722,512) # center
    B.setName('B')
    #C = PointRoi(imp.getWidth()*2/3, imp.getHeight()/2)
    C = PointRoi(722+100,512+100)
    C.setName('C')

    for p in [A, B, C]: # common features
        p.setSize(4) # extra-large
        p.setStrokeColor(Color.GREEN)
        RoiManager.addRoi(p)


    # Allow user to move the points
    IJ.setTool('Point') 
    RoiManager.runCommand(imp, "Show All with labels") # update in ROI
    WaitForUserDialog("Curvature Measure", \
        "Move the points and press OK to compute the center").show()

    # read the last three entries in the ROI manager
    p_list = [RoiManager.getRoi(i) for i in range(index, index+3)]
    return (p_list) 

def draw_Line(segment, RoiManager = None,  color = None, label = None ):
    """
    Draw a line thourgh a segment in the current image and RoiManager.
    A segment is a tuple, like (A,B) where A and B are PointRoi objects.

    Arguments:
    ----------
    segment: tuple
        (A,B), where A and B are PointRoi objects with x,y coordinates.

    Roimanager: RoiManager
        a RoiManager can be created with RoiManager().getInstance()
    
    color: the line color
        a java.awt color, for example Color.GREEN

    label : string
        a the name of the line (default is None)
    
    Returns:
    --------
    A line through the points given. Returns a tuple with 
    the slope and the y-intercept of the line.
    
    """

    start, end = segment

    myLine = Line(start.XBase, start.YBase, end.XBase, end.YBase)
    myLine.setStrokeColor( Color.GREEN )

    if label:
        myLine.setName( label )
    else:
        myLine.setName( ' ' )

    if color:
        myLine.setStrokeColor( color )

    if RoiManager is not None:
        RoiManager.addRoi(myLine)

def draw_Circle(center, diam, RoiManager, label = None):
    """
    Draw a circle of a given diameter in the current image and
    RoiManagers.

    Arguments:
    ----------
    center: PointRoi
        a (x,y) coor. It can be obtained from Roi
        with WindowManager.getCurrentImage().getRoi()

    diam: float 
        the diameter of the circle

    Roimanager: RoiManager
        a RoiManager can be created with RoiManager().getInstance()


    label : string
        a the name of the circle (default is None)
    
    Returns:
    --------
    A circle through the points given. Returns a tuple with 
    x and y coordinates of its center.
    """

    xloc = center.XBase - diam/2 
    yloc = center.YBase - diam/2 
    # to draw a circle we must move the coordinates
    myCircle = OvalRoi(xloc,yloc, diam,diam)
    myCircle.setStrokeColor( Color.RED)
    myCircle.setName( label ) 
    RoiManager.addRoi( myCircle)

#=========================================================================
# Main program
# see why if __name__ == '__main__': cannot be used
# http://forum.imagej.net/t/jython-isssue-with-if---name-----main--/5544/2
#=========================================================================

if __name__ in ['__builtin__', '__main__']:

    # remove previous ROI if existing
    if RoiManager().getInstance().getCount(): # if >0
        WindowManager.getWindow("ROI Manager").close() # close ROI Manager
        
    # get current image and calibration
    imp = WindowManager.getCurrentImage()
    ct = IJ.getImage().getCalibration()

    # Prepare RoiManager with labels and names
    myRoiManager = RoiManager().getInstance() # ROI Manager 
    #myRoiManager.runCommand("UseNames", "true")

    # use Circle custom object
    A, B, C = set_circlepoints(RoiManager = myRoiManager) 
    mycircle = Circumference([A,B,C])
    X = mycircle.center
    diam = mycircle.get_distance(segment = (X,B)) * 2

    draw_Line(segment = (A, B), RoiManager = myRoiManager, label = 'AB')
    draw_Line(segment = (B, C), RoiManager = myRoiManager, label = 'BC')

    # Draw a circle through three point
    draw_Circle(center = X, diam =diam, RoiManager = myRoiManager, label = 'X')


    IJ.setTool('polygon') # switch to polygon-tool
    WaitForUserDialog("Cell selection","Select on the cell somata and press OK to compute the curvatures").show()
    mypoly = imp.getRoi()
    mypoly.setName ('somata')
    mypoly.setStrokeColor(Color.YELLOW)
    myRoiManager.addRoi( mypoly ) # allow user-manipulation

    # obtain points from the polygon
    # and transform polygon coordinates into PointRois
    ncells = mypoly.getNCoordinates;
    P = zip(mypoly.getFloatPolygon().xpoints,mypoly.getFloatPolygon().ypoints)
    mycell = list()
    for x,y in P:
        mycell.append(PointRoi(int(x), int(y)))

    #======================================================================
    # Result table 1: compute euclidean distances in physical units
    #======================================================================
    rt1 = ResultsTable()
    for row, pre in enumerate(mycell):
        rt1.incrementCounter() # jump to next row
        P1 = pre 
        for col,post  in enumerate(mycell):
            P2 = post
            mysegment = (P1,P2)
            mydist = mycircle.get_distance( segment = mysegment )
            rt1.addValue(col, ct.getX( mydist ) )

    rt1.show('Euclidean distances ' + imp.getTitle())
            
    #======================================================================
    # Result table 2: compute curvature for every segment
    #======================================================================
    rt2 = ResultsTable()
    for row, pre in enumerate(mycell):
        rt2.incrementCounter()
        P1 = pre
        for col, post in enumerate(mycell):
            P2 = post
            myseg = (P1,P2)
            if row==col:
                rt2.addValue(col, 0)
            else:
                l1 = mycircle.get_bisector_equation( myseg )
                l2 = mycircle.get_parallel_equation( myseg, X )
                I = mycircle.get_intersect_from_param( l1, l2 )
                arc_length = ct.getX( mycircle.get_arclength(myseg, I) )
                rt2.addValue(col, arc_length)
                # plot from I to midline
                F = mycircle.get_midpoint(myseg)
                label = 'bisect ' + str(col+row)
                draw_Line(myseg, myRoiManager, Color.YELLOW, label)
                draw_Line((I,F), myRoiManager, color=Color.BLUE)

    rt2.show('Curvature distances ' + imp.getTitle())

    #======================================================================
    # Tests
    #======================================================================
    print('\n======DEBUG==========================\n')
    AB = 14.1
    BC = 14.1
    AC = 20.

    P1 = PointRoi(622,212)
    P1.setName('P1')
    P2 = PointRoi(822,212)
    P2.setName('P2')
    P3 = PointRoi(822,412)
    P3.setName('P3')
    P4 = PointRoi(622,412)
    P4.setName('P4')

    X1 = PointRoi(622,512)
    X1.setName('X1')

    X2 = PointRoi(822,512)
    X2.setName('X2')

    mypoints = [P1, P2, P3, P4]
    for p in [P1, P2, P3, P4, X1, X2]:
        p.setSize(4)
        p.setStrokeColor(Color.MAGENTA)
        myRoiManager.addRoi(p)
    
    # TABLE 3 #
    rt3 = ResultsTable()
    for row, pre in enumerate(mypoints):
        rt3.incrementCounter()
        for col, post in enumerate(mypoints):
            myval = row + col
            myseg = (pre, post)
            myval = mycircle.get_distance(segment = myseg)
            rt3.addValue(col, myval)

    rt3.show('TEST_DIST')
    
    rt4 = ResultsTable()
    for row, pre in enumerate(mypoints):
        rt4.incrementCounter()
        for col, post in enumerate(mypoints):
            myval = row + col
            myseg = (pre, post)
            if row == col:
                myval = 0
            else:
                l1 = mycircle.get_bisector_equation(segment = myseg) 
                l2 = mycircle.get_parallel_equation(segment = myseg, point =X)
                I = mycircle.get_intersect_from_param(l1, l2)
                myval = mycircle.get_arclength(segment = myseg, center= I) 

            rt4.addValue(col, myval)

    rt4.show('TEST_ARC')
    
    #print mycircle.get_distance(segment = (A,B)) # AB = 141.42 pix
    #print mycircle.get_distance(segment = (B,C)) # BC = 141.42 pix
    #print mycircle.get_distance(segment = (A,C)) # AC = 200.00 pix
    
    
    #print mycircle.get_angle(segment = (A,B)) # 90
    #print mycircle.get_arclength(segment = (A,B)) # 156.2 
    #print mycircle.get_arclength(segment = (B, C)) # 156.2 
    #print mycircle.get_arclength(segment = (A,C)) # 156.2 *2  (pi)
    #print mycircle.get_distance(segment = (P1,P2))
    #print mycircle.get_angle(segment = (P1,P2))
    #print 'AX1 ang' + str(mycircle.get_angle(segment = (A,X1), center = X))
    #print 'X1X2 ang' + str(mycircle.get_angle(segment = (X1,X2), center = X))
    l1 = mycircle.get_bisector_equation(segment = (P1, P2))
    l2 = mycircle.get_parallel_equation(segment = (P1, P2), point = X)
    print(l2)
    I = mycircle.get_intersect_from_param(l1, l2)
    M = mycircle.get_midpoint((P1,P2))
    draw_Line((M,I), myRoiManager, Color.MAGENTA, 'test')
    myRoiManager.addRoi(I)
    I.setColor(Color.ORANGE)
    I.setSize(4)
    I.setName('I')
    print(I)
    print('\n==END-DEBUG==========================\n')

