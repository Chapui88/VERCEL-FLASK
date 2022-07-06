#from application import app
from flask import render_template, url_for
#from flask import Flask
#from plotly.validators.scatter.marker import SymbolValidator
#import plotly.validators
from plotly.subplots import make_subplots
import pandas as pd 
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go 
import shapefile
import os
import numpy as np
import plotly.io as pio
import pickle

#------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html', title = "Übersicht") 
#------------------------------------------------------------------------------
@app.route('/Klimaauswirkung')
def Klimaauswirkung():
    return render_template('Klimaauswirkung.html', title = "Klimaauswirkung") 
#------------------------------------------------------------------------------
@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html', title = "Kontakt") 


INPUTFOLDER = r'C:\Users\echterhoff\Desktop\FlaskApp\Flask_Tutorial\application\data'
os.chdir(INPUTFOLDER)
#------------------------------------------------------------------------------

# Funktionen
def read_shapefile(shp_path):
	#read file, parse out the records and shapes
	sf = shapefile.Reader(shp_path)
	fields = [x[0] for x in sf.fields][1:]
	records = sf.records()
	shps = [s.points for s in sf.shapes()]
	#write into a dataframe
	df = pd.DataFrame(columns=fields, data=records)
	df = df.assign(coords=shps)
	return df
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Daten für Fig SR - W3
with shapefile.Reader("SR_Kreis_Viersen_Flaeche.shp") as shp:
    geojson_data = shp.__geo_interface__
#------------------------------------------------------------------------------

gdf = read_shapefile('SR_Kreis_Viersen_Flaeche.shp')
#------------------------------------------------------------------------------

gdf['Date_START'] =gdf['Date_START'].str.slice(start=0, stop=16)
gdf['Datum'] =gdf['Date_START'].str.slice(start=0, stop=10)
gdf['Date_END'] =gdf['Date_END'].str.slice(start=0, stop=16)
#gdf['Date_START'] =gdf['Date_START'].str.replace(":00.000", "")

gdf_2 = read_shapefile('SR_Kreis_Viersen_UTM.shp')
gdf_2['lon'] = [x[0] for x in [x[0] for x in gdf_2.coords]]
gdf_2['lat'] = [x[1] for x in [x[0] for x in gdf_2.coords]]

df = gdf[['OBJECTID', 'Datum','Date_START', 'Date_END','Duration','SRImax', 'GMD_RRmax','RRmax', 'RRmean', 'Tmax','Tmean']]
minimum = gdf_2.SRImax.min()
maximum = gdf_2.SRImax.max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Daten für Fig SR - größer T5
with shapefile.Reader("SR_Kreis_Viersen_gr_T5_Flaechen.shp") as shp:
    geojson_data3 = shp.__geo_interface__
#------------------------------------------------------------------------------

gdf3 = read_shapefile('SR_Kreis_Viersen_gr_T5_Flaechen.shp')
#------------------------------------------------------------------------------

gdf3['Date_START'] =gdf3['Date_START'].str.slice(start=0, stop=16)
gdf3['Datum'] =gdf3['Date_START'].str.slice(start=0, stop=10)
gdf3['Date_END'] =gdf3['Date_END'].str.slice(start=0, stop=16)
#gdf['Date_START'] =gdf['Date_START'].str.replace(":00.000", "")

gdf3_2 = read_shapefile('SR_Kreis_Viersen_gr_T5.shp')
gdf3_2['lon'] = [x[0] for x in [x[0] for x in gdf3_2.coords]]
gdf3_2['lat'] = [x[1] for x in [x[0] for x in gdf3_2.coords]]

df3_2 = gdf3[['OBJECTID', 'Datum','Date_START', 'Date_END','Duration','SRImax', 'GMD_RRmax','RRmax', 'RRmean', 'Tmax','Tmean']]
minimum_gdf3_2 = gdf3_2.SRImax.min()
maximum_gdf3_2 = gdf3_2.SRImax.max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Daten für Fig1
with shapefile.Reader("SR_Kreis_Viersen_Hitzetage_geo.shp") as shp:
    geojson_data_1 = shp.__geo_interface__
#------------------------------------------------------------------------------

df_1 = read_shapefile('SR_Kreis_Viersen_Hitzetage.shp')
#------------------------------------------------------------------------------

minimum_1 = df_1.value.min()
maximum_1 = df_1.value.max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Daten für Fig1
with shapefile.Reader("SR_Kreis_Viersen_Hitzetage_geo.shp") as shp:
    geojson_data_1 = shp.__geo_interface__
#------------------------------------------------------------------------------

df_1 = read_shapefile('SR_Kreis_Viersen_Hitzetage.shp')
#------------------------------------------------------------------------------

minimum_1 = df_1.value.min()
maximum_1 = df_1.value.max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Daten für Fig2
with shapefile.Reader("SR_Kreis_Viersen_Hitzetage_lang_geo.shp") as shp:
    geojson_data_2 = shp.__geo_interface__
#------------------------------------------------------------------------------

df_2 = read_shapefile('SR_Kreis_Viersen_Hitzetage_lang.shp')
#------------------------------------------------------------------------------

#df_1 = df_1[df_1.color != -999]
minimum_2 = df_1.value.min()
maximum_2 = df_1.value.max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Daten für Fig3
df_3 = pd.read_csv('Wetterdaten_Station_2_1.csv', encoding = "iso-8859-1", sep=",")


df_3['Datum'] =  pd.to_datetime(df_3['Datum'], format="%Y-%m-%d")

df_3['Datum'].min().year
df_3['Datum'].max().year

period= (df_3['Datum'].max() - df_3['Datum'].min()).days/365*12
timeseries = pd.date_range(str(df_3['Datum'].min().year),  periods=period, freq="MS").to_frame()
timeseries.columns = ['Datum']

df_3 = pd.merge(timeseries, df_3, how='left', left_on='Datum', right_on='Datum')


maximum_3 = df_3['MO_TT'].max()
df_3.replace(-999, np.inf, inplace=True)
minimum_3 = df_3['MO_TT'].min()
minimum_3_y = df_3[['Datum']].min()
maximum_3_y = df_3['Datum'].max()

df_3.loc[df_3['STATIONS_ID'] ==  15963, 'STATIONS_ID'] = 'St. Tönies'
df_3.loc[df_3['STATIONS_ID'] ==  5064, 'STATIONS_ID'] = 'Tönisvorst'

