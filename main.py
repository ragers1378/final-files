
from Functions import *
import os
import numpy 

from tkinter import * 
from tkinter.ttk import *
 
# creating main tkinter window
master = Tk()
 
# create a label widget
l_rec_h = Label(master, text = "Rectangular Height")
l_rec_w = Label(master, text = "Recgular Width")

l_ellipse_h = Label(master, text = "Ellipse Height")
l_ellipse_w = Label(master, text = "Ellipse Width")

l_cell_count=Label(master, text = "Cell Count Around Ellipse")


l_document_name=Label(master, text = "Document Name")

###########################################################

# grid method to arrange labels in respective
# rows and columns as specified
l_rec_h.grid(row = 0, column = 0, sticky = W, pady = 2)
l_rec_w.grid(row = 1, column = 0, sticky = W, pady = 2)

l_ellipse_h.grid(row = 5, column = 0, sticky = W, pady = 2)
l_ellipse_w.grid(row = 6, column = 0, sticky = W, pady = 2)

l_cell_count.grid(row = 8, column = 0, sticky = W, pady = 2)

l_document_name.grid(row = 9, column = 0, sticky = W, pady = 2)


# entry widgets, used to take entry from user
##########################################################

e_rec_h = Entry(master)
e_rec_w = Entry(master)

e_ellipse_h = Entry(master)
e_ellipse_w = Entry(master)

e_cell_count=Entry(master)

e_document_name=Entry(master)

###################################################
# this will arrange entry widgets
e_rec_h.grid(row = 0, column = 1, pady = 2)
e_rec_w.grid(row = 1, column = 1, pady = 2)
 
e_ellipse_h.grid(row = 5, column = 1, pady = 2)
e_ellipse_w.grid(row = 6, column = 1, pady = 2)

e_cell_count.grid(row = 8, column = 1, pady = 2)


e_document_name.grid(row = 9, column = 1, pady = 2)

######################################################

#This function executes commands which are required to generate mesh
def run():

   #Command to execute mesh process 
   os.system("blockMesh")
   os.system("checkMesh")
   os.system("paraFoam")   
   
#Main Function For generating mesh file
def Generate_Mesh():
        
    line=""			#This variable will hold the script contents of the file
    line=line+Title()+2*"\n"
    
     #Obtaining inputs from the interface
    rec_h=int(e_rec_w.get())
    rec_w=int(e_rec_w.get())
    
    ellipse_h=int(e_ellipse_h.get())
    ellipse_w=int(e_ellipse_w.get())
    
    cell_number=int(e_cell_count.get())



   #Factors are used to create imaginary ellipse section
   #This section contain mesh which are paralel to the surface
   #Factors are given separately for each axis in case different factors
   #need to be used   
    fac_x=1.25
    fac_y=1.25
 
 #The imaginary ellipse called outer ellipse   
    ellipse_w_outer=ellipse_w*fac_x
    ellipse_h_outer=ellipse_h*fac_y
    

    #This if-else is used to distinguish wheter ellipse is laying
    #horizontally or vertically    
    if(ellipse_w>ellipse_h):
     	
     	#if width > height ellipse focus point formulation gives x value of the focus point
        foc_inner_x=abs(((ellipse_w**2)-(ellipse_h**2))**(0.5))  #Inner ellipse focus point x value
    
        foc_outer_x=abs(((ellipse_w_outer**2)-(ellipse_h_outer**2))**(0.5))# Outer ellipse x value
        foc_outer_y=ellipse_find(ellipse_w_outer,ellipse_h_outer,foc_outer_x,1)# outer ellipse focus points y value
        
    else:
        #if width<Height, Focus point formulation gives the y value of the ellipse
        
        #Focus points x values are calculated with the calculated y values for outer and inner ellipses
        foc_outer_y=abs(((ellipse_w_outer**2)-(ellipse_h_outer**2))**(0.5))    
        foc_outer_x=abs(((ellipse_w_outer**2)-( ((ellipse_w_outer**2)*(foc_outer_y**2))/(ellipse_h_outer**2)  ) )**(0.5))
        
        foc_inner_y=abs(((ellipse_w**2)-(ellipse_h**2))**(0.5))
        foc_inner_x=abs(((ellipse_w**2)-( ((ellipse_w**2)*(foc_inner_y**2))/(ellipse_h**2)  ) )**(0.5))   
       
    #Section For writing the mesh files
       
    file_name=e_document_name.get()   #Receive name from gui to create a file which contain the mesh files
    path = os.getcwd()
    
    os.makedirs(path+"/"+file_name)  # create the file
    os.chdir(path+"/"+file_name)
    
    #path = os.getcwd() 
    os.makedirs(path+"/"+file_name+"/system") 
    os.chdir(path+"/"+file_name+"/system")
    
    line=line+"convertToMeters 1;\n"
    
    line=line+vertices(rec_h,rec_w,ellipse_w,ellipse_h,ellipse_w_outer,ellipse_h_outer,foc_inner_x,foc_outer_x)
    
    line=line+blocks(cell_number)+2*"\n"
    
    line=line+edges(ellipse_w,ellipse_h,ellipse_w_outer,ellipse_h_outer,foc_inner_x,foc_outer_x)+2*"\n"
    
    line=line+boundary()
    
    #creating files and writing script in it
    f = open("blockMeshDict", "w")
    f.write(line)
    f.close()


    line=control() 
    f = open("controlDict", "w")
    f.write(line)
    f.close() 
    
    
    
    line=fvSchemes()
    f = open("fvSchemes", "w")
    f.write(line)
    f.close()
    
    line=fvSolution()
    f = open("fvSolution", "w")
    f.write(line)
    f.close()      

    # Return the back in order to execute process
    os.chdir(path+"/"+file_name)   
    
    #Execute blockMesh
    run()
    

# button widget
b1 = Button(master,text = "Generate Mesh",command=Generate_Mesh)

b1.grid(row = 60, column = 66, sticky = E)


mainloop()
