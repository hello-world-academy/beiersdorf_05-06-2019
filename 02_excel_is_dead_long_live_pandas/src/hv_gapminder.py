import pandas as pd
import numpy as np
import holoviews as hv

#from bokeh.io import curdoc, output_notebook, show
#from bokeh.application import Application
#from bokeh.application.handlers import FunctionHandler

from bokeh.layouts import layout
from bokeh.models import Slider, Button
from holoviews.plotting.bokeh import BokehRenderer


# Load data set 
gapminder_df = pd.read_csv("../data/gapminder.CSV")
# Declare data set
ds = hv.Dataset(gapminder_df)

def gapminder_plot(doc):    
    # Apply dimension labels and ranges
    kdims = ['Fertility', 'Life expectancy']
    vdims = ['Country', 'Population', 'Group']
    dimensions = {
        'Fertility' : dict(label='Children per woman (total fertility)', range=(0, 10)),
        'Life expectancy': dict(label='Life expectancy at birth (years)', range=(15, 100)),
        'Population': ('population', 'Population')
    }
    
    # Create Points plotting fertility vs life expectancy indexed by Year
    gapminder_ds = ds.redim(**dimensions).to(hv.Points, kdims, vdims, 'Year')

    # Define annotations
    text = gapminder_ds.clone({yr: hv.Text(1.2, 25, str(int(yr)), fontsize=30)
                               for yr in gapminder_ds.keys()})

    # Define options
    opts = {'plot': dict(width=950, height=450,tools=['hover'], size_index='Population',
                         color_index='Group', size_fn=np.sqrt, title_format="{label}"),
           'style': dict(cmap='Set1', size=0.3, line_color='black', alpha=0.6)}
    text_opts = {'style': dict(text_font_size='52pt', text_color='lightgray')}

    # Combine Points and Text
    hvgapminder = (gapminder_ds({'Points': opts}) * text({'Text': text_opts})).relabel('Gapminder Demo')

    # Define custom widgets
    def animate_update():
        year = slider.value + 1
        if year > end:
            year = start
        slider.value = year

    # Update the holoviews plot by calling update with the new year.
    def slider_update(attrname, old, new):
        hvplot.update((new,))

    def animate():
        if button.label == '► Play':
            button.label = '❚❚ Pause'
            doc.add_periodic_callback(animate_update, 200)
        else:
            button.label = '► Play'
            doc.remove_periodic_callback(animate_update)

    start, end = ds.range('Year')
    slider = Slider(start=start, end=end, value=start, step=1, title="Year")
    slider.on_change('value', slider_update)

    button = Button(label='► Play', width=60)
    button.on_click(animate)
    
    # Get HoloViews plot
    hvplot = BokehRenderer.get_plot(hvgapminder, doc)
    # Make a bokeh layout and add it as the Document root
    plot = layout([[hvplot.state], [slider, button]], sizing_mode='fixed')
    doc.add_root(plot)
    return doc