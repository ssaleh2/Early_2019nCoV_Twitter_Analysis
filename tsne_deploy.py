import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import seaborn as sns

# Bokeh
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column
from bokeh.palettes import all_palettes

# hm = pd.read_csv('hmdf_FINAL_tsne_020420_0.csv').values
embedding = pd.read_csv('embeddings_FINAL_tsne_020420_0.csv')
wuhan_virus = pd.read_csv('2019nCoV_time_w_tweet_text.csv')
wuhan_virus.timestamp_epochs = pd.to_datetime(wuhan_virus.timestamp_epochs)
# embedding = pd.DataFrame(embedding, columns=['x','y'])
# embedding['hue'] = hm.argmax(axis=1)

source = ColumnDataSource(
        data=dict(
            x = embedding.x,
            y = embedding.y,
            colors = [all_palettes['Category10'][10][i] for i in embedding.hue],
            title = wuhan_virus.text,
            day = [x.day for x in wuhan_virus.timestamp_epochs],
            alpha = [0.9] * embedding.shape[0],
            size = [6] * embedding.shape[0]
        )
    )
hover_tsne = HoverTool(names=["wuhan_virus"], tooltips="""
    <div style="margin: 10">
        <div style="margin: 0 auto; width:300px;">
            <span style="font-size: 12px; font-weight: bold;">Tweet:</span>
            <span style="font-size: 12px">@title</span>
            <span style="font-size: 12px; font-weight: bold;">Day:</span>
            <span style="font-size: 12px">@day</span>
        </div>
    </div>
    """)
tools_tsne = [hover_tsne, 'pan', 'wheel_zoom', 'reset']
plot_tsne = figure(plot_width=700, plot_height=700, tools=tools_tsne, title='nCoV-2019 Tweets')
# plot_tsne.axis.visible = False
plot_tsne.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
plot_tsne.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
plot_tsne.grid.visible = False
plot_tsne.circle('x', 'y', size='size', fill_color='colors', 
                 alpha='alpha', line_alpha=0, line_width=0.01, source=source, name="wuhan_virus")

callback = CustomJS(args=dict(source=source), code=
    """
    var data = source.data;
    var f = cb_obj.value
    x = data['x']
    y = data['y']
    colors = data['colors']
    alpha = data['alpha']
    title = data['title']
    day = data['day']
    size = data['size']
    for (i = 0; i < x.length; i++) {
        if (day[i] <= f) {
            alpha[i] = 0.9
            size[i] = 6
        } else {
            alpha[i] = 0.02
            size[i] = 3
        }
    }
    source.change.emit();
    """)

slider = Slider(start=wuhan_virus.timestamp_epochs.min().day, end=wuhan_virus.timestamp_epochs.max().day, value=27, step=1, title="Through January")
slider.js_on_change('value', callback)

layout = column(slider, plot_tsne)
