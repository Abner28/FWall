#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code can be useful for 2 different types of application:

    1) Create wing: If you want to define a wing and then calculate the circulation and
    others aerodynamics parameters, go to "MAIN CODE" at the bottom, and adjust
    the essential parameters. First of all, type "1" to "type_analysis".

    2) Posprocessement: If you already have the circulation and coordinates
    of a wing (or multiple wings), please type "0" to "type_analysis" and enter 
    the data from a .txt file.

     @autor: Abner Micael de Paula Souza
"""

##############################################################################
# Which type of analysis? [1 for 'create wing' or 0 for 'Posprocessement']                                                                           
type_analysis = 0                                                          
##############################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl

##############################################################################
#                          DO NOT MODIFY THIS CODE BLOCK                     #
##############################################################################

def call_Vortex_sheet(Nelem, wing_type,Nwings):
    type_analysis == 0

    if type_analysis == 1:

        class main():
        
            def __init__(self, b, S, theta, y, deg, Vinf):
                self.b = b
                self.S = S
                self.AR = self.b**2/self.S
                self.stations = [-self.b/2,0,self.b/2]
                self.theta = theta
                self.y = y
                self.deg = deg
                self.Vinf = Vinf
                return
        
            def interp(self, lamb, alpha_l0, incid, z):
                self.lamb = lamb
                self.cr = 2*self.S/(self.b*(self.lamb + 1))
                self.ct = self.lamb * self.cr
                self.chord = [self.ct,self.cr,self.ct]
                self.chords = np.interp(y,self.stations,self.chord)
                self.alpha_l0 = np.interp(y,self.stations,alpha_l0)
                self.incid = np.interp(y,self.stations,incid)
                self.z = np.interp(np.linspace(-np.cos(gamma)*self.b/2,np.cos(gamma)*self.b/2,len(y)),[-np.cos(gamma)*self.b/2,0,np.cos(gamma)*self.b/2],z)
                return
                                                    ###
        
            def Fourier(self, n):
        
                self.interp(lamb,alpha_l0,incid,z)
        
                self.B = np.zeros((n,n))
        
                for i in range(len(self.theta)):
                    for j in np.arange(1,n+1,1):
                        self.B[j-1][i] = 2*self.b/(np.pi*self.chords[i])*np.sin(self.theta[i]*j) + j*np.sin(j*self.theta[i])/np.sin(self.theta[i])
        
        
                C = alpha*n + np.subtract(self.incid*np.pi/180,self.alpha_l0*np.pi/180)
                self.A = np.dot(np.linalg.inv(self.B.transpose()),C.transpose())
        
                return
        
            def delta(self):
        
                self.Fourier(n)
        
                delta_old = 0
        
                for i in np.arange(2,n+1,1):
                    self.delta = delta_old + i*(self.A[i-1]/self.A[0])**2
                    delta_old = self.delta
        
                self.e = (1 + self.delta)**(-1)  # efficiency factor
                return print("e = {:.4f}".format(self.e))
        
        
            def aerodynamics(self):
        
                self.delta()
        
                G1 = np.zeros((n,n))
        
                # Aerodynamics coefficients
                self.CL = self.A[0]*np.pi*self.AR
                self.CDi = self.CL**2/(np.pi*self.e*self.AR)
                print("CL = {:.3f} \nCDi = {:.6f} \ne = {:.3f}".format(self.CL,self.CDi,self.e))
        
                # Circulation distribution
                for i in np.arange(len(self.theta)):
                    for j in np.arange(1,n+1,1):
                        G1[i][j-1] = 2*self.b*self.Vinf*self.A[j-1]*np.sin(j*self.theta[i])
        
                self.G = np.sum(G1,axis=1)
                plt.plot(y,self.G,'r')
                plt.xlabel("Span [m]")
                plt.ylabel("Circulation [..]")
                plt.grid(True)
                plt.show()
                return self.G
        
            def downwash(self):
        
                Ai1 = np.zeros((n,n))
        
                for i in np.arange(len(theta)):
                   for j in np.arange(1,n+1,1):
                       Ai1[i][j-1] = j*self.A[j-1]*np.sin(j*theta[i])/np.sin(theta[i])
        
                self.Ai = np.sum(Ai1,axis=1)
        
                w = -np.dot(self.Ai,self.Vinf)
                plt.figure()
                plt.plot(y,w,'m')
                plt.xlabel("Span [m]")
                plt.ylabel("Downwash [...]")
                plt.grid(True)
                plt.show()
                return
                                                    ###
        
            def define_trefftz_plane(self):
                self.yp = np.linspace(-b,b,n,endpoint=True)
                self.zp = np.linspace(-b,b,n,endpoint=True)
                [self.YP,self.ZP] = np.meshgrid(self.yp,self.zp)
                return
        
            def bound_vortex(self):
        
                self.define_trefftz_plane()
                self.aerodynamics()
        
                self.wy =  np.zeros((len(self.zp),len(self.yp)))
                self.wz = np.zeros((len(self.zp),len(self.yp)))
                self.M = np.zeros((len(self.wy),len(self.wy)))
                Iy = np.zeros((len(self.zp),len(self.yp)))
                Iz = np.zeros((len(self.zp),len(self.yp)))
                h = [0]*n
        
                if gamma == 0:  # Planar wing
                    for i in np.arange(0,len(self.ZP)):
                        for j in np.arange(0,len(self.YP)):
                                for k in np.arange(0,len(self.y)-1):
                                    self.wy[i][j] += 1/(np.pi*4)*(self.G[k+1]-self.G[k])/(self.y[k+1]-self.y[k])*((np.arctan((self.y[k+1]-self.yp[j])/self.zp[i])) - np.arctan((self.y[k]-self.yp[j])/self.zp[i]))
                                    self.wz[i][j] += -1/(np.pi*8)*(self.G[k+1]-self.G[k])/(self.y[k+1]-self.y[k])*(np.log((self.y[k]-self.yp[j])**2+self.zp[i]**2) - np.log((self.y[k+1]-self.yp[j])**2+ self.zp[i]**2))
                                self.M[i][j] = np.sqrt(self.wy[i][j]**2 + self.wz[i][j]**2)
        
                    plt.figure()
                    plt.title('Induced velocity - Planar case')
                    Q = plt.quiver(self.YP, self.ZP, self.wy/self.M, self.wz/self.M,self.M,cmap=plt.cm.jet,units = 'width',headwidth = 2,scale = 90)
                    plt.colorbar(Q, cmap=plt.cm.jet)
                    plt.savefig("Induced_velocity.pdf")
        
                else:  # NONPLANAR WING
                    [t,w] = np.polynomial.legendre.leggauss(self.deg)
                    for i in np.arange(0,len(self.ZP)):
        
                        for j in np.arange(0,len(self.YP)):
        
                            for k in np.arange(0,len(self.y)-1):
                                h[k] =  np.sqrt((self.z[k+1] - self.z[k])**2 + (y[k+1] - y[k])**2)
        
                                for l in np.arange(0,self.deg):
                                    x = y[k] + h[k]/2*(t[l] + 1)
                                    wy = (self.zp[i] - self.z[k] - x*np.sin(gamma))/((self.yp[j]-self.y[k]-x*np.cos(gamma))**2 + (self.zp[i]-self.z[k]-x*np.sin(gamma))**2)
                                    Iy[i][j] += (self.G[k+1]-self.G[k])/(2*4*np.pi)*w[l]*wy
        
                                    wz = (self.yp[j]-self.y[k]-x*np.cos(gamma))/((self.yp[j]-self.y[k]-x*np.cos(gamma))**2 + (self.zp[i]-self.z[k]-x*np.sin(gamma))**2)
                                    Iz[i][j] += -(self.G[k+1]-self.G[k])/(2*4*np.pi)*w[l]*wz
        
                            self.M[i][j] =  np.sqrt(Iy[i][j]**2 + Iz[i][j]**2)
                    plt.figure()
                    plt.title('Induced velocity - Non-Planar case')
                    Q = plt.quiver(self.YP, self.ZP, Iy/self.M, Iz/self.M,self.M,cmap=plt.cm.jet,units = 'width',headwidth = 2,scale = 50)
                    plt.colorbar(Q, cmap=plt.cm.jet)
                    plt.savefig("Induced_velocity_nonplanar.pdf")
        
        
                return


    else:
        
        def posprocessement():
            coords = pd.read_csv("C:\\Users\\Administrador\\Desktop\\Qt Projects\\FWall\\coords", sep = ",", header = None)
            y = coords.iloc[:,0]
            z = coords.iloc[:,1]
            
            return y,z
        
        def aerodynamics(y):
            
            circ =  pd.read_csv("C:\\Users\\Administrador\\Desktop\\Qt Projects\\FWall\\circulation", sep = ",", header = None)
            G = circ.iloc[:,0]
            
            
            return G
        
        def define_trefftz_plane(y,z):
            ymin = min(i for i in y)
            ymax = max(j for j in y)
            zmin = min(i for i in z)
            zmax = max(j for j in z)
            
            yp = np.linspace(-12,12,n,endpoint=True)
            zp = np.linspace(-0.5,1.5,n,endpoint=True)
            [YP,ZP] = np.meshgrid(yp,zp)
            return yp,zp,YP,ZP
            
        def bound_vortex(yp,zp,YP,ZP,G,y,z):
            
            define_trefftz_plane(y,z)
            aerodynamics(y)
            
            wy =  np.zeros((len(zp),len(yp)))
            wz = np.zeros((len(zp),len(yp)))
            M = np.zeros((len(wy),len(wy)))
            Iy = np.zeros((len(zp),len(yp)))
            Iz = np.zeros((len(zp),len(yp)))
            h = [0]*len(y)
            phi = [0]*len(y)
            
            if(wing_type == "Planar" or wing_type == "planar"):
            
                for i in np.arange(0,len(ZP)):
                    for j in np.arange(0,len(YP)):
                            for k in np.arange(0,len(y)-1):
                                wy[i][j] += 1/(np.pi*4)*(G[k+1]-G[k])/(y[k+1]-y[k])*((np.arctan((y[k+1]-yp[j])/zp[i])) - np.arctan((y[k]-yp[j])/zp[i]))
                                wz[i][j] += -1/(np.pi*8)*(G[k+1]-G[k])/(y[k+1]-y[k])*(np.log((y[k]-yp[j])**2+zp[i]**2) - np.log((y[k+1]-yp[j])**2+ zp[i]**2))
                            M[i][j] = np.sqrt(wy[i][j]**2 + wz[i][j]**2)
                
                plt.figure()
                #plt.title('Induced velocity - Planar case')
                plt.autoscale
                plt.xlabel("Y-coordinate [m]", fontsize = 14)
                plt.ylabel("Z-coordinate [m]", fontsize = 14)
                Q = plt.quiver(YP, ZP, wy/M, wz/M, M,cmap=plt.cm.jet, units = 'width',headwidth = 1,scale = 80)
                plt.colorbar(Q, cmap=plt.cm.jet)
                plt.plot(y[int(Nwings/2)*(Nelem+1):(int(Nwings/2)+1)*(Nelem+1)], z[int(Nwings/2)*(Nelem+1):(int(Nwings/2)+1)*(Nelem+1)], '-ok',markersize = 1.2, linewidth = .5, label = "Wing")
                
                plt.legend(loc = (0.73,0.84), framealpha = 1.0)
                plt.savefig("Induced_velocity_planar.svg")
                
                return 
                
            else:  # NONPLANAR WING (Gauss - Lengendre)
                
                [t,w] = np.polynomial.legendre.leggauss(deg)
                for i in np.arange(0,len(ZP)):
               
                   for j in np.arange(0,len(YP)):
               
                       for k in np.arange(0,len(y)-1):
                           h[k] =  np.sqrt((z[k+1] - z[k])**2 + (y[k+1] - y[k])**2)
                           phi[k] = np.arctan((z[k+1] - z[k])/(y[k+1] - y[k]))
               
                           for l in np.arange(0,deg):
                               x = h[k]/2*(t[l] + 1)
                               wy = (zp[i] - z[k] - t[l]*np.sin(phi[k]))/((yp[j]-y[k]-t[l]*np.cos(phi[k]))**2 + (zp[i]-z[k]-t[l]*np.sin(phi[k]))**2)
                               Iy[i][j] += (G[k+1]-G[k])/(8*np.pi)*w[l]*wy
               
                               wz = (yp[j]-y[k]-t[l]*np.cos(phi[k]))/((yp[j]-y[k]-t[l]*np.cos(phi[k]))**2 + (zp[i]-z[k]-t[l]*np.sin(phi[k]))**2)
                               Iz[i][j] += -(G[k+1]-G[k])/(8*np.pi)*w[l]*wz
            
                            
                           M[i][j] =  np.sqrt(Iy[i][j]**2 + Iz[i][j]**2)
            
            plt.figure()
            Q = plt.quiver(YP, ZP, Iy/M, Iz/M, M,cmap=plt.cm.jet, units = 'width',headwidth = 1,scale = 80)
            plt.colorbar(Q, cmap=plt.cm.jet)
            plt.plot(y[int(Nwings/2)*(Nelem+1):(int(Nwings/2) + 1)*(Nelem+1)], z[int(Nwings/2)*(Nelem+1):(int(Nwings/2)+1)*(Nelem+1)], '-ok',markersize = 1.2, linewidth = .5, label = "Wing")
            plt.legend(loc = (0.73,0.84), framealpha = 1.0)
            plt.savefig("Induced_velocity_nonplanar.svg")
        
            return Iy, Iz, M
            
        def plot(y,G,YP,ZP):
            
            plt.figure()
            plt.plot(y,G,'k')
            
            plt.xlabel("X-coordinate [m]")
            plt.ylabel("Circulation $[\\frac{m^2}{s^2}]$")
            plt.grid(True)
            plt.show()
               
        
##############################################################################
#                                    MAIN CODE                               #
##############################################################################
    n = 60
    gamma = 0*np.pi/180  # wing's tilt, in rad.
    deg = 4
    #Nelem = 30  # Auxiliar nos gráficos!

    if type_analysis == 1:

        b = 40
        
        
        theta = np.linspace(np.pi/(50*n),np.pi - np.pi/(50*n),n,endpoint=True)
        
        y = -b/2*np.cos(theta)
        #z = [-np.sin(gamma)*b/2,0,np.sin(gamma)*b/2]
        
        alpha_l0 = [0.5]*3
        incid = [0]*3
        S = 20
        lamb = 1
        alpha = [2*np.pi/180]
        Vinf = 20

    else:
        
        [yy,zz] = posprocessement()
        [yp,zp,YP,ZP] = define_trefftz_plane(yy,zz)
        G = aerodynamics(yy)
        bound_vortex(yp, zp, YP, ZP, G,yy,zz)
        plot(yy,G,YP,ZP)

##############################################################################