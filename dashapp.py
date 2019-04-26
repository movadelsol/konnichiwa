# -*- coding: utf-8 -*-
# this: https://qiita.com/OgawaHideyuki/items/6df65fbbc688f52eb82c
# next: https://qiita.com/OgawaHideyuki/items/1eea435b3f7c90375848
import dash  
import dash_core_components as dcc 
import dash_html_components as html  

# 付け加え　外部スタイルシート
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# 付け加え　色
colors = {
    'background': 'limegreen',
    'text': '#7FDBFF'
}

# 付け加え　外部スタイルシート
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style = {'backgroundColor': colors['background']}, # 背景色
    children = [html.H1('Hello Dash', 
    style={
        'textAlign': 'center',    # テキストセンター寄せ
        'color': colors['text'],  # 文字色
    }),
    dcc.Graph(
        id = "first-graph",
        figure = {
        'data': [
            {'x': [1,2,3,4],
            'y':[3,2,4,6],
            'type': 'bar',
            'name': '東京'},
            {'x':[1,2,3,4],
            'y':[2,4,3,2],
            'type': 'bar',
            'name': '大阪'},
            {'x': [1,2,3,4],    # データ２つ足す
            'y':[2,1,4,6],
            'type': 'bar',
            'name': '京都'},
            {'x': [1,2,3,4],
            'y':[1,3,4,7],
            'type': 'bar',
            'name': '福岡'},
        ],
        'layout': {
            'title': 'グラフ1',
            'paper_bgcolor': colors['background'],  # グラフの外の背景色
            'plot_bgcolor': colors['background']    # グラフの中の背景色
        }
        }
    )
])

if __name__=='__main__':
    app.run_server(debug=True)