import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../stats/stats.csv')

fig = go.Figure(go.Scatter(x = df['Name'], y = df['@Conditional'],
                  name='Number of @Conditional'))

fig.update_layout(title='Apple Share Prices over time (2014)',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

fig.show()