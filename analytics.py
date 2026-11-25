import pandas as pd
from pathlib import Path
ROOT=Path(__file__).parent

def load(name): return pd.read_csv(ROOT/'data'/f'{name}.csv')
def portfolio(df):
    d=df.copy(); d['revenue']=(d.enrolled-d.withdrawn)*d.tuition; d['cost']=d.fixed_cost+d.enrolled*d.variable_cost
    d['margin']=d.revenue-d.cost; d['fill_rate']=d.enrolled/d.capacity; d['completion_rate']=d.completed/d.enrolled
    return d

def funnel(d):
    return d.groupby('channel')[['sourced','screened','interviewed','offered','hired']].sum()

def scenario(price,variable,fixed,enrollment):
    import math
    return {'contribution':(price-variable)*enrollment-fixed,'break_even':math.ceil(fixed/(price-variable)) if price>variable else None}
