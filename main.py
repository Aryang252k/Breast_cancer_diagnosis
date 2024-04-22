from dash import Dash, html, dcc,Input,Output,callback
import plotly.graph_objects as go
import Data
import pickle


# loading model and standard scaler
scaler=pickle.load(open("model/scaler.pkl",'rb'))
model=pickle.load(open("model/model.pkl",'rb'))
mmscaler=pickle.load(open("model/mmscaler.pkl",'rb'))

# slider code
col_names=Data.col_names
sliders = [
    html.Div(children=[
        html.H5(children=[name],className='sd-tit'),  # Title for the slider
        dcc.Slider(
            min=float(0),
            max=Data.Max(col),
            value=round(Data.Mean(col),2),
            step=0.01,
            marks={0:'0',Data.Max(col):f"{Data.Max(col)}"},
            tooltip={
                'always_visible':True
                },
            id=name
        )
    ])for name, col in col_names
]



   

# app code

app = Dash(__name__)
server=app.server 
app.title="Breast Cancer Predictor"

app.layout =  html.Div(children=[
    # Side navigation bar
    html.Div([
        html.Div(children=[
            html.H3("Cell Nuclei Details",className='nav-head'),
            html.Div(sliders)], 
            style={'height': '95vh'},className='nav')

    ], style={'width': '20%', 'display': 'inline-block'},className='main-nav'),
    
    # Main content area
    html.Div([
        # Title row
        html.Div([
            html.H1("Breast Cancer Diagnosis"),  # Title div
            html.P(children=["Please connect the app to your cytology lab to help diagnose breast cancer from your tissue sample. This app predict using a machine learning model whether a breast mass is benign or malignant based on the measurements it receives from your cytosis lab. You can also update the measurements by hand using the slider in the sidebar."])
        ], className='title'),
        
        # Content rows
        html.Div([
            # First column
            html.Div([
                html.Div(style={'height': '470px'},id="graph")
                ], style={'width': '75%', 'display': 'inline-block'}),
            
            # Second column
            html.Div([
                html.Div(children=[
                    html.H2('Cell cluster prediction'),
                    html.H4('The cell cluster is:',style={'margin-top':'5%','margin-bottom':'7%'}),
                    html.Div(id="small-div"),
                    html.H4("Probability of being Benign:",style={'margin-top':'5%','margin-bottom':'7%'}),
                    html.Div(id="prob-b"),
                    html.H4("Probability of being Malignant:",style={'margin-top':'5%','margin-bottom':'7%'}),
                    html.Div(id="prob-m"),
                    html.H5("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.",style={'color':"red"})
                ], style={'height': '525px', 'background-color': '#2CB9A1','padding-left':'6%','border-radius':'10px','padding-top':'6%'})
            ], style={'width': '20%', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center'})
    ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'},className='main')
])




# slider val-update
def radar_graph(vals_dic,categories):

    fig = go.Figure(layout={'paper_bgcolor':'black',
                            'font':{'color':'white','size':16},
                            'polar':{'bgcolor':'black'}
                            })
    

    fig.add_trace(go.Scatterpolar(
      r=[
          vals_dic['Radius (mean)'],vals_dic['Texture (mean)'],vals_dic['Perimeter (mean)'],vals_dic['Area (mean)'],
          vals_dic['Smoothness (mean)'],vals_dic['Compactness (mean)'],vals_dic['Concavity (mean)'],vals_dic['Concave points (mean)'],
          vals_dic['Symmetry (mean)'],vals_dic['Fractal dimension (mean)']
      ],
      theta=categories,
      fill='toself',
      name='Mean values'
     ))
    fig.add_trace(go.Scatterpolar(
      r=[
          vals_dic['Radius (se)'],vals_dic['Texture (se)'],vals_dic['Perimeter (se)'],vals_dic['Area (se)'],
          vals_dic['Smoothness (se)'],vals_dic['Compactness (se)'],vals_dic['Concavity (se)'],vals_dic['Concave points (se)'],
          vals_dic['Symmetry (se)'],vals_dic['Fractal dimension (se)']
      ],
      theta=categories,
      fill='toself',
      name='Standard error'
     ))
    
    fig.add_trace(go.Scatterpolar(
      r=[
          vals_dic['Radius (worst)'],vals_dic['Texture (worst)'],vals_dic['Perimeter (worst)'],vals_dic['Area (worst)'],
          vals_dic['Smoothness (worst)'],vals_dic['Compactness (worst)'],vals_dic['Concavity (worst)'],vals_dic['Concave points (worst)'],
          vals_dic['Symmetry (worst)'],vals_dic['Fractal dimension (worst)']
      ],
      theta=categories,
      fill='toself',
      name='Worst value'
     ))

    fig.update_layout(
      polar=dict(
      radialaxis=dict(
      visible=True,
      range=[0, 1]
    )),
    showlegend=True
     )

    return fig

@app.callback(
    Output("graph",'children'),
    [Input(name,'value') for name,_ in col_names],
        )
def update_slider_value(*values):
    values=[[i for i in values]]
    values=mmscaler.transform(values)
    vals_dic = {k:v for (k,v) in zip([i for i,_ in col_names],[i for i in values[0]])}
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 
                  'Concavity', 'Concave points', 'Symmetry', 'Fractal dimension']
    fig=radar_graph(vals_dic,categories)
    return dcc.Graph(figure=fig,className="graph-set")
    
    

# prediction

@app.callback(
    Output('small-div','children'),
    [Input(name,'value') for name,_ in col_names]
)
def prediction(*values):
     values=[[i for i in values]]
     values=scaler.transform(values)
     pred=model.predict(values)
     if pred[0]==0:
         return html.Div("Benign",id='ben')
     else:
         return html.Div("Malicious",id='mal')
    
# probability
@app.callback(
    Output('prob-b','children'),
    [Input(name,"value") for name,_ in col_names]
)
def probability_banign(*values):
    values=[[i for i in values]]
    values=scaler.transform(values)
    model.predict(values)
    return f"{(model.predict_proba(values)[0][0])*100}"
    

@app.callback(
    Output('prob-m','children'),
    [Input(name,"value") for name,_ in col_names]
)
def probability_banign(*values):
    values=[[i for i in values]]
    values=scaler.transform(values)
    model.predict(values)
    return f"{(model.predict_proba(values)[0][1])*100}"
  



if __name__ == '__main__':
    app.run(debug=True)


