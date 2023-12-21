import pandas as pd


scan1=pd.read_csv("3Q2022_reqmgr_ds.csv").drop_duplicates()
scan1.fillna('none',inplace=True)  ##replace NaN values with 'none' String
filt=~((scan1['DependencyName'].str.contains('com.ibm.security.access.')) | (scan1['DependencyPath'].str.contains('cucumber')))  #remove  com.ibm.security deoendencies


filtered_report1=scan1.loc[filt]
filtered_report1.to_excel('3Q_filtered.xlsx')

print(filtered_report1)


scan2=pd.read_csv("4Q2022_reqmgr_ds.csv").drop_duplicates()
scan2.fillna('none',inplace=True)  ##replace NaN values with 'none' String
filt=~((scan2['DependencyName'].str.contains('com.ibm.security.access.')) | (scan2['DependencyPath'].str.contains('cucumber')))  #remove  com.ibm.security deoendencies


filtered_report2=scan2.loc[filt]
filtered_report2.to_excel('4Q_filtered.xlsx')
print(filtered_report2)