#MO_TN	Monatsmittel des Lufttemperatur Minimums
#MO_TX	Monatsmittel des Lufttemperatur Maximums
#MO_TT	Monatsmittel der Lufttemperatur in 2m Hoehe
df_3 = df_3.sort_values(by=['Datum'])

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_6 = pd.read_csv('Pegel_Boisheim.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_601 = pd.read_csv('Pegel_Boisheim_raw.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_61 = pd.read_csv('Pegel_Oedt.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_611 = pd.read_csv('Pegel_Oedt_raw.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_62 = pd.read_csv('Pegel_Pannenmuehle.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_621 = pd.read_csv('Pegel_Pannenmuehle_raw.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_63 = pd.read_csv('Pegel_Langenfeld.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_631 = pd.read_csv('Pegel_Langenfeld_raw.csv', encoding = "iso-8859-1", sep=";", decimal=",")

#df_6 = px.data.gapminder()
#------------------------------------------------------------------------------
df_5 = df_3.copy()
df_5.replace(np.nan, np.inf, inplace=True)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_sklearn4 = df_3.copy()
# Diese Schritte sollten alle in der Preparation stattfinden!!!
# Gerade um Jare mit fehlerhaften Daten nciht zu berücksichtigen
df_sklearn5 = df_sklearn4[['Jahr', 'Jahreszeit', 'Anomalie_Jahreszeit_MO_TT']].groupby(['Jahr', 'Jahreszeit']).mean().reset_index()
df_sklearn6 = df_sklearn4.groupby(['Jahr']).mean().reset_index()
df_sklearn6 = df_sklearn6.loc[df_sklearn6['Jahr'] !=  1952]
#------------------------------------------------------------------------------
df_sklearn7 =  df_sklearn4[['Jahr', 'Jahreszeit', 'MO_RR']].groupby(['Jahr', 'Jahreszeit']).sum().reset_index()
df_sklearn7 = df_sklearn7.loc[df_sklearn7['Jahr'] !=  1952]
df_sklearn7 = df_sklearn7.loc[df_sklearn7['Jahr'] !=  1953]

df_sklearn8 = df_sklearn7[['Jahr', 'MO_RR']].groupby(['Jahr']).sum().reset_index()

df_sklearn9 =  df_sklearn4[['Jahr', 'Trendlinie_MO_RR_Jahr']].groupby(['Jahr']).mean().reset_index()
df_sklearn9 = df_sklearn9.loc[df_sklearn9['Jahr'] !=  1952]
df_sklearn9 = df_sklearn9.loc[df_sklearn9['Jahr'] !=  1953]

minimum_df_sk_6 = df_sklearn6[['MO_TT']].min()
maximum_df_sk_6 = df_sklearn6['MO_TT'].max()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_7 = pd.read_csv('Duerreindex.csv',)
poly_json = pickle.load(open('poly_json_duerre', 'rb'))
minimum_7 = df_7.color.min()
maximum_7 = df_7.color.max()
df_7.rename(columns={df_7.columns[0]: "index" }, inplace = True)
#------------------------------------------------------------------------------
colorscale_blue_red = ['rgb(5,48,97)', 'rgb(33,102,172)', 'rgb(67,147,195)', 'rgb(214,96,77)', 'rgb(178,24,43)', 'rgb(103,0,31)']
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

df_4 = pd.read_csv('Wetterdaten_Station_3_1.csv', encoding = "iso-8859-1", sep=",")

df_4_1 =df_4.groupby('Jahr').mean().reset_index()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

df_5_1 = pd.read_csv('Wetterdaten_Station_4_1.csv', encoding = "iso-8859-1", sep=",")
#------------------------------------------------------------------------------

dfd1_2_1_x = df_5_1[['Jahr', 'Jahreszeit', ' RSK']].loc[df_5_1[' RSK'] < 1 ]
dfd1_2_1_x[' RSK'] = dfd1_2_1_x[' RSK']/dfd1_2_1_x[' RSK']
df_5_1_2 = dfd1_2_1_x.groupby(['Jahreszeit', 'Jahr']).sum().reset_index()
df_5_1_2 = df_5_1_2.loc[df_5_1_2['Jahr']!= 2022]
#------------------------------------------------------------------------------


df_5_1 = df_5_1.loc[df_5_1['Jahreszeit'] == 'Fruehling']
df_5_1 = df_5_1.loc[df_5_1[' TNK'] < 0]

df_5_1 = df_5_1.groupby('Jahr').last().reset_index()

df_5_1['Datum'] = pd.to_datetime(df_5_1['Datum'], format="%Y-%m-%d")

df_5_1['letzter Frosttag'] = (((df_5_1['Datum'] - df_5_1['Datum'].apply(lambda dt: dt.replace(day=1)).apply(lambda dt: dt.replace(month=1))) / np.timedelta64(1, 'D'))).astype(int)
#------------------------------------------------------------------------------

df_5_1_1 = pd.read_csv('Wetterdaten_Station_8_1.csv', encoding = "iso-8859-1", sep=",")

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_6_1 = pd.read_csv('Wetterdaten_raster_SR_1.csv', encoding = "iso-8859-1", sep=",")
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_7_1 = pd.read_csv('Wetterdaten_Station_5_1.csv', encoding = "iso-8859-1", sep=",")
df_7_1 = df_7_1.loc[df_7_1['Jahr']>= 1985]

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_8_1 = pd.read_csv('Wetterdaten_Station_6_1.csv', encoding = "iso-8859-1", sep=",")
df_8_1 = df_8_1.loc[df_8_1['Jahr']>= 1985]
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_9_1 = pd.read_csv('Wetterdaten_Station_7_1.csv', encoding = "iso-8859-1", sep=",")
df_9_1 = df_9_1.loc[df_9_1['Jahr']>= 1985]
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_10_1 = pd.read_csv('Wetterdaten_Station_10_1.csv', encoding = "iso-8859-1", sep=",")
df_10_1 = df_10_1.loc[df_10_1['Jahr']>= 1985]

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
df_11 = pd.read_csv('Grundwasser.csv', encoding = "iso-8859-1", sep=";", decimal=",")
df_11['Datum'] = pd.to_datetime(df_11['Datum'], format="%d.%m.%Y")

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#INPUTFOLDER = r'C:\Users\echterhoff\Desktop\FlaskApp\Flask_Tutorial\application\data'
#os.chdir(INPUTFOLDER)
#
#FILENAME = 'Crops'
#df_dict_erg = pickle.load(open(FILENAME, 'rb'))
#
#path = r'C:\Users\echterhoff\Desktop\Geodaten\Kreis Viersen\DWD\Crops\Plots'
#os.chdir(path)
#for key,val in df_dict_erg.items():
#    exec(key + '=val')
##    print("'"+key+"',")
#    fig_crops = px.scatter(eval(key), x=' Referenzjahr', y=' Jultag', color='Phase', title=key)
#    pio.write_html(fig_crops, file=str(key)+'.html', auto_open=True)    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

  
@app.route("/Klimaentwicklung")
def Klimaentwicklung():
    fig = px.choropleth_mapbox(df, geojson=geojson_data, locations=df.OBJECTID, featureidkey="properties.OBJECTID", color='SRImax',
                           color_continuous_scale="Reds",
                           hover_data = df[['Date_START', 'Date_END','Duration','SRImax', 'GMD_RRmax','RRmax', 'RRmean', 'Tmax','Tmean']],
                           range_color=(minimum, maximum),
                           mapbox_style="carto-positron",
                           zoom=8.5, center = {"lat": 51.3, "lon": 6.3},
                           opacity=0.5,
                           animation_frame ="Datum",
#                           title = 'Starkregenereignisse im Kreis Viersen von 2001 - 2020',
                           labels={'year':'Betrachtungszeitraum', 'locations':'Index','SRImax':'Starkregenindex'},)
    #------------------------------------------------------------------------------
    fig.add_scattermapbox(
    lat = gdf_2.lat,
    lon = gdf_2.lon,
    marker_size=6, 
    marker_color='rgb(255, 64, 64)')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------    

    fig0 = px.choropleth_mapbox(df3_2, geojson=geojson_data3, locations=df3_2.OBJECTID, featureidkey="properties.OBJECTID", color='SRImax',
                           color_continuous_scale="Reds",
                           hover_data = df3_2[['Date_START', 'Date_END','Duration','SRImax', 'GMD_RRmax','RRmax', 'RRmean', 'Tmax','Tmean']],
                           range_color=(minimum_gdf3_2, maximum_gdf3_2),
                           mapbox_style="carto-positron",
                           zoom=8.5, center = {"lat": 51.3, "lon": 6.3},
                           opacity=0.5,
                           animation_frame ="Datum",
#                           title = 'Starkregenereignisse im Kreis Viersen von 2001 - 2020',
                           labels={'year':'Betrachtungszeitraum', 'locations':'Index','SRImax':'Starkregenindex'},)
    #------------------------------------------------------------------------------
    fig0.add_scattermapbox(
    lat = gdf3_2.lat,
    lon = gdf3_2.lon,
    marker_size=6, 
    marker_color='rgb(255, 64, 64)')
    
    graph0JSON = json.dumps(fig0, cls=plotly.utils.PlotlyJSONEncoder)
    
#    pio.write_html(fig0, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------    
    
    
    
    fig1 = px.choropleth_mapbox(data_frame=df_1, geojson=geojson_data_1, locations=df_1['index'], featureidkey="properties.index",
                               color='value',
                               color_continuous_scale="Reds",
                               range_color=(minimum_1, maximum_1),
                               mapbox_style="carto-positron",
                               zoom=8.5, center = {"lat": 51.3, "lon": 6.3},
                               opacity=0.5,
                               animation_frame ="year",
#                               title = 'Entwicklung der Hitzetage im Kreis Viersen von 1961 - 2020 (30-jährige Mittel)',
                               labels={'year':'Betrachtungszeitraum', 'locations':'Index','value':'Anzahl Hitzetage'})



    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
#
    #------------------------------------------------------------------------------
    
    fig2 = px.choropleth_mapbox(data_frame=df_2, geojson=geojson_data_2, locations=df_2['index'], featureidkey="properties.index",
                               color='value',
                               color_continuous_scale="Reds",
                           hover_data = df_2[['year', 'value']],
                               range_color=(minimum_1, maximum_1),
                               mapbox_style="carto-positron",
                               zoom=8.5, center = {"lat": 51.3, "lon": 6.3},
                               opacity=0.5,
                               animation_frame ="year",
#                               title = 'Entwicklung der Hitzetage im Kreis Viersen von 1951 - 2020 (Jahresdurchschnittswerte',
                           labels={'year':'Betrachtungszeitraum', 'locations':'Index','value':'Anzahl Hitzetage'})
    
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
#MO_TN	Monatsmittel des Lufttemperatur Minimums
#MO_TX	Monatsmittel des Lufttemperatur Maximums
#MO_TT	Monatsmittel der Lufttemperatur in 2m Hoehe
    lineplt = go.Figure()
    lineplt.add_trace(go.Scatter(x= df_sklearn6['Jahr'], y = df_sklearn6['MO_TT'],
                        mode='lines+markers',
                        name='Jahresmittelwert der Lufttemperatur - bodennah',
                        visible = False))

    lineplt.add_trace(go.Scatter(x=df_3['Datum'], y = df_3['Trendlinie_MO_TT'],
                        mode='lines',
                        name='Trendlinie'))

    lineplt.add_trace(go.Scatter(
                   x=df_3['Datum'],
                  y=df_3['MO_TT'],
                  mode='lines+markers',
                  name='Monatsmittelwert der Lufttemperatur - bodennah'))

    #------------------------------------------------------------------------------

    updatemenus2 = [
    {'buttons': [
                {
                'method': 'restyle',
                'label': 'Jahresmittel des Lufttemperatur',
                  'visible': True,
                 'args': [{'visible':[False, True, True],}]
                },
                {
                'method': 'restyle',
                'label': 'Monatsmittel der Lufttemperatur',
                  'visible': True,
                 'args': [{'visible':[True, True, False],}]
                },],
    'direction': 'down',
    'showactive': True,}]
    #------------------------------------------------------------------------------

    lineplt = lineplt.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=False,)
    lineplt = lineplt.update_traces( hovertemplate= 'Datum = %{x} <br>' + 'Temperatur = °C%{y:.2f}')
    lineplt = lineplt.update_yaxes(title_text='Temperatur in [°C]')
    lineplt = lineplt.update_traces(line_width=1, marker_size=2)
    #------------------------------------------------------------------------------
    lineplt.update_layout(updatemenus=updatemenus2)
    #------------------------------------------------------------------------------
    lineplt.update_layout(updatemenus=[go.layout.Updatemenu(
                                    x = 0.0,
                                    xanchor = 'left',
                                    y = 1.2,
                                    yanchor = 'top',)])
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #pio.write_html(lineplt, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph3JSON = json.dumps(lineplt, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    MO_TT_RCP85 = df_8_1.filter(regex='MO_TT').filter(regex='RCP8.5')
    MO_TT_RCP45 = df_8_1.filter(regex='MO_TT').filter(regex='RCP4.5')
    MO_TT_RCP26 = df_8_1.filter(regex='MO_TT').filter(regex='RCP2.6')

    
    pro_plot_0 = go.Figure()
    
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Maximum',visible=True))
    
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=True))
        
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'], 
            y = MO_TT_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Maximum',visible=True))
    
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=True))
        
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'], 
            y = MO_TT_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Maximum',visible=True))
    
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'],
            y=MO_TT_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=True))
        
    pro_plot_0.add_trace(go.Scatter(
            x=df_8_1['Jahr'], 
            y = MO_TT_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=True))
    #------------------------------------------------------------------------------    
    pro_plot_0.add_trace(go.Scatter(
            x=df_sklearn6.loc[df_sklearn6['Jahr'] >= 1985]['Jahr'], 
            y = df_sklearn6.loc[df_sklearn6['Jahr'] >= 1985]['MO_TT'],
            mode='lines',
            line_color='rgba(255,27,0,0.8)',
            name='Jahresmittelwert der Lufttemperatur', visible=True))

    #------------------------------------------------------------------------------    
    pro_plot_0 = pro_plot_0.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=True,
                yaxis_showgrid=True,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    pro_plot_0 = pro_plot_0.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Temperatur in [°C] = %{y:.2f}')
    pro_plot_0 = pro_plot_0.update_yaxes(title_text='Temperatur in [°C]')
    #------------------------------------------------------------------------------
