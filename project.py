'''
Name: Alden Lee
Title: Effects of Lockdown Lifting on Covid Cases in NYC
Email: Alden.lee06@myhunter.cuny.edu
Resources: https://github.com/nychealth/covid-vaccine-data/blob/main/doses/doses-by-day.csv 
https://github.com/nychealth/coronavirus-data/blob/master/totals/data-by-modzcta.csv 
https://github.com/nychealth/coronavirus-data/blob/master/trends/data-by-day.csv 
https://github.com/nychealth/coronavirus-data/blob/master/Geography-resources/MODZCTA_2010_WGS1984.geo.json
https://stackoverflow.com/questions/65888553/fitting-a-line-through-3d-x-y-z-scatter-plot-data 
https://stackoverflow.com/questions/51457738/animating-a-3d-scatterplot-with-matplotlib-to-gif-ends-up-empty
https://stackoverflow.com/questions/60252480/how-to-plot-3d-multiple-linear-regression-with-2-features-using-matplotlib
URL: https://aldenl.github.io/Data-Science-Project/ 

'''

#libraries
from scipy.sparse import data
from sklearn.decomposition import PCA
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import pandasql as psql
import folium
from folium.features import DivIcon
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#load data using pandas
TrendDataCovid = pd.read_csv("data-by-day-trends.csv")
TotalDataCovid = pd.read_csv("data-by-modzcta-total.csv")
VaccineData = pd.read_csv('doses-by-day.csv')

#normalize data by converting dates to datetime
TrendDataCovid['date_of_interest'] = pd.to_datetime(TrendDataCovid['date_of_interest'])
VaccineData['DATE'] = pd.to_datetime(VaccineData['DATE'])

################################ Daily covid cases
def trendcovid(TrendDataCovid):
    ax = plt.gca()
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b - %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

    figure = plt.gcf()
    figure.set_size_inches(15, 10)

    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['CASE_COUNT'])
    plt.xticks(rotation = 45)
    plt.title("Covid Case Count in New York City Since Beginning of Pandemic")
    plt.xlabel("Date by Months")
    plt.ylabel("Case Counts")
    plt.savefig('TrendDataCovid.png',dpi=100)
    plt.show()

#trendcovid(TrendDataCovid)

################################# cases and death overlay
def CasesOverlay(TrendDataCovid):
    ax = plt.gca()
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b - %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

    figure = plt.gcf()
    figure.set_size_inches(15, 10)

    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['CASE_COUNT'], color = 'g',label='Covid Cases')
    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['DEATH_COUNT'], color = 'b', label='Covid Deaths')
    plt.legend()
    plt.xticks(rotation = 45)
    plt.xlabel('Date by Months')
    plt.ylabel('Covid Counts')
    plt.title('Covid Cases Count and Death')
    plt.savefig('CasesOverlay.png',dpi=100)
    plt.show()

#CasesOverlay(TrendDataCovid)

#####################looks for linear relationship btwn vaccine and cases
def linearRelationshipVaccine(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)
    
    m,b = np.polyfit(df['ADMIN_ALLDOSES_CUMULATIVE'], df['CASE_COUNT'], 1)
    r = np.corrcoef(df['ADMIN_ALLDOSES_CUMULATIVE'],df['CASE_COUNT'])[0][1]

    figure = plt.gcf()
    figure.set_size_inches(15, 10)

    plt.scatter(df['ADMIN_ALLDOSES_CUMULATIVE'], df['CASE_COUNT'])
    plt.title(f'Cases Vs Vaccine to check for linear relationship\nCorrelation Coefficient: {r:.5f}, Slope: {m:.5f}, Intercept: {b:.5f}', fontsize=14)
    plt.xlabel('Daily Vaccine Administered', fontsize=14)
    plt.ylabel('Daily Cases', fontsize=14)
    plt.grid(True)
    plt.plot(df['ADMIN_ALLDOSES_CUMULATIVE'], m*df['ADMIN_ALLDOSES_CUMULATIVE'] + b,color='orange')
    plt.savefig('CasesVaccineRelation.png',dpi=100)
    plt.show()
    

