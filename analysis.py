import datadotworld as dw
import pandas as pd
import numpy as np

company_df = dw.query(
	'lynxrose/startup-analysis',
    'SELECT country_code, count(country_code) FROM companies GROUP BY country_code ORDER BY count(country_code) ASC')

company_df = dw.query(
	'lynxrose/startup-analysis',
    'SELECT country_code, count(country_code) FROM companies GROUP BY country_code ORDER BY count(country_code) ASC')

# df = dw.load_dataset('lynxrose/startup-analysis')
df = company_df.dataframe

# not('homepage_url'.isnull())
print(df)

