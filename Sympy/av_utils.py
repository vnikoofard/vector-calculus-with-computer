#! /home/vahid/miniconda3/bin/python

import plotly.graph_objects as go
import sympy as sp
import pandas as pd
import numpy as np
import sympy.vector as sv
import plotly.figure_factory as ff
from collections.abc import Iterable


# 2D curve plot. A wrapper for plotly scatter plot
def plot_curve(x, y, fig=None, xtitle='X', ytitle='Y', title='2D Plot', lw=5):    
    if fig is None:
        fig = go.Figure()
        fig.add_scatter(x=x, y=y, showlegend=False, mode='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title=ytitle, yaxis=dict(scaleanchor="x", scaleratio=1))
    else:
        fig.add_scatter(x=x, y=y, showlegend=False, mode ='lines', line_width=lw)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title=ytitle, yaxis=dict(scaleanchor="x", scaleratio=1))   

    return fig      


# 3D curve plot. A wrapper for plotly scatter3d plot
def plot_curve3d(x, y, z, fig=None, xtitle='X', ytitle='Y', title='3D Plot', aspectmode='data', lw =5):
    
    if fig is None:
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


# plot a 2D implicit function like a circle or an ellipse.
def plot_implicit(func, inter1=None, inter2=None, fig=None, xtitle='X',
                  ytitle='Y', title=None, points=50, colorscale = 'Blues'):
    '''
    - Argument:
        `func`: must be a function like g(y)+f(x)=0 (just the left handside) or as a sp.Eq() object
        `inter1`: (variable1, start, end)
        `inter2`: (variable2, start, end)
    -Return:
        a Plotly graph object

    ========
    Example:
    import sympy as sp
    x,y = sp.symbols('x y')
    eq = sp.Eq(x**2/2,-y**2/2+1)
    plot_implicit(x**2+y**2-1, (x,-2,2), (y,-2,2))
    '''
    if title is None:
        title = str(func)

    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))

    if func.is_Equality:
        func = func.lhs - func.rhs
    
    vars = list(sp.ordered(func.free_symbols))
    assert len(vars) == 2, 'The function must have at most one variable'

    if inter1 is None:
        inter1 = (vars[0], -5, 5)
    if inter2 is None:
        inter2 = (vars[1], -5, 5)

    # assert func.free_symbols == set([inter1[0], inter2[0]]), "The variables of the function aren't the same as the declared in the intervals"

    func_np = sp.lambdify([inter1[0], inter2[0]], func)

    xx = np.linspace(inter1[1], inter1[2], points)
    yy = np.linspace(inter2[1], inter2[2], points)
    X, Y = np.meshgrid(xx, yy)
    Z = func_np(X, Y)

    if fig is None:
        fig = go.Figure()
        fig.add_contour(x=xx, y=yy, z=Z, showlegend=False, name=str(func),contours_coloring='lines',
        line_width=2, colorscale=colorscale,
        contours=dict(start=0, end=0, size=2))
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title=ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1))

    else:
        fig.add_contour(x=xx, y=yy, z=Z, showlegend=False, name=str(func),contours_coloring='lines',
        line_width=2, colorscale=colorscale,
        contours=dict(start=0, end=0, size=2))
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1))

    return fig

# Plot a parametric curve in 2D
def plot_parametric_curve(func, inter1=None, fig=None, xtitle='X', ytitle='Y', 
                            title='Curve Plot', points=50,
                            ):

    '''
    - Arguments:
        `func`: must be either a tuple with three components (e.g. Sympy objects) or a parametric equation in the class sympy.vector
        `inter1`: (parameter, start, end)
        `fig`: A plotly figure object
        `xtitle`: x-axis title
        `ytitle`: y-axis title
        `title`: title of the figure
        `points`: the number of points to plot the curve
    - Return:
        A figure object of Plotly
    '''
    if inter1 is None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")

    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())

    # check if the parametric equation has three components.        
    assert len(func) == 2, 'The parametric equation of a 2D curve must has 2 components.'

    # check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func)) if isinstance(func[i], sp.Expr) ]
    params_unique = set([item for sublist in params for item in sublist])
    assert params_unique == set([inter1[0]]), "The parameters of the function aren't the same as the ones declared in the intervals"

    xx_np = sp.lambdify(inter1[0], func[0])
    yy_np = sp.lambdify(inter1[0], func[1])

    var1 = np.linspace(inter1[1], inter1[2], points)
    xx, yy = xx_np(var1), yy_np(var1)
    #xx, yy, zz = xx_np(var1), yy_np(var1), zz_np(var1)

    l = list([xx, yy])
    for item in range(len(l)):
        if type(item) != np.ndarray:
            l[item] *= np.ones(var1.shape)

    xx, yy = l[0], l[1]

    if fig is None:

        return plot_curve(x=xx, y=yy, xtitle=xtitle, ytitle=ytitle, title=title)

    else:
        return plot_curve(x=xx, y=yy, fig=fig, xtitle=xtitle, ytitle=ytitle, title=title)