#    pro_plot_0.update_layout(legend=dict(orientation="h", yanchor="top",y=1.05,xanchor="left",x=0.01, bgcolor= 'rgba(0,0,0,0)'))
    pro_plot_0.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
#    pio.write_html(pro_plot_0, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph14JSON = json.dumps(pro_plot_0, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------   
    barplt1 = go.Figure()
    
  
    barplt1.add_trace(go.Bar(
                   x=df_3['Datum'],
                   y=df_3['MO_RR'],
                   name='Monatliche Niederschlagssummen',visible=False,  marker_color="blue"))
    
    
    barplt1.add_trace(go.Scatter(x=df_3['Datum'], 
                                 y = df_3['Trendlinie_MO_RR_Monat'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))
  
    barplt1.add_trace(go.Scatter(x=df_3['Datum'], 
                                 y = df_3['Trendlinie_MO_RR_ab_1990'],
                                 mode='lines',
                                 name='Trendlinie ab 1990',visible=False))    

    
    
    
    barplt1.add_trace(go.Bar(x=df_sklearn8['Jahr'], 
                                 y = df_sklearn8['MO_RR'],
                                 name='Jährliche Niederschlagssummen',visible=True))
    
    barplt1.add_trace(go.Scatter(x=df_sklearn9['Jahr'], 
                                 y = df_sklearn9['Trendlinie_MO_RR_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=True))
    
    barplt1.add_trace(go.Scatter(x=df_3.loc[df_3['Jahr'] >  1990]['Jahr'].unique(),
                                 y = df_3.loc[df_3['Jahr'] >  1990]['Trendlinie_MO_RR_Jahr_ab_1990'].unique(),
                                 mode='lines',
                                 name='Trendlinie ab 1990',visible=True))





    barplt1.add_trace(go.Bar(x=df_sklearn7['Jahr'].unique(), 
                                 y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Fruehling']['MO_RR'],
                                 name='Frühling',visible=False))
    
    barplt1.add_trace(go.Bar(x=df_sklearn7['Jahr'].unique(),
                                 y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Sommer']['MO_RR'],
                                 name='Sommer',visible=False))

    barplt1.add_trace(go.Bar(x=df_sklearn7['Jahr'].unique(),
                                 y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Herbst']['MO_RR'],
                                 name='Herbst',visible=False))

    barplt1.add_trace(go.Bar(x=df_sklearn7['Jahr'].unique(),
                                 y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Winter']['MO_RR'],
                                 name='Winter',visible=False))
    


    
    
    barplt1.add_trace(go.Scatter(x= df_3[df_3['Trendlinie_MO_RR_Fruehling'].notna()]['Jahr'], 
                                 y = df_3[df_3['Trendlinie_MO_RR_Fruehling'].notna()]['Trendlinie_MO_RR_Fruehling'],
                                 mode='lines',
                                 name='Trendlinie Frühling',visible=False))
        
    barplt1.add_trace(go.Scatter(x= df_3[df_3['Trendlinie_MO_RR_Sommer'].notna()]['Jahr'], 
                                 y = df_3[df_3['Trendlinie_MO_RR_Sommer'].notna()]['Trendlinie_MO_RR_Sommer'],
                                 mode='lines',
                                 name='Trendlinie Sommer',visible=False))
    
    barplt1.add_trace(go.Scatter(x= df_3[df_3['Trendlinie_MO_RR_Herbst'].notna()]['Jahr'], 
                                 y = df_3[df_3['Trendlinie_MO_RR_Herbst'].notna()]['Trendlinie_MO_RR_Herbst'],
                                 mode='lines',
                                 name='Trendlinie Herbst',visible=False))
    
    barplt1.add_trace(go.Scatter(x= df_3[df_3['Trendlinie_MO_RR_Winter'].notna()]['Jahr'], 
                                 y = df_3[df_3['Trendlinie_MO_RR_Winter'].notna()]['Trendlinie_MO_RR_Winter'],
                                 mode='lines',
                                 name='Trendlinie Winter',visible=False))
    #------------------------------------------------------------------------------
    updatemenus4 = [
    {'buttons': [
                {
                'method': 'restyle',
                'label': 'Jahressummen der Niederschlagshöhe',
                  'visible': True,
                 'args': [{'visible':[False, False, False, True, True, True, False, False, False, False, False, False, False, False],}]
                 },
                {
                'method': 'restyle',
                'label': 'Monatssummen der Niederschlagshöhe',
                  'visible': True,
                 'args': [{'visible':[True, True, True, False, False, False, False, False, False, False, False, False, False, False],}]
                },                
                {
                'method': 'restyle',
                'label': 'Saisonale Summen der Niederschlagshöhe',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, True, True, True, True, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Trendlinien der saisonalen Niederschlagshöhe - Frühling',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, True, False, False, False, True, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Trendlinien der saisonalen Niederschlagshöhe - Sommer',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, True, False, False, False, True, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Trendlinien der saisonalen Niederschlagshöhe - Herbst',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, False, False, False, True, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Trendlinien der saisonalen Niederschlagshöhe - Winter',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, False, False, True, False, False, False, True],}]
                },
                ],
    'direction': 'down',
    'showactive': True,}]
    #------------------------------------------------------------------------------
    barplt1 = barplt1.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt1 = barplt1.update_traces( hovertemplate= 'Datum = %{x} <br>' + 'Niederschlag = mm%{y:.2f}')
    barplt1 = barplt1.update_yaxes(title_text='NIederschagshöhe in [mm]')
    #------------------------------------------------------------------------------
    barplt1.update_layout(updatemenus=updatemenus4)
#    barplt1.update_layout(updatemenus=dict(yanchor="top", y=1, xanchor="left", x=1 ))
   
    barplt1.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.225,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    
    barplt1.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    
    #------------------------------------------------------------------------------
    #pio.write_html(barplt1, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph8JSON = json.dumps(barplt1, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    # Sommertage, Heiße Tage, Tropennächte, 
    barplt2 = go.Figure()
    
   
    barplt2.add_trace(go.Bar(
                   x=df_4['Datum'],
                   y=df_4['MO_SOMMERTAGE'],
                   name='Monatliche Anzahl an Sommertagen',visible=True))

    barplt2.add_trace(go.Scatter(x=df_4['Datum'], 
                                 y = df_4['Trendlinie_MO_SOMMERTAGE_MONAT'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=True))    
   
    barplt2.add_trace(go.Bar(
                   x=df_4['Datum'],
                   y=df_4['MO_HEISSE_TAGE'],
                   name='Monatliche Anzahl an Heißen Tagen',visible=False))

    barplt2.add_trace(go.Scatter(x=df_4['Datum'], 
                                 y = df_4['Trendlinie_MO_HEISSE_TAGE_MONAT'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    
    
    barplt2.add_trace(go.Bar(
                   x=df_4['Datum'],
                   y=df_4['MO_TROPENNAECHTE'],
                   name='Monatliche Anzahl an Tropennächten',visible=False))

    barplt2.add_trace(go.Scatter(x=df_4['Datum'], 
                                 y = df_4['Trendlinie_MO_TROPENNAECHTE_MONAT'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))

    barplt2.add_trace(go.Bar(
                   x=df_4['Datum'],
                   y=df_4['MO_FROSTTAGE'],
                   name='Monatliche Anzahl an Frosttagen',visible=False))

    barplt2.add_trace(go.Scatter(x=df_4['Datum'], 
                                 y = df_4['Trendlinie_MO_FROSTTAGE_MONAT'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    
    
    barplt2.add_trace(go.Bar(
                   x=df_4['Datum'],
                   y=df_4['MO_EISTAGE'],
                   name='Monatliche Anzahl an Eistagen',visible=False))

    barplt2.add_trace(go.Scatter(x=df_4['Datum'], 
                                 y = df_4['Trendlinie_MO_EISTAGE_MONAT'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    #------------------------------------------------------------------------------
    updatemenus5 = [
    {'buttons': [
                {
                'method': 'restyle',
                'label': 'Anzahl an Sommertagen',
                  'visible': True,
                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Heißen Tagen',
                  'visible': True,
                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Tropennächten',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Frosttagen',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Eistagen',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True],}]
                },
                ],
    'direction': 'down',
    'showactive': True,}]
    #------------------------------------------------------------------------------
    barplt2 = barplt2.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt2 = barplt2.update_traces( hovertemplate= 'Datum = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    barplt2 = barplt2.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    barplt2.update_layout(updatemenus=updatemenus5)
    
    barplt2.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.225,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
#    barplt1.update_layout(updatemenus=dict(yanchor="top", y=1, xanchor="left", x=1 ))
    barplt2.update_layout(updatemenus=[go.layout.Updatemenu(
                                    x = 0.0,
                                    xanchor = 'left',
                                    y = 1.2,
                                    yanchor = 'top',)])
    #------------------------------------------------------------------------------
    graph9JSON = json.dumps(barplt2, cls=plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    barplt3 = go.Figure()
   
    barplt3.add_trace(go.Bar(
                   x=df_4_1['Jahr'],
                   y=df_4_1['MO_SOMMERTAGE_Jahr_sum'],
                   name='Jährliche Anzahl an Sommertagen',visible=True))

    barplt3.add_trace(go.Scatter(x=df_4_1['Jahr'], 
                                 y = df_4_1['Trendlinie_MO_SOMMERTAGE_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=True))    
   
    barplt3.add_trace(go.Bar(
                   x=df_4_1['Jahr'],
                   y=df_4_1['MO_HEISSE_TAGE_Jahr_sum'],
                   name='Jährliche Anzahl an Heißen Tagen',visible=False))

    barplt3.add_trace(go.Scatter(x=df_4_1['Jahr'], 
                                 y = df_4_1['Trendlinie_MO_HEISSE_TAGE_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    
   
    barplt3.add_trace(go.Bar(
                   x=df_4_1['Jahr'],
                   y=df_4_1['MO_TROPENNAECHTE_Jahr_sum'],
                   name='Jährliche Anzahl an Tropennächten',visible=False))

    barplt3.add_trace(go.Scatter(x=df_4_1['Jahr'], 
                                 y = df_4_1['Trendlinie_MO_TROPENNAECHTE_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))
    
    barplt3.add_trace(go.Bar(
                   x=df_4_1['Jahr'],
                   y=df_4_1['MO_FROSTTAGE_Jahr_sum'],
                   name='Jährliche Anzahl an Frosttagen',visible=False))

    barplt3.add_trace(go.Scatter(x=df_4_1['Jahr'], 
                                 y = df_4_1['Trendlinie_MO_FROSTTAGE_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    
    
    barplt3.add_trace(go.Bar(
                   x=df_4_1['Jahr'],
                   y=df_4_1['MO_EISTAGE_Jahr_sum'],
                   name='Jährliche Anzahl an Eistagen',visible=False))

    barplt3.add_trace(go.Scatter(x=df_4_1['Jahr'], 
                                 y = df_4_1['Trendlinie_MO_EISTAGE_Jahr'],
                                 mode='lines',
                                 name='Trendlinie ab 1952',visible=False))    
    #------------------------------------------------------------------------------
    
    barplt3.add_trace(go.Scatter(x=df_5_1['Jahr'], 
                                 y = df_5_1['letzter Frosttag'],
                                 mode='markers',
                                 name='Letzter Frosttag im Jahr',visible=False))   
    #------------------------------------------------------------------------------

    updatemenus6 = [
    {'buttons': [
                {
                'method': 'restyle',
                'label': 'Anzahl an Sommertagen',
                  'visible': True,
                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Heißen Tagen',
                  'visible': True,
                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Tropennächten',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Frosttagen',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Anzahl an Eistagen',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True, False],}]
                },
                {
                'method': 'restyle',
                'label': 'Letzter Frosttag im Frühling',
                  'visible': True,
                 'args': [{'visible':[False, False, False, False, False, False, False, False, False, False, True],}]
                },                
                ],
    'direction': 'down',
    'showactive': True,}]
    #------------------------------------------------------------------------------
    barplt3 = barplt3.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt3 = barplt3.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    barplt3 = barplt3.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    barplt3.update_layout(updatemenus=updatemenus6)


    barplt3.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.225,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
       
    
    
    barplt3.update_layout(updatemenus=[go.layout.Updatemenu(
                                    x = 0.0,
                                    xanchor = 'left',
                                    y = 1.6,
                                    yanchor = 'top',)])
    #------------------------------------------------------------------------------
#    pio.write_html(barplt3, file='test.html', auto_open=True)
    
    graph10JSON = json.dumps(barplt3, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    MO_TROPENNAECHTE_RCP85 = df_7_1.filter(regex='MO_TROPENNAECHTE').filter(regex='RCP8.5')
    MO_TROPENNAECHTE_RCP45 = df_7_1.filter(regex='MO_TROPENNAECHTE').filter(regex='RCP4.5')
    MO_TROPENNAECHTE_RCP26 = df_7_1.filter(regex='MO_TROPENNAECHTE').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------
    MO_FROSTTAGE_RCP85 = df_7_1.filter(regex='MO_FROSTTAGE').filter(regex='RCP8.5')
    MO_FROSTTAGE_RCP45 = df_7_1.filter(regex='MO_FROSTTAGE').filter(regex='RCP4.5')
    MO_FROSTTAGE_RCP26 = df_7_1.filter(regex='MO_FROSTTAGE').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------
    MO_SOMMERTAGE_RCP85 = df_7_1.filter(regex='MO_SOMMERTAGE').filter(regex='RCP8.5')
    MO_SOMMERTAGE_RCP45 = df_7_1.filter(regex='MO_SOMMERTAGE').filter(regex='RCP4.5')
    MO_SOMMERTAGE_RCP26 = df_7_1.filter(regex='MO_SOMMERTAGE').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------
    MO_HEISSE_TAGE_RCP85 = df_7_1.filter(regex='MO_HEISSE_TAGE').filter(regex='RCP8.5')
    MO_HEISSE_TAGE_RCP45 = df_7_1.filter(regex='MO_HEISSE_TAGE').filter(regex='RCP4.5')
    MO_HEISSE_TAGE_RCP26 = df_7_1.filter(regex='MO_HEISSE_TAGE').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------
    MO_EISTAGE_RCP85 = df_7_1.filter(regex='MO_EISTAGE').filter(regex='RCP8.5')
    MO_EISTAGE_RCP45 = df_7_1.filter(regex='MO_EISTAGE').filter(regex='RCP4.5')
    MO_EISTAGE_RCP26 = df_7_1.filter(regex='MO_EISTAGE').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------    
    
    pro_plot_1 = go.Figure()
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_SOMMERTAGE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Sommertagen',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=True))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=True))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_SOMMERTAGE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=True))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=True))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_SOMMERTAGE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=True))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_SOMMERTAGE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=True))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_SOMMERTAGE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=True))
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_HEISSE_TAGE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Heißen Tagen',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_TROPENNAECHTE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Tropennächten',visible=False))
    #------------------------------------------------------------------------------

    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum', visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite', visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_TROPENNAECHTE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median', visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum', visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite', visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_TROPENNAECHTE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median', visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum', visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_TROPENNAECHTE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite', visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_TROPENNAECHTE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median', visible=False))
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_FROSTTAGE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Frosttagen',visible=False))
    #------------------------------------------------------------------------------

    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_FROSTTAGE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_FROSTTAGE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_FROSTTAGE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_FROSTTAGE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_EISTAGE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Eistagen',visible=False))
    #------------------------------------------------------------------------------

    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_EISTAGE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_EISTAGE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_EISTAGE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_1.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_EISTAGE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))
    #------------------------------------------------------------------------------    
    
    updatemenus_pro_1 = [
        {'buttons': [
                    {
                    'method': 'restyle',
                    'label': 'Sommertage',
                      'visible': True,
                     'args': [{'visible':[True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                         
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Heiße Tage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Tropennächte',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Frosttage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Eistage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True],}]
                    },
                    ],
        'direction': 'down',
        'showactive': True,}]
    
    #------------------------------------------------------------------------------
    pro_plot_1 = pro_plot_1.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    pro_plot_1 = pro_plot_1.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    pro_plot_1 = pro_plot_1.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    pro_plot_1.update_layout(updatemenus=updatemenus_pro_1)
#    pro_plot_1.update_layout(legend=dict(orientation="h", yanchor="top",y=1.05,xanchor="left",x=0.01, bgcolor= 'rgba(0,0,0,0)'))
    pro_plot_1.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
#    pio.write_html(pro_plot_1, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph12JSON = json.dumps(pro_plot_1, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    MO_RR_JAHR_RCP85 = df_9_1.filter(regex='MO_RR_Jahr').filter(regex='RCP8.5')
    MO_RR_JAHR_RCP45 = df_9_1.filter(regex='MO_RR_Jahr').filter(regex='RCP4.5')
    MO_RR_JAHR_RCP26 = df_9_1.filter(regex='MO_RR_Jahr').filter(regex='RCP2.6')
    
    MO_RR_SOMMER_RCP85 = df_9_1.filter(regex='MO_RR_Sommer').filter(regex='RCP8.5')
    MO_RR_SOMMER_RCP45 = df_9_1.filter(regex='MO_RR_Sommer').filter(regex='RCP4.5')
    MO_RR_SOMMER_RCP26 = df_9_1.filter(regex='MO_RR_Sommer').filter(regex='RCP2.6')
    
    MO_RR_WINTER_RCP85 = df_9_1.filter(regex='MO_RR_Winter').filter(regex='RCP8.5')
    MO_RR_WINTER_RCP45 = df_9_1.filter(regex='MO_RR_Winter').filter(regex='RCP4.5')
    MO_RR_WINTER_RCP26 = df_9_1.filter(regex='MO_RR_Winter').filter(regex='RCP2.6')

    pro_plot_3 = go.Figure()
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_sklearn8.loc[df_sklearn8['Jahr'] >= 1985]['Jahr'].unique(),
            y=df_sklearn8.loc[df_sklearn8['Jahr'] >= 1985]['MO_RR'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.8)',
            showlegend=True,
            name='Jährliche Niederschlagssummen',
            visible=True))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum'))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite'))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_JAHR_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median'))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum'))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite'))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_JAHR_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median'))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum'))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_JAHR_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite'))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_JAHR_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median'))
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
                                x=df_sklearn7.loc[df_sklearn7['Jahr'] >= 1985]['Jahr'].unique(),
                                y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Sommer'].loc[df_sklearn7['Jahr'] >=  1985]['MO_RR'],
                                fill=None,
                                mode='lines',
                                line_color='rgba(255,27,0,0.8)',
                                showlegend=True,
                                name='Sommer - Niederschlagssummen',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_SOMMER_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_SOMMER_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_SOMMER_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_SOMMER_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
                                 x=df_sklearn7.loc[df_sklearn7['Jahr'] >= 1985]['Jahr'].unique(),
                                 y = df_sklearn7.loc[df_sklearn7['Jahreszeit'] ==  'Winter'].loc[df_sklearn7['Jahr'] >=  1985]['MO_RR'],
                                 fill=None,
                                 mode='lines',
                                 line_color='rgba(255,27,0,0.8)',
                                 showlegend=True,
                                 name='Winter - Niederschlagssummen',visible=False))
    #------------------------------------------------------------------------------

    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_WINTER_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_WINTER_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=MO_RR_WINTER_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_3.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = MO_RR_WINTER_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))
    #------------------------------------------------------------------------------
    updatemenus_pro_3 = [
        {'buttons': [
                    {
                    'method': 'restyle',
                    'label': 'Jahresniederschlag',
                      'visible': True,
                     'args': [{'visible':[True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                                                             
                                          ],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Sommerniederschlag',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,

                                   
                                          ],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Winterniederschlag',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,

                                                                                  
                                         ],}]},
                     ],
        'direction': 'down',
        'showactive': True,}]
    
    #------------------------------------------------------------------------------
    pro_plot_3 = pro_plot_3.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    pro_plot_3 = pro_plot_3.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Niederschlag in mm = %{y:.2f}')
    pro_plot_3 = pro_plot_3.update_yaxes(title_text='Niederschlag [mm]')
    #------------------------------------------------------------------------------
    pro_plot_3.update_layout(updatemenus=updatemenus_pro_3)
#    pro_plot_3.update_layout(legend=dict(orientation="h", yanchor="top",y=1.05,xanchor="left",x=0.01, bgcolor= 'rgba(0,0,0,0)'))
    pro_plot_3.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
    #pio.write_html(pro_plot_3, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph15JSON = json.dumps(pro_plot_3, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    
    RSK_RCP85 = df_9_1.filter(regex='RSK').filter(regex='RCP8.5')
    RSK_RCP45 = df_9_1.filter(regex='RSK').filter(regex='RCP4.5')
    RSK_RCP26 = df_9_1.filter(regex='RSK').filter(regex='RCP2.6')

    RSK_Fruehling_RCP85 = df_10_1.filter(regex='RSK_Fruehling').filter(regex='RCP8.5')
    RSK_Fruehling_RCP45 = df_10_1.filter(regex='RSK_Fruehling').filter(regex='RCP4.5')
    RSK_Fruehling_RCP26 = df_10_1.filter(regex='RSK_Fruehling').filter(regex='RCP2.6')

    RSK_Sommer_RCP85 = df_10_1.filter(regex='RSK_Sommer').filter(regex='RCP8.5')
    RSK_Sommer_RCP45 = df_10_1.filter(regex='RSK_Sommer').filter(regex='RCP4.5')
    RSK_Sommer_RCP26 = df_10_1.filter(regex='RSK_Sommer').filter(regex='RCP2.6')
    
    RSK_Herbst_RCP85 = df_10_1.filter(regex='RSK_Herbst').filter(regex='RCP8.5')
    RSK_Herbst_RCP45 = df_10_1.filter(regex='RSK_Herbst').filter(regex='RCP4.5')
    RSK_Herbst_RCP26 = df_10_1.filter(regex='RSK_Herbst').filter(regex='RCP2.6')
    
    RSK_Winter_RCP85 = df_10_1.filter(regex='RSK_Winter').filter(regex='RCP8.5')
    RSK_Winter_RCP45 = df_10_1.filter(regex='RSK_Winter').filter(regex='RCP4.5')
    RSK_Winter_RCP26 = df_10_1.filter(regex='RSK_Winter').filter(regex='RCP2.6')
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    pro_plot_4 = go.Figure()
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(x=df_5_1_1.loc[df_5_1_1['Jahr'] >= 1985]['Jahr'],
                         y = df_5_1_1.loc[df_5_1_1['Jahr'] >=  1985][' RSK'],
                        fill=None,
                        mode='lines',
                        line_color='rgba(255,27,0,0.8)',
                        showlegend=True,
                        name='Anzahl an Trockentagen',visible=True))

    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=True))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=True))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = RSK_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=True))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=True))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = RSK_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=True))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'],
            y=RSK_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=True))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_9_1['Jahr'], 
            y = RSK_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=True))
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------    

    pro_plot_4.add_trace(go.Scatter(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Fruehling'].loc[df_5_1_2['Jahr']>= 1985]['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Fruehling'].loc[df_5_1_2['Jahr']>= 1985][' RSK'],
                        fill=None,
                        mode='lines',
                        line_color='rgba(255,27,0,0.8)',
                        showlegend=True,
                        name='Frühling - Anzahl an Trockentagen',
                        visible=False))

    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Fruehling_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Fruehling_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Fruehling_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Fruehling_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    pro_plot_4.add_trace(go.Scatter(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Sommer'].loc[df_5_1_2['Jahr']>= 1985]['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Sommer'].loc[df_5_1_2['Jahr']>= 1985][' RSK'],
                        fill=None,
                        mode='lines',
                        line_color='rgba(255,27,0,0.8)',
                        showlegend=True,
                        name='Frühling - Anzahl an Trockentagen',
                        visible=False))

    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Sommer_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Sommer_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Sommer_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Sommer_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    pro_plot_4.add_trace(go.Scatter(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Herbst'].loc[df_5_1_2['Jahr']>= 1985]['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Herbst'].loc[df_5_1_2['Jahr']>= 1985][' RSK'],
                        fill=None,
                        mode='lines',
                        line_color='rgba(255,27,0,0.8)',
                        showlegend=True,
                        name='Frühling - Anzahl an Trockentagen',
                        visible=False))

    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Herbst_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Herbst_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Herbst_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Herbst_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    pro_plot_4.add_trace(go.Scatter(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Winter'].loc[df_5_1_2['Jahr']>= 1985]['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Winter'].loc[df_5_1_2['Jahr']>= 1985][' RSK'],
                        fill=None,
                        mode='lines',
                        line_color='rgba(255,27,0,0.8)',
                        showlegend=True,
                        name='Frühling - Anzahl an Trockentagen',
                        visible=False))

    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 8.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Winter_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 4.5 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Winter_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=False))
    #------------------------------------------------------------------------------
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='RCP 2.6 - Maximum',visible=False))
    
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'],
            y=RSK_Winter_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=False))
        
    pro_plot_4.add_trace(go.Scatter(
            x=df_10_1['Jahr'], 
            y = RSK_Winter_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=False))    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    updatemenus_pro_4 = [
        {'buttons': [
                    {
                    'method': 'restyle',
                    'label': 'Jahressummen - Trockentage',
                      'visible': True,
                     'args': [{'visible':[True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          ],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Frühling - Trockentage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          ],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Sommer - Trockentage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          ],}]
                    },    
                    {
                    'method': 'restyle',
                    'label': 'Herbst - Trockentage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          ],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Winter - Trockentage',
                      'visible': True,
                     'args': [{'visible':[False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          False,
                                          False, False, False,
                                          False, False, False, 
                                          False, False, False,
                                          
                                          True,
                                          True, True, True,
                                          True, True, True, 
                                          True, True, True,
                                          ],}]
                    },    
                    ],
        'direction': 'down',
        'showactive': True,}]    
    
    #------------------------------------------------------------------------------
    pro_plot_4 = pro_plot_4.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    pro_plot_4 = pro_plot_4.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Trockentagen in d = %{y:.2f}')
    pro_plot_4 = pro_plot_4.update_yaxes(title_text='Anzahl an Trockentagen [d]')
    #------------------------------------------------------------------------------
    pro_plot_4.update_layout(updatemenus=updatemenus_pro_4)
