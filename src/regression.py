import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../data/raw/body.csv")
print(type(df['daytime_routes'][0]))
df['lines']=df['daytime_routes'].apply(lambda x: len(str(x).split(' ')))
df['congestion'] = df['entries'].div(df['lines'])
print(df['congestion'].head(10))
df.to_csv("congestion.csv")