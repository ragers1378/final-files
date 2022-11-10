import numpy as np

#Funtions are named with respect to which part of the file they create

#--------------------------------------------------------------------------#
#-----------------------Vertices Functions---------------------------------#
#--------------------------------------------------------------------------#

#Main Ellipse Function        
def vertices(rec_h,rec_w,ellipse_w,ellipse_h,ellipse_w_outer,ellipse_h_outer,foc_inner_x,foc_outer_x):

    #Outer ellipse y value at focus point
    foc_outer_y=ellipse_find(ellipse_w_outer,ellipse_h_outer,foc_outer_x,1)
    
    #Array for rectangular point in vertices
    rec_x=[-1*rec_w,-1*foc_outer_x,0,foc_outer_x,rec_w]
    rec_y=[-1*rec_h,-1*foc_outer_y,0,foc_outer_y,rec_h]
    
    #print(rec_x,rec_y)
    #Writing script of vertices
    Vertices="vertices "+"( \n\n"
    
    #points list 
    vertices_point=[]

    #obtain first part of vertices list
    #First section is consist of rectangular points
    vertices_point+=movement(rec_x,-rec_h,2)                        #rectangular bottom surface points
    vertices_point+=movement(rec_y[1:],rec_w,1)                     #rectangular right surface points
    vertices_point+=movement(list(reversed(rec_x))[1:-1],rec_h,2)   #rectangular top surface points
    vertices_point+=movement(reversed(rec_y[1:]),-rec_w,1)          #rectangular right surface points
    
    #ellipses x points
    ellipse_point_outer=[-1*ellipse_w_outer,-1*foc_outer_x,0,foc_outer_x,ellipse_w_outer]
    ellipse_point_inner=[-1*ellipse_w,-1*foc_inner_x,0,foc_inner_x,ellipse_w]
    
    #second part of the vertices is consist of ellipses points
    vertices_point=ellipse_points(vertices_point, ellipse_point_outer, ellipse_w_outer, ellipse_h_outer)
    vertices_point=ellipse_points(vertices_point, ellipse_point_inner, ellipse_w, ellipse_h)
    
    #obtaining 3D(front and rear) points.
    #Thickness in third dimension is kept so low to have a 2D model
    Vertices=vertices_2d_to_3d_and_write(vertices_point,Vertices) + ")"
    
    return Vertices+"; \n\n"


#Find a specific y value for given point
def ellipse_find(ellipse_w,ellipse_h,x,region):

    y=abs(((ellipse_h**2)-( ((ellipse_h**2)*(x**2))/(ellipse_w**2)  ) )**(0.5))   #Ellipse Formula
    
    return y*region

#Iterate the list on a direction
#Direction is given as static_pos
def movement(lis,static_loc,static_pos):
    vert_lis=[]
    
    if(static_pos==2):       
        
        for i in lis:
            #print([i,static_loc])  
            vert_lis.append([i,static_loc])  
    
    else:
        for i in lis:
            #print([static_loc,i])  
            vert_lis.append([static_loc,i])  
    
    return vert_lis



#Find Ellipse point for an given interval
#Interval is given with ellipse_point variable
def ellipse_points(vertices_point,ellipse_point,ellipse_w,ellipse_h):
    
    for region in [-1,1]: #region define the y value location
    
        for x in ellipse_point:

            y=ellipse_find(ellipse_w,ellipse_h,x,region)           
            vertices_point.append([x,y])
   
        ellipse_point=list(reversed(ellipse_point))[1:-1]
    
    return vertices_point
    
#Convert 2D point to 3D points with 0.1 Z offset
def vertices_2d_to_3d_and_write(vertices_point,Vertices):
    number=0
    
    for z in [0,1]:
        for x,y in vertices_point:
            number=number+1
            
            Points= "(" +str(round(x,3))+" "+str(round(y,2))+" "+str(int(z))+")"
            Vertices=Vertices+Points+(20-len(Points))*" "+"////"+str(int(number-1))+"\n"
        
        Vertices=Vertices+2*"\n"
    return Vertices


#--------------------------------------------------------------------------#
#--------------------------Block Functions---------------------------------#
#--------------------------------------------------------------------------#


#Main block function, it takes one argument which is cell_number
def blocks(cell_number):
    
    #Block location of the set is given in array. Mesh is consist of 20 blocks 
    block_rear=[
           [0,1,17,15],[1,2,18,17],[2,3,19,18],[3,4,5,19],
           [19,5,6,20],[20,6,7,21],[21,7,8,9],[22,21,9,10],
           [23,22,10,11],[13,23,11,12],[14,16,23,13],
           [15,17,16,14],[16,17,25,24],[17,18,26,25],
           [18,19,27,26],[19,20,28,27],[28,20,21,29],
           [30,29,21,22],[31,30,22,23],[24,31,23,16]   ]
    
    #Matching the rear and front section blocks
    block=[]
    for p1,p2,p3,p4 in block_rear:
        block.append( [p1,p2,p3,p4,p1+32,p2+32,p3+32,p4+32] )

    line="blocks  ( \n\n"
    grade=cell_grade(cell_number)  #grade is the number of the element in a direction of the block.

    #Creating the writing script by following the writing rule of openfoam
    for i in range(len(block)):
        current_line="" 
        current_line=current_line+"hex "+"("+''
     
        for j in range(8):
            
            if(j==7):
                current_line=current_line+str(block[i][j])+""        #points for the block
            else:
                current_line=current_line+str(block[i][j])+"  "
                 
        current_line=current_line+")"+" "
        current_line=current_line+"("+str(grade[i][0])+" "+str(grade[i][1])+" "+str(grade[i][2])+")"+" "
        current_line=current_line+"simpleGrading"+" (1 1 1)"
        line=line+current_line+(abs(70-len(current_line)))*" "+"// Block Number "+str(i)+2*"\n"

    line=line+")"+";"
    return line


