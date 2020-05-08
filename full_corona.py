from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

my_url = 'https://www.mohfw.gov.in/'

client_open = urlopen(my_url)
page_html = client_open.read()
soup_html = soup(page_html, 'html.parser')

file_name = 'covid_data.csv'
f = open(file_name, mode = 'w')

headers = 'State Name,Total Number of Confirmed Cases,Cured/Discharged/Migrated,Death\n'
f.write(headers)

table = soup_html.find('tbody')

rows = table.find_all('tr', limit = 32)

for i, state in enumerate(rows):
    state_data = rows[i].find_all('td')
    state_name = state_data[1].text
    confirmed_cases = state_data[2].text
    cured = state_data[3].text
    death = state_data[4].text
    f.write(state_name + ',' + confirmed_cases + ',' + cured + ',' + death +'\n')

f.close()

map_df = gpd.read_file('Indian_States.shp')
corona_df = pd.read_csv('covid_data.csv')
map_df['st_nm'][0] = 'Andaman and Nicobar'
map_df['st_nm'][12] = 'Jammu and Kashmir'
map_df['st_nm'][23] = 'Delhi'

merged = map_df.set_index('st_nm').join(corona_df.set_index('State Name'))
merged['Death'].fillna(0, inplace = True)

fig, ax = plt.subplots(1, figsize=(20, 12))
merged.plot(column='Total Number of Confirmed Cases', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
ax.set_title('Heatmap of India based upon total number corona-virus cases', \
              fontdict={'fontsize': '16',
                        'fontweight' : '3'})
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=10000, vmax=corona_df['Total Number of Confirmed Cases'].max()))
sm._A = []
cbar = fig.colorbar(sm)
plt.show()
