import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def plot_sales_analysis(df, groupBy, axisX, axisY):
    df['day'] = df['date'].dt.to_period('D')
    df['month'] = df['date'].dt.to_period('M')
    df['year'] = df['date'].dt.to_period('Y')

    df[['price', 'cost', 'revenue', 'profit']] = df[['price', 'cost', 'revenue', 'profit']].replace({'R\$': ''}, regex=True).apply(pd.to_numeric)

    # Group sales by month and by product
    analisisByGroup_df = df.groupby([groupBy, axisX])[axisY].sum().unstack() 

    # Add the prfix 'R$'
    analisisByGroup_df = analisisByGroup_df.applymap(lambda x: f'R$ {x:,.2f}')
    #print(analisisByGroup_df, '\n')
    #print(analisisByGroup_df.to_markdown(), '\n')

    #plt.figure(figsize=(12, 6))
    for product in analisisByGroup_df.index:
        print(f'\033[92m{product}\33[0;0m\n\n')
        print("\n\033[91manalisisByGroup_df.columns.astype(str)\033[0;0m\n",analisisByGroup_df.columns.astype(str), "\n\033[91manalisisByGroup_df.loc[product].str.extract('(\d+\.\d+)').astype(float)\033[0;0m\n",analisisByGroup_df.loc[product].str.extract('(\d+\.\d+)').astype(float),'\n\n\n')
    '''
    plt.title(f'{axisX.title()} and {axisY.title()} per {groupBy.title()}')
    plt.xlabel(f'{axisX.title()}')
    plt.ylabel(f'{axisY.title()}')
    plt.xticks(rotation=45, ha='right')
    
    # Format the values in axisY using prefix 'R$'
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('R${x:,.2f}'))

    plt.legend()
    plt.show()
    '''
    return analisisByGroup_df

sales_df = pd.read_csv('salesBase.csv')
sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce', format='%m/%d/%Y')
sales_df[['price','cost','revenue','profit']] = sales_df[['price','cost','revenue','profit']].applymap(lambda x: f'R$ {x}')

plot_sales_analysis(sales_df, axisX='month', axisY='profit', groupBy='store')
