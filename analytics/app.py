import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Local imports
from constants import stopwords, speaker_data, plot_colours, plot_style

# Norton interviews Keanu video: https://www.youtube.com/watch?v=QItsI9ynzxo

# Pre-processing
# Expect input table to have columns:
# time_ms - milliseconds since start of recording
# word - lower case word spoken at time
# speaker - name of identified speaker
# entity - is the word an identified entity
# e.g. 
# time_ms   word    speaker entity
#   100.0  thing    Joe Bob    NaN

text_df = pd.read_excel('test_data/keanu_timeseries.xlsx')
if text_df.word.iloc[-1] == 'END':
    text_df = text_df.iloc[:-1]

not_stopword = [w not in stopwords for w in text_df.word]
text_no_stopwords = text_df[not_stopword]
# Sorted word count for all people
word_count = text_no_stopwords.groupby('word').count().time_ms
word_count = word_count.sort_values(ascending=False)
# Unsorted word count for each speaker
word_count_by_speaker = text_no_stopwords.groupby(['speaker', 'word']).count().time_ms
# How many speakers
speakers = list(text_df.speaker.unique())

# Audio timeblocks
time_blocks = pd.to_datetime(text_df.time_ms, unit='ms') # Convert time to datetime
time_blocks = pd.Series(index=time_blocks.values).resample('1S').count() # round to 1 second intervals

# Set up plotting parameters
colours = plot_colours(len(speakers))




# Application
app = dash.Dash(__name__) # This will pull css from 'assets' folder
app.css.config.serve_locally = True
app.layout = html.Div([
    # Heading
    html.Div([
        html.Img(src='assets/data-pipe.jpg', className='two columns'), 
        html.H1('ePlumbers - Analytics Dashboard', className='four columns banner-text'),
        html.H4('Select recording for analysis, and interrogate using the supplied visualisations', className='six columns banner-text')
    ], className='banner row'),
    # Analytics panel (two columns)
    html.Div([
        html.Div([
            # Timeline panel
            html.Div([
                html.P('First plot is just a placeholder. It should show the audio trace.'),
                html.P('Audio player works, but I want to find something better looking. Also need to add a drop down to allow selection of audio file.'), 
                html.P('Words can be added to the timeline using the dropdown. Supports search if you type in also.') 
            ]),
            dcc.Graph(id='audio-timeline',
                style={
                    'height': 100
                },
                figure={
                    'data': [
                        go.Bar(
                            x=time_blocks.index,
                            y=[1] * len(time_blocks),
                            marker=dict(
                                color=colours[0],
                                line=dict(
                                    color='rgb(230, 240, 250)',
                                    width=1
                                )
                            ),
                            opacity=0.7,
                            name='audio-trace'                    
                        )
                    ],
                    'layout': go.Layout(
                        plot_bgcolor=plot_style['background'],
                        paper_bgcolor=plot_style['background'],
                        font=dict(color=plot_style['font_color']),
                        yaxis=dict(showticklabels=False),
                        xaxis=dict(tickformat='%M:%S'),
                        margin=dict(
                            l=40, b=40, t=10, r=10
                        ),
                        showlegend=False,
                        barmode='stack',
                        hovermode=False
                    )
                }
            ),
            html.Div([
                html.Audio(
                    id='audio-player', 
                    controls=True, 
                    src='assets/keanu_reeves_interview.mp3', 
                    style=dict(
                        height=50, 
                        display='block'
                    )
                )
            ], 
            style=dict(
                margin=dict(
                    l=40, b=80, t=80, r=10
                )
            )
            ),
            dcc.Dropdown(
                id='word-dropdown', 
                options=[{'label': w, 'value': w} for w in word_count.index], 
                multi=True, 
                style=dict(
                    background='rgb(30, 30, 30)',
                    color='rgb(0, 0, 0)',
                    margin=dict(
                        l=40, b=40, t=80, r=10
                    )
                )
            ),
            html.Div([
                dcc.Graph(id='word-timeline',
                    style={
                        'height': 200
                    },
                    figure={
                        'data': [
                            go.Bar(
                                x=time_blocks.index,
                                y=[0] * len(time_blocks),
                            )
                        ],
                        'layout': go.Layout(
                            plot_bgcolor=plot_style['background'],
                            paper_bgcolor=plot_style['background'],
                            font=dict(color=plot_style['font_color']),
                            yaxis=dict(title='Count', dtick=1),
                            xaxis=dict(tickformat='%M:%S'),
                            margin=dict(
                                l=40, b=60, t=10, r=10
                            ),
                            legend=dict(x=0.9, y=1),
                            barmode='stack',
                            hovermode='closest'
                        )
                    }
                )
            ])
        ], className='six columns'), 
        html.Div([
        # Word frequency panel
            html.Div([
                html.P('This side is meant to be an overview.'),
                html.P('You can hover over the histogram, and details of the speaker will show up.')
            ]),
            # ID Card
            html.Div([
                html.Img(id='card-image', src='', className='two columns', style=dict(height='150px', width='100px')), 
                html.Div([
                    html.H5(id='card-name', children='', className='card-name'), 
                    html.P(id='card-content', children='')
                ])
            ], 
            id='id-card', 
            style=dict(visibility='hidden'), 
            className="card row"
            ),
            # Speaker word histogram
            dcc.Graph(id='word-histogram',
                style={
                    'height': 200
                },
                figure={
                    'data': [
                        go.Bar(
                            x=word_count.index,
                            y=word_count_by_speaker[s][word_count.index],
                            marker=dict(
                                color=colours[speakers.index(s)],
                                line=dict(
                                    color='rgb(230, 230, 230)',
                                    width=1
                                )
                            ),
                            opacity=0.7,
                            name=s                    
                        ) for s in speakers
                    ],
                    'layout': go.Layout(
                        plot_bgcolor=plot_style['background'],
                        paper_bgcolor=plot_style['background'],
                        font=dict(color=plot_style['font_color']),
                        yaxis=dict(title='Count'),
                        xaxis=dict(range=(-1,8)),
                        margin=dict(
                            l=40, b=60, t=10, r=10
                        ),
                        legend=dict(x=1, y=1),
                        barmode='stack',
                        hovermode='closest'
                    )
                }
            )
        ], className='six columns')
    ])
    
])

