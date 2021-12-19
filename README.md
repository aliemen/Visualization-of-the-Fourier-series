# Visualization of the Fourier series
Here is some Python code that allows you to read in SVG files and approximate their paths using a Fourier series. The Fourier series can be animated and visualized, the function can be output as a two dimensional vector for Desmos and there is a method to output the coefficients as LaTeX code.

Some example videos of the animations can be found under [example_animations](https://github.com/aliemen/Visualization-of-the-Fourier-series/tree/main/example_animations).

# How to use the program
You will need the packages `numpy`, `matplotlib.pyplot`, `matplotlib.animation`, `svgpathtools` and `scipy.optimize`. 
The important settings can be done in the `main` function (file `FourierMain.py`) using the different variables (shortly explained in the code). If you want to read your own image, change the path for the SVG handler, for example `handler = SVG_Handler("images/img13.svg")`. Here `images/img13.svg` is the path relative to the `FourierMain.py` file.

# How to create a usable SVG file
I used [Inkscape](https://inkscape.org/de/) to draw the images. I tested the program with the freehand pen (the result of which can be seen [here](https://www.reddit.com/r/mathmemes/comments/rjvakh/merry_christmas_from_a_complex_fourier_series/), for example) and the Bézier tool. Since the Fourier series at discontinuity points is only (mostly) point convergent and no longer uniformly convergent, one should try to start the new path as close as possible to the end of the old path in the case of several lines. For the same reason, the start and end points of the complete image should be close together.

# What do the internal equations look like?
It is mainly a set of complex polynomials (representations of mostly Bézier curves). These complex polynomials are then parameterized from <img src="https://render.githubusercontent.com/render/math?math=t=0"> to <img src="https://render.githubusercontent.com/render/math?math=t=1">, depending on the setup, to represent a "partial curve". If we concatenates all partial curves together, we have a large parameterization, which can be normalized by means of the method `_get_parameter_func()` in the file `svg_handler.py` again also to a parameterization for <img src="https://render.githubusercontent.com/render/math?math=t\in [0, 1]">. 

## Finding the Fourier coefficients
Once one has the parameterization of the function (which corresponds to the paths of "the image") <img src="https://render.githubusercontent.com/render/math?math=\gamma : [0, 1] \rightarrow \mathbb{C}">, one can integrate over the complete function <img src="https://render.githubusercontent.com/render/math?math=c_k = \int_0^1 \gamma(t) \cdot e^{2\pi i k \cdot t} \,\text{d}t">. Calculating this integral for <img src="https://render.githubusercontent.com/render/math?math=N"> coefficients (<img src="https://render.githubusercontent.com/render/math?math=k = -N, ..., N">), the Fourier series is <img src="https://render.githubusercontent.com/render/math?math=f_N(x) = \sum_{-N}^N c_k e^{2\pi i k t}">, which approximates the path of the SVG file. Based on the representation of the curves in the `svgpathtools` library, the image is now described by the two dimensional path <img src="https://render.githubusercontent.com/render/math?math=g(t) = \left(\begin{array}{l} \text{Re}(f_N(t)) \\ -\text{Im}(f_N(t)) \end{array}\right)"> for <img src="https://render.githubusercontent.com/render/math?math=t\in [0, 1]">.

## Animation of the "Fourier vector"
Sorting all coefficients by their absolute value and then appending the vectors <img src="https://render.githubusercontent.com/render/math?math=g(t)"> for each of the "partial sums <img src="https://render.githubusercontent.com/render/math?math=f_N">" with the newly sorted summands, we have a nice looking path the Fourier series takes to approximate a point. If you do this for every single data point of the graph, all plotted one after the other result in the animation. 