#    pro_plot_4.update_layout(legend=dict(orientation="h", yanchor="top",y=1.05,xanchor="left",x=0.01, bgcolor= 'rgba(0,0,0,0)'))
    pro_plot_4.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
#    pio.write_html(pro_plot_4, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph17JSON = json.dumps(pro_plot_4, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    
    
    
    
    
    
    
    #------------------------------------------------------------------------------
    pro_plot_2 = go.Figure()
    #------------------------------------------------------------------------------    
    pro_plot_2.add_trace(go.Scatter(
            x=df_4_1.loc[df_4_1['Jahr']>= 1985]['Jahr'],
            y=df_4_1.loc[df_4_1['Jahr']>= 1985]['MO_HEISSE_TAGE_Jahr_sum'],
            fill=None,
            mode='lines',
            line_color='rgba(255,27,0,0.5)',
            showlegend=True,
            name=' Anzahl an Heißen Tagen',visible=True))    
    #------------------------------------------------------------------------------
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP85.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Maximum',visible=True))
    
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP85.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,100,80,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 8.5 - Bandbreite',visible=True))
        
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP85.iloc[:,1],
            mode='lines',
            line_color='rgba(0,100,80,1)',
            name='RCP 8.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP45.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Maximum',visible=True))
    
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP45.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(0,176,246,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 4.5 - Bandbreite',visible=True))
        
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP45.iloc[:,1],
            mode='lines',
            line_color='rgba(0,176,246,1)',
            name='RCP 4.5 - Median',visible=True))
    #------------------------------------------------------------------------------
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP26.iloc[:,2],
            fill=None,
            mode='lines',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Maximum',visible=True))
    
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'],
            y=MO_HEISSE_TAGE_RCP26.iloc[:,0],
            fill='tonexty', # fill area between trace0 and trace1
            mode='lines', 
            fillcolor='rgba(231,107,243,0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=True,
            name='RCP 2.6 - Bandbreite',visible=True))
        
    pro_plot_2.add_trace(go.Scatter(
            x=df_7_1['Jahr'], 
            y = MO_HEISSE_TAGE_RCP26.iloc[:,1],
            mode='lines',
            line_color='rgba(231,107,243,1)',
            name='RCP 2.6 - Median',visible=True))
    #------------------------------------------------------------------------------    
    pro_plot_2 = pro_plot_2.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=True,
                yaxis_showgrid=True,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    pro_plot_2 = pro_plot_2.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    pro_plot_2 = pro_plot_2.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    pro_plot_2.update_layout(legend=dict(orientation="h", yanchor="top",y=1.05,xanchor="left",x=0.01, bgcolor= 'rgba(0,0,0,0)'))
    pro_plot_2.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