#linearRelationshipVaccine(TrendDataCovid,VaccineData)

####################################linear relationship btwn vaccine and date, convert dates to ordinal for calculations on slope,intercept,coef
def linearRelationshipDate(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    df['ORDINAL_DATE'] = df['DATE'].map(dt.datetime.toordinal)
    date = df['ORDINAL_DATE']
    
    ax = plt.gca()
    ax.grid(True)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b - %Y'))

    m,b = np.polyfit(date, df['CASE_COUNT'], 1)
    r = np.corrcoef(date,df['CASE_COUNT'])[0][1]

    figure = plt.gcf()
    figure.set_size_inches(15, 10)
    
    plt.scatter(df['DATE'], df['CASE_COUNT'])
    plt.title(f'Cases Vs Dates to check for linear relationship\nCorrelation Coefficient: {r:.5f}, Slope: {m:.5f}, Intercept: {b:.5f}', fontsize=14)
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Daily Cases', fontsize=14)
    plt.xticks(rotation=45)
    plt.plot(df['DATE'], m*date + b,color='orange')
    plt.savefig('CasesDateRelation.png',dpi=100)
    plt.show()

#linearRelationshipDate(TrendDataCovid,VaccineData)

########################################linear model for dates shows decrease in cases over time, convert dates to ordinal for calculations on slope,intercept,coef and also linear regression does not work on datetime
def linearDate(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['ORDINAL_DATE'] = df['DATE'].map(dt.datetime.toordinal)

    x = df[['ORDINAL_DATE']] #indepent
    y = df['CASE_COUNT']   #dependent var to be predicted

    x_train, x_test, y_train, y_test = train_test_split(x,y)
    clf = LinearRegression()
    clf.fit(x_train,y_train)
    
    score = clf.score(x_test,y_test)
    pred_y = clf.predict(x_test)

    figure = plt.gcf()
    figure.set_size_inches(15, 10)
    print(clf.coef_)
    plt.title(f'Linear Model of Cases by Ordinal Date\n Accuracy Score: {score:.5f}, Correlation Coefficient: {clf.coef_[0]:.5f}, MSE: {mean_squared_error(y_test,pred_y):.5f}, R2 Score: {r2_score(y_test,pred_y):.5f}, Intercept: {clf.intercept_:.5f}', fontsize=14)
    plt.xlabel('Ordinal Dates', fontsize=14)
    plt.ylabel('Daily Cases', fontsize=14)
    plt.scatter(x_test,y_test)
    plt.plot(x_test,pred_y, color='orange')
    #plt.savefig('lineardatemodel.png',dpi=100)
    plt.show()

#linearDate(TrendDataCovid,VaccineData)

###############################################linear model for vaccine shows decrease in cases as more vaccine
def linearVaccine(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)

    x = df[['ADMIN_ALLDOSES_CUMULATIVE']] #indepent
    y = df['CASE_COUNT']   #dependent var to be predicted
    
    x_train, x_test, y_train, y_test = train_test_split(x,y)
    clf = LinearRegression()
    clf.fit(x_train,y_train)
    
    score = clf.score(x_test,y_test)
    pred_y = clf.predict(x_test)

    figure = plt.gcf()
    figure.set_size_inches(15, 10)
    
    plt.title(f'Linear Model of Cases by Vaccine\n Accuracy Score: {score:.5f}, Correlation Coefficient: {clf.coef_[0]:.5f}, MSE: {mean_squared_error(y_test,pred_y):.5f}, R2 Score: {r2_score(y_test,pred_y):.5f}, Intercept: {clf.intercept_:.5f}', fontsize=14)
    plt.xlabel('Daily Vaccine', fontsize=14)
    plt.ylabel('Daily Cases', fontsize=14)
    plt.scatter(x_test,y_test)
    plt.plot(x_test,pred_y, color='orange')
    plt.savefig('linearvaccinemodel.png',dpi=100)
    plt.show()

#linearVaccine(TrendDataCovid,VaccineData)

################################check for multi linear relation in vaccine,dates,cases, convert dates to ordinal for calculations on slope,intercept,coef and also linear regression does not work on datetime
def multiLinearRelation(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['ORDINAL_DATE'] = df['DATE'].map(dt.datetime.toordinal)
    
    ####calc 3d slope
    x3d = df['ORDINAL_DATE']
    y3d = df['ADMIN_ALLDOSES_CUMULATIVE']
    z3d = df['CASE_COUNT']
   
    coords = np.array((x3d, y3d, z3d)).T
    pca = PCA(n_components=1)
    pca.fit(coords)
    direction_vector = pca.components_

    origin = np.mean(coords, axis=0)
    euclidian_distance = np.linalg.norm(coords - origin, axis=1)
    extent = np.max(euclidian_distance)
    line = np.vstack((origin - direction_vector * extent, origin + direction_vector * extent))
    ###
    
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x3d, y3d, z3d, marker='o')
    ax.plot(line[:, 0], line[:, 1], line[:, 2], 'r')

    ax.set_xlabel('Ordinal Dates')
    ax.set_ylabel('Daily Vaccine Administered')
    ax.set_zlabel('Daily Covid Cases')
    
    plt.title(f'Multiple Linear Relationship of Daily Vaccine and Dates to Covid Cases\n Direction Vector: [{direction_vector[0][0]:.5f},{direction_vector[0][1]:.5f},{direction_vector[0][2]:.5f}]')
    plt.savefig('MultiLinearRelation.png',dpi=100)
    def rotate(angle):
        ax.view_init(azim=angle)
    
    gif = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    gif.save('MultiLinearRelation.gif', dpi=80, writer='Pillow')
    plt.show()
    
#multiLinearRelation(TrendDataCovid,VaccineData)

###########################Linear regression model of vaccine and dates to predict cases, convert dates to ordinal for calculations on slope,intercept,coef and also linear regression does not work on datetime
def multiLinearRegress(TrendDataCovid,VaccineData):
    query = 'SELECT * FROM VaccineData INNER JOIN TrendDataCovid ON VaccineData.DATE = TrendDataCovid.date_of_interest ORDER BY VaccineData.DATE'
    df = psql.sqldf(query)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['ORDINAL_DATE'] = df['DATE'].map(dt.datetime.toordinal)
    
    x = df[['ORDINAL_DATE','ADMIN_ALLDOSES_CUMULATIVE']] # independent var
    y = df['CASE_COUNT']   #dependent var to be predicted

    x_train, x_test, y_train, y_test = train_test_split(x,y)
    clf = LinearRegression()
    clf.fit(x_train,y_train)
    pred_z = clf.predict(x_test)

    score = clf.score(x_test,y_test)
    corr = clf.coef_
    b = clf.intercept_
    mse = mean_squared_error(y_test,pred_z)
    r2 = r2_score(y_test,pred_z)

    ####calc 3d slope
    x3d = x_test['ORDINAL_DATE']
    y3d = x_test['ADMIN_ALLDOSES_CUMULATIVE']
    z3d = pred_z
    
    coords = np.array((x3d, y3d, z3d)).T
    pca = PCA(n_components=1)
    pca.fit(coords)
    direction_vector = pca.components_

    origin = np.mean(coords, axis=0)
    euclidian_distance = np.linalg.norm(coords - origin, axis=1)
    extent = np.max(euclidian_distance)

    line = np.vstack((origin - direction_vector * extent, origin + direction_vector * extent))
    ###
    
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_test['ORDINAL_DATE'], x_test['ADMIN_ALLDOSES_CUMULATIVE'], pred_z, marker='o')
    ax.plot(line[:, 0], line[:, 1], line[:, 2], 'r')

    ax.set_xlabel('Ordinal Dates')
    ax.set_ylabel('Daily Vaccine Administered')
    ax.set_zlabel('Daily Covid Cases')
    plt.title(f'Multiple Linear Regression of Daily Vaccine and Dates to Covid Cases\n Accuracy Score: {score:.5f},\n Correlation Coefficient of Dates: {corr[0]:.5f}, Correlation Coefficient of Vaccination: {corr[1]:.5f}\n \
    MSE: {mse:.5f}, R2 Score: {r2:.5f} Intercept: {b:.5f}')
    plt.savefig('MultiLinearRegress.png',dpi=100)
    def rotate(angle):
        ax.view_init(azim=angle)
    
    gif = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    gif.save('MultiLinearRegress.gif', dpi=80, writer='Pillow')

    plt.show()
    
#multiLinearRegress(TrendDataCovid,VaccineData)

###########################
#BOROUGH DATA
##########################

#####################case by borough
def CasesByBorough(TrendDataCovid):
    ax = plt.gca()
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b - %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['BX_CASE_COUNT'],label='Bronx')
    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['BK_CASE_COUNT'],label='Brooklyn')
    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['MN_CASE_COUNT'],label='Manhattan')
    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['QN_CASE_COUNT'],label='Queens')
    plt.plot(TrendDataCovid['date_of_interest'], TrendDataCovid['SI_CASE_COUNT'],label='Staten Island')
    
    figure = plt.gcf()
    figure.set_size_inches(15, 10)

    plt.legend()
    plt.xticks(rotation = 45)
    plt.savefig('CasesByBoroughLine.png',dpi=100)
    plt.show()

