import colorlover as cl

# ANALYTICS DATA
stopwords = ['i', "i've", 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

speaker_data = {
    'Keanu Reeves' : {
        'image' : 'reeves.jpg', 
        'content' : 'Keanu Charles Reeves, whose first name means "cool breeze over the mountains" in Hawaiian, was born September 2, 1964 in Beirut, Lebanon.'
    }, 
    'Graham Norton' : {
        'image' : 'norton.jpg', 
        'content' : 'Graham Norton was born on April 4, 1963 in County Cork, Ireland as Graham Walker.'
    }, 
    'Unknown': {
        'image' : 'unknown.png', 
        'content' : 'No data'
    }
}


# STYLE DATA
# Colour helpers
def plot_colours(N):
    '''
    Provides a list of N colours to be used for plotting.
    Typically N is the number of traces in the plot. N max is 11.
    Colours are provided by colorlover package (https://plot.ly/ipython-notebooks/color-scales/).
    If N <7 we use sequential colours, else we switch to divergent colour
    set.
    '''
    N = 3 if N < 3 else N
    sequential = 'Blues'
    diverging = 'Spectral'
    if N > 11:
        return None
    scale_type = 'seq' if N < 7 else 'div'
    colours = sequential if N < 7 else diverging

    return cl.scales[str(N)][scale_type][colours]

plot_style = {
    'background' : 'rgb(0, 5, 10)', 
    'font_color' : 'rgb(200, 200, 200)'
}

index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>ePlumbers</title>
        <link rel="icon" href="assets/pipe_icon.png" type="image/png" sizes="16x16">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
        <div>Hackathon Oct 2018</div>
    </body>
</html>
'''