# WORD SELECTION CALLBACKS
@app.callback(
    Output('word-timeline', 'figure'), 
    [Input('word-dropdown', 'value')]
)
def update_word_timeline(words):
    times = pd.to_datetime(text_df.time_ms, unit='ms') # Convert time to datetime
    times = times.apply(lambda t: t.round('5S')) # round to 5 second intervals
    word_key = text_df.word.apply(lambda w: w in words)
    df = pd.DataFrame({'time': times[word_key], 'word': text_df.word[word_key], 'count': [1] * word_key.sum()}) # need to add dummy 'count' column so groupby works properly
    word_times = df.groupby(['word', 'time']).count()
    word_colours = plot_colours(len(words))
    fig = {
        'data': [
            go.Bar(
                x=word_times.loc[w].index,
                y=word_times.loc[w]['count'],
                marker=dict(
                    color=word_colours[words.index(w)],
                    line=dict(
                        color='rgb(230, 240, 250)',
                        width=1
                    )
                ),
                opacity=0.7,
                name=w                    
            ) for w in words
        ],
        'layout': go.Layout(
            plot_bgcolor=plot_style['background'],
            paper_bgcolor=plot_style['background'],
            font=dict(color=plot_style['font_color']),
            yaxis=dict(title='Count', dtick=1),
            xaxis=dict(tickformat='%M:%S'),
            margin=dict(
                l=40, b=60, t=10, r=10
            ),
            legend=dict(x=0.9, y=1),
            barmode='stack',
            hovermode='closest'
        )
    }
    return fig


# ID CARD CALLBACKS
@app.callback(
    Output('card-image', 'src'), 
    [Input('word-histogram', 'hoverData')]
)
def update_id_card_image(hover_data):
    if hover_data is None:
        return None
    speaker_name = speakers[hover_data['points'][0]['curveNumber']]
    if speaker_name not in speaker_data:
        speaker_name = 'Unknown'
    return 'assets/{}'.format(speaker_data[speaker_name]['image'])

@app.callback(
    Output('card-name', 'children'), 
    [Input('word-histogram', 'hoverData')]
)
def update_id_card_name(hover_data):
    if hover_data is None:
        return None
    return speakers[hover_data['points'][0]['curveNumber']]

@app.callback(
    Output('card-content', 'children'), 
    [Input('word-histogram', 'hoverData')]
)
def update_id_card_content(hover_data):
    if hover_data is None:
        return None
    speaker_name = speakers[hover_data['points'][0]['curveNumber']]
    if speaker_name not in speaker_data:
        speaker_name = 'Unknown'
    return speaker_data[speaker_name]['content']

@app.callback(
    Output('id-card', 'style'), 
    [Input('word-histogram', 'hoverData')]
)
def show_id_card(hover_data):
    if hover_data is None:
        return {'visibility': 'hidden'}
    else:
        return {'visibility': 'visible'}


if __name__ == '__main__':
    app.run_server(debug=True)