#This function create the cell numbers which each block must have

def cell_grade(cell_number):
    
    #k is a cell factor. Each block cell are defined with respect to k
    k=int((cell_number/20)**(0.5))  
    
    grade=[[2*k,k,1],[k,k,1],[k,k,1],[2*k,k,1],
           [2*k,k,1],[2*k,k,1],[2*k,k,1],[k,k,1],
           [k,k,1],[2*k,k,1],[2*k,k,1],[2*k,k,1]] + 8*[[k,k,1]] 
    
    return grade



#--------------------------------------------------------------------------#
#-----------------------Edges Functions------------------------------------#
#--------------------------------------------------------------------------#

#Main Edges Function
def edges(ellipse_w,ellipse_h,ellipse_w_outer,ellipse_h_outer,foc_inner_x,foc_outer_x):
    
    line=""
    
    #polyLine edges numbers name
    vertices_outer=np.linspace(16,23,8)  #Inner Ellipse Surface Points
    vertices_inner=np.linspace(24,31,8)  #Outer Ellipse Surface Points
    
    #Merge the first point name since ellipse ends at its starting points name of inner and outer ellipses
    vertices_outer=np.append(vertices_outer,vertices_outer[0]) 
    vertices_inner=np.append(vertices_inner,vertices_inner[0])    
    
    #x points of the inner ellipse points
    x_inner=[-1*ellipse_w,-1*foc_inner_x,0,foc_inner_x,ellipse_w]
    x_inner += list(reversed(x_inner))[1:]    
    
    #x points of the outer ellipse
    x_outer=[-1*ellipse_w_outer,-1*foc_outer_x,0,foc_outer_x,ellipse_w_outer]
    x_outer += list(reversed(x_outer))[1:] 

    #combining value and the name of the points  
    line=line+edges_points(ellipse_w,ellipse_h,vertices_inner,x_inner)
    line=line+edges_points(ellipse_w_outer,ellipse_h_outer,vertices_outer,x_outer)
    
    return "edges (\n\n\n"+line+");"
 
 
#This function merge points name and value
#Names are required during defining polyline 
#points are required to draw spline by blockmesh      
def edges_points(x,y,vertices,x_points):
    
    line=""    
    for i in range(len(vertices)-1):
         
        x_rear1=vertices[i]
        x_rear2=vertices[i+1]                        
                        
        x_front1=vertices[i]+32
        x_front2=vertices[i+1]+32
        
        if(x_rear1 >= vertices[4]):
            region=1
        else:
            region=-1

        line=line+script(x,y,x_points[i],x_points[i+1],x_rear1,x_rear2,region,0)
        line=line+script(x,y,x_points[i],x_points[i+1],x_front1,x_front2,region,1)      
    
    return line


 
#This Function produce proper writing script for blockmesh file
def script(ellipse_w,ellipse_h,x_point1,x_point2,x_point1_name,x_point2_name,region,z):
    a=ellipse_w
    b=ellipse_h
    line="polyLine "+ str(int(x_point1_name)) +" "+str(int(x_point2_name))+" (" 

    lis=np.linspace(x_point1,x_point2,50)

    for x in lis:
        
        y=abs(((b**2)-((b*b*x*x)/(a*a)))**(0.5))
        line=line+"("+str(x)+" "+str(y*region)+" "+str(z)+")\n"
        

    line=line+")\n\n"

    return line
 






#--------------------------------------------------------------------------#
#-------------- Title,Boundary,control,fvSchemes,fvSolution----------------#
#--------------------------------------------------------------------------#

#Returns script that contains title part of the file
def Title():
    a=""" 
/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n
                         """
                         
    return a

#--------------------------------------------------------------------------#

#Boundary part left blank
def boundary():
    
    line="""
boundary
(
 
);                   
         """    
    return line


#--------------------------------------------------------------------------#

#controlDict file's content
def control():
    line_control="""
   
/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

application     icoFoam;

startFrom       startTime;

startTime       0;

stopAt          endTime;

endTime         0.5;

deltaT          0.005;

writeControl    timeStep;

writeInterval   20;

purgeWrite      0;

writeFormat     ascii;

writePrecision  6;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable true;


// ************************************************************************* //
    
    """    
    return line_control

#--------------------------------------------------------------------------#

#fvSchemes File's Content
def fvSchemes():
    line="""
/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    grad(p)         Gauss linear;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}


// ************************************************************************* //

"""
    return line
    
#--------------------------------------------------------------------------#    

#fvSolution file's content
def fvSolution():
    line="""


	/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solvers
{
    p
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.05;
    }

    pFinal
    {
        $p;
        relTol          0;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-05;
        relTol          0;
    }
}

PISO
{
    nCorrectors     2;
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;
}


// ************************************************************************* //


"""

    return line