# Plot a parametric curve in 3D
def plot3d_parametric_curve(func, inter1=None, fig=None, xtitle='X', ytitle='Y', 
                            title='3D Curve Plot', points=50,
                            aspectmode='data'):

    '''
    - Arguments:
        `func`: must be either a tuple with three components (e.g. Sympy objects) or a parametric equation in the class sympy.vector
        `inter1`: (parameter, start, end)
        `fig`: A plotly figure object
        `xtitle`: x-axis title
        `ytitle`: y-axis title
        `title`: title of the figure
        `points`: the number of points to plot the curve
        `aspectmode`: a parameter of figure object
    - Return:
        A figure object of Plotly
    '''
    if inter1 is None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")

    if isinstance(func, sp.Expr):
        if func.is_Vector:
            func = tuple(func.components.values())

    # check if the parametric equation has three components.        
    assert len(func) ==3, 'The parametric equation of a 3D curve must has 3 components.'

    # check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func)) if isinstance(func[i], sp.Expr) ]
    params_unique = set([item for sublist in params for item in sublist])
    assert params_unique == set([inter1[0]]), "The parameters of the function aren't the same as the ones declared in the intervals"

    xx_np = sp.lambdify(inter1[0], func[0])
    yy_np = sp.lambdify(inter1[0], func[1])
    zz_np = sp.lambdify(inter1[0], func[2])

    var1 = np.linspace(inter1[1], inter1[2], points)
    xx, yy, zz = xx_np(var1), yy_np(var1), zz_np(var1)

    l = list([xx, yy, zz])
    for item in range(len(l)):
        if type(item) != np.ndarray:
            l[item] *= np.ones(var1.shape)

    xx, yy, zz = l[0], l[1], l[2]

    if fig is None:

        return plot_curve3d(x=xx, y=yy, z=zz, xtitle=xtitle, ytitle=ytitle, title=title,aspectmode=aspectmode)

    else:
        return plot_curve3d(x=xx, y=yy, z=zz, fig=fig, xtitle=xtitle, ytitle=ytitle, title=title, aspectmode=aspectmode)


