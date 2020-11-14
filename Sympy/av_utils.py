#! /home/vahid/miniconda3/bin/python

import plotly.graph_objects as go
import sympy as sp
import pandas as pd
import numpy as np
import sympy.vector as sv
import plotly.figure_factory as ff


# 2D curve plot
def plot_curve(x, y, fig=False, xtitle='X', ytitle='Y', title='2D Plot', lw=5):    
    if fig is False:
        fig = go.Figure()
        fig.add_scatter(x=x, y=y, showlegend=False, mode='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title=ytitle, yaxis=dict(scaleanchor="x", scaleratio=1))
        fig.show()    
    else:
        fig.add_scatter(x=x, y=y, showlegend=False, mode ='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title=ytitle, yaxis=dict(scaleanchor="x", scaleratio=1))         


# 3D curve plot
def plot_curve3d(x , y , z, fig = False, xtitle = 'X', ytitle= 'Y', title='3D Plot', aspectmode='data', lw =5):
    
    if fig is False:
        fig = go.Figure()
        fig.add_scatter3d(x=x, y=y, z=z, showlegend=False,
                          mode='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title= ytitle, 
                          scene=dict(camera=dict(eye=dict(x=1.15, y=1.15, z=0.8)), #the default values are 1.25, 1.25, 1.25
                          xaxis=dict(),
           yaxis=dict(),
           zaxis=dict(),
           aspectmode=aspectmode, #this string can be 'data', 'cube', 'auto', 'manual'
           #a custom aspectratio is defined as follows:
           aspectratio=dict(x=1, y=1, z=0.95)
           ))
        fig.show()
    
    else:
        fig.add_scatter3d(x=x, y=y, z=z, showlegend=False, mode='lines', 
                        line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                        yaxis_title=ytitle, 
                        scene=dict(camera=dict(eye=dict(x=1.15, y=1.15, z=0.8)),  # the default values are 1.25, 1.25, 1.25
                        xaxis=dict(),
                        yaxis=dict(),
                        zaxis=dict(),
                        aspectmode=aspectmode,  # this string can be 'data', 'cube', 'auto', 'manual'
                        # a custom aspectratio is defined as follows:
                        aspectratio=dict(x=1, y=1, z=0.95)
                        )) 
    return fig


# Plot a parametric curve in 3D
def plot3d_parametric_curve(func, inter1=None, fig=False, xtitle='X', ytitle='Y', 
                            title='3D Curve Plot', points=50,
                            aspectmode='data'):

    '''
    - Arguments:
    	``func``: must be either a tuple with three components (e.g. Sympy objects) or a parametric equation in the class sympy.vector
    	``inter1``: (parameter, start, end)
    	``fig``: A plotly figure object
    	``xtitle``: x-axis title
    	``ytitle``: y-axis title
    	``title``: title of the figure
    	``points``: the number of points to plot the curve
    	``aspectmode``: a parameter of figure object
    - Return:
        A figure object of Plotly
    '''
    if inter1 is None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")

    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())

    #check if the parametric equation has three components.        
    assert len(func) ==3, 'The parametric equation of a 3D surface must has 3 components.'

    #check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func)) if isinstance(func[i], sp.Expr) ]
    params_unique = set([item for sublist in params for item in sublist])
    assert params_unique == set([inter1[0]]), "The parameters of the function aren't the same as the ones declared in the intervals"
    
    
    xx_np = sp.lambdify(inter1[0], func[0])
    yy_np = sp.lambdify(inter1[0], func[1])
    zz_np = sp.lambdify(inter1[0], func[2])
    
    
    
    var1 = np.linspace(inter1[1],inter1[2],points)
    xx, yy, zz = xx_np(var1), yy_np(var1), zz_np(var1)
    
    
    l = [xx,yy,zz]
    for item in range(len(l)):
        if type(item)!= np.ndarray:
            l[item] *= np.ones(var1.shape)
            
    xx, yy, zz = l[0], l[1], l[2]
          
    if fig == False:
        
        
        return plot_curve3d(x = xx , y = yy, z = zz, xtitle = xtitle, ytitle= ytitle, title=title,aspectmode = aspectmode)
        
    
    else:
        return plot_curve3d(x = xx , y = yy, z = zz, fig = fig, xtitle = xtitle, ytitle= ytitle, title=title, aspectmode=aspectmode)
        


        
        
# Position vector originating from origin!

def position_vector(x_0,y_0, rt1 = 0.1, rt2 = 1/3, fig=False, color = 'black', showgrid = True, zeroline=True, lw=2):
    
    '''
    The ideia of the below function is as follow. First, we write the parametric equation for the segment of 
    the line that pass through $(0,0)$ and $(x_0, y_0)$. It is 
    $$
    \vec r(t) = \begin{cases}
    x = x_0 t \\
    y = y_0 t
    \end{cases}
    $$
    Then using the variable *rt1* we decide about the proportion of the head of the vector em relation to 
    the total length of vector. The variable *rt2* is about the proportion of the base 
    of the triangle em relation to its altitude. *l* is the total length of the vector. *t = 1-ratio1* is the 
    parameter of the line $\vec r(t)$ that the base of the head is located, 
    we call this point as $(\hat x , \hat y)$. Through this point, perpendicular to the $\vec r$ passes 
    another line that is base of the head. The equation of this line is 
    $$
    \vec{r^\prime} = \begin{cases}
    x = y_0 s + \hat x \\
    y = -x_0 s + \hat y
    \end{cases}
    $$
    Now we want to find other two corners of the head, beside $(x_0,y_0)$. These two points are located of 
    the both side of $(\hat x , \hat y)$ with the distance $\frac{lenght2}{2}$. 
    The value of parameter $s$ associated with these points is $\hat s = \pm \frac{length2}{2 l}$. 
    So these two points are 
    $(y_0 \hat s +\hat x, -x_0 \hat s + \hat y)$ and $(-y_0 \hat s +\hat x, x_0 \hat s +\hat y)$.
    '''
    
    l = np.sqrt((x_0)**2 + (y_0)**2)
    length1 = rt1 *l
    length2 = rt2 * length1
    
    t = 1 - rt1
    x_bar , y_bar = x_0 * t, y_0 * t
    
    s_bar = length2/(2*l)
    
    if fig==False:
        fig = go.Figure()
    
        fig.add_scatter(x = [x_0,y_0*s_bar+x_bar, -y_0*s_bar+x_bar,x_0],
                    y=[y_0, -x_0*s_bar +y_bar,x_0*s_bar+y_bar, y_0],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [0,x_bar], y=[0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.update_scatter(dict(opacity=1))
        fig.show()
    else:
        fig.add_scatter(x = [x_0,y_0*s_bar+x_bar, -y_0*s_bar+x_bar,x_0],
                    y=[y_0, -x_0*s_bar +y_bar,x_0*s_bar+y_bar, y_0],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [0,x_bar], y=[0,y_bar], mode='lines',line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.show()

        
def position_vector3d(x_0, y_0, z_0, ratio1 = 0.1, ratio2 = 1/3, fig=False, color = 'black', lw=2):
    
    if fig == False:
        fig = go.Figure()
        fig.add_scatter3d(x = [0,0.95*x_0],y=[0,0.95*y_0],z=[0,0.95*z_0], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_0],y=[y_0],z=[z_0],u=[x_0],v=[y_0],w=[z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.show()
    else:
        fig.add_scatter3d(x = [0,0.95*x_0],y=[0,0.95*y_0],z=[0,0.95*z_0], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_0],y=[y_0],z=[z_0],u=[x_0],v=[y_0],w=[z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)

def vector(x ,y ,u, v, rt1 = 0.1, rt2 = 1/3, fig=False, color = 'black', showgrid = True, zeroline=True, lw=3):
    
    '''
    (x,y): initial point of the vector
    (u ,v): the projection of the vector along x and y axis
    
    for x_0,u,y_0,v in zip(x,u,y,v):
        x_1 = x_0 + u
        y_1 = y_0 + v
    
    The ideia of the below function is as follow. First, we write the parametric equation for the segment of 
    the line that pass through $(0,0)$ and $(x_0, y_0)$. It is 
    $$
    \vec r(t) = \begin{cases}
    x = (x_1 - x_0) t + x_0 \\
    y = (y_1 - y_0) t + y_0
    \end{cases}
     = 
     \begin{cases}
    x = a t + x_0 \\
    y = b t + y_0
    \end{cases}
    $$
    Then using the variable *rt1* we decide about the proportion of the head of the vector em relation to 
    the total length of vector. The variable *rt2* is about the proportion of the base 
    of the triangle em relation to its altitude. *l* is the total length of the vector. *t = 1-ratio1* is the 
    parameter of the line $\vec r(t)$ that the base of the head is located, 
    we call this point as $(\hat x , \hat y)$. Through this point, perpendicular to the $\vec r$ passes 
    another line that is base of the head. The equation of this line is 
    $$
    \vec{r^\prime} = \begin{cases}
    x = b s + \hat x \\
    y = -a s + \hat y
    \end{cases}
    $$
    Now we want to find other two corners of the head, beside $(x_0,y_0)$. These two points are located of 
    the both side of $(\hat x , \hat y)$ with the distance $\frac{lenght2}{2}$. 
    The value of parameter $s$ associated with these points is $\hat s = \pm \frac{length2}{2 l}$. 
    So these two points are 
    $(b \hat s +\hat x, -a \hat s + \hat y)$ and $(-b \hat s +\hat x, a \hat s +\hat y)$.
    
    Example:
    ========
    R = sv.CoordSys3D("R")
    x,y,z = sp.symbols('x y z')
    def field1(x,y): return -y*R.i + x*R.j
    xx, yy = np.mgrid[-5:5:5j, -5:5:5j]
    field1_np = sp.lambdify([x,y], list(field1(x,y).components.values()), 'numpy')
    u,v = field1_np(xx,yy)
    f = vector(x=xx.flatten(),y=yy.flatten(), u=u.flatten(), v=v.flatten())
    '''
    df = pd.DataFrame(columns=['x','y'])

    for x_0,u,y_0,v in zip(x,u,y,v):
        x_1 = x_0 + u
        y_1 = y_0 + v

        a = x_1 - x_0
        b = y_1 - y_0
        
        l = np.sqrt(a**2 + b**2)
        length1 = rt1 *l
        length2 = rt2 * length1

        t = (1-rt1)
        x_bar , y_bar = a * t + x_0, b * t + y_0
        
        s_bar = length2/(2*l)

        x_11 = b*s_bar+x_bar
        x_12 = -b*s_bar+x_bar
        y_11 = -a*s_bar +y_bar
        y_12 = a*s_bar+y_bar

        df = df.append({'x':x_1, 'y':y_1}, ignore_index=True)
        df = df.append({'x':x_11, 'y':y_11}, ignore_index=True)
        df = df.append({'x':x_12, 'y':y_12}, ignore_index=True)
        df = df.append({'x':x_1, 'y':y_1}, ignore_index=True)
        df = df.append({'x':None, 'y':None}, ignore_index=True)
        df = df.append({'x':x_0, 'y':y_0}, ignore_index=True)
        df = df.append({'x':x_bar, 'y':y_bar}, ignore_index=True)
        df = df.append({'x':None, 'y':None}, ignore_index=True)
    
    if fig==False:
        fig = go.Figure()
        fig.add_scatter(x = df.x, y=df.y,fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        fig.show()
    else:
        fig.add_scatter(x = df.x, y=df.y,fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)        

# it is an old version of `vector` method. This old version needs a loop to plot multiple vectors
def plot_vector(x_0,y_0,x_1,y_1, rt1 = 0.1, rt2 = 1/3, fig=False, color = 'black', showgrid = True, zeroline=True, lw=3):
    
    '''
    (x_0,y_0): initial point of the vector
    (x_1,y_1): final point of the vetor
    
    
    The ideia of the below function is as follow. First, we write the parametric equation for the segment of 
    the line that pass through $(0,0)$ and $(x_0, y_0)$. It is 
    $$
    \vec r(t) = \begin{cases}
    x = (x_1 - x_0) t + x_0 \\
    y = (y_1 - y_0) t + y_0
    \end{cases}
     = 
     \begin{cases}
    x = a t + x_0 \\
    y = b t + y_0
    \end{cases}
    $$
    Then using the variable *rt1* we decide about the proportion of the head of the vector em relation to 
    the total length of vector. The variable *rt2* is about the proportion of the base 
    of the triangle em relation to its altitude. *l* is the total length of the vector. *t = 1-ratio1* is the 
    parameter of the line $\vec r(t)$ that the base of the head is located, 
    we call this point as $(\hat x , \hat y)$. Through this point, perpendicular to the $\vec r$ passes 
    another line that is base of the head. The equation of this line is 
    $$
    \vec{r^\prime} = \begin{cases}
    x = b s + \hat x \\
    y = -a s + \hat y
    \end{cases}
    $$
    Now we want to find other two corners of the head, beside $(x_0,y_0)$. These two points are located of 
    the both side of $(\hat x , \hat y)$ with the distance $\frac{lenght2}{2}$. 
    The value of parameter $s$ associated with these points is $\hat s = \pm \frac{length2}{2 l}$. 
    So these two points are 
    $(b \hat s +\hat x, -a \hat s + \hat y)$ and $(-b \hat s +\hat x, a \hat s +\hat y)$.
   
    '''
    
    a = x_1 - x_0
    b = y_1 - y_0
    
    l = np.sqrt((x_1 - x_0)**2 + (y_1 - y_0)**2)
    length1 = rt1 *l
    length2 = rt2 * length1

    t = (1-rt1)
    x_bar , y_bar = a * t + x_0, b * t + y_0
    
    s_bar = length2/(2*l)
    
    if fig==False:
        fig = go.Figure()
    
        fig.add_scatter(x = [x_1,b*s_bar+x_bar, -b*s_bar+x_bar,x_1],
                    y=[y_1, -a*s_bar +y_bar,a*s_bar+y_bar, y_1],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [x_0,x_bar], y=[y_0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.update_scatter(dict(opacity=1))
        fig.show()
    else:
        fig.add_scatter(x = [x_1,b*s_bar+x_bar, -b*s_bar+x_bar,x_1],
                    y=[y_1, -a*s_bar +y_bar,a*s_bar+y_bar, y_1],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [x_0,x_bar], y=[y_0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.show()
    
    
def vector3d(x_0, y_0, z_0, x_1, y_1, z_1, ratio1 = 0.1, ratio2 = 1/3, fig=False, color = 'royalblue', lw = 6):
    
    if fig == False:
        fig = go.Figure()
        fig.add_scatter3d(x = [x_0,0.95*x_1],y=[y_0,0.95*y_1],z=[z_0,0.95*z_1], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_1],y=[y_1],z=[z_1],u=[x_1 - x_0],v=[y_1 - y_0],w=[z_1 - z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.show()
    else:
        fig.add_scatter3d(x = [x_0,0.95*x_1],y=[y_0,0.95*y_1],z=[z_0,0.95*z_1], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_1],y=[y_1],z=[z_1],u=[x_1 - x_0],v=[y_1 - y_0],w=[z_1 - z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        
def plot3d(func, inter1 = None, inter2 = None, fig = False, xtitle = 'X', ytitle= 'Y', ztitle = "Z", title='3D Surface Plot', points = 50, opacity = 1):
    
    '''
    func: must be function with two variables
    inter1: (variable1, start, end)
    inter2: (variable2, start, end)
    '''
    
    if inter1 ==None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 ==None:
        print("Please input the interval for the second variable in the format (variable, begin, end)")
    
    import sympy as sp
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    assert func.free_symbols ==set([inter1[0],inter2[0]]), "The variables of the function aren't the same as the declared in the intervals"
    
    func_np = sp.lambdify([inter1[0],inter2[0]], func)
    
    points = eval(str(points) + 'j')
    xx, yy = np.mgrid[inter1[1]:inter1[2]:points, inter2[1]:inter2[2]:points]
    zz = func_np(xx,yy)
    
    
       
    if fig == False:
        fig = go.Figure()
        fig.add_surface(x = xx , y = yy, z = zz, showlegend=False)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube',
                         opacity = opacity)
        fig.show()
    
    else:
        fig.add_surface(x = xx , y = yy, z = zz, showlegend=False)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube',
                         opacity = opacity)


    
# Parametric plot 3D

def plot3d_parametric_surface(func, inter1 = None, inter2 = None, fig = False, xtitle = 'X', ytitle= 'Y', ztitle = "Z", title='3D Surface Plot', points = 50):

    '''
    func: must be a either a tuple with three components or a parametric equation in the class sympy.vector
    inter1: (parameter, start, end)
    inter2: (parameter, start, end)
    '''
    
    if inter1 ==None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")
    if inter2 ==None:
        print("Please input the interval for the second parameter in the format (parameter, begin, end)")
    
    import sympy as sp
    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())

    #check if the parametric equation has three components.        
    assert len(func) ==3, 'The parametric equation of a 3D surface must has 3 components.'

    #check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func))]
    params_unique = set([item for sublist in params for item in sublist])
    assert params_unique == set([inter1[0],inter2[0]]), "The parameters of the function aren't the same as the ones declared in the intervals"
    
    
    xx_np = sp.lambdify([inter1[0],inter2[0]], func[0])
    yy_np = sp.lambdify([inter1[0],inter2[0]], func[1])
    zz_np = sp.lambdify([inter1[0],inter2[0]], func[2])
    
    var1,var2 = np.linspace(inter1[1],inter1[2],points), np.linspace(inter2[1],inter2[2],points)
    uGrid, vGrid = np.meshgrid(var1, var2)
    xx, yy, zz = xx_np(uGrid,vGrid), yy_np(uGrid,vGrid), zz_np(uGrid,vGrid)
    
          
    if fig == False:
        fig = go.Figure()
        fig.add_surface(x = xx , y = yy, z = zz, showlegend=False)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube')
        fig.show()
    
    else:
        fig.add_surface(x = xx , y = yy, z = zz, showlegend=False)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube')

# Density function (or Scalar field) plot
        
def plot_density_function(func, inter1 = None, inter2 = None, fig = False, xtitle = 'X', ytitle= 'Y', ztitle = "Z", title='2D Density Function', points = 50):
    
    '''
    func: must be function with two variables
    inter1: (variable1, start, end)
    inter2: (variable2, start, end)
    '''
    
    if inter1 ==None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 ==None:
        print("Please input the interval for the second variable in the format (variable, begin, end)")
    
    import sympy as sp
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    assert func.free_symbols ==set([inter1[0],inter2[0]]), "The variables of the function aren't the same as the declared in the intervals"
    
    func_np = sp.lambdify([inter1[0],inter2[0]], func)
    
    points1 = eval(str(points) + 'j')
    
    xx, yy = np.mgrid[inter1[1]:inter1[2]:points1, inter2[1]:inter2[2]:points1]
    zz = func_np(xx,yy)
    
    x ,y = np.linspace(inter1[1],inter2[2],points), np.linspace(inter1[1],inter2[2],points)   
    
    if fig == False:
        fig = go.Figure()
        fig.add_heatmap(x = x , y = y, z = zz, connectgaps=True, zsmooth='best')
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1), 
                          width = (inter1[2]-inter1[1])*50, height = (inter2[2]-inter2[1])*50)
        
        fig.show()
    
    else:
        fig.add_heatmap(x = x , y = y, z = zz, connectgaps=True, zsmooth='best')
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1),
                         width = (inter1[2]-inter1[1])*50, height = (inter2[2]-inter2[1])*50)
        
#3D Density Function (or Scalar Field) plot
        
def plot3d_density_function(func, inter1 = None, inter2 = None, inter3 = None, 
                          fig = False, xtitle = 'X', ytitle= 'Y', ztitle = "Z", 
                          title='2D Density Function', points = 50, isomin=0, isomax=20, opacity=0.4,surface_count=5):
    
    '''
    func: must be function with three variables
    inter1: (variable1, start, end)
    inter2: (variable2, start, end)
    inter3: (variable2, start, end)
    '''
    
    if inter1 ==None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 ==None:
        print("Please input the interval for the second variable in the format (variable, begin, end)")
    if inter3 ==None:
        print("Please input the interval for the third variable in the format (variable, begin, end)")
    
    
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    assert func.free_symbols ==set([inter1[0],inter2[0],inter3[0]]), "The variables of the function aren't the same as the declared in the intervals"
    
    func_np = sp.lambdify([inter1[0],inter2[0],inter3[0]], func)
    
    points1 = eval(str(points) + 'j')
    
    xx, yy, zz = np.mgrid[inter1[1]:inter1[2]:points1, inter2[1]:inter2[2]:points1, inter3[1]:inter3[2]:points1]
    values = func_np(xx, yy, zz)
    
    #x ,y = np.linspace(inter1[1],inter2[2],points), np.linspace(inter1[1],inter2[2],points)   
    
    if fig == False:
        fig = go.Figure()
        fig.add_isosurface(x = xx.flatten(), y = yy.flatten(), z = zz.flatten(),value=values.flatten(),
        isomin=isomin,
        isomax=isomax,
        caps=dict(x_show=False, y_show=False),
                          opacity=opacity,
                          surface_count=surface_count, # number of isosurfaces, 2 by default: only min and max
                          colorbar_nticks=8 # colorbar ticks correspond to isosurface values
                          )
        fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title= ytitle)
        
        fig.show()
    
    else:
        fig.add_isosurface(x = xx.flatten(), y = yy.flatten(), z = zz.flatten(),value=values.flatten(),
        isomin=isomin,
        isomax=isomax,
        caps=dict(x_show=False, y_show=False),
                          opacity=opacity,
                          surface_count=surface_count, # number of isosurfaces, 2 by default: only min and max
                          colorbar_nticks=8 # colorbar ticks correspond to isosurface values
                          )
        fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title= ytitle)

        
        
        
# plotting a 3D vector field
def plot3d_vector_field(func, inter1=None, inter2=None, inter3 = None, fig = None, points=15, sizemode=None, sizeref=1):
    
    
    '''
    - Arguments:
        ``func``: must be vector field with three variables, with Sympy symbols in the format of a vector or tuple
        ``inter1``: (variable1, start, end)
        ``inter2``: (variable2, start, end)
        ``inter3``: (variable3, start, end)
    - Return:
        ``fig``: a Plotly figure object
    '''
    
    
    vars = list(sp.ordered(func.free_symbols))
    if inter1 is None:
        inter1 = (vars[0], -5,5)
    if inter2 is None:
        inter2 = (vars[1], -5,5)
    if inter3 is None:
        inter3 = (vars[2], -5,5)
    
    var1 = inter1[0]
    var2 = inter2[0]
    var3 = inter3[0]
    num = eval(str(points) +'j')
    
    
    
    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())
    
    assert len(func)==3, "the field must have three elements"
    
    xx,yy,zz = np.mgrid[inter1[1]:inter1[2]:num, inter2[1]:inter2[2]:num, inter3[1]:inter3[2]:num]        


    func_np = sp.lambdify([var1,var2,var3],func)

    u,v,w = func_np(xx,yy,zz)
    u,v,w = normalize(u), normalize(v),normalize(w)
    
    
    
    xx,yy,zz,u,v,w = flatten_vf(xx,yy,zz,u,v,w)
    
    if fig is None:
        fig = go.Figure()
        fig.add_cone(x= xx,y = yy,z = zz,u = u,v = v,w = w, colorscale='Blues',
    sizemode=sizemode, sizeref = sizeref)
        return fig
            
    else:
        fig.add_cone(x= xx,y = yy,z = zz,u = u,v = v,w = w, colorscale='Blues',
    sizemode=sizemode, sizeref = sizeref)
        return fig


# Plot a 2D vector field    
def plot_vector_field(func, inter1=None, inter2=None, fig = None, points=15, arrow_scale = 0.1,name=None):

    '''
    - Arguments:
        ``func``: must be vector field with three variables, with Sympy symbols in the format of a vector or tuple
        ``inter1``: (variable1, start, end)
        ``inter2``: (variable2, start, end)
    - Return:
        ``fig``: a Plotly figure object
    '''
    
    vars = list(sp.ordered(func.free_symbols))
    if inter1 is None:
        inter1 = (vars[0], -5,5)
    if inter2 is None:
        inter2 = (vars[1], -5,5)
   
        
    var1 = inter1[0]
    var2 = inter2[0]
    num = eval(str(points) +'j')   

    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())
    
    assert len(func)==2, "the field must have two elements"

    if name is None:
        name = str(func)
    
    xx,yy = np.mgrid[inter1[1]:inter1[2]:num, inter2[1]:inter2[2]:num]        

    func_np = sp.lambdify([var1,var2],func)

    u,v = func_np(xx,yy)
        
    if fig is None:
        fig = ff.create_quiver(xx, yy, u, v, arrow_scale=arrow_scale, name=name)
        return fig
    
    else:
        f = ff.create_quiver(xx, yy, u, v, arrow_scale=arrow_scale,name=name);
        fig.add_trace(*f.data)
        return fig   


#normalizing an array
def normalize(array):
    return (array - np.mean(array))/(np.max(array)-np.min(array))

# normalize a mesh of vectors
def normalize_mesh(u,v,w):
    l = u**2 + v**2 + w**2
    l_norm = (l - np.mean(l))/(np.max(l)-np.min(l))
    return u/l_norm, v/l_norm, w/l_norm


#flattening of lists
def flatten_vf(x, y, z, u, v, w):
    return x.flatten(), y.flatten(), z.flatten(), u.flatten(), v.flatten(), w.flatten()
            
        
        
# construct plane given three points using normal vector 
def plane_1(a,b,c): 
    '''
    a,b,c : tuples with three element (x,y,z)
    '''
    x, y , z = sp.symbols("x y z")
    plane_temp = sp.Plane(sp.Point3D(*a),sp.Point3D(*b),sp.Point3D(*c))
    vn = plane_temp.normal_vector
    
    return -(vn[0]*(x-a[0])+vn[1]*(y-a[1]))/vn[2] + a[2]

# construct plane given three points using determinent 

def plane_2(a,b,c): 
    '''
    a,b,c : tuples with three element (x,y,z)
    '''
    x, y , z = sp.symbols("x y z")
      
    matrix = [[x ,y, z,1],[a[0],a[1],a[2],1],
                      [b[0],b[1],b[2],1],[c[0],c[1],c[2],1]]
    matrix = sp.Matrix(matrix)
    return sp.solve(matrix.det(),z)[0]

# Norm of a vector
def Norm(v):
    return sp.simplify(sp.sqrt(v.dot(v)))

#Unit vector
def Unit_Vector(curve):
    return curve/Norm(curve)

#Arc Length
def Arc_Length(curve, a): 
    #a: Um Tuple (variavel, inicio, fim)
    return sp.integrate(Norm(curve.diff()),a)

# Tangent Unitary vector
def UT(curve): return curve.diff()/Norm(curve.diff())

# Normal Unitary Vector
def UN(curve): return UT(curve).diff()/Norm(UT(curve).diff())

# Binormal Unitary Vector
def UB(curve): return (UT(curve)^UN(curve)).simplify()

# Curvature of a curve
def curvature(curve): return Norm(UT(curve).diff())/Norm(curve.diff())

# Torsion of a curve
def torsion(curve , t=None): 
    # t: is the parameter of the curve

    if t ==None:
        t = sp.symbols('t')

    return (curve.diff().cross(curve.diff(t,2))).dot(curve.diff(t,3))/Norm(curve.diff().cross(curve.diff(t,2)))

#Integral of a parametric curve accepting the boundary condition to determine the constant of integration
def integral_vector(curve,var, ics=None):
    """
    ``curve``: a parametric curve with a coordinate system using sp.Coordsys3D
    ``var``: the parameter of the curve
    ``ics``: inicial/boundary conditions in the format of a dictionary {var:t_0, 'x':x_0, 'y':y_0, 'z':z_0}
    
    Example
    =========
    import sympy as sp
    import sympy.vector as sv
    R = sv.CoordSys3D('R')
    t = sp.symbols('t')
    def r(t):
        return 2*t*R.i + t**2*R.j - R.k
    
    integral_vector(r(t),t, {t:1,'x':2, 'y':-1, 'z':-1})
    
    """
    
    c_1,c_2,c_3 = sp.symbols('c_1 c_2 c_3')
    
    R = list(curve.separate().keys())[0]
    
    x_c = curve.dot(R.i)
    y_c = curve.dot(R.j)
    z_c = curve.dot(R.k)
    x_c_int = sp.integrate(x_c,var)
    y_c_int = sp.integrate(y_c,var)
    z_c_int = sp.integrate(z_c,var)
    v_int = (x_c_int+c_1)*R.i + (y_c_int + c_2)*R.j + (z_c_int + c_3)*R.k
    
    if ics is not None:
        eq_x = sp.Eq(x_c_int.subs(var,ics[var])+c_1,ics['x'])
        sol_x = sp.solve(eq_x,dict=True)[0][c_1]
        
        eq_y = sp.Eq(y_c_int.subs(var,ics[var])+c_2,ics['y'])
        sol_y = sp.solve(eq_y,dict=True)[0][c_2]
        
        eq_z = sp.Eq(z_c_int.subs(var,ics[var])+c_3, ics['z'])
        sol_z = sp.solve(eq_z,dict=True)[0][c_3]
        
        v_int_n = v_int.subs(c_1,sol_x).subs(c_2,sol_y).subs(c_3,sol_z)
        
        return v_int_n
    else:

        return v_int

#Line Integral for a scalar field
def line_integral_scalar(field,curve,a):
    '''
    field: Scalar field F(x,y,z). NOTE: the function must be inserted without its arguments.
    curve: parametrized curve r(t) = x(t)i + y(t)j + z(t)k
    a:(Tuple) (parameter of the curve, initial point, final point)
    Note: if the field is tridimensional, the curve also must have the same dimension. 
    
    '''
    
    c = tuple(curve.components.values())
    
    # parametrizing the field using the curve parametric equation
    parametrized_field = field(*c)
    module = Norm(curve.diff())
        
  
    integrand = parametrized_field*module
        
    return sp.integrate(integrand,a).simplify()


#Line integral for a vectorial field
def line_integral_vectorial(field,curve,a):
    '''
    ``field``: Vector field F(x,y,z) = P(x,y,z)i + R(x,y,z)j + Q(x,y,z)k. The parameters of the field must be `x`,`y` and `z`
    ``curve``: parametrized curve r(t) = x(t)i + y(t)j + z(t)k
    ``a``:(Tuple) (parameter of the curve, initial point, final point)
    **Note**: if the field is tridimensional, the curve also must have the same dimensions. 

    Example:
    =====
    import sympy as sp
    import sympy.vector as sv
    R = sv.CoordSys3D('R')
    t,x,y,z = sp.symbols('t x y z')
    def f(x,y,z):
        x*R.i + y*z*R.j + x*z*R.k
    def r(t):
        return 2*t*R.i + t**2*R.j - R.k
    
    line_integral_vectorial(f, r(t), (t,-1,2))
    
    '''

    #taking the name of the coordinate system. Here we assume that the filed and curve are using the same coordinate system
    R = list(curve.separate().keys())[0]
    
    x_c  = curve.dot(R.i)
    y_c  = curve.dot(R.j)
    z_c  = curve.dot(R.k)
    
    # parametrizing the field using the curve equation
    parametrized_field =field.subs(x, x_c).subs(y, y_c).subs(z, z_c)
    
    
    integrand = parametrized_field.dot(curve.diff())
    
        
    return sp.integrate(integrand,a)

# gradient in Cartesian coordinate system
def gradient(func, point=None, coordinate=None):
    """
    - Arguments:
        ``func``: A function with 2 or 3 variables in the Cartesian coordinate system (x,y) or (x,y,z). 
        ``point``: optional. A point in the plano or space.
        ``coordinate``: optional. The name of the coordinate system.
    - Return:
        ``grad``: The gradient of the function
    """
    #vars = (list(sp.ordered(func.free_symbols)))

    if not coordinate:
        R = sv.CoordSys3D('R')
    else:
        R = coordinate
     
    grad = func.diff(x)*R.i + func.diff(y)*R.j + func.diff(z)*R.k
    
    
    if point:
        if len(point)==3:
            grad = grad.subs({x:point[0], y:point[1], z:point[2]})
        else:
            grad = grad.subs({x:point[0], y:point[1]})

    return grad


# Curl in the Cartesian coordinate system   
def rotacional(func, point=None, coordinate=None):
    """
    - Arguments:
        ``func``: A function with 3 variables in the Cartesian coordinate system (x,y,z). 
        ``point``: optional. A point in the plano or space.
        ``coordinate``: optional. The name of the coordinate system.
    - Return:
        ``curl``: The curl of the function
    """
    if coordinate:
        R = coordinate
    else:
        R = sv.CoordSys3D('R')
    func_x = func & R.i
    func_y = func & R.j
    func_z = func & R.k
    curl_x = func_z.diff(y) - func_y.diff(z)
    curl_y = func_x.diff(z) - func_z.diff(x)
    curl_z = func_y.diff(x) - func_x.diff(y)
    curl = curl_x*R.i + curl_y*R.j + curl_z*R.k
    if point:
        curl = curl.subs({x:point[0], y:point[1], z:point[2]})

    return curl
    
# Divergent in the Cartesian coordinate system
def divergente(func, point=None, coordinate=None):
    """
    - Arguments:
        ``func``: A function with 3 variables in the Cartesian coordinate system (x,y,z). 
        ``point``: optional. A point in the plano or space.
        ``coordinate``: optional. The name of the coordinate system.
    - Return:
        ``div``: The divergent of the function
    """
    if coordinate:
        R = coordinate
    else:
        R = sv.CoordSys3D('R')
    func_x = func & R.i
    func_y = func & R.j
    func_z = func & R.k

    div = func_x.diff(x) + func_y.diff(y) + func_z.diff(z)

    if point:
        div = div.subs({x:point[0], y:point[1], z:point[2]})
    
    return div
    
# finding the minimum of an univariate function using gradient descent
def minimum(func, a, alpha=0.01, epochs=100, precision=0.0001):
    '''
    func: uma função no formato de Sympy
    a: um tuple (varivel da função, inicio, fim)
    '''
    #fining the derivative of the func
    derivative = func.diff()
    #grads = np.zeros((epochs,2))

    #lambdify
    f = sp.lambdify(a[0], func, 'numpy')
    deriv = sp.lambdify(a[0], derivative, 'numpy')

    #finding an aproximation of the mininum by a random search
    l = np.linspace(a[1],a[2], 100)
    f_min_index = np.argmin(f(l))
    local_min = l[f_min_index]

    #print(f"inicial local_min is {local_min}")

    # starting the gradient descent
    for epoch in range(epochs):
        last_local_min = local_min
        local_min -= alpha * deriv(local_min)
        #print(f"the {epoch}th local_min is {local_min}")
        #grads[epoch,:] = local_min, f(local_min)
        
        if abs(f(local_min) - f(last_local_min)) < precision:
            print('reached the precision')
            break
        
        if local_min > a[2] or local_min < a[1]:
            local_min = last_local_min
            print('out of interval')
            break

    return local_min #,grads

