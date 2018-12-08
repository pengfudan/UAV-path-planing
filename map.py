#!/usr/bin/env python
#-*-coding: utf-8 -*-
'''
author: Lin Peng
create_time:2018.12.08 21:30
organization:Fudan University
introduction: create 3D map for Fudan Guanghua Tower and discretization
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
import cv2

class Point(object):
    '''
    点
    '''
    def __init__(self, x, y, z):
        '''
        点的三维坐标（相对）
        '''
        self.x=x
        self.y=y
        self.z=z
    def neighbor(self, delta_xyz):
        '''
        由对于某点的相对位置新建一个点
        '''
        neighbor_point = Point(self.x+delta_xyz[0], self.y+delta_xyz[1], self.z+delta_xyz[2])
        return neighbor_point
    def point2list(self):
        '''
        将一个点的三维坐标转换成列表
        '''
        return [self.x, self.y, self.z]
    def distance(self, another_point):
        '''
        计算两个点的相对坐标
        '''
        return np.array(another_point.point2list()) - np.array(self.point2list())


class Cuboid(object):
    '''
    长方体
    '''
    def __init__(self, original, delta_xyz):
        self.original = original
        self.delta_xyz = delta_xyz
        self.vertex0 = original
        self.vertex1 = original.neighbor([0,			0,				delta_xyz[2]	])
        self.vertex2 = original.neighbor([0,			delta_xyz[1],	0				])
        self.vertex3 = original.neighbor([0,			delta_xyz[1],	delta_xyz[2]	])
        self.vertex4 = original.neighbor([delta_xyz[0],	0,				0				])
        self.vertex5 = original.neighbor([delta_xyz[0],	0,				delta_xyz[2]	])
        self.vertex6 = original.neighbor([delta_xyz[0],	delta_xyz[1],	0				])
        self.vertex7 = original.neighbor([delta_xyz[0],	delta_xyz[1],	delta_xyz[2]	])
        self.vertex_list = [self.vertex0, self.vertex1, self.vertex2, self.vertex3, self.vertex4, self.vertex5, self.vertex6, self.vertex7]
        self.center_point = original.neighbor([0.5*delta_xyz[0], 0.5*delta_xyz[1], 0.5*delta_xyz[2]])
    def cuboid2array(self):
        a=[point.point2list() for point in self.vertex_list]
        return np.array(a)
    def collision(self, newpoint):
        ans = 1
        delta = np.array(newpoint.point2list())-np.array(self.original.point2list())
        if (delta[0]>=0 and delta[0]<=self.delta_xyz[0]) or (delta[0]<=0 and delta[0]>=self.delta_xyz[0]):
            if (delta[1]>=0 and delta[1]<=self.delta_xyz[1]) or (delta[1]<=0 and delta[1]>=self.delta_xyz[1]):
                if (delta[2]>=0 and delta[2]<=self.delta_xyz[2]) or (delta[2]<=0 and delta[2]>=self.delta_xyz[2]):
                    ans = 0
        return ans

    def draw(self,ax=None):
        if ax==None:
            return False
        x,y,z = self.original.point2list()
        dx,dy,dz = self.delta_xyz
        xx = np.linspace(x, x+dx,10)
        yy = np.linspace(y, y+dy,10)
        zz = np.linspace(z, z+dz,10)

        xp, yp = np.meshgrid(xx,yy)
        z = z*(np.cos(xp-xp))
        ax.plot_wireframe(xp,yp,z)
        ax.plot_wireframe(xp,yp,z+dz)

        yp, zp = np.meshgrid(yy,zz)
        x = x * (np.cos(yp - yp))
        ax.plot_wireframe(x,yp,zp)
        ax.plot_wireframe(x+dx,yp,zp)

        zp, xp = np.meshgrid(zz,xx)
        y = y * (np.cos(xp - xp))
        ax.plot_wireframe(xp,y,zp)
        ax.plot_wireframe(xp,y+dy,zp)



class Ball(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    def collision(self, newpoint):
        ans = 1
        if np.linalg.norm(self.center.distance(newpoint))<=self.radius:
            ans = 0
        return ans
    def draw(self,ax):
        u = np.linspace(0,2*np.pi,50)
        v = np.linspace(0,np.pi,50)
        x = self.radius*np.outer(np.cos(u), np.sin(v)) + self.center.x
        y = self.radius*np.outer(np.sin(u), np.sin(v)) + self.center.y
        z = self.radius*np.outer(np.ones(np.size(u)), np.cos(v)) + self.center.z

        ax.plot_wireframe(x,y,z,rstride=4,cstride=4,color='b')
#		ax.plot_wireframe(x,y,z,rstride=4,cstride=4,color='r')

class Cylinder_z(object):
    def __init__(self, center,radius, height):
        self.center = center
        self.radius = radius
        self.height = height
    def collision(self, newpoint):
        ans = 1
        d = self.center.distance(newpoint)
        d[2]=0
        if np.linalg.norm(d)<=self.radius:
            if (newpoint.z>=self.center.z and newpoint.z<=self.center.z+self.height) or (newpoint.z<=self.center.z and newpoint.z>=self.center.z+self.height):
                ans = 0
        return ans
    def draw(self,ax):
        u = np.linspace(0,2*np.pi,100)
        v = np.linspace(0,np.pi,100)
        x = self.radius*np.outer(np.cos(u), np.sin(v)) + self.center.x
        y = self.radius*np.outer(np.sin(u), np.sin(v)) + self.center.y
        z = self.center.z
        dz = self.height
        xx = self.radius*np.cos(u) + self.center.x
        ax.plot_surface(x,y,z,color='b')
        ax.plot_surface(x,y,z+dz,color='b')


class Map(object):
    def __init__(self, obstacle_list):
        self.obstacle_list = obstacle_list
    def add_obstacle(obstacle):
        self.obstacle_list.append(obstacle)
    def collision(self, newpoint):
        for obs in self.obstacle_list:
            if obs.collision(newpoint)==0:
                return 0
        return 1
    def draw_map(self,ax):
        for obs in self.obstacle_list:
            obs.draw(ax)
        ax.set(xlabel='x',ylabel='y',zlabel='z')
        plt.title("Map")




def main():
    point0=Point(0,0,0)
    point1=Point(5,5,5)
    cuboid1=Cuboid(point1,[29.3087,43.6147,19])

    point2=Point(34.3087,10.8712,5)
    cuboid2=Cuboid(point2,[18.5953,30.8047,19])

    point3=Point(21.1136,17.2091,24)
    cuboid3=Cuboid(point3,[31.7904,24.4668,15])

    point4=Point(52.904,5.3421,5)
    cuboid4=Cuboid(point4,[24.8854,40.3111,138])

    point5=Point(77.7894,5.3421,5)
    cuboid5=Cuboid(point5,[25.1011,40.3111,64])

    point10=Point(90.3399,25.4977,69)
    ball1 = Ball(point10,9)
    #cylinder1=Cylinder_z(point1,5,10)

    point6=Point(102.8905,5.3421,5)
    cuboid6 = Cuboid(point6, [24.8854,40.3111,138])

    point7=Point(127.7759,17.2091,24)
    cuboid7 = Cuboid(point7, [31.7904,24.4668,15])

    point8=Point(127.7759,10.8712,5)
    cuboid8 = Cuboid(point8, [18.5953,30.8047,19])

    point9=Point(146.3712,5,5)
    cuboid9 = Cuboid(point9, [29.3087,43.6147,19])

    obs_list=[cuboid1,cuboid2,cuboid3,cuboid4,cuboid5,cuboid6,cuboid7,cuboid8,cuboid9,ball1]
    map1 = Map(obs_list)
    #print map1.collision(point0.neighbor([5,5,5]))
    #print cylinder1.collision(Point(0,0,5))
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1,projection='3d')
    #map1.draw_map(ax)
    plt.xlim(0, 180)
    plt.ylim(0, 180)

    mmmap = [[[1 for i in range(0, 160)] for i in range(0, 60)] for i in range(0, 190)]
    for i in range(0, 180, 1):
        for j in range(0, 50, 1):
            for k in range(0, 150, 1):
                if (map1.collision(point0.neighbor([i, j, k])) <= 0):
                    mmmap[i][j][k] = 0
    m = np.array(mmmap)
    np.save('guanghua.npy', m)

    for i in range(0, 180, 5):
        for j in range(0, 50, 5):
            for k in range(0, 150, 5):
                if mmmap[i][j][k] == 0:
                    ax.scatter(i, j, k, s=5, c='b', marker='o')
    plt.show()

if __name__ == '__main__':
    main()