#CasesByBorough(TrendDataCovid)

########################## pie chart case borough
def CasesByBoroughPie(TrendDataCovid):
    bx = TrendDataCovid['BX_CASE_COUNT'].sum()
    bk = TrendDataCovid['BK_CASE_COUNT'].sum()
    mn = TrendDataCovid['MN_CASE_COUNT'].sum()
    qn = TrendDataCovid['QN_CASE_COUNT'].sum()
    si = TrendDataCovid['SI_CASE_COUNT'].sum()

    totalcases = bx + bk + mn + qn + si
    borough = [bx,bk,mn,qn,si]

    figure = plt.gcf()
    figure.set_size_inches(15, 10)

    labels = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
    plt.pie(borough,labels=labels, autopct = lambda p: f'{p:.2f}% \n Cases: {round((p/100)*totalcases)}')
    plt.title(f"Pie Chart of Cases By Borough out of {totalcases} Total Cases in NYC")
    plt.savefig('CasesByBoroughPie.png',dpi=100)
    plt.show()

#CasesByBoroughPie(TrendDataCovid)

#######################################folium map of case by modzcta
def modzctamap(TotalDataCovid):
    map = folium.Map(location= [40.73683608424286, -73.99533554906766], zoom_start=11, tiles="cartodbpositron")
    folium.GeoJson("MODZCTA_2010_WGS1984.geo.json", name="geojson").add_to(map)
    folium.LayerControl().add_to(map)
    
    TotalDataCovid.apply(lambda row:folium.Marker(location=[row["lat"], row["lon"]], icon= DivIcon(icon_size=(150,36),icon_anchor=(7,20),html=f'<div style="font-size: 9pt; color : red">{row["COVID_CONFIRMED_CASE_COUNT"]}</div>')).add_to(map), axis=1)
    map.save('map.html')

#modzctamap(TotalDataCovid)

###########################folium choropleth modzcta
def modzctachoro(TotalDataCovid):
    TotalDataCovid.rename(columns={"MODIFIED_ZCTA": "MODZCTA"},inplace=True)
    TotalDataCovid['MODZCTA'] = TotalDataCovid['MODZCTA'].astype(str)
    map = folium.Map(location= [40.73683608424286, -73.99533554906766], zoom_start=11, tiles="cartodbpositron")
    #folium.GeoJson("MODZCTA_2010_WGS1984.geo.json", name="geojson").add_to(map)
    folium.LayerControl().add_to(map)
    
    
    map_geo = r'MODZCTA_2010_WGS1984.geo.json'
    folium.Choropleth(
        geo_data=map_geo,
        data=TotalDataCovid,
        columns=['MODZCTA','COVID_CONFIRMED_CASE_COUNT'],
        key_on="feature.properties.MODZCTA",
        fill_color='YlGnBu', 
        fill_opacity=1, 
        line_opacity=1,
        legend_name='Covid cases in each modzcta',
        smooth_factor=0).add_to(map)
    
    map.save('choromap.html')

#modzctachoro(TotalDataCovid)
###############################