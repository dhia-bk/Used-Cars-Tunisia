from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots

import pickle



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
    df = pd.read_csv(r"EDA Data/EDA.csv")
    df.dropna(inplace=True)
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
    
    df['Posting Date'] = pd.to_datetime(df['Posting Month'] + ' ' + df['Posting Year'].astype(int).astype(str), format='%B %Y')
    
    # Group the data by 'Posting Date' and calculate the median and mean price separately
    grouped_data = df.groupby('Posting Date')['Price'].agg(['median', 'mean']).reset_index()
    
    # Melt the DataFrame to have 'Price Type' as a column
    melted_data = pd.melt(grouped_data, id_vars=['Posting Date'], var_name='Price Type', value_name='Price')
    
    # Create an interactive line plot
    fig = px.line(melted_data, x='Posting Date', y='Price', color='Price Type',
                  title='Median and Mean Price over Posting Date',
                  labels={'Posting Date': 'Date', 'Price': 'Price'},
                  hover_data={'Price': ':.2f TND'},
                  line_shape='spline',
                  )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Posting Date',
        yaxis_title='Price',
        hovermode='x',
        template='plotly_white',
        title_font_size=24,
        title_x=0.5,  # Title centered
    )
    
    # Update legend title
    fig.update_layout(legend_title_text='Price Type')
    price_dis_json = fig.to_json()

    inflation_data = {
        'Posting Date': pd.to_datetime(['Nov-2022', 'Dec-2022', 'Jan-2023', 'Feb-2023', 'Mar-2023', 'Apr-2023', 'May-2023',
                                        'Jun-2023', 'Jul-2023', 'Aug-2023', 'Sep-2023', 'Oct-2023', 'Nov-2023', 'Dec-2023',
                                        'Jan-2024', 'Feb-2024', 'Mar-2024'], format='%b-%Y'),
        'Inflation Rate': [9.8, 10.1, 10.2, 10.4, 10.3, 10.1, 9.6, 9.4, 9.1, 9.2, 8.9, 8.7,
                           8.2, 8.1, 7.8, 7.5, 7.5]
    }
    inflation_df = pd.DataFrame(inflation_data)
    
    # Calculate percent change in median and mean prices
    median_percent_change = grouped_data['median'].pct_change() * 100
    mean_percent_change = grouped_data['mean'].pct_change() * 100
    
    # Create a line plot for percent change in median and mean prices
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=grouped_data['Posting Date'], y=median_percent_change,
                             mode='lines+markers', name='Median Price Change'))
    fig.add_trace(go.Scatter(x=grouped_data['Posting Date'], y=mean_percent_change,
                             mode='lines+markers', name='Mean Price Change'))
    
    # Add inflation rate to the plot
    fig.add_trace(go.Scatter(x=inflation_df['Posting Date'], y=inflation_df['Inflation Rate'],
                             mode='lines', name='Inflation Rate', line=dict(color='black', dash='dash')))
    
    # Update layout
    fig.update_layout(
        title='Percent Change in Median and Mean Prices vs. Inflation Rate',
        xaxis_title='Posting Date',
        yaxis_title='Percent Change / Inflation Rate (%)',
        template='plotly_white',
        legend=dict(x=0.02, y=0.95), 
         title_font_size=24,
        title_x=0.5, 
         
    )

    price_inf_json = fig.to_json()

    grouped_data = df.groupby('Age').agg({'Price': 'mean'}).reset_index()
    
    median_price = df.groupby('Age')['Price'].median().reset_index()
    
    # Create a scatter plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=grouped_data['Age'],
        y=grouped_data['Price'],
        mode='lines+markers',
        marker=dict(color='red', size=8),
        line=dict(color='red', width=2),
        name='Mean Price'
    ))
    
    fig.add_trace(go.Scatter(
        x=median_price['Age'],
        y=median_price['Price'],
        mode='lines+markers',
        marker=dict(color='blue', size=8),
        line=dict(color='blue', width=2),
        name='Median Price'
    ))
    
    # Update layout
    fig.update_layout(
        title='Average and Median Price over Age',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Price'),
        xaxis_tickangle=-45,
        hovermode='closest',
        template='plotly_white',
         title_font_size=24,
        title_x=0.5, 
    )
    mm_price = fig.to_json()

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Distribution of Mileage", "Distribution of Price"))
    
    # Define layout for the subplots
    subplot_layout = {
        'xaxis': dict(title='Mileage', titlefont=dict(size=16), tickfont=dict(size=14)),
        'yaxis': dict(title='Frequency', titlefont=dict(size=16), tickfont=dict(size=14)),
        'bargap': 0.05,
        'plot_bgcolor': 'rgba(255, 255, 255, 0.7)',
        'paper_bgcolor': 'rgba(255, 255, 255, 0.7)',
        'title_font_size': 24,
        'title_x': 0.5
    }
    
    # Add histogram for mileage to subplot 1
    fig.add_trace(
        px.histogram(df, x='Mileage', nbins=20, color_discrete_sequence=['orange']).data[0],
        row=1, col=1
    )
    
    # Add histogram for price to subplot 2
    fig.add_trace(
        px.histogram(df, x='Price', nbins=20, color_discrete_sequence=['blue']).data[0],
        row=1, col=2
    )
    
    # Update subplot layout
    fig.update_layout(subplot_layout)

    pm = fig.to_json()

    fuel_counts = df.groupby('Fuel').size().reset_index(name='count')
    
    fig_fuel = go.Figure(go.Pie(
        labels=fuel_counts['Fuel'],
        values=fuel_counts['count'],
        name='Fuel',
        hole=0.4,
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'], line=dict(color='#ffffff', width=2))
    ))
    fig_fuel.update_layout(
        title_text='Fuel Distribution',
        font=dict(family="Arial, sans-serif", size=14),
        legend=dict(font=dict(family="Arial, sans-serif", size=12)),
        title_font_size=24,
        title_x=0.5,
    )

    fuel = fig_fuel.to_json()

    transmission_counts = df.groupby('Transmission').size().reset_index(name='count')
    
    fig_transmission = go.Figure(go.Pie(
        labels=transmission_counts['Transmission'],
        values=transmission_counts['count'],
        name='Transmission',
        hole=0.4,
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c'], line=dict(color='#ffffff', width=2))
    ))
    fig_transmission.update_layout(
        title_text='Transmission Distribution',
        font=dict(family="Arial, sans-serif", size=14),
        legend=dict(font=dict(family="Arial, sans-serif", size=12)),
        title_font_size=24,
        title_x=0.5,
    )

    trans = fig_transmission.to_json()

    avg_price_transmission = df.groupby('Transmission')['Price'].mean().reset_index()
    
    fig_avg_price_transmission = go.Figure(go.Bar(
        x=avg_price_transmission['Transmission'],
        y=avg_price_transmission['Price'],
        marker=dict(color='#1f77b4'),
        opacity=0.8
    ))
    fig_avg_price_transmission.update_layout(
        title_text='Average Price per Transmission',
        xaxis_title='Transmission',
        yaxis_title='Average Price',
        font=dict(family="Arial, sans-serif", size=14),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        bargap=0.2,
        title_font_size=24,
        title_x=0.5,
    )

    trans_dis = fig_avg_price_transmission.to_json()

    avg_price_fuel = df.groupby('Fuel')['Price'].mean().reset_index()
    
    fig_avg_price_fuel = go.Figure(go.Bar(
        x=avg_price_fuel['Fuel'],
        y=avg_price_fuel['Price'],
        marker=dict(color='#ff7f0e'),
        opacity=0.8
    ))
    fig_avg_price_fuel.update_layout(
        title_text='Average Price per Fuel',
        xaxis_title='Fuel',
        yaxis_title='Average Price',
        font=dict(family="Arial, sans-serif", size=14),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        bargap=0.3,
        title_font_size=24,
        title_x=0.5,
    )

    fuel_dis = fig_avg_price_fuel.to_json()

    return render_template('Understand the Market.html',fuel_dis = fuel_dis, cars_man_json=cars_man_json, price_dis_json=price_dis_json, price_inf_json=price_inf_json, mm_price = mm_price, pm = pm, fuel = fuel, trans = trans, trans_dis= trans_dis)

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
