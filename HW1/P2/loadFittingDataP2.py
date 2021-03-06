import pylab as pl
import numpy as np
from math import *
import matplotlib as plt

#def getData(ifPlotData=True):
def getData():
    # load the fitting data and (optionally) plot out for examination
    # return the X and Y as a tuple

    data = pl.loadtxt('curvefittingp2.txt')

    X = data[0,:]
    Y = data[1,:]

#    if ifPlotData:
#        plt.plot(X,Y,'o')
#        plt.xlabel('x')
#        plt.ylabel('y')
#        plt.show()

    return (X,Y)

def Batchgradient(m,x,y,start_pos,convCriterion,alpha, max_iti, phi):
    iti=0
    p=[]
    while (iti<max_iti):
        costFunc_old, costFuncGrad_old=cost(start_pos, phi)
        c_old,l_old=costFunc_old(y,m,x)
        p.append(start_pos)
        gradient=np.asarray(costFuncGrad_old(y,m, x))
        print(gradient)
        pos=start_pos-gradient/alpha
        costFunc_new, costFuncGrad_new= cost(pos, phi)
        c_new, l_new=costFunc_new(y,m,x)
        
        if abs(c_old-c_new)< convCriterion:
            return  pos
        else:
            start_pos=pos
            iti=iti+1
    else:
        return pos
    
def StochasticGradient(batch_size,m, x,y,pos,convCriterion,alpha, max_iti, phi):
    condition=True
    j=0
    #cost=0
    while condition==True:
        randomize=list(range(0,x.shape[0]))
        np.random.shuffle(randomize)
        x1=x
        y1=y
        
        for i in range(0, x.shape[0]):
            x1[i]=x[randomize[i]]
            #y1[i,:]=y[randomize[i],:]
            
        for i in range(0, y.shape[0]):
            y1[i]=y[randomize[i]]

        x2=x1[:batch_size]
        y2=y1[:batch_size]
        m=x2.shape[0]
        alphat=pow((alpha+j),(-0.5))
        pos_new=Batchgradient(m,x2,y2,pos, convCriterion, alphat, max_iti, phi)
        j=j+1
 #Help identifying the convergence criterion
        if (j==max_iti ):
            condition=False
        else:
            pos=pos_new
            #cost=cost_new
            print(pos_new)
    return pos_new

def getBasisFunctions(m):
    def basis(x):
        phi=[]
        for i in range (0,m):
            phi.append(x**i)
        #print(phi)
        return phi
    def basis_cos(x):
        phi=[None]*8
        for i in range(0,8):
            phi[i]=cos(pi*(i+1)*x)
        phi1=np.asarray(phi)
        return phi1
    return basis, basis_cos

def inverse(phi):
    phi_inv=np.linalg.pinv(phi)
    return phi_inv

def maxlikelihood(t,m,x,n):
    basis, basis_cos=getBasisFunctions(m)
    phi=[[None]*m]*x.shape[0]
    
    for i in range(0,n):
        phi[i]=basis(x[i])
        #print(phi)
    phi=np.asmatrix(phi)
    y=np.asmatrix(t)
    y=y.T

   
    w=np.dot(inverse(np.dot(phi.T,phi)),phi.T)*y
  
    return w, phi

def Ridge(t1,m,x1,n, lam):
    m=3
    n=13

    basis, basis_cos=getBasisFunctions(3)
    phi4=[[None]*3]*13
    
    for i in range(0,13):
        phi4[i]=basis(x1[i].item())
        print(phi4[i])

    
    phi5=np.asmatrix(phi4)
    print(phi5.shape[0])
    print(phi5.shape[1])
    print(phi5)
    y=np.asmatrix(t1)
    y=y.T
    print(y)

   
    w=np.dot(np.dot(inverse(lam*np.identity(phi5.shape[1])+np.dot(phi5.T,phi5)),phi5.T),y.T)
  
    return w, phi5    
    
    
    
    
def maxlikelihood_cos(t,m,x,n):
    basis, basis_cos=getBasisFunctions(m)
    phi=[[None]*m]*x.shape[0]
    
    for i in range(0,n):
        phi[i]=basis_cos(x[i])
        #print(phi)
    phi=np.asmatrix(phi)
    print(phi)
    y=np.asmatrix(t)
    y=y.T

   
    w=np.dot(inverse(np.dot(phi.T,phi)),phi.T)*y
  
    return w, phi


def cost(w, phi):
    def sOfSquares(t,m,x):
        basis, basis_cos=getBasisFunctions(m)
        error=0
        l=0
        n=y.shape[0]
        for i in range(0,n):
            ycalc=0
            for j in range(0,m):
                ycalc+=(w[j]*phi[i,j])
            
            error+=(t[i]-ycalc)**2
            l+=(t[i]-ycalc)
        error=error/2
        e=error.item(0)
        l=l.item(0)
        return e,l
    
    def sOfSquareGradient(t,m,x):
        e,l=sOfSquares(t,m,x)
        gradient=[None]*m
        for i in range(0,m):
            gradient[i]=l*w[i]
        return gradient
    return sOfSquares, sOfSquareGradient

def getData1(name):
    data = pl.loadtxt(name)
    # Returns column matrices
    X = data[0:1].T
    Y = data[1:2].T
    return X, Y

def regressAData():
    return getData1('regressA_train.txt')

def regressBData():
    return getData1('regressB_train.txt')

def validateData():
    return getData1('regress_validate.txt')

               
if __name__ == '__main__':
    m=3
#    x,y=getData()
    n=x.shape[0]
    w, phi=(maxlikelihood(y,m,x,n))
    #print(w)
    sOfSquares, sOfSquareGradient=cost(w, phi)
    e,l=sOfSquares(y,m,x)
    #print(e)
    #print(l)
    g=sOfSquareGradient(y,m,x)
    
    convCriterion=1e-20
    alpha=1000000
    max_iti=100000
    start_pos=np.asarray([1,1,1])
    batchsize=m
    pos_bg=Batchgradient(m,x,y,start_pos,convCriterion,alpha, max_iti, phi)
    pos_sg=StochasticGradient(batchsize,m,x,y,start_pos,convCriterion,alpha, max_iti, phi)
    
    w_cos,phi_cos=maxlikelihood_cos(y,m,x,n)
    lam=2
    w,phi=Ridge(y,m,x,n, lam)
    print(w)
    

    