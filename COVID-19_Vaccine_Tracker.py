
import requests
import pandas as pd
import matplotlib as plt
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

countries = ["USA", "India", "Türkiye"]
def get_country_vaccine_data(country):
    url = f"https://disease.sh/v3/covid-19/vaccine/coverage/countries/{country}"
    data = response.json()
    return data
country_data = {}
for country in countrries:
    country_data[country] = get_country_vaccine_data(country)['timeline']

country_dfs = []
for country, data in country_data.items():
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Total Vaccinations'])
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df['Country'] = country
    country_dfs.append(df)
combined_df = pd.concat(country_dfs)

populations = {
    "USA":331000000,
    "India":1380000000,
    "Türkiye":83000000
}
combined_df['Vaccination Rate'] = combined_df.apply(lambda row:(row['Total Vaccinations']))

plt.figure(figsize=(12,8))
sns.lineplot(data=combined_df, x=combined_df.index, y='Vaccination Rate', hue='Country')
plt.title('COVID-19 Vaccination Rate Over Time by Country')
plt.xlabel('Date')
plt.ylabl('Vaccination Rate(%)')
plt.legend(title='Country')
plt.xticks(rotations=45)
plt.tight_layout()
plt.show()

app = dash.Dash(___name___)
app.layout = html.Div([
    html,H1("COVID-19 Vaccine Tracker"),
    dcc.Graph(id='vaccination-graph'),
    dcc.Dropdown(
        id='country-dropdown'
        options=[{'label': country, 'value': cuntry}for country in countries],
        value=countries,
        multi=True
    )
])

@app.callback(
    Output('vaccination-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graph(selected_countries):
    filtered_df = combined_df[combined_df['Country'].isin(selected_countries)]
    fig = {
        'data': [
            {'x': filtered_df[filtered_df['Country']== country].index,
             'y': filtered_df[filtered_df['Country']== country]['Vaccination Rate'],
             'type': 'line', 'name': country} for country in selected_countries  
        ],
        'layout':{
            'title':'COVID-19 Vaccination Rates Over Time by Country',
            'xaxis':{'title':'Date'},
            'yaxis': {'title': 'Vaccination Rate(%)'}
        }
    }
    return  fig

if __name__ == '__main__':
    app.run_server(debug=True)
    