#! /home/vahid/miniconda3/bin/python

import plotly.graph_objects as go

import numpy as np

# 2D curve plot
def curve(x , y , fig = False,xtitle = 'X', ytitle= 'Y', title='2D Plot', lw =5):
    
    if fig == False:
        fig = go.Figure()
        fig.add_scatter(x= x , y = y, showlegend=False, mode ='lines',line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, yaxis=dict(scaleanchor="x", scaleratio=1))
        fig.show()
    
    else:
        fig.add_scatter(x = x , y = y, showlegend=False,mode ='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,yaxis=dict(scaleanchor="x", scaleratio=1)) 
        

# 3D curve plot

def curve3d(x , y , z, fig = False, xtitle = 'X', ytitle= 'Y', title='3D Plot', lw =5):
    
    if fig == False:
        fig = go.Figure()
        fig.add_scatter3d(x= x , y = y, z =z, showlegend=False, mode ='lines',line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title= ytitle, 
            scene=dict(camera=dict(eye=dict(x=1.15, y=1.15, z=0.8)), #the default values are 1.25, 1.25, 1.25
            xaxis=dict(),
           yaxis=dict(),
           zaxis=dict(),
           aspectmode='data', #this string can be 'data', 'cube', 'auto', 'manual'
           #a custom aspectratio is defined as follows:
           aspectratio=dict(x=1, y=1, z=0.95)
           ))
        fig.show()
    
    else:
        fig.add_scatter3d(x = x , y = y, z =z, showlegend=False,mode ='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, 
            scene=dict(camera=dict(eye=dict(x=1.15, y=1.15, z=0.8)), #the default values are 1.25, 1.25, 1.25
            xaxis=dict(),
           yaxis=dict(),
           zaxis=dict(),
           aspectmode='data', #this string can be 'data', 'cube', 'auto', 'manual'
           #a custom aspectratio is defined as follows:
           aspectratio=dict(x=1, y=1, z=0.95)
           )) 
        

# Plot a parametric curve in 3D
def plot3d_parametric_curve(func, inter1 = None, inter2 = None, fig = False, xtitle = 'X', ytitle= 'Y', ztitle = "Z", title='3D Surface Plot', points = 50):

    '''
    - func: must be a either a tuple with three components (e.g. Sympy objects) or a parametric equation in the class sympy.vector
    - inter1: (parameter, start, end)
    '''
    
    if inter1 ==None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")

    
    import sympy as sp
    if isinstance(func, tuple(sp.core.all_classes)):
        if func.is_Vector:
            func = tuple(func.components.values())

    #check if the parametric equation has three components.        
    assert len(func) ==3, 'The parametric equation of a 3D surface must has 3 components.'

    #check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func)) if isinstance(func[i], tuple(sp.core.all_classes)) ]
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
        
        curve3d(x = xx , y = yy, z = zz)
        
    
    else:
        curve3d(x = xx , y = yy, z = zz, fig = fig)
        


        
        
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
    import plotly.graph_objects as go
    import numpy as np
    
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
    
    import plotly.graph_objects as go
    import numpy as np
    
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

        
def vector(x_0,y_0,x_1,y_1, rt1 = 0.1, rt2 = 1/3, fig=False, color = 'black', showgrid = True, zeroline=True, lw=3):
    
    '''The ideia of the below function is as follow. First, we write the parametric equation for the segment of 
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
    
    import plotly.graph_objects as go
    import numpy as np
    
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
    
    import plotly.graph_objects as go
    import numpy as np
    
    
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
    
    if inter1 ==None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 ==None:
        print("Please input the interval for the second variable in the format (variable, begin, end)")
    
    import sympy as sp
    if not isinstance(func, tuple(sp.core.all_classes)):
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
    if isinstance(func, tuple(sp.core.all_classes)):
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
        
# construct plane given three points using normal vector 
def plane_1(a,b,c): 
    '''
    a,b,c : tuples with three element (x,y,z)
    '''
    x, y , z = sp.symbols("x y z")
    plane_temp = sp.Plane(sp.Point3D(*a),sp.Point3D(*b),sp.Point3D(*c))
    vn = plane_temp.normal_vector;
    
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