#              pio.write_html(pro_plot_2, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    graph13JSON = json.dumps(pro_plot_2, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    
    barplt4 = go.Figure(data=go.Bar(
                   x=df_6_1['year'],
                   y=df_6_1['Anzahl_SR_10_mm'],
                   name='Anzahl der Tage mit einem Niederschlag > 10 mm'))

    barplt4.add_trace(go.Scatter(
                   x=df_6_1['year'],
                   y=df_6_1['Trendlinie_Anzahl_SR_10_mm'],
                   name='Trend der Tage mit einem Niederschlag > 10 mm',visible=True))
    
    barplt4.add_trace(go.Bar(
                   x=df_6_1['year'],
                   y=df_6_1['Anzahl_SR_20_mm'],
                   name='Anzahl der Tagen mit einem Niederschlag > 20 mm',visible=False))

    barplt4.add_trace(go.Scatter(
                   x=df_6_1['year'],
                   y=df_6_1['Trendlinie_Anzahl_SR_20_mm'],
                   name='Trend der Tage mit einem Niederschlag > 20 mm',visible=False))
    
    barplt4.add_trace(go.Bar(
                   x=df_6_1['year'],
                   y=df_6_1['Anzahl_SR_30_mm'],
                   name='Anzahl der Tagen mit einem Niederschlag > 30 mm',visible=False))

    barplt4.add_trace(go.Scatter(
                   x=df_6_1['year'],
                   y=df_6_1['Trendlinie_Anzahl_SR_30_mm'],
                   name='Trend der Tage mit einem Niederschlag > 30 mm',visible=False))
    #------------------------------------------------------------------------------

    updatemenus7 = [
        {'buttons': [
                    {
                    'method': 'restyle',
                    'label': 'Anzahl an Tagen mit einem Niederschlag > 10 mm',
                      'visible': True,
                     'args': [{'visible':[True, True, False, False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Anzahl an Tagen mit einem Niederschlag > 20 mm',
                      'visible': True,
                     'args': [{'visible':[False, False, True, True, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Anzahl an Tagen mit einem Niederschlag > 30 mm',
                      'visible': True,
                     'args': [{'visible':[False, False, False, False, True, True],}]
                    },
                    ],
        'direction': 'down',
        'showactive': True,}]
    #------------------------------------------------------------------------------
    barplt4 = barplt4.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt4 = barplt4.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    barplt4 = barplt4.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    barplt4.update_layout(updatemenus=updatemenus7)
    
    barplt4.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.225,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
        
    barplt4.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
   # pio.write_html(barplt4, file='test.html', auto_open=True)
    graph11JSON = json.dumps(barplt4, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    barplt5 = go.Figure()
    
    barplt5.add_trace(go.Bar(
                   x=df_5_1_1['Jahr'],
                   y=df_5_1_1[' RSK'],
                   name='Anzahl an Trockentagen pro Jahr',
                   visible=True))
    #------------------------------------------------------------------------------
    barplt5.add_trace(go.Scatter(
               x=df_5_1_1['Jahr'],
               y=df_5_1_1['Trendlinie_RSK'],
               name='Trend der Trockentagen',
               visible=True))
    #------------------------------------------------------------------------------
    barplt5.add_trace(go.Bar(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Fruehling']['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Fruehling'][' RSK'],
                   name='Frühling - Anzahl an Trockentagen',
                   visible=False))
    #------------------------------------------------------------------------------
    barplt5.add_trace(go.Bar(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Sommer']['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Sommer'][' RSK'],
                   name='Sommer - Anzahl an Trockentagen',
                   visible=False))
    #------------------------------------------------------------------------------
    barplt5.add_trace(go.Bar(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Herbst']['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Herbst'][' RSK'],
                   name='Herbst - Anzahl an Trockentagen',
                   visible=False))
    #------------------------------------------------------------------------------
    barplt5.add_trace(go.Bar(
                   x=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Winter']['Jahr'],
                   y=df_5_1_2.loc[df_5_1_2['Jahreszeit'] == 'Winter'][' RSK'],
                   name='Winter - Anzahl an Trockentagen',
                   visible=False))
    #------------------------------------------------------------------------------
    
    updatemenus8 = [
        {'buttons': [
                    {
                    'method': 'restyle',
                    'label': 'Trockentage - Jahressumme',
                      'visible': True,
                     'args': [{'visible':[True, True, False, False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Trockentage - Summe Frühling',
                      'visible': True,
                     'args': [{'visible':[False, False, True, False, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Trockentage - Summe Sommer',
                      'visible': True,
                     'args': [{'visible':[False, False, False, True, False, False],}]
                    },
                    {
                    'method': 'restyle',
                    'label': 'Trockentage - Summe Herbst',
                      'visible': True,
                     'args': [{'visible':[False, False, False, False, True, False],}]
                    },                    
                    {
                    'method': 'restyle',
                    'label': 'Trockentage - Summe Winter',
                      'visible': True,
                     'args': [{'visible':[False, False, False, False, False, True],}]
                    },],
        'direction': 'down',
        'showactive': True,}]
    #------------------------------------------------------------------------------
    barplt5 = barplt5.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt5 = barplt5.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f}')
    barplt5 = barplt5.update_yaxes(title_text='Anzahl an Tagen [d]')
    #------------------------------------------------------------------------------
    barplt5.update_layout(updatemenus=updatemenus8)
    
    
    barplt5.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.225,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))

    barplt5.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------
#    pio.write_html(barplt5, file='test.html', auto_open=True)
    
    graph16JSON = json.dumps(barplt5, cls=plotly.utils.PlotlyJSONEncoder)
    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    fig4 = px.scatter(df_5, x="Monat", y="MO_TT", animation_frame="Jahr", 
               color="STATIONS_ID",
                range_x=[1,12], range_y=[minimum_3,maximum_3])    
    fig4 = fig4.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                legend=dict(title='Name der Klimamessstation', bgcolor='rgba(255,255,255,0.75)',
                             orientation="h", yanchor="bottom", y=1, xanchor="right", x=1 ,traceorder='normal')) 
    fig4 = fig4.update_yaxes(title_text='Monatsmittel der Lufttemperatur in 2m Hoehe [°C]')
#    pio.write_html(fig4, file='test.html', auto_open=True)
    
    
    
#     markers=True, symbol="STATIONS_ID",
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
#    pio.write_html(fig4, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    x1 = df_sklearn4['Jahr']
    z1 = df_sklearn4['Anomalie_Monat_MO_TT']
    
    x2 = df_sklearn5['Jahr']
    z2 = df_sklearn5['Anomalie_Jahreszeit_MO_TT']
    
    x3 = df_sklearn6['Jahr']
    z3 = df_sklearn6['Anomalie_Jahr_MO_TT']
    #-------------------------------------------------------------------------------

    fig5 = go.Figure(data=go.Heatmap(colorscale = colorscale_blue_red,
                   z=[z1],
                   x=x1,
                   y=[''],
                   hoverongaps = False,
                   colorbar={"title": ' '},
                   showscale=False))
    #-------------------------------------------------------------------------------

    fig5.add_trace(go.Heatmap(colorscale = colorscale_blue_red,
                   z=[z2],
                   x=x2,
                   y=[''],
                   hoverongaps = False, 
                   visible = False,
                   colorbar={"title": ' '},
                   showscale=False))
                   
    #-------------------------------------------------------------------------------

    fig5.add_trace(go.Heatmap(colorscale = colorscale_blue_red,
                   z=[z3],
                   x=x3,
                   y=[''],
                   hoverongaps = False,
                   visible = False,
                   colorbar={"title": ' '},
                   showscale=False))
                   
   
    #-------------------------------------------------------------------------------
    # construct menus
    updatemenus3 = [{'buttons': [{'method': 'restyle',
                                 'label': 'Kalenderjahre',
                                  'visible': True,
                                 'args': [{'visible':[False, False, True],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Jahreszeiten',
                                  'visible': True,
                                 'args': [{'visible':[False, True, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Monate',
                                  'visible': True,
                                 'args': [{'visible':[True, False, False],}]
                                 }],
                    'direction': 'down',
                    'showactive': True,}]
    
    # update layout with buttons, and show the figure
    fig5.update_layout(updatemenus=updatemenus3)
    fig5.update_layout(updatemenus=[go.layout.Updatemenu(
                                    x = 0.0,
                                    xanchor = 'left',
                                    y = 1.2,
                                    yanchor = 'top',)])

    
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    #pio.write_html(scatter7, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    return render_template('Klimaentwicklung.html', title = "AP 1.1", graphJSON=graphJSON, graph0JSON=graph0JSON, graph1JSON=graph1JSON, 
                           graph2JSON=graph2JSON, graph3JSON=graph3JSON, 
                           graph4JSON=graph4JSON, graph5JSON= graph5JSON,   graph8JSON= graph8JSON,
                           graph9JSON= graph9JSON, graph10JSON= graph10JSON, graph11JSON=graph11JSON, graph12JSON=graph12JSON, 
                           graph13JSON=graph13JSON,
                           graph14JSON=graph14JSON, graph15JSON=graph15JSON, graph16JSON=graph16JSON, graph17JSON=graph17JSON
                           )
    
    
  

##------------------------------------------------------------------------------
#------------------------------------------------------------------------------
INPUTFOLDER = r'C:\Users\echterhoff\Desktop\FlaskApp\Flask_Tutorial\application\data'
os.chdir(INPUTFOLDER)


FILENAME = 'Fruits'
df_dict_erg_2 = pickle.load(open(FILENAME, 'rb'))

path = r'C:\Users\echterhoff\Desktop\Geodaten\Kreis Viersen\DWD\Fruits\Plots'
os.chdir(path)

from plotly.colors import n_colors

Apfelfarbe  = n_colors('rgb(136, 250, 5)', 'rgb(5, 250, 144)', 3, colortype='rgb')
Birnenfarbe  = n_colors('rgb(250, 193, 5)', '246, 250, 5', 3, colortype='rgb')
Johannisbeerfarbe  = ('rgb(250, 144, 5)')
Sauerkirschefarbe = 'rgb(242, 12, 204)'
Stachelbeerfarbe  = 'rgb(0, 247, 231)'
Kirschfarbe  = n_colors('rgb(250, 5, 5)', 'rgb(133, 50, 50)', 3, colortype='rgb')

fruchtfarben = Apfelfarbe + Birnenfarbe
fruchtfarben.append(Johannisbeerfarbe)
fruchtfarben.append(Sauerkirschefarbe)
fruchtfarben.append(Stachelbeerfarbe)
fruchtfarben = fruchtfarben +  Kirschfarbe 

filtered_dict = {k:v for (k,v) in df_dict_erg_2.items() if "2020" in k}

##------------------------------------------------------------------------------
#------------------------------------------------------------------------------
                       
@app.route('/Klimafolgen')
def Klimafolgen():
    

    fig_crops = go.Figure()
    
    count = -1
    for key,val in filtered_dict.items():
        exec(key + '=val')
        count = count + 1
        print(count)
        val['Phase'] = val['Phase'].str.rstrip()
        red_df = val.loc[val['Phase']=='Blüte Beginn']
        
        
        fig_crops.add_trace(go.Scatter(x= red_df[' Referenzjahr'], y = red_df[' Jultag'],
                                mode='markers',
                                name= red_df['Objekt'].iloc[1].rstrip(),
                                marker=dict(color=fruchtfarben[count]),
                                visible = True))
     
    fig_crops.add_trace(go.Scatter(x=df_5_1['Jahr'], 
                                     y = df_5_1['letzter Frosttag'],
                                     mode='lines',
                                     name='Letzter Frosttag im Jahr',visible=True, line=dict(color="#1017e8", width=2)))   
    fig_crops = fig_crops.update_layout(
                    title_x=0.5,
                    plot_bgcolor= 'rgb(255, 255, 255)',
                    xaxis_showgrid=False,
                    yaxis_showgrid=False,
                    hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                    bordercolor= 'whitesmoke'),
                    showlegend=True)
                    
    fig_crops = fig_crops.update_traces( hovertemplate= 'Jahr = %{x} <br>' + 'Letzter Frosttag %{y:.0f}')
    fig_crops = fig_crops.update_yaxes(title_text='letzter Frosttag im Jahr')
    fig_crops = fig_crops.update_traces(line_width=2, marker_size=4)
    
    graph_crops_JSON = json.dumps(fig_crops, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt6, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    fig7 = px.choropleth_mapbox(data_frame=df_7, geojson=poly_json, locations=df_7['index'], 
                               color='color',
                               color_continuous_scale="Reds",
                               range_color=(minimum_7, maximum_7),
                               mapbox_style="carto-positron",
                               zoom=8.0, center = {"lat": 51.3, "lon": 6.3},
                               opacity=0.5,
                               animation_frame ="year",
                               labels={'year':'Betrachtungszeitraum', 'locations':'Index','color':'Bodenfeuchteindex'})
#    pio.write_html(fig7, file='test.html', auto_open=True)
    graph7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    #    fig5 = px.scatter(df_6, x="Monat", y="MO_TT", animation_frame="Jahr", animation_group="STATIONS_ID",
#               size="MO_TX", color="STATIONS_ID", hover_name="STATIONS_ID", facet_col="STATIONS_ID",
#               log_x=True, size_max=45, range_x=[0,12], range_y=[minimum_3,maximum_3])
    barplt6 = make_subplots(specs=[[{'secondary_y': True}]])

    barplt6.add_trace(go.Bar(
                   x=df_6.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_6.groupby('Hydro_Jahr').sum().reset_index()['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=True))

    barplt6.add_trace(go.Scatter(
                   x=df_6.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_6.groupby('Hydro_Jahr').sum().reset_index()['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=True), secondary_y=True)

    barplt6.add_trace(go.Bar(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Fruehling']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt6.add_trace(go.Scatter(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Fruehling']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)
  
    barplt6.add_trace(go.Bar(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Sommer']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt6.add_trace(go.Scatter(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Sommer']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    barplt6.add_trace(go.Bar(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Herbst']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt6.add_trace(go.Scatter(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Herbst']['Summe Ablussdefizite'],
                   mode='markers',
                   name='Abflussdefizit',
                   visible=False), secondary_y=True)
   
    barplt6.add_trace(go.Bar(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Winter']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt6.add_trace(go.Scatter(
                   x=df_6.loc[df_6['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_6.loc[df_6['Jahreszeit'] == 'Winter']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    updatemenus9 = [{'buttons': [{'method': 'restyle',
                                 'label': 'Gesamtjahr',
                                  'visible': True,
                                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Frühling',
                                  'visible': True,
                                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Sommer',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Herbst',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Winter',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True],}]
                                 }
                                
                                ],
                    'direction': 'down',
                    'showactive': True,}]
#    fig6 = px.scatter(df_6, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#               size="pop", color="continent", hover_name="country", facet_col="continent",
#               log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])    
  
    barplt6 = barplt6.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt6 = barplt6.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [d]')
    barplt6 = barplt6.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Abflussdefizit = %{y:.2f} [m³/s]', secondary_y=True)
    
    barplt6 = barplt6.update_yaxes(title_text="Anzahl an Tagen [d]", secondary_y=False)
    barplt6 = barplt6.update_yaxes(title_text="Abflussdefizit [m³/s]", secondary_y=True)    
    #------------------------------------------------------------------------------
    barplt6.update_layout(updatemenus=updatemenus9)

    barplt6.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))


    barplt6.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph6JSON = json.dumps(barplt6, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt6, file='test.html', auto_open=True)
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    barplt601 = go.Figure()

    barplt601.add_trace(go.Scatter(
                   x=df_601['Datum'],
                   y=df_601['Abfluss [m³/s]'],
                   name='Abfluss [m³/s]',
                    mode='lines',
                   visible=True))

    barplt601.add_trace(go.Scatter(
                   x=df_601['Datum'],
                   y=df_601['MNQ'],
                   name='Mittlerer Niedrigwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))

    barplt601.add_trace(go.Scatter(
                   x=df_601['Datum'],
                   y=df_601['MQ'],
                   name='Mittlerer Abfluss [m³/s]',
                   mode='lines',
                   visible=True))
 
    barplt601.add_trace(go.Scatter(
                   x=df_601['Datum'],
                   y=df_601['MHQ'],
                   name='Mittlerer Hochwasserabfluss [m³/s]',
                   mode='lines',
                   visible=False))
   
  
    barplt601 = barplt601.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt601 = barplt601.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [m³/s]')
    
    barplt601 = barplt601.update_yaxes(title_text="Abfluss [m³/s]")
    #------------------------------------------------------------------------------

    barplt601.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.65,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    barplt601.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph601JSON = json.dumps(barplt601, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt601, file='test.html', auto_open=True)    
    
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------    


    barplt61 = make_subplots(specs=[[{'secondary_y': True}]])

    barplt61.add_trace(go.Bar(
                   x=df_61.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_61.groupby('Hydro_Jahr').sum().reset_index()['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=True))

    barplt61.add_trace(go.Scatter(
                   x=df_61.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_61.groupby('Hydro_Jahr').sum().reset_index()['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=True), secondary_y=True)

    barplt61.add_trace(go.Bar(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Fruehling']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt61.add_trace(go.Scatter(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Fruehling']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)
  
    barplt61.add_trace(go.Bar(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Sommer']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt61.add_trace(go.Scatter(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Sommer']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    barplt61.add_trace(go.Bar(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Herbst']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt61.add_trace(go.Scatter(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Herbst']['Summe Ablussdefizite'],
                   mode='markers',
                   name='Abflussdefizit',
                   visible=False), secondary_y=True)
   
    barplt61.add_trace(go.Bar(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Winter']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt61.add_trace(go.Scatter(
                   x=df_61.loc[df_61['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_61.loc[df_61['Jahreszeit'] == 'Winter']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    updatemenus9 = [{'buttons': [{'method': 'restyle',
                                 'label': 'Gesamtjahr',
                                  'visible': True,
                                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Frühling',
                                  'visible': True,
                                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Sommer',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Herbst',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Winter',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True],}]
                                 }
                                
                                ],
                    'direction': 'down',
                    'showactive': True,}]
  
    barplt61 = barplt61.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt61 = barplt61.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [d]')
    barplt61 = barplt61.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Abflussdefizit = %{y:.2f} [m³/s]', secondary_y=True)
    
    barplt61 = barplt61.update_yaxes(title_text="Anzahl an Tagen [d]", secondary_y=False)
    barplt61 = barplt61.update_yaxes(title_text="Abflussdefizit [m³/s]", secondary_y=True)    
    #------------------------------------------------------------------------------
    barplt61.update_layout(updatemenus=updatemenus9)
   
    barplt61.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    barplt61.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph61JSON = json.dumps(barplt61, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt61, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    
    barplt611 = go.Figure()

    barplt611.add_trace(go.Scatter(
                   x=df_611['Datum'],
                   y=df_611['Abfluss [m³/s]'],
                   name='Abfluss [m³/s]',
                    mode='lines',
                   visible=True))

    barplt611.add_trace(go.Scatter(
                   x=df_611['Datum'],
                   y=df_611['MNQ'],
                   name='Mittlerer Niedrigwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))

    barplt611.add_trace(go.Scatter(
                   x=df_611['Datum'],
                   y=df_611['MQ'],
                   name='Mittlerer Abfluss [m³/s]',
                   mode='lines',
                   visible=True))
 
    barplt611.add_trace(go.Scatter(
                   x=df_611['Datum'],
                   y=df_611['MHQ'],
                   name='Mittlerer Hochwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))
   
  
    barplt611 = barplt611.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt611 = barplt611.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [m³/s]')
    
    barplt611 = barplt611.update_yaxes(title_text="Abfluss [m³/s]")
    #------------------------------------------------------------------------------
    barplt611.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.65,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
        
    barplt611.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph611JSON = json.dumps(barplt611, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt611, file='test.html', auto_open=True)    
    
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------    



    barplt62 = make_subplots(specs=[[{'secondary_y': True}]])

    barplt62.add_trace(go.Bar(
                   x=df_62.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_62.groupby('Hydro_Jahr').sum().reset_index()['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=True))

    barplt62.add_trace(go.Scatter(
                   x=df_62.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_62.groupby('Hydro_Jahr').sum().reset_index()['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=True), secondary_y=True)

    barplt62.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt62.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)
  
    barplt62.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt62.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    barplt62.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt62.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Summe Ablussdefizite'],
                   mode='markers',
                   name='Abflussdefizit',
                   visible=False), secondary_y=True)
   
    barplt62.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt62.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    updatemenus9 = [{'buttons': [{'method': 'restyle',
                                 'label': 'Gesamtjahr',
                                  'visible': True,
                                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Frühling',
                                  'visible': True,
                                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Sommer',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Herbst',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Winter',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True],}]
                                 }
                                ],
                    'direction': 'down',
                    'showactive': True,}]

    
    barplt62 = barplt62.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt62 = barplt62.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [d]')
    barplt62 = barplt62.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Abflussdefizit = %{y:.2f} [m³/s]', secondary_y=True)
    
    barplt62 = barplt62.update_yaxes(title_text="Anzahl an Tagen [d]", secondary_y=False)
    barplt62 = barplt62.update_yaxes(title_text="Abflussdefizit [m³/s]", secondary_y=True)    
    #------------------------------------------------------------------------------
    barplt62.update_layout(updatemenus=updatemenus9)
    
    barplt62.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    barplt62.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph62JSON = json.dumps(barplt62, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt62, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------    

    
    barplt621 = go.Figure()

    barplt621.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['Abfluss [m³/s]'],
                   name='Abfluss [m³/s]',
                    mode='lines',
                   visible=True))

    barplt621.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MNQ'],
                   name='Mittlerer Niedrigwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))

    barplt621.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MQ'],
                   name='Mittlerer Abfluss [m³/s]',
                   mode='lines',
                   visible=True))
 
    barplt621.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MHQ'],
                   name='Mittlerer Hochwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))
   
  
    barplt621 = barplt621.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt621 = barplt621.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [m³/s]')
    
    barplt621 = barplt621.update_yaxes(title_text="Abfluss [m³/s]")
    #------------------------------------------------------------------------------
    barplt621.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.65,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    
    barplt621.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph621JSON = json.dumps(barplt621, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt621, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------



    barplt63 = make_subplots(specs=[[{'secondary_y': True}]])

    barplt63.add_trace(go.Bar(
                   x=df_62.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_62.groupby('Hydro_Jahr').sum().reset_index()['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=True))

    barplt63.add_trace(go.Scatter(
                   x=df_62.groupby('Hydro_Jahr').sum().reset_index()['Hydro_Jahr'],
                   y=df_62.groupby('Hydro_Jahr').sum().reset_index()['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=True), secondary_y=True)

    barplt63.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt63.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Fruehling']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)
  
    barplt63.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt63.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Sommer']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    barplt63.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt63.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Herbst']['Summe Ablussdefizite'],
                   mode='markers',
                   name='Abflussdefizit',
                   visible=False), secondary_y=True)
   
    barplt63.add_trace(go.Bar(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Unterschreitungsdauer'],
                   name='Unterschreitungstage',
                   visible=False))

    barplt63.add_trace(go.Scatter(
                   x=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Hydro_Jahr'],
                   y=df_62.loc[df_62['Jahreszeit'] == 'Winter']['Summe Ablussdefizite'],
                   name='Abflussdefizit',
                   mode='markers',
                   visible=False), secondary_y=True)

    updatemenus9 = [{'buttons': [{'method': 'restyle',
                                 'label': 'Gesamtjahr',
                                  'visible': True,
                                 'args': [{'visible':[True, True, False, False, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Frühling',
                                  'visible': True,
                                 'args': [{'visible':[False, False, True, True, False, False, False, False, False, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Sommer',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, True, True, False, False, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Herbst',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, True, True, False, False],}]
                                 },
                                {'method': 'restyle',
                                 'label': 'Winter',
                                  'visible': True,
                                 'args': [{'visible':[False, False, False, False, False, False, False, False, True, True],}]
                                 }
                                ],
                    'direction': 'down',
                    'showactive': True,}]

    
    barplt63 = barplt63.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt63 = barplt63.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [d]')
    barplt63 = barplt63.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Abflussdefizit = %{y:.2f} [m³/s]', secondary_y=True)
    
    barplt63 = barplt63.update_yaxes(title_text="Anzahl an Tagen [d]", secondary_y=False)
    barplt63 = barplt63.update_yaxes(title_text="Abflussdefizit [m³/s]", secondary_y=True)    
    #------------------------------------------------------------------------------
    barplt63.update_layout(updatemenus=updatemenus9)
    
    barplt63.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    
    barplt63.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph63JSON = json.dumps(barplt63, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt62, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------    

    
    barplt631 = go.Figure()

    barplt631.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['Abfluss [m³/s]'],
                   name='Abfluss [m³/s]',
                    mode='lines',
                   visible=True))

    barplt631.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MNQ'],
                   name='Mittlerer Niedrigwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))

    barplt631.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MQ'],
                   name='Mittlerer Abfluss [m³/s]',
                   mode='lines',
                   visible=True))
 
    barplt631.add_trace(go.Scatter(
                   x=df_621['Datum'],
                   y=df_621['MHQ'],
                   name='Mittlerer Hochwasserabfluss [m³/s]',
                   mode='lines',
                   visible=True))
   
  
    barplt631 = barplt631.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    barplt631 = barplt631.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Anzahl an Tagen = %{y:.2f} [m³/s]')
    
    barplt631 = barplt631.update_yaxes(title_text="Abfluss [m³/s]")
    #------------------------------------------------------------------------------
    barplt631.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.65,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    barplt631.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph631JSON = json.dumps(barplt631, cls=plotly.utils.PlotlyJSONEncoder)
    #pio.write_html(barplt631, file='test.html', auto_open=True)    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

    scatter7 = go.Figure()
#    scatter7.add_trace(go.Scatter(
#                   x=df_11.loc[df_11['Messst.-Nr.'] == 28908371]['Datum'],
#                   y=df_11.loc[df_11['Messst.-Nr.'] == 28908371]['Gw-Stand [mNHN]'],
#                   name='Grundwasserstand - Leuther Mühle',
#                   mode='lines',
#                   visible=True))
# 
#    scatter7.add_trace(go.Scatter(
#                   x=df_11.loc[df_11['Messst.-Nr.'] != 28908371]['Datum'],
#                   y=df_11.loc[df_11['Messst.-Nr.'] != 28908371]['Gw-Stand [mNHN]'],
#                   name='Grundwasserstand - Dülken',
#                   mode='lines',
#                   visible=True))
    
    scatter7.add_trace(go.Scatter(
                   x=df_11.loc[df_11['Messst.-Nr.'] == 28908371]['Datum'],
                   y=df_11.loc[df_11['Messst.-Nr.'] == 28908371]['Gw-Stand [mNHN]'],
                   name='Grundwasserstand - Leuther Mühle',
                   mode='lines',
                   visible=True))
  
    scatter7.add_trace(go.Scatter(
                   x=df_11.loc[df_11['Messst.-Nr.'] != 28908371]['Datum'],
                   y=df_11.loc[df_11['Messst.-Nr.'] != 28908371]['Gw-Stand [mNHN]'],
                   name='Grundwasserstand - Dülken',
                   mode='lines',
                   marker_color='rgb(247, 5, 5)',
                   visible=False))

    updatemenus9 = [{'buttons': [
#                                {'method': 'restyle',
#                                 'label': 'Messtelle - Alle',
#                                  'visible': True,
#                                 'args': [{'visible':[True, , False],}]
#                                  },
                                 {'method': 'restyle',
                                 'label': 'Messtelle - Leuther Mühle',
                                  'visible': True,
                                 'args': [{'visible':[True, False],}]
                                  },
                                {'method': 'restyle',
                                 'label': 'Messtelle - Dülken',
                                  'visible': True,
                                 'args': [{'visible':[False, True],}]
                                  }
                                ],
                    'direction': 'down',
                    'showactive': True,}]
  
    scatter7 = scatter7.update_layout(
                title_x=0.5,
                plot_bgcolor= 'rgb(255, 255, 255)',
                xaxis_showgrid=False,
                yaxis_showgrid=False,
                hoverlabel=dict(font_size=10, bgcolor='rgb(0, 0, 0, 0 )',
                bordercolor= 'whitesmoke'),
                showlegend=True,)
    scatter7 = scatter7.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Grundwasserstand = %{y:.2f} [mNHN]')
#    scatter7 = scatter7.update_traces(hovertemplate= 'Jahr = %{x} <br>' + 'Grundwasserstand = %{y:.2f} [mNHN]')
    scatter7 = scatter7.update_yaxes(title_text="Grundwasserstand [mNHN]")    
    #------------------------------------------------------------------------------
    scatter7.update_layout(updatemenus=updatemenus9)
    
    scatter7.update_layout(legend=dict(
    orientation = "h",
    yanchor="bottom",
    y=-0.35,
    xanchor="left",
    x=0.01,
    bgcolor= 'rgba(0,0,0,0)'))
    
    
    scatter7.update_layout(updatemenus=[go.layout.Updatemenu(x = 0.0, xanchor = 'left', y = 1.25, yanchor = 'top',)])
    #------------------------------------------------------------------------------    
    graph71JSON = json.dumps(scatter7, cls=plotly.utils.PlotlyJSONEncoder)

    
    return render_template("Klimafolgen.html", title="Klimafolgen", graph6JSON=graph6JSON, graph7JSON=graph7JSON,
                           graph61JSON=graph61JSON, graph62JSON=graph62JSON,
                           graph601JSON=graph601JSON, graph611JSON=graph611JSON, graph621JSON=graph621JSON,
                           graph63JSON=graph63JSON, 
                           graph631JSON=graph631JSON,
                           graph71JSON=graph71JSON,
                           graph_crops_JSON=graph_crops_JSON)
    
    
