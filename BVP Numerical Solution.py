import matplotlib.pyplot as plt
import numpy as np 
import timeit

#B value calculation for Analytic solution
def B(n):
    
    B_value=0               # storage for B(n) for current n value              
    x=np.linspace(0,1,101)  #list of x point in order to execute integral process numerically.
    dx=0.01                 #TimeStep  
      

    # İntegration Section For B(n)
    for i in x:         
    
        B_value=B_value+((np.sin(np.pi*i))*(np.sin(np.pi*i*n)))*dx   
    
    B_value= ((B_value)*(-2))/np.sinh(n*np.pi) 

    return B_value


def analytic_solution(node):
    
    
    
    result_list=np.zeros((node,node))  # Initialization of the matrix in order to add values for each node
    
    nn=np.linspace(1,110,111)           # n points array for power series
     

    # points for nodes in x and y direction
    xx=np.linspace(0,1,node)            
    yy=xx
       
    #Calculations power serie for each nodes
    for y in xx:
        for x in yy:
            sum_result=0
            
            for n in nn:
        
                result=B(n)*(np.sinh(np.pi*n*(y-1))*(np.sin(n*np.pi*x)) )   
                sum_result=sum_result+result
            
            result_list[int(y*(node-1))][int(x*(node-1))]=sum_result

        
    
    Graph(node,result_list,"Analytic")
    return result_list


def MatrixDecomposition(node):  


    A=np.zeros((node**2,node**2)) #Coefficient Matrix Initialization     
    F=np.zeros(node**2)           #Nodal values 
    

    #Matrix Build-up Sequences
    for j in range(node):        
           
        for i in range(node):    
            point_number=(node*j)+i  #Each node represents in a row.This value calculate the row number for each node   
            
            #Boundary Conditions
            if(j==0):  #Tottom
                
                A[point_number][point_number]=1
                #F[point_number]=np.sin((i/node)*np.pi)
                
                F[point_number]=np.sin((i/(node-1))*np.pi)
                   
            elif(j==(node-1)):  #Top    
                
                A[point_number][point_number]=1            
                F[point_number]=0
            
            elif(i==0):    #Left
                
                A[point_number][point_number]=1
                F[point_number]=0
            
            
            elif(i==(node-1)):  #Right   
                A[point_number][point_number]=1
                F[point_number]=0
            
            else: # Inner Points

                A[point_number][point_number]=4
                
                A[point_number][point_number-1]=-1
                A[point_number][point_number+1]=-1
                                   
                A[point_number][point_number-node]=-1
                A[point_number][point_number+node]=-1                
                
                F[point_number]=0


    #Decomposition Of The Matrix                       
    y = np.linalg.solve(A,F)  
    
    
    #Convert Matrix to (cell_number,cell_number) shape for visualization
    #Backward Operation for transforming
    ii=0
    jj=0
    result=np.zeros((node,node))
     
    for i in range(node):
         for j in range(node):
             
             result[j][i]=y[(j*node)+i]       
    
        

    Graph(node,result,"Decomposition")    
    return result



def iterative_solution(iteration_count,node):

   

    U_guess = 2  #Initial guess value  
  
    U_top = 0
    U_left = 0
    U_right = 0
    
 
    #U_initial = 30

    #Initilization Matrix
    U = np.empty((node,node))  
    U.fill(U_guess)
    #U.fill(U_initial)
    #Boundary Condition Assignment
    U[(node-1):, :] = U_top
    U[:, (node-1):] = U_right   
    U[:, :1] = U_left
    
    #Sin() boundary condition for bottom
    for i in range(node):
        U[0][i] = np.sin((i/node)*np.pi)        

    #Iterative Process 
    for iteration in range(iteration_count):
        for i in range(1, node-1):
            for j in range(1, node-1):
                U[i, j] = 0.25 * (U[i+1][j] + U[i-1][j] + U[i][j+1] + U[i][j-1])
   
  
    Graph(node,U,"iterative")
    return U


def Graph(node,U,name):
    
    #colour interpolation and colour map
    colorinterpolation = 50
    colourMap = plt.cm.jet #you can try: colourMap = plt.cm.coolwarm
    
    #Prepare meshgrid
    X, Y = np.meshgrid(np.linspace(0,1,node),np.linspace(0,1,node))
    
    # Arrange Contours for given matrix and given name
    plt.title("Contour of U Distribution  "+name)
    plt.contourf(X, Y, U, colorinterpolation, cmap=colourMap)
    
    # Colorbar
    plt.colorbar()
    
    # indicate result
    plt.show()
    
    
    

cell_number=10 #Number of cell desired to be in numerical calculation

node=cell_number+1

#Matrix Decomposition Process
start = timeit.default_timer() #start time to calculate calculation time
print("Matrix Decomposition Process Initilized")
matrix=MatrixDecomposition(node)
stop = timeit.default_timer()
print("Matrix Decomposition Process Completed within",stop-start,"sec")
#print('Time: ', stop - start) 


#Analytic Process
start = timeit.default_timer()
print("Analytical Calculation Process Started")
analytic=analytic_solution(node)
stop = timeit.default_timer()
print("Analytical Calculation Process Completed Within",stop-start,"sec")

#Iterative Process
start = timeit.default_timer()
print("Iterative Calculation Process Started")
iterative=iterative_solution(5000, node)
stop = timeit.default_timer()
print("Iterative Calculation Process Completed Within",stop-start,"sec")


#Results
dif_matrix_between_analytic=matrix-analytic         # Differences of the results between Matrix and analytic method
dif_iterative_between_analytic=iterative-analytic    # Differences of the results between iterative and analytic method

#Visualization Of Results Differences
Graph(node,dif_matrix_between_analytic,"Differences Of Matrix-Analytic Method On Each Node")
Graph(node,dif_matrix_between_analytic,"Differences Of iterative-Analytic Method On Each Node")   