# Position vector originating from origin!
def position_vector(x_0, y_0, rt1=0.1, rt2=1/3, fig=None, color='black', showgrid=True, zeroline=True, lw=2):

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
    
    if fig is None:
        fig = go.Figure()
    
        fig.add_scatter(x = [x_0,y_0*s_bar+x_bar, -y_0*s_bar+x_bar,x_0],
                    y=[y_0, -x_0*s_bar +y_bar,x_0*s_bar+y_bar, y_0],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [0,x_bar], y=[0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.update_scatter(dict(opacity=1))
    else:
        fig.add_scatter(x = [x_0,y_0*s_bar+x_bar, -y_0*s_bar+x_bar,x_0],
                    y=[y_0, -x_0*s_bar +y_bar,x_0*s_bar+y_bar, y_0],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [0,x_bar], y=[0,y_bar], mode='lines',line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)

    return fig

        
def position_vector3d(x_0, y_0, z_0, ratio1 = 0.1, ratio2 = 1/3, fig=None, color = 'black', lw=2):
    
    if fig is None:
        fig = go.Figure()
        fig.add_scatter3d(x = [0,0.95*x_0],y=[0,0.95*y_0],z=[0,0.95*z_0], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_0],y=[y_0],z=[z_0],u=[x_0],v=[y_0],w=[z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)

    else:
        fig.add_scatter3d(x = [0,0.95*x_0],y=[0,0.95*y_0],z=[0,0.95*z_0], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_0],y=[y_0],z=[z_0],u=[x_0],v=[y_0],w=[z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
    
    return fig

def vector(x, y, u, v, rt1=0.1, rt2=1/3, fig=None, color='black', showgrid=True, zeroline=True, lw=3):
    
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
    f = vector(x=xx, y=yy, u=u, v=v)
    '''
    df = pd.DataFrame(columns=['x','y'])

    x, y, u, v = x.flatten(), y.flatten(), u.flatten(), v.flatten()

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
    
    if fig is None:
        fig = go.Figure()
        fig.add_scatter(x = df.x, y=df.y,fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)

    else:
        fig.add_scatter(x = df.x, y=df.y,fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)   

    return fig     

# it is an old version of `vector` method. This old version needs a loop to plot multiple vectors
def plot_vector(x_0,y_0,x_1,y_1, rt1 = 0.1, rt2 = 1/3, fig=None, color = 'black', showgrid = True, zeroline=True, lw=3):
    
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
    
    if fig is None:
        fig = go.Figure()
    
        fig.add_scatter(x = [x_1,b*s_bar+x_bar, -b*s_bar+x_bar,x_1],
                    y=[y_1, -a*s_bar +y_bar,a*s_bar+y_bar, y_1],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [x_0,x_bar], y=[y_0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        #fig.update_scatter(dict(opacity=1))
    else:
        fig.add_scatter(x = [x_1,b*s_bar+x_bar, -b*s_bar+x_bar,x_1],
                    y=[y_1, -a*s_bar +y_bar,a*s_bar+y_bar, y_1],
                    fill='toself', mode = 'lines', opacity=1,line_color = color, line_width=lw)
        fig.add_scatter(x = [x_0,x_bar], y=[y_0,y_bar], mode='lines',line_color = color,line_width=lw)
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1),showlegend = False)
        fig.update_xaxes(showgrid=showgrid, zeroline=zeroline)
        fig.update_yaxes(showgrid=showgrid, zeroline=zeroline)
        
    return fig
    
    
def vector3d(x_0, y_0, z_0, x_1, y_1, z_1, ratio1 = 0.1, ratio2 = 1/3, fig=None, color = 'royalblue', lw = 6):
    
    if fig is None:
        fig = go.Figure()
        fig.add_scatter3d(x = [x_0,0.95*x_1],y=[y_0,0.95*y_1],z=[z_0,0.95*z_1], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_1],y=[y_1],z=[z_1],u=[x_1 - x_0],v=[y_1 - y_0],w=[z_1 - z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)

    else:
        fig.add_scatter3d(x = [x_0,0.95*x_1],y=[y_0,0.95*y_1],z=[z_0,0.95*z_1], mode = 'lines'
                          , line_width=lw,line_color = 'royalblue')
        fig.add_cone(x=[x_1],y=[y_1],z=[z_1],u=[x_1 - x_0],v=[y_1 - y_0],w=[z_1 - z_0], anchor = 'tip',
                     showscale= False, sizeref = 0.1 ,colorscale=[[0, color], [1,color]])
        fig.update_layout(showlegend = False)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)

    return fig

#Plot a curve using its symbolic equation in the format f(x)
def plot(func, inter1 = None, fig = None, xtitle = 'X', ytitle= 'Y', title=None, points = 50):
    
    '''
    - Argument:
        `func`: must be a function like y=f(x)
        `inter1`: (variable1, start, end)
    -Return:
        a Plotly graph object
    '''
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    
    var = list(sp.ordered(func.free_symbols))
    assert len(var)==1, 'The function must have at most one variable'
    if inter1 is None:
        inter1 = (var[0], -5,5)
        
    if title is None:
        title = str(func)
    
    
    assert func.free_symbols ==set([inter1[0]]), "The variable of the function isn't the same as the declared in the interval"
    
    func_np = sp.lambdify(inter1[0], func)
    
    xx = np.linspace(inter1[1],inter1[2], points)
    yy = func_np(xx)
    
    
       
    if fig is None:
        fig = go.Figure()
        fig.add_scatter(x=xx, y=yy, showlegend=False, mode='lines', name= str(func))
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1))
    
    else:
        fig.add_scatter(x=xx, y=yy, showlegend=False, mode='lines', name= str(func))
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1))

    return fig

# Plot a surface using its symbolic equation in the format f(x,y)        
def plot3d(func, inter1=None, inter2=None, fig=None,
 xtitle='X', ytitle='Y', ztitle="Z", title=None, showscale=False,
 points = 50, opacity = 0.9):
    
    '''
    - Arguments:
        `func`: must be function with two variables
        `inter1`: (variable1, start, end)
        `inter2`: (variable2, start, end)
    - Return:
        a plotly graph object
    '''
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    
    if isinstance(func, sp.Eq): # in the case of a av.plane object
        func = func.rhs

    
    vars_func = list(sp.ordered(func.free_symbols))
    

    if len(vars_func) == 2:
        vars = vars_func
        if inter1 is None:
            inter1 = (vars[0], -5,5)
        if inter2 is None:
            inter2 = (vars[1], -5,5)
    elif len(vars_func) < 2:
        vars = [inter1[0], inter2[0]]
    
    
    
    assert all([param in vars for param in vars_func]),  "The variables of the function aren't the same as the declared in the intervals"
        
    if title is None:
        title = str(func)
    
    
    
    func_np = sp.lambdify(vars, func)
    
    points = eval(str(points) + 'j')
    xx, yy = np.mgrid[inter1[1]:inter1[2]:points, inter2[1]:inter2[2]:points]
    zz = func_np(xx,yy)
    
    if isinstance(zz, int) or isinstance(zz, float):
        zz = zz*np.ones((len(xx), len(yy)))
       
    if fig is None:
        fig = go.Figure()
        fig.add_surface(x = xx , y = yy, z = zz, showscale=showscale,name= str(func), opacity=opacity)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube')
    
    else:
        fig.add_surface(x = xx , y = yy, z = zz, showscale=showscale,name= str(func), opacity=opacity)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode='cube')

    return fig
    
# Parametric plot 3D

def plot3d_parametric_surface(func, inter1 = None, inter2 = None, fig = None, xtitle = 'X', 
                                ytitle= 'Y', ztitle = "Z", title='3D Surface Plot', 
                                points = 50, scene_aspectmode = 'data', surfacecolor=None,  showscale=True):

    '''
    `func`: must be a either a tuple with three components or a parametric equation in the class sympy.vector
    `inter1`: (parameter, start, end)
    `inter2`: (parameter, start, end)
    `scene_aspectmode`: string. 'data' or 'cube'
    `surfacecolor`: function. a sympy function to determine the color of the surface. 
    '''
    
    if inter1 is None:
        print("Please input the interval for the first parameter in the format (parameter, begin, end)")
    if inter2 is None:
        print("Please input the interval for the second parameter in the format (parameter, begin, end)")
    
    if isinstance(func, sp.Expr):
        if func.is_Vector:
            R = list(func.separate().keys())[0]
            func_x = func & R.i
            func_y = func & R.j
            func_z = func & R.k
            func = tuple(func.components.values())
    elif isinstance(func, tuple) or isinstance(func, list):
        assert len(func)==3, "the field must have three elements"
        func_x = func[0]
        func_y = func[1]
        func_z = func[2]
    else:
        print("the field isn't recognized. it must be a tuple of three sympy functions or a vector field of class sympy.vector")
    #check if the parametric equation has three components.        
    #assert len(func) ==3, 'The parametric equation of a 3D surface must has 3 components.'

    #check if the parameters of the equation are the same as parameters declared in the intervals.
    params = [func[i].free_symbols for i in range(len(func))]
    params_unique = set([item for sublist in params for item in sublist])
    assert params_unique == set([inter1[0],inter2[0]]), "The parameters of the function aren't the same as the ones declared in the intervals"
    
    
    xx_np = sp.lambdify([inter1[0],inter2[0]], func_x)
    yy_np = sp.lambdify([inter1[0],inter2[0]], func_y)
    zz_np = sp.lambdify([inter1[0],inter2[0]], func_z)
    
    var1,var2 = np.linspace(inter1[1],inter1[2],points), np.linspace(inter2[1],inter2[2],points)
    uGrid, vGrid = np.meshgrid(var1, var2)
    xx, yy, zz = xx_np(uGrid,vGrid), yy_np(uGrid,vGrid), zz_np(uGrid,vGrid)
    
    # if one of the coordinate be constant. 
    if isinstance(xx,int):
        xx = xx*np.ones((points,points))
    if isinstance(yy,int):
        yy = yy*np.ones((points,points))
    if isinstance(zz,int):
        zz = zz*np.ones((points,points))
    
    if surfacecolor:
        x_col = np.linspace(xx.min(), xx.max(), points)
        y_col = np.linspace(yy.min(), yy.max(), points)
        z_col = np.linspace(zz.min(), zz.max(), points)
        
        xx_col, yy_col, zz_col = np.meshgrid(x_col,y_col, z_col)
        
        vars = list(surfacecolor.free_symbols)
        color_np = sp.lambdify(vars, surfacecolor) 
        for ind, var in enumerate(vars):
            if var.name == 'x':
                vars[ind] = xx
            elif var.name == 'y':
                vars[ind] = yy
            elif var.name == 'z':
                vars[ind] = zz
        surfacecolor = color_np(*vars)

        
    if fig is None:
        fig = go.Figure()
        fig.add_surface(x = xx , y = yy, z = zz, surfacecolor = surfacecolor, showscale=showscale)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode=scene_aspectmode)
    
    else:
        fig.add_surface(x = xx , y = yy, z = zz, surfacecolor = surfacecolor, showscale=showscale)
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle, scene_aspectmode=scene_aspectmode)
    return fig


# Density function (or Scalar field) plot
        
def plot_density_function(func, inter1 = None, inter2 = None, fig = None, xtitle = 'X', ytitle= 'Y', ztitle = "Z", title='2D Density Function', points = 50):
    
    '''
    func: must be function with two variables
    inter1: (variable1, start, end)
    inter2: (variable2, start, end)
    '''
    
    if inter1 is None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 is None:
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
    
    if fig is None:
        fig = go.Figure()
        fig.add_heatmap(x = x , y = y, z = zz, connectgaps=True, zsmooth='best')
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1), 
                          width = (inter1[2]-inter1[1])*50, height = (inter2[2]-inter2[1])*50)
        
    
    else:
        fig.add_heatmap(x = x , y = y, z = zz, connectgaps=True, zsmooth='best')
        fig.update_layout(title=title, xaxis_title=xtitle,
                          yaxis_title= ytitle,
                          yaxis=dict(scaleanchor="x", scaleratio=1),
                         width = (inter1[2]-inter1[1])*50, height = (inter2[2]-inter2[1])*50)
    
    return fig
        
#3D Density Function (or Scalar Field) plot
        
def plot3d_density_function(func, inter1 = None, inter2 = None, inter3 = None, 
                          fig = None, xtitle = 'X', ytitle= 'Y', ztitle = "Z", 
                          title='2D Density Function', points = 50, isomin=0, isomax=20, opacity=0.4,surface_count=5):
    
    '''
    func: must be function with three variables
    inter1: (variable1, start, end)
    inter2: (variable2, start, end)
    inter3: (variable2, start, end)
    '''
    
    if inter1 is None:
        print("Please input the interval for the first variable in the format (variable, begin, end)")
    if inter2 is None:
        print("Please input the interval for the second variable in the format (variable, begin, end)")
    if inter3 is None:
        print("Please input the interval for the third variable in the format (variable, begin, end)")
    
    
    if not isinstance(func, sp.Expr):
        func = sp.sympify(str(func))
    assert func.free_symbols ==set([inter1[0],inter2[0],inter3[0]]), "The variables of the function aren't the same as the declared in the intervals"
    
    func_np = sp.lambdify([inter1[0],inter2[0],inter3[0]], func)
    
    points1 = eval(str(points) + 'j')
    
    xx, yy, zz = np.mgrid[inter1[1]:inter1[2]:points1, inter2[1]:inter2[2]:points1, inter3[1]:inter3[2]:points1]
    values = func_np(xx, yy, zz)
    
    #x ,y = np.linspace(inter1[1],inter2[2],points), np.linspace(inter1[1],inter2[2],points)   
    
    if fig is None:
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

    return fig

        
# plotting a 3D vector field
def plot3d_vector_field(field, inter1=None, inter2=None, inter3 = None, fig = None, points=15, sizemode=None, sizeref=1):
    
    '''
    - Arguments:
        `field`: must be vector field with three variables, with Sympy symbols in the format of a vector or tuple
        `inter1`: (variable1, start, end)
        `inter2`: (variable2, start, end)
        `inter3`: (variable3, start, end)
    - Return:
        `fig`: a Plotly figure object
    '''
    
    
    vars = list(sp.ordered(field.free_symbols))
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
    
    if isinstance(field, sp.Expr):
        if field.is_Vector:
            R = list(field.separate().keys())[0]
            field_x = field & R.i
            field_y = field & R.j
            field_z = field & R.k
            #field = tuple(field.components.values())
    elif isinstance(field, tuple) or isinstance(field, list):
        assert len(field)==3, "the field must have three elements"
        field_x = field[0]
        field_y = field[1]
        field_z = field[2]
    else:
        print("the field isn't recognized. it must be a tuple of three sympy functions or a vector field of class sympy.vector")
    
    
    xx,yy,zz = np.mgrid[inter1[1]:inter1[2]:num, inter2[1]:inter2[2]:num, inter3[1]:inter3[2]:num]     
    
    
    field_x_np = sp.lambdify([var1,var2,var3], field_x)
    field_y_np = sp.lambdify([var1,var2,var3], field_y)
    field_z_np = sp.lambdify([var1,var2,var3], field_z)


    if isinstance(field_x, sp.core.numbers.Number):
        u = np.ones(xx.shape)*float(field_x)
    else:
        u = field_x_np(xx,yy,zz)
        u = normalize(u)
    
    if isinstance(field_y, sp.core.numbers.Number):
        v = np.ones(yy.shape)*float(field_y)
    else:
        v = field_y_np(xx,yy,zz)
        v = normalize(v)
    
    if isinstance(field_z, sp.core.numbers.Number):
        w = np.ones(zz.shape)*float(field_z)
    else:
        w = field_z_np(xx,yy,zz)
        w = normalize(w)

    
    xx,yy,zz,u,v,w = flatten_vf(xx,yy,zz,u,v,w)
    
    if fig is None:
        fig = go.Figure()
        fig.add_cone(x= xx, y = yy, z = zz,u = u, v = v, w = w, colorscale='Blues',
    sizemode=sizemode, sizeref = sizeref)
        return fig
            
    else:
        fig.add_cone(x= xx, y = yy, z = zz, u = u, v = v, w = w, colorscale='Blues',
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
def plane(a,b,c): 
    '''
    a,b,c : tuples with three element (x,y,z)
    '''
    x, y , z = sp.symbols("x y z")
    plane_temp = sp.Plane(sp.Point3D(*a),sp.Point3D(*b),sp.Point3D(*c))
    vn = plane_temp.normal_vector
    
    return sp.Eq(z, -(vn[0]*(x-a[0])+vn[1]*(y-a[1]))/vn[2] + a[2])

# construct plane given three points using determinent 

def plane_1(a,b,c): 
    '''
    a,b,c : tuples with three element (x,y,z)
    '''
    x, y , z = sp.symbols("x y z")
      
    matrix = [[x ,y, z,1],[a[0],a[1],a[2],1],
                      [b[0],b[1],b[2],1],[c[0],c[1],c[2],1]]
    matrix = sp.Matrix(matrix)
    return sp.Eq(sp.solve(matrix.det(),z)[0],0)

# Norm of a vector
def Norm(v):
    return sp.simplify(sp.sqrt(v.dot(v)))

#Unit vector
def Unit_Vector(curve):
    return curve/Norm(curve)

#Arc Length
def Arc_Length(curve, a): 
    #a: Um Tuple (variavel, inicio, fim)

    return sp.integrate(Norm(curve.diff(t)),a)

# Tangent Unitary vector
def UT(curve, param=None): 
    if param is None:
        t = sp.symbols('t')
    else:
        t = param
    return curve.diff(t)/Norm(curve.diff(t))

# Normal Unitary Vector
def UN(curve, param=None): 
    if param is None:
        t = sp.symbols('t')
    else:
        t = param
    return (UT(curve).diff(t)/Norm(UT(curve).diff(t))).simplify()

# Binormal Unitary Vector
def UB(curve): return (UT(curve)^UN(curve)).simplify()

# Curvature of a curve
def curvature(curve, param=None, point=None): 
    if param is None:
        t = sp.symbols('t')
    else:
        t = param
    
    if point is None:
        return ((UT(curve).diff(t).magnitude())/(curve.diff(t).magnitude()))
    else:
        return ((UT(curve).diff(t).magnitude())/(curve.diff(t).magnitude())).subs(t, point)

# Torsion of a curve
def torsion(curve , param=None): 
    # t: is the parameter of the curve

    if param is None:
        t = sp.symbols('t')
    else:
        t = param

    return ((curve.diff(t).cross(curve.diff(t,2))).dot(curve.diff(t,3))/Norm(curve.diff(t).cross(curve.diff(t,2))))

#Integral of a parametric curve accepting the boundary condition to determine the constant of integration
def integral_curve(curve,var, ics=None):
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
    - Arguments:
        `field`: Scalar field F(x,y,z). 
        `curve`: one or a list of parametrized curve r(t) = x(t)i + y(t)j + z(t)k
        `a`: a tuple or a list of tuples each one as (parameter of the curve, initial point, final point
        Note: if the field is tridimensional, the curve also must have the same dimension. 
    - Return:
        line integral of the scalar filed along the curve(s) for the given interval(s). 

    ===================
    Example:
        import sympy as sp
        import av_utils as av
        x,y,z = sp.symbols('x y z')
        def field(x,y,z):
            return z**2 +x +y
        l = av.lines([(1,2,3), (3,4,5),(5,6,7)])
        av.line_integral_scalar(z, curve=l, a=(t,0,3)) # one interval for all curves
        av.line_integral_scalar(z, curve=l, a=((t,0,3),(t,0,1))) #one interval for each curve
    '''    

    if isinstance(curve, Iterable):
        if not isinstance(a[0], Iterable):
            a = len(curve)*(a,)
        else:
            assert len(a) == len(curve), 'the number of intervals must be the same as the curves'
    else:
        curve = [curve]
        a = [a]

    #getting the name of the coordinate system of the curve.
    R = list(curve[0].separate().keys())[0]

    #getting the parameters of the field
    param_field = [p for p in field.free_symbols if not p.is_Vector]

    integral = 0
    for item,var in zip(curve,a):
        field_tmp = field
        param_curve = [p for p in item.free_symbols if not p.is_Vector]
        assert len(param_curve)==1, "A curve has only one parameter"
        assert param_curve[0].name==var[0].name, "the parameter of the curve must be the same as the integration variable."
        rx,ry,rz = item.dot(R.i),item.dot(R.j),item.dot(R.k)
        
        # parametrizing the field using the curve parametric equation
        # parametrizing the field using the curve equation
        for par in param_field:
            if par.name == 'x':
                field_tmp = field_tmp.subs(par, rx)
            elif par.name == 'y':
                field_tmp = field_tmp.subs(par, ry)
            elif par.name == 'z':
                field_tmp = field_tmp.subs(par, rz)      

        module = item.diff().magnitude().simplify()
            
    
        integrand = (field_tmp*module).simplify()
        integral += sp.integrate(integrand,(param_curve[0], var[1],var[2])).evalf()
        
    return integral

#Line integral for a vectorial field
def line_integral_vectorial(field,curve,a):
    '''
    - Arguments:
        `field`: Vector field F(x,y,z) = P(x,y,z)i + R(x,y,z)j + Q(x,y,z)k. The parameters of the field must be `x`,`y` and `z`
        `curve`: one or a list of parametrized curves as r(t) = x(t)i + y(t)j + z(t)k
        `a`: one or a list of tuples each one as (parameter of the curve, initial point, final point)
        **Note**: the dimensionality of curve and field must be the same. 
    - Return:
        line integral of the vectorial filed along the curve(s) for the given interval(s). 


    Example:
    =====
    import sympy as sp
    import sympy.vector as sv
    import av_utils as av
    R = sv.CoordSys3D('R')
    t,x,y,z = sp.symbols('t x y z')
    def f(x,y,z):
        x*R.i + y*z*R.j + x*z*R.k

    l = av.lines([(1,2,3), (3,4,5),(5,6,7)])
    
    av.line_integral_vectorial(f(x,y,z), l, (t,-1,2)) # one interval for all curves
    av.line_integral_vectorial(f(x,y,z), l, ((t,-1,2),(t,0,2))) # one interval for each curve
    
    '''

    if isinstance(curve, Iterable):
        if not isinstance(a[0], Iterable):
            a = len(curve)*(a,)
        else:
            assert len(a) == len(curve), 'the number of intervals must be the same as the curves'
    else:
        curve = [curve]
        a = [a]
    
    #getting the name of the coordinate system. Here we assume that the filed and curve are using the same coordinate system
    R = list(curve[0].separate().keys())[0]
    R_f = list(field.separate().keys())[0]
    assert R==R_f, 'the given filed and curve(s) must be in a same coordinate system'
    
    #getting the parameters of the field
    param_field = [p for p in field.free_symbols if not p.is_Vector]

    integral = 0
    for item,var in zip(curve,a):
        field_tmp = field
    
        x_c = item.dot(R.i)
        y_c = item.dot(R.j)
        z_c = item.dot(R.k)

        #getting the parmeter of the curve
        param_curve = [p for p in item.free_symbols if not p.is_Vector]
        assert len(param_curve)==1, "A curve has only one parameter"
        assert param_curve[0].name == var[0].name, "the parameter of the curve must be the same as the integration variable."
        
        # parametrizing the field using the curve equation
        for par in param_field:
            if par.name == 'x':
                field_tmp = field_tmp.subs(par, x_c)
            elif par.name == 'y':
                field_tmp = field_tmp.subs(par, y_c)
            elif par.name == 'z':
                field_tmp = field_tmp.subs(par, z_c)        
        
        integrand = field_tmp.dot(item.diff())
        integral += sp.integrate(integrand,(param_curve[0], var[1],var[2])).evalf()
    
    return integral

# gradient in Cartesian coordinate system
def gradient(func, vars, point=None, coordinate=None):
    """
    - Arguments:
        `func`: A function with 2 or 3 variables in the Cartesian coordinate system (x,y) or (x,y,z). 
        `vars`: variables of the function
        `point`: optional. A point in the plano or space.
        `coordinate`: optional. The name of the coordinate system.
    - Return:
        The gradient of the function
    """
    #vars = (list(sp.ordered(func.free_symbols)))

    if not coordinate:
        R = sv.CoordSys3D('R')
    else:
        R = coordinate
        
    x = [var for var in vars if var.name=='x']
    y = [var for var in vars if var.name=='y']
    z = [var for var in vars if var.name=='z']
        
    if len(x)>0:
        x = x[0]
    else:
        x = sp.symbols('x')
    if len(y)>0:
        y = y[0]
    else:
        y = sp.symbols('y')
    if len(z)>0:
        z = z[0]
    else:
        z = sp.symbols('z')
            
    #if len(vars) == 3: 
    #    grad = func.diff(vars[0])*R.i + func.diff(vars[1])*R.j + func.diff([vars[2]])*R.k
    #if len(vars) == 2:
        
            
    grad = func.diff(x)*R.i + func.diff(y)*R.j + func.diff(z)*R.k
    
    
    if point:
        if len(point)==3:
            grad = grad.subs({x:point[0], y:point[1], z:point[2]})
        else:
            grad = grad.subs({x:point[0], y:point[1]})

    return grad


# Curl in the Cartesian coordinate system   
def curl(func, vars, point=None, coordinate=None):
    """
    - Arguments:
        `func`: A function with 3 variables in the Cartesian coordinate system (x,y,z).
        `vars`: variables of the function
        `point`: optional. A point in the plano or space.
        `coordinate`: optional. The name of the coordinate system.
    - Return:
        The curl of the function
    """
    x = [var for var in vars if var.name=='x']
    y = [var for var in vars if var.name=='y']
    z = [var for var in vars if var.name=='z']

    if len(x)>0:
        x = x[0]
    else:
        x = sp.symbols('x')
    if len(y)>0:
        y = y[0]
    else:
        y = sp.symbols('y')
    if len(z)>0:
        z = z[0]
    else:
        z = sp.symbols('z')
        
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
def divergence(func, vars, point=None, coordinate=None):
    """
    - Arguments:
        `func`: A function with 3 or 3 variables in the Cartesian coordinate system (x,y,z). 
        `vars`: variables of the function
        `point`: optional. A point in the plano or space.
        `coordinate`: optional. The name of the coordinate system.
    - Return:
        The divergent of the function
    """
    x = [var for var in vars if var.name=='x']
    y = [var for var in vars if var.name=='y']
    z = [var for var in vars if var.name=='z']
        
    if len(x)>0:
        x = x[0]
    else:
        x = sp.symbols('x')
    if len(y)>0:
        y = y[0]
    else:
        y = sp.symbols('y')
    if len(z)>0:
        z = z[0]
    else:
        z = sp.symbols('z')
        
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
    - Arguments:
        `func`: uma função no formato de Sympy
        `a`: um tuple (varivel da função, inicio, fim)
    - Return:
        the value of the variable where the function has its minimum inside the interval.
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

def halley(func, var, x0=0, epochs = 500, tol=1e-5, epsilon = 1e-10):
    """
    - Argumentos:
    `func`: o lado esquerdo da equação f(x)=0
    `var`: a variavel da função acima como uma variavel do Sympy
    `x0`: o chute inicial para iniciar a busca
    `epochs`: o numero da iterações para se aproximar a resposta
    `tol` a tolerancia para aproximação da resposta
    `epsilon`: zero numerico. 
    - Return:
    `x`: uma das raizes da função.
    """
    df = func.diff(var)
    ddf = df.diff(var)
    
    f_numpy = sp.lambdify(var,func,'numpy')
    df_numpy = sp.lambdify(var,df, 'numpy')
    ddf_numpy = sp.lambdify(var,ddf, 'numpy')
    
    x = x0
    for i in range(epochs):
        nom = 2*f_numpy(x)*df_numpy(x)
        denom = 2*df_numpy(x)**2 - f_numpy(x)*ddf_numpy(x)
        if abs(denom) < epsilon:
            x = False
            #it's better to raise an Exception than returning False 
            raise Exception('Divisão por zero')
            #return x
        
        x_tmp = nom/denom
        
        if abs(x_tmp)<tol:
            return x
        
        x -= x_tmp 
        
    return float(x)

# constructing the parametric equation of a line using two points
def line(a,b, coordinate=None):
    """
    - Arguments:
        `a`: the inicial point, for example (1,2,3) or (1,2)
        `b`: the final point, for example (1,2,3) or (1,2)
        `coordinate`: optional. a coordinate system object of sympy.vector.CoordSys3D 
    - Return:
        a sympy.vector object
    
    =======
    Example:
    line((1,2),(3,4))
    """
    t= sp.symbols('t', real=True)
    if not coordinate:
        R = sv.CoordSys3D('R')
    else:
        R = coordinate
    assert len(a)==len(b), 'the points must have the same dimension'

    if len(a)==3:
        x = (b[0] - a[0])*t + a[0]
        y = (b[1] - a[1])*t + a[1]
        z = (b[2] - a[2])*t + a[2]
        return x*R.i + y*R.j + z*R.k
    elif len(a)==2:
        x = (b[0] - a[0])*t + a[0]
        y = (b[1] - a[1])*t + a[1]
        return x*R.i + y*R.j

# constructing a list of lines that connect a list of points
def lines(points, coordinate=None):
    """
    - Arguments:
        `points`: a list of points in two or three dimensions
    - Return:
        a list of connecting lines of the points

    ==========
    Example:
    import sympy as sp
    import sympy.vector as sv
    R = sv.CoordSys3D('R')
    lines([(1,2,3),(4,5,6),(-1,-1,0)], coordinate=R)    """

    assert all([len(i)==len(points[0]) for i in points]), 'all the points must have the same dimension'

    lins=[]
    i = 0
    while i<(len(points))-1:
        lins.append(line(points[i],points[i+1], coordinate=coordinate))
        i+=1
    return lins

    
# change the variables from Cartesian to polar coordinate system
def cartesian_to_polar(func):
    r, theta = sp.symbols('r theta')
    params = [p for p in func.free_symbols if not p.is_Vector]

    for var in params:
        
        if var.name =='x':
            func = func.subs(var, r*sp.cos(theta))
        if var.name == 'y':
            func = func.subs(var,r*sp.sin(theta))
    return func.simplify()


# Integration by Riemannian Sum
def riemann_sum(func,a,b,N,method='midpoint'):
    '''Compute the Riemann sum of f(x) over the interval [a,b].
    
    Credit to: https://www.math.ubc.ca/~pwalls/math-python/integration/riemann-sums/
    
    Parameters
    ----------
    `func` : function
        Vectorized function of one variable
    `a` , `b` : numbers
        Endpoints of the interval [a,b]
    `N` : integer
        Number of subintervals of equal length in the partition of [a,b]
    `method` : string
        Determines the kind of Riemann sum:
        `right` : Riemann sum using right endpoints
        `left` : Riemann sum using left endpoints
        `midpoint` (default) : Riemann sum using midpoints

    Returns
    -------
    float
        Approximation of the integral given by the Riemann sum.
    '''
    a, b = float(a), float(b)
    dx = (b - a)/N
    x = np.linspace(a,b,N+1)
    
    var = list(func.free_symbols)[0]
    f_np = sp.lambdify(var, func)

    if method == 'left':
        x_left = x[:-1]
        return np.sum(f_np(x_left)*dx)
    elif method == 'right':
        x_right = x[1:]
        return np.sum(f_np(x_right)*dx)
    elif method == 'midpoint':
        x_mid = (x[:-1] + x[1:])/2
        return np.sum(f_np(x_mid)*dx)
    else:
        raise ValueError("Method must be 'left', 'right' or 'midpoint'.")
