import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation



def fourier_animation(figure_data, fourier_data, plot_reference=False, handler=None, plot_whole_approximation=False, animation_time=20):
    '''
    Parameters
    ----------
    figure_data : data of the figure
        Axis 0: N points representing the fourier graph
        Axis 1: x and y coordinate
    fourier_data : data of the fourier series
        Axis 0: N number of data points
        Axis 1: number of points from the fourier coefficients
        Axis 2: x and y of "coefficient line"
    handler : svg handler object necessary for the "reference whole plot"
    '''
    t_stop = animation_time                 # length of animation in seconds
    N = figure_data.shape[0]    # number of data points
    frames_per_sec = 25         # frames per second of animation
    plot_speed = int(N / t_stop / frames_per_sec)    
    if plot_speed==0:
        plot_speed = 1 # 0 does not work

    
    def update_lines(num): # Das passiert pro "frame" während der Animation
        num = num * plot_speed
        
        if not plot_whole_approximation:
            graph[0].set_data(figure_data[:num+1,0], figure_data[:num+1,1])
        
        if not fourier_data is None:
            fourier_vector[0].set_data(fourier_data[num,:,0], fourier_data[num,:,1])
        
    
    
    
    
    
    if fourier_data is None:
        fig = plt.figure() # (12,8)
        ax = plt.axes()
    else:
        add_margin = 0.1 # 10% more margin
        x_lim = (np.amin(fourier_data[...,0]), np.amax(fourier_data[...,0]))
        y_lim = (np.amin(fourier_data[...,1]), np.amax(fourier_data[...,1]))
        x_abs, y_abs = x_lim[1]-x_lim[0], y_lim[1]-y_lim[0]
        
        fig = plt.figure(figsize=(10, 10*y_abs/x_abs)) # (12,8)
        
        ax = plt.axes(xlim=(x_lim[0]-x_abs*add_margin, x_lim[1]+x_abs*add_margin),
                      ylim=(y_lim[0]-y_abs*add_margin, y_lim[1]+y_abs*add_margin))
        
        
    ### plot the picture to be approximated ###
    if plot_reference:
        assert not handler is None, "Need svg handler if whole plot should be painted"
        x_whole, y_whole = handler.get_whole_image()
        for i, (x_tmp, y_tmp) in enumerate(zip(x_whole, y_whole)):
            if i==0:
                ax.plot(x_tmp, y_tmp, label="Whole Image")
            else:
                ax.plot(x_tmp, y_tmp, color="tab:blue")
            
            
    if not fourier_data is None:
        fourier_N = fourier_data.shape[1]-1
    else:
        fourier_N = "None"
    
    if plot_whole_approximation:
        #plt.plot(np.real(ret_values), -np.imag(ret_values), label=f"Fourier N = {fourier_N}")
        ax.plot(figure_data[:,0], figure_data[:,1], label=f"Fourier Graph N = {fourier_N}", zorder=2)

    
    if not plot_whole_approximation:
        graph = ax.plot([figure_data[0,0]], [figure_data[0,1]], label=f"Fourier Graph N = {fourier_N}", zorder=2)
    
    if not fourier_data is None:
        fourier_vector = ax.plot(fourier_data[0,:,0], fourier_data[0,:,1], "-o", markersize=3.5,
                                 label=f"Fourier Vector N = {fourier_data.shape[1]-1}", zorder=3)
   
    
    # Creating the Animation object
    animation_obj = animation.FuncAnimation(fig, update_lines, frames=figure_data.shape[0] // plot_speed,
                                            interval=1000 // frames_per_sec, repeat=True, blit=False)
    
    
    ax.set_title(f"Animation - Fourier Series, N = {fourier_N}")
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    
    return animation_obj # Return of the animation object so that animation does not stop



