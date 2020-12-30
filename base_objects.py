import plotly.express as px


fig = px.scatter(height=1000,
                 width=1600)
fig.update_layout(plot_bgcolor='rgb(180, 180, 180)')

# TODO: consolidate database calls so that tables can be imported (make this a class?)