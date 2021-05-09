import pandas as pd
import csv
import re


def get_id(url):
    return re.search(r'g187849-(.*?)-Reviews', url).group(1)


inputfile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan_old.csv"
inputfile327 = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan327.csv"
outputile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan.csv"
outputile1 = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan_new.csv"

df = pd.read_csv(inputfile, sep=',', quotechar='"', encoding='utf-8')

df327 = pd.read_csv(inputfile327, sep=';')


df_all = df.merge(df327, on=['partial_rank', 'url', 'n_reviews', 'rating', 'type'], suffixes=['_df', '_df327'])

df_all.drop(['name_df327', 'zone_df327'], axis=1, inplace=True)

df_all['id'] = df_all.apply(lambda row: get_id(row['url']), axis=1)

df_all.rename(columns={'name_df': 'name', 'zone_df': 'zone'}, inplace=True)

cols = ['id', 'name', 'url', 'partial_rank', 'zone', 'n_reviews', 'rating', 'type']

df_all = df_all[cols].sort_values(by=['id'])

df_all.to_csv(outputile, sep=',', quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8', index=False)

##############################################################################################################

df_all = pd.read_csv(outputile, sep=',', quotechar='"', encoding='utf-8')

df_all.insert(0, 'index', df_all.index+1)


df_all.to_csv(outputile1, sep=',', quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8', index=False)

