from flask import Flask, render_template, request, jsonify

import plotly.graph_objs as go
import plotly.io as pio

import pickle

import pandas as pd
import numpy as np



with open(r"Part 3 model building/Models/xgb_model.pkl", 'rb') as f:
    xgb_model = pickle.load(f)

df = pd.read_csv(r"EDA Data/EDA.csv")
df.dropna(inplace=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':

        df_model = pd.read_csv(r"Part 3 model building/Model_Data/df_model.csv")

        categorical_cols = ['Fuel','Transmission','Manufacturer' , 'Model']
        numerical_cols = ['Age','Mileage','Horse Power']
        X = df_model[numerical_cols + categorical_cols]


        manufacturer = request.form.get('manufacturer', '')
        model = request.form.get('model', '')
        age = float(request.form.get('age', '0')) 
        mileage = float(request.form.get('mileage', '0'))
        horsepower = float(request.form.get('horsepower', '0')) 
        transmission = request.form.get('transmission', '')
        fuel = request.form.get('fuel', '')

        car_info = {
            'Age': age,
            'Mileage': mileage,
            'Horse Power': horsepower,
                'Fuel': fuel,
                  'Transmission': transmission,
                  'Manufacturer': manufacturer,
                'Model': model,
                }
        new_df = pd.DataFrame(car_info, index=[0])

        X = pd.concat([new_df, X], ignore_index=True)
        X[categorical_cols] = X[categorical_cols].astype('category')

        predicted_price_xgb = xgb_model.predict(X.head(1))
        
        return render_template('prediction.html', prediction_text=f'Predicted Price: TND {predicted_price_xgb}')
  
    return render_template('prediction.html')
    
@app.route("/Understand the Market", methods=['GET'])
def understand_the_market():
    manufacturer_counts = df['Manufacturer'].value_counts().sort_values(ascending=False).head(20)
    
    cars_man = go.Figure(data=[
        go.Bar(
            x=manufacturer_counts.index,
            y=manufacturer_counts.values,
            marker_color=manufacturer_counts.values,
            marker=dict(colorscale='Viridis'),
        )
    ])
    
    cars_man.update_layout(
        title='Top 20 Car Manufacturers Listed for Sale',
        xaxis=dict(title='Manufacturer'),
        yaxis=dict(title='Count'),
        xaxis_tickangle=-45,
        bargap=0.1,
        title_x=0.5,
    )
    cars_man_json = cars_man.to_json()

    return render_template('Understand the Market.html', cars_man_json=cars_man_json)

@app.route("/graphs/cars_by_country_map", methods=['GET'])
def cars_by_country_map():
    return render_template('/graphs/cars_by_country_map.html')


@app.route('/dashboard' )
def graphs():
    return render_template('dashboard.html')  


@app.route('/update_graphs', methods=['POST'])
def update_graphs():
    selected_value = request.form['selected_value']
    updated_data = df[df['Manufacturer'] == selected_value]

    average_age = updated_data['Age'].mean()
    average_mileage = updated_data['Mileage'].mean()
    average_price = updated_data['Price'].mean()
    

    

    top_three_models = updated_data['Model'].value_counts().head(3)
    popular_models_fig = go.Figure(data=[go.Bar(
        x=top_three_models.values, 
        y=top_three_models.index,  
        orientation='h',  
        marker_color='rgb(78, 121, 167)',  
        hoverinfo='x+y',  
    )])

    popular_models_fig.update_layout(
        title=f"Most Popular Models for {selected_value}",
        xaxis_title="Count",
        yaxis_title="Model",
        template="plotly_white",  
        font=dict(family="Arial, sans-serif", size=12, color="black"),  
        margin=dict(l=100, r=50, t=70, b=50),  
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.3,
      
        title_x=0.5,
    )

    popular_models_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    popular_models_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    popular_models_fig_json = popular_models_fig.to_json()

    price_distribution_fig = go.Figure(data=[go.Histogram(
        x=updated_data['Price'],
        marker_color='rgb(78, 121, 167)',
        hoverinfo='x+y',
        xbins=dict(
        size=10000  
    )
    )])

    price_distribution_fig.update_layout(
        title=f"Price Distribution for {selected_value}",
        xaxis_title="Price",
        yaxis_title="Count",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(l=100, r=50, t=70, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
    )

    price_distribution_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    price_distribution_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    age_distribution_fig = go.Figure(data=[go.Histogram(
        x=updated_data['Age'],
        marker_color='rgb(78, 121, 167)',
        hoverinfo='x+y',
        xbins=dict(
        size=1  
    )
    )])

    age_distribution_fig.update_layout(
        title=f"Age Distribution for {selected_value}",
        xaxis_title="Age",
        yaxis_title="Count",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(l=100, r=50, t=70, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
    )

    age_distribution_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    age_distribution_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    mileage_distribution_fig = go.Figure(data=[go.Histogram(
        x=updated_data['Mileage'],
        marker_color='rgb(78, 121, 167)',
        hoverinfo='x+y',
        xbins=dict(
        size=10000  
    )
    )])

    mileage_distribution_fig.update_layout(
        title=f"Mileage Distribution for {selected_value}",
        xaxis_title="Mileage",
        yaxis_title="Count",
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(l=100, r=50, t=70, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
    )

    mileage_distribution_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    mileage_distribution_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')



    trace = go.Scatter(x=updated_data['Age'], y=updated_data['Price'], mode='markers', 
                    marker=dict(color='blue', size=8), name='Price over Age')

    layout = go.Layout(title='Price over Age',
                    xaxis=dict(title='Age'),
                    yaxis=dict(title='Price'))

    price_age_plot = go.Figure(data=[trace], layout=layout)   
    price_age_plot.update_layout(title_x=0.5,)



  
    transmission_counts = updated_data['Transmission'].value_counts()    
    fuel_counts = updated_data['Fuel'].value_counts()

    transmission_trace = go.Pie(labels=transmission_counts.index, values=transmission_counts.values, name='Transmission', hole=0.8)

    transmission_layout = go.Layout(title='Transmission Distribution', margin=dict(l=10, r=10, t=30, b=10))  

    transmission_fig = go.Figure(data=[transmission_trace], layout=transmission_layout)
    transmission_fig.update_layout(title_x=0.5,)

    fuel_trace = go.Pie(labels=fuel_counts.index, values=fuel_counts.values, name='Fuel' , hole=0.8)

    fuel_layout = go.Layout(title='Fuel Distribution', margin=dict(l=10, r=10, t=30, b=10))  

    fuel_fig = go.Figure(data=[fuel_trace], layout=fuel_layout)
    fuel_fig.update_layout(title_x=0.5,)

    transmission_fig_json = transmission_fig.to_json()
    fuel_fig_json = fuel_fig.to_json()
    price_distribution_fig_json = price_distribution_fig.to_json()
    age_distribution_fig_json = age_distribution_fig.to_json()
    mileage_distribution_fig_json = mileage_distribution_fig.to_json()
    price_age_plot_json = price_age_plot.to_json()

    return {
         'average_age': average_age,
        'average_mileage': average_mileage,
        'average_price': average_price,
        'graph1JSON': popular_models_fig_json,
        'graph2JSON': price_distribution_fig_json,
        'graph3JSON': age_distribution_fig_json,
        'graph4JSON': mileage_distribution_fig_json,
        'graph5JSON' : price_age_plot_json,
        'graph6JSON' : transmission_fig_json,
        'graph7JSON' : fuel_fig_json,

        }



if __name__ == '__main__':  
    app.run(host = '0.0.0.0', debug=True)
