# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSlot

from Fwall import start_simulation 
from Fwall import Ui_MainWindow
from Fwall import *
def call_Galerkin(Nwings,span, AoA_user, y_offset_user, z_offset_user, elem_type, mesh_type, plot_together, wing_type, Nelem, r):
    #### Global functions:

    #  discretization r (global feature)
    def disc(N,b,r):
        n = int((N-1)/2)
        if (r==1.0):
            y = np.linspace(-b/2,b/2,N)
        else:
            q = np.exp((np.log(r))/(n-1))
            L = (b/2)*((1-q)/(1-q**(n)))
            y2 = np.array([])
            for i in range(0,n+1):
                y1 = L*(1-q**(i))/(1-q)
                y2 = np.append(y1,y2)
        
            y3 = np.negative(y2)
            y4 = np.concatenate((y3,y2))
            y = np.unique(y4)
        return y

    # Criação das matrizes K1 e K2 para múltiplas asas:

    def multiple_wings_solve(wings,Uinf,AoA):
        Nwings = len(wings)
        Nnodes = len(wings[0].coords)
        
        K1 = np.zeros((Nnodes*Nwings, Nnodes*Nwings))
        K2 = np.zeros((Nnodes*Nwings, Nnodes*Nwings))
        f = np.zeros(Nnodes*Nwings)
        
        for t in np.arange(Nwings):
            for elnumber,element in enumerate(wings[t].elements):
                [i1, j1, K1_elem] = element.K1_matrix(Uinf)                     
                [i3, f_elem] = element.f_vector(AoA[t])
                            
                K1[t*Nnodes + elnumber, t*Nnodes + elnumber] += K1_elem[0] 
                K1[t*Nnodes + elnumber, t*Nnodes + elnumber + 1] += K1_elem[1]
                K1[t*Nnodes + elnumber + 1, t*Nnodes + elnumber] += K1_elem[2]
                K1[t*Nnodes + elnumber + 1, t*Nnodes + elnumber + 1] += K1_elem[3]
            
                f[t*Nnodes + elnumber] += f_elem[0] 
                f[t*Nnodes + elnumber + 1] += f_elem[1]
        
        for t in np.arange(Nwings):
            for elnumber,element in enumerate(wings[t].elements):
                for t2 in np.arange(Nwings):          
                   for elnumber2,element2 in enumerate(wings[t2].elements):
                        [i2, j2, K2_elem, dfdy] = element.K2_matrix(element2, Uinf)
                        
                        K2[t*Nnodes + elnumber, t2*Nnodes + elnumber2] += K2_elem[0] 
                        K2[t*Nnodes + elnumber, t2*Nnodes + elnumber2 + 1] += K2_elem[1]
                        K2[t*Nnodes + elnumber + 1, t2*Nnodes + elnumber2] += K2_elem[2]
                        K2[t*Nnodes + elnumber + 1, t2*Nnodes + elnumber2 + 1] += K2_elem[3]
                        
        K = K1 + K2
            
        for t in np.arange(Nwings):
            K[:,t*Nnodes] = 0
            K[t*Nnodes,:] = 0
            K[t*Nnodes,t*Nnodes] = 1
            K[:,(t+1)*Nnodes - 1] = 0
            K[(t+1)*Nnodes - 1,:] = 0
            K[(t+1)*Nnodes - 1,(t+1)*Nnodes - 1] = 1
            
            f[t*Nnodes] = 0
            f[(t+1)*Nnodes - 1] = 0    
        
        K = np.linalg.inv(K)
                
        resp = np.matmul(K, f)
        
        gamma_int = 0.0
        
        for t in np.arange(Nwings):
            if (t == int(Nwings/2)): 
                for elnumber, element in enumerate(wings[t].elements):            
                    gamma_int += (resp[t*(Nelem + 1) + element.nodes[1].label]+ resp[t*(Nelem + 1) + element.nodes[0].label]) * (element.h/2.0) * np.sqrt((1/(1 + dfdy**2)))
                    #gamma_int += (resp[element.nodes[1].label]+ resp[element.nodes[0].label]) * (element.h/2.0) * np.sqrt((1/(1 + dfdy**2)))
        CL = 2.0 * gamma_int/(area*Uinf)
        #CL = np.zeros(Nwings)
       


        
        print('CL (múltiplas asas):', CL)
              
        
        for t in np.arange(Nwings):
            wings[t].circ = resp[t*Nnodes:(t+1)*Nnodes] 
               
        return resp


    def multiple_wings_plot(wings_resp,wings,coords,plot_together):   
        if (plot_together == "True" or plot_together == "true"): 
        
            plt.figure()                                                            # Wing's position and circ together

            #if(wing_type == "planar"):
            for t in np.arange(Nwings):   
                if (t != Nwings - 1):
                    
                    wings[t].plot_wing(t)
                    plt.plot(coords[t*(Nelem+1):(t+1)*(Nelem+1),0],wings_resp[t*(Nelem+1):(t+1)*(Nelem+1)]
                        + np.ones(Nelem + 1)*z[t], '-k') 
                else:
                    
                    wings[t].plot_wing(t)
                    plt.plot(coords[t*(Nelem+1):(t+1)*(Nelem+1),0],wings_resp[t*(Nelem+1):(t+1)*(Nelem+1)]
                        + np.ones(Nelem + 1)*z[t], '-k', label = "Circulation") 
            
            #plt.title("Circulation")                                               # Não colocar título nos relatórios
            plt.xlabel("Y-coordinate [m]", fontsize = 14)
            plt.ylabel("Circulation $[\\frac{m^2}{s}]$", fontsize = 14)
            plt.grid(True)
            plt.legend(loc = "center",prop={'size': 9})
            plt.savefig("Circulation.svg")
            plt.show()

        else:
            
            plt.figure()                                                            # Wing's position
            for t in np.arange(Nwings):   
                wings[t].plot_wing(t)
            
            plt.ylabel("Z-coordinate [m]", fontsize = 14)
            plt.xlabel("Y-coordinate [m]", fontsize = 14)
            plt.grid(True)
            plt.savefig("Wings_position.svg")
            plt.show()
       
            plt.figure()                                                            # Circulation
        
            plt.plot(coords[:,0],wings_resp, '-k', label = "Circulation") 
            #plt.title("Circulation")                                               # Não colocar título nos relatórios
            plt.xlabel("Y-coordinate [m]", fontsize = 14)
            plt.ylabel("Circulation $[\\frac{m^2}{s}]$", fontsize = 14)
            plt.grid(True)
            plt.legend(loc = "best",prop={'size': 9})
            plt.savefig("Circulation.svg")
            plt.show()

        
        return 

        
    def create_coordinates(wings,wings_resp):
        coords = np.zeros((Nwings*(Nelem + 1),2))
        
        for t in np.arange(Nwings):
            coords[t*(Nelem + 1):(t+1)*(Nelem + 1),:] = wings[t].coords
            
        file_coords = "coords"
        np.savetxt(file_coords, coords, delimiter=',')
        
        file_circ = "circulation"
        np.savetxt(file_circ, wings_resp, delimiter = ',')
        
        return coords    

    # nodes
    class node():
        def __init__(self, label, coords, chord, cl_alpha, alpha_l0):
            self.label = label
            self.coords = coords
            self.chord = chord
            self.cl_alpha = cl_alpha
            self.alpha_l0 = alpha_l0
            self.theta = theta
            return


    # elements
    class LL2():
        def __init__(self, nodes): 
            self.nodes = nodes
            self.ngauss = 4;
            [self.qsi, self.w] = np.polynomial.legendre.leggauss(self.ngauss)
            [self.qsi2, self.w2] = np.polynomial.legendre.leggauss(self.ngauss + 2)

            self.h = self.nodes[1].coords[0] - self.nodes[0].coords[0]
            return
        
        def shape_functions(self, qsi):
            N1 = lambda qsi: (1.0 - qsi) / 2.0
            N2 = lambda qsi: (1.0 + qsi) / 2.0
            Nmat = np.array([[N1(qsi), N2(qsi)]]) 
            return Nmat
        
        def shape_functions_diff(self, qsi):
            N1_diff = lambda qsi: -1.0/2.0
            N2_diff = lambda qsi:  1.0/2.0
            Nmat_diff = np.array([[N1_diff(qsi), N2_diff(qsi)]]) 
            return Nmat_diff
        
            
        
        def K1_matrix(self, Uinf):
            n1 = self.nodes[0].label
            n2 = self.nodes[1].label
            
            i = np.array([n1, n1, n2, n2])
            j = np.array([n1, n2, n1, n2])
            
            w = self.w
            qsi = self.qsi

            Ke = np.zeros((2,2))
            coords = np.array([[self.nodes[0].coords[0]],[self.nodes[1].coords[0]]])
            chords = np.array([[self.nodes[0].chord[0]],[self.nodes[1].chord[0]]])
            cl_alphas = np.array([[self.nodes[0].cl_alpha[0]],[self.nodes[1].cl_alpha[0]]])
            
        
            for k in range(self.ngauss):
                Nmat = self.shape_functions(qsi[k])
                y = np.matmul(Nmat, coords)
                y = y[0][0]
                chord = np.matmul(Nmat, chords)
                cl_alpha = np.matmul(Nmat,cl_alphas)

                Ke += (self.h/2.0) * np.matmul(Nmat.T, Nmat) * w[k] *(2.0/(cl_alpha * chord * Uinf))
                
            values = np.array([Ke[0][0], Ke[0][1], Ke[1][0], Ke[1][1]])
            
            return i, j, values
        
        def K2_matrix(self, element, Uinf):
            n1i = self.nodes[0].label
            n2i = self.nodes[1].label
            n1j = element.nodes[0].label
            n2j = element.nodes[1].label
            
            i = np.array([n1i, n1i, n2i, n2i])
            j = np.array([n1j, n2j, n1j, n2j])
            
            w = self.w
            qsi = self.qsi
            w2 = self.w2
            qsi2 = self.qsi2
            
            Ke = np.zeros((2,2))
            
            for k1 in range(self.ngauss):
                p2 = 0.0
                Nmat1 = self.shape_functions(qsi[k1])
                Nmat_diff1 = self.shape_functions_diff(qsi[k1])
                coordsy1 = np.array([[self.nodes[0].coords[0]],[self.nodes[1].coords[0]]])   
                coordsz1 = np.array([[self.nodes[0].coords[1]],[self.nodes[1].coords[1]]])   
                y1 = np.matmul(Nmat1,coordsy1)
                y1 = y1[0][0]
                z1 = np.matmul(Nmat1,coordsz1)
                z1 = z1[0][0]
                dfdy = np.matmul(Nmat_diff1,coordsz1)/np.matmul(Nmat_diff1,coordsy1)  
                dfdy = dfdy[0][0]
                y1elem = element.nodes[0].coords[0]
                y2elem = element.nodes[1].coords[0]
            
                for k2 in range(self.ngauss + 1):
                    coordsy2 = np.array([[element.nodes[0].coords[0]],[element.nodes[1].coords[0]]])
                    coordsz2 = np.array([[element.nodes[0].coords[1]],[element.nodes[1].coords[1]]]) 
                    Nmat2 = element.shape_functions(qsi2[k2])          
                    Nmat_diff2 = element.shape_functions_diff(qsi2[k2])
                    y2 = np.matmul(Nmat2,coordsy2)
                    y2 = y2[0][0]
                    z2 = np.matmul(Nmat2,coordsz2)
                    z2 = z2[0][0]
                    a = (z1 - z2)/(y1 - y2)
                    h = (a * dfdy + 1)/(a**2 + 1) 
                    p1 = (self.h/2.0)*(element.h/2.0)*np.matmul(Nmat1.T,((h * Nmat_diff2-Nmat_diff1)/(y1-y2))) * w[k1] * w2[k2]
                    

                p2 =  (self.h/element.h)* np.matmul(Nmat1.T, Nmat_diff1) * np.log(np.abs((y2elem-y1)/(y1-y1elem))) * w[k1]
                Ke += (1.0/(4.0 * np.pi * Uinf * np.sqrt(1 + dfdy**2))) * (p1 + p2)
            

            Ke = -Ke
            values = np.array([Ke[0][0], Ke[0][1], Ke[1][0], Ke[1][1]])
            
            return i, j, values, dfdy
        
        def f_vector(self, AoA):
        
            n1 = self.nodes[0].label
            n2 = self.nodes[1].label
            i = np.array([n1,n2])
            
            w = self.w
            qsi = self.qsi
            
            alphas_l0 = np.array([[self.nodes[0].alpha_l0[0]],[self.nodes[1].alpha_l0[0]]])
            thetas = np.array([[self.nodes[0].theta[0]],[self.nodes[1].theta[0]]])
            fe = np.zeros((2,1))
            for k in range(self.ngauss):
                Nmat = self.shape_functions(qsi[k])   
                alpha_l0 = np.matmul(Nmat,alphas_l0)
                theta = np.matmul(Nmat,thetas)
                fe += (self.h/2.0) * Nmat.T * w[k] * (AoA - alpha_l0 + theta)
            
            values = np.array([fe[0],fe[1]])
            return i, values
            



    # problem
    class lifting_line():
        
        #for t in np.arange(Nwings):
            def __init__(self):
                self.span = [10]*Nwings  
                self.area = [10]*Nwings  
                self.nodes = []
                self.elements = []
                return
            
            def create_planar_retangular_wing(self, span, area, cl_alpha, alpha_l0,t):  
                self.span = span[t]         
                self.area = area
                self.chord = area/span[t]  
                self.cl_alpha = cl_alpha
                self.alpha_l0 = alpha_l0
                return
            
            def create_wing_from_sections(self, stations, chords, cl_alpha, alpha_l0,theta,t): 
                self.stations = stations + y_offset[t]
                self.span[t] = stations[t][-1] - stations[t][0]
                self.chords = chords 
                self.area = np.trapz(chords,stations[t,:])
                self.cl_alpha = cl_alpha
                self.alpha_l0 = alpha_l0
                self.theta = theta
                return self.area
                
            def create_mesh(self, mesh_type, Nelem, elem_type, r, z,t):
                self.elem_type = elem_type
                self.mesh_type = mesh_type
                self.Nelem = Nelem
                if (mesh_type == 'uniform'):
                    if (elem_type == 'LL2' or elem_type == 'll2'):
                       
                        self.Nnodes = Nelem+1
                        self.coords = np.zeros((self.Nnodes, 2)) 
                        self.coords[:,0] = np.linspace(-self.span[t]/2.0 , self.span[t]/2.0, self.Nnodes) + y_offset[t]  
                        
                        if (wing_type == "flexible" or wing_type == "Flexible"):
                            self.coords[:,1] = (0.15*2/self.span[t])*self.coords[:,0]**2
                            z[t] = self.coords[:,1]
                        else:
                            self.coords[:,1] = z[t]
                            
                        self.create_nodes()

                        for k in range(Nelem):
                            new_element = LL2((self.nodes[k], self.nodes[k+1]))
                            self.elements.append(new_element)
                      
                elif (mesh_type == 'r'):
                    if (elem_type == 'LL2' or elem_type == 'll2'):
                        self.Nnodes = Nelem+1
                        self.coords = np.zeros((self.Nnodes, 2))
                        self.coords[:,0] = disc(self.Nnodes,self.span[t],r)  
                        #self.coords[:,1] = np.zeros(self.Nnodes)
                        self.coords[:,1] = z[t]     
                        self.create_nodes()
                        
                        for k in range(Nelem):
                            new_element = LL2((self.nodes[k], self.nodes[k+1]))
                            self.elements.append(new_element)
                                   
                elif (mesh_type == 'cos'):
                    if (elem_type == 'LL2' or elem_type == 'll2'):
                        self.Nnodes = Nelem+1
                        self.coords = np.zeros((self.Nnodes, 2))
                        self.coords[:,0] = -(self.span[t]/2.0) *(np.cos(np.linspace(0, np.pi, self.Nnodes)))
                        #self.coords[:,1] = np.zeros(self.Nnodes)
                        self.coords[:,1] = z[t]
                        self.create_nodes()
                        
                        for k in range(Nelem):
                            new_element = LL2((self.nodes[k], self.nodes[k+1]))
                            self.elements.append(new_element)
        # inserir aqui                
                return 
            
            def create_nodes(self):
                for k in range(self.Nnodes):
                    chord = np.interp(self.coords[k], self.stations[t,:], self.chords)
                    cl_alpha = np.interp(self.coords[k], self.stations[t,:], self.cl_alpha)
                    alpha_l0 = np.interp(self.coords[k], self.stations[t,:], self.alpha_l0)
                    new_node = node(k, self.coords[k], chord, cl_alpha, alpha_l0)
                    self.nodes.append(new_node)
                return
            
            def solve(self,t):
                
                if (elem_type == 'LL2' or elem_type == 'll2'):
                    NGDL = 1
               
                K1 = np.zeros((self.Nnodes*NGDL, self.Nnodes*NGDL))
                K2 = np.zeros((self.Nnodes*NGDL, self.Nnodes*NGDL))
                f = np.zeros(self.Nnodes*NGDL)
                
                for element1 in self.elements:
                    [i1, j1, K1_elem] = element1.K1_matrix(self.Uinf)                     
                    [i3, f_elem] = element1.f_vector(self.AoA)
                        
                    for k in range(len(i1)):
                        K1[i1[k], j1[k]] += K1_elem[k]
                    
                    for k in range(len(i3)):
                        f[i3[k]] += f_elem[k]
        
                    for element2 in self.elements:
                        [i2, j2, K2_elem, dfdy] = element1.K2_matrix(element2, self.Uinf)
                        for k in range(len(i2)):
                            K2[i2[k], j2[k]] += K2_elem[k]
        
                self.K1 = K1
                self.K2 = K2
                
                K = K1 + K2      
                

                K[:,0] = 0
                K[0,:] = 0
                K[0,0] = 1
                K[:,-1] = 0
                K[-1,:] = 0
                K[-1,-1] = 1

                f[0] = 0
                f[-1] = 0
        
                self.f = f
                self.K = K
            
                K = np.linalg.inv(K)
                
                self.circ = np.matmul(K, f)    
                
            
                gamma_int = 0.0
                for element in self.elements:
                    gamma_int += (self.circ[element.nodes[1].label]+ self.circ[element.nodes[0].label]) * (element.h/2.0) * np.sqrt((1/(1 + dfdy**2)))
                
                #CL = np.zeros(Nwings)
                CL = 2.0 * gamma_int/(self.area*self.Uinf)
            
        
                
                print('CL (única asa):', CL)
                      
                return self.circ, CL
            
            def erro(self, Gamma0):
                span = self.span  
                E = (2.0*span*Gamma0**2)/3.0 
                for element in self.elements:
                    gamma1 = self.circ[element.nodes[0].label]
                    gamma2 = self.circ[element.nodes[1].label]
                    y1 = self.coords[element.nodes[0].label][0]
                    y2 = self.coords[element.nodes[1].label][0]
                    E21 = y2/3.0 - y1/3.0
                    E22 = y2/6.0 - y1/6.0
                    E23 = y2/3.0 - y1/3.0
                    
                    arg1 = (span**2 - 4*y1**2.0)
                    arg2 = (span**2 - 4*y2**2.0)
                    arg3 = (2*y1)/span
                    arg4 = (2*y2)/span
                    
                    if abs(abs(y1) - span/2.0) < 1e-8:
                        arg1 = 0.0
                        arg3 = -1.0
                    if abs(abs(y2) - span/2.0) < 1e-8:
                        arg2 = 0.0
                        arg4 = 1.0
        
                    E31 = Gamma0*(arg1**1.5 - arg2**1.5 - 6*y2**2*arg2**0.5 + 6*y1*y2*arg1**0.5)/(12*span*(y1 - y2)) + (span*Gamma0*y2*(np.arcsin(arg3) - np.arcsin(arg4)))/(4.0*(y1 - y2))
                    E32 =-Gamma0*(arg1**1.5 - arg2**1.5)/(12.0*span*(y1 - y2)) - (Gamma0*y1*((y1*(4.0*arg1)**0.5 - y2*(4.0*arg2)**0.5)/span + span*(np.arcsin(arg3) - np.arcsin(arg4))))/(4.0*(y1 - y2))
                
                    Einc = 0.0
                    Einc = E21*gamma1**2.0 + 2.0*E22*gamma1*gamma2 + E23*gamma2**2.0 - 2.0*(E31*gamma1 + E32*gamma2)
        
                    E +=  Einc
                
                return E
            
            def print_props(self):
                print('Wing area: ', self.area)
                print('Wing span: ', self.span[t])
                return
            

            def plot_wing(self,t):

                if (Nwings == 1):
                        plt.plot(self.coords[:,0], self.coords[:,1], '-ob', label = 'Wing')

                elif (Nwings == 3):
                        if(t == 0 or t == 2):

                            plt.plot(self.coords[:,0], self.coords[:,1], '-og')

                        else:

                             plt.plot(self.coords[:,0], self.coords[:,1], '-sb', label = 'Wing')

                elif(Nwings == 9):
                    if (t == 0 or t == 2 or t == 6 or t == 8):
                        plt.plot(self.coords[:,0], self.coords[:,1], '-sc')
                    elif (t == 1 or t == 3 or t == 5 or t == 7):
                        plt.plot(self.coords[:,0], self.coords[:,1], '-og')
                    else: 
                        plt.plot(self.coords[:,0], self.coords[:,1], '-ob', label = "Wing" )
                    
                    return
         
            def setcase(self, case):
                self.Uinf = case['Uinf']
                self.AoA = case['AoA']
                return
       
    # ===============================
    # MAIN CODE
    # ===============================

    #plt.close('all')

    #INPUTS - WING


    #Nwings =                    
    stations = np.zeros((Nwings,300))  
                        
    if (Nwings == 1):
        span = [span]
        y_offset = [y_offset_user]         
        z1 = [z_offset_user] 
        z = [j*np.ones(Nelem+1) for j in z1]
        AoA1 = [AoA_user] 
        
    elif (Nwings == 3):
        span = [span]*Nwings
        y_offset = [-y_offset_user*span[0],0,y_offset_user*span[0]] 
        z1 = [z_offset_user]*Nwings 
        z = [j*np.ones(Nelem+1) for j in z1]
        AoA1 = [AoA_user]*Nwings

    elif (Nwings == 9):
        span = [span]*Nwings

        y_offset = [-y_offset_user*span[0],-y_offset_user*span[0],-y_offset_user*span[0],0,0,0,
        y_offset_user*span[0],y_offset_user*span[0],y_offset_user*span[0]] 

        z1 = [-z_offset_user,0,z_offset_user,-z_offset_user,0,z_offset_user,-z_offset_user,0,z_offset_user]*Nwings 
        z = [j*np.ones(Nelem+1) for j in z1]
        AoA1 = [-AoA_user,AoA_user,-AoA_user,-AoA_user,AoA_user,-AoA_user,-AoA_user,AoA_user,-AoA_user]



    for t in np.arange(Nwings):       
        stations[t,:] = np.linspace(-span[t]/2, span[t]/2, 300)
        chords = 1.909859317102744* np.sqrt(1-(2*stations[t,:]/span[t])**2) # Elliptical distriubtion
        cl_alpha = 2.0*np.pi * np.ones(np.size(stations[t,:]))
        alpha_l0 = 0 * np.pi/180.0 * np.ones(np.size(stations[t,:]))
        theta = 0.0 * np.ones(np.size(stations[t,:]))

    mesh_type = str(mesh_type)
    elem_type = str(elem_type)
    wing_type = str(wing_type)
   
    AoA = [i*np.pi/180 for i in AoA1]

    problem = [] 

    for t in np.arange(Nwings):
        wing = lifting_line()
        area = wing.create_wing_from_sections(stations, chords, cl_alpha, alpha_l0, theta,t)
        wing.create_mesh(mesh_type, Nelem, elem_type, r, z,t)
        problem.append(wing)

    resp = multiple_wings_solve(problem,30,AoA)
    coords = create_coordinates(problem, resp)
    #plt.plot(resp[4*(Nelem+1):5*(Nelem+1)])
    plot = multiple_wings_plot(resp, problem, coords,plot_together)



