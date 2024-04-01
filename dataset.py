import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def errorCodes(typeError):
    return f"\33[91mWARNING: {typeError.title()}\33[0;0m\n"

def exitMessange(index_value,typeMessange):
    return f"\033[93m{index_value} {typeMessange}\033[0m\n"

def nextMessange(index_value, typeMessange):
    return f"\033[94m{index_value} {typeMessange}\033[0m\n"

def viewDataFrame(df):
    return print(f"{df.to_markdown(index=False)}\n")

def calculateSum(df, toFilter, groupBy):
    #dataFrame, group by determinate element, filter to calculate sum(quantity_sold,price,cost,revenue or profit)

    df['day'] = df['date'].dt.to_period('D')
    df['month'] = df['date'].dt.to_period('M')
    df['year'] = df['date'].dt.to_period('Y')

    result_df = pd.DataFrame()
    for filter_by in toFilter:
       
        if df[filter_by].dtype == 'int64':
            sumGroup_df = df.groupby(groupBy)[filter_by].sum().reset_index()

        else:
            sumGroup_df = df.groupby(groupBy)[filter_by].count().reset_index()

        result_df = pd.concat([result_df, sumGroup_df], axis=1)

    sorted_products_df = result_df.sort_values(by=toFilter[0], ascending=False) #sort by filter, decrescent order
    sorted_products_df = sorted_products_df.loc[:, ~sorted_products_df.columns.duplicated()]#exclude duplicated columns

    print(f"\033[0;0m\nMore \033[94m{toFilter}\033[0;0m per \033[94m{groupBy}\033[0;0m\n")
    viewDataFrame(sorted_products_df)

    top3 = sorted_products_df.head(3)
    less = sorted_products_df.tail(1)

    print(f'\033[0;0m\nThe 3 \033[94m{groupBy}\033[0;0m with more \033[94m{toFilter}\033[0;0m\n')
    viewDataFrame(top3)
    print(f'\033[0;0m\nThe \033[94m{groupBy}\033[0;0m with less \033[94m{toFilter}\033[0;0m\n')
    viewDataFrame(less)

    return sorted_products_df

def percentualVariation(df, toFilter, groupBy):

    df['day'] = df['date'].dt.to_period('D')
    df['month'] = df['date'].dt.to_period('M')
    df['year'] = df['date'].dt.to_period('Y')

    variation_df = pd.DataFrame()
    for filter_by in toFilter:
        #Verify columns type
        if df[filter_by].dtype == 'int64':
            #If integer calculate average
            sumGroup_df = df.groupby(groupBy)[filter_by].sum().pct_change()*100
        else:
            #If not integer count elements 
            sumGroup_df = df.groupby(groupBy)[filter_by].sum().pct_change()*100

        variation_df = pd.concat([variation_df, sumGroup_df], axis=1)

    print(f"\033[0;0m\nThe percentage change in \033[94m{groupBy}\033[0;0m between \033[94m{toFilter}\033[0;0m\n")
    #viewDataFrame(sorted_products_df)
    print(variation_df.to_markdown())

    return variation_df

def temporalAnalisis(df, axisX, axisY, groupBy):

    df['day'] = df['date'].dt.to_period('D')
    df['month'] = df['date'].dt.to_period('M')
    df['year'] = df['date'].dt.to_period('Y')

    df[['price', 'cost', 'revenue', 'profit']] = df[['price', 'cost', 'revenue', 'profit']].replace({'R\$': ''}, regex=True).apply(pd.to_numeric)

    # Group sales by month and by product
    analisisByGroup_df = df.groupby([groupBy, axisX])[axisY].sum().unstack() 

    print(analisisByGroup_df.to_markdown(), '\n')

    plt.figure(figsize=(12, 6))
    for product in analisisByGroup_df.index:
        plt.plot(analisisByGroup_df.columns.astype(str), analisisByGroup_df.loc[product], marker='o', label=product)

    plt.title(f'{axisX.title()} and {axisY.title()} per {groupBy.title()}')
    plt.xlabel(f'{axisX.title()}')
    plt.ylabel(f'{axisY.title()}')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.show()

    return analisisByGroup_df

def plot_sales_analysis(df, groupBy, axisX, axisY):
    df['day'] = df['date'].dt.to_period('D')
    df['month'] = df['date'].dt.to_period('M')
    df['year'] = df['date'].dt.to_period('Y')

    df[['price', 'cost', 'revenue', 'profit']] = df[['price', 'cost', 'revenue', 'profit']].replace({'R\$': ''}, regex=True).apply(pd.to_numeric)

    # Group sales by month and by product
    analisisByGroup_df = df.groupby([groupBy, axisX])[axisY].sum().unstack() 

    # Add the prfix 'R$'
    analisisByGroup_df = analisisByGroup_df.applymap(lambda x: f'R$ {x:,.2f}')
    print(analisisByGroup_df, '\n')
    #print(analisisByGroup_df.to_markdown(), '\n')

    plt.figure(figsize=(12, 6))
    for product in analisisByGroup_df.index:
        plt.plot(analisisByGroup_df.columns.astype(str), analisisByGroup_df.loc[product].str.extract('(\d+\.\d+)').astype(float), marker='o', label=product)

    plt.title(f'{axisX.title()} and {axisY.title()} per {groupBy.title()}')
    plt.xlabel(f'{axisX.title()}')
    plt.ylabel(f'{axisY.title()}')
    plt.xticks(rotation=45, ha='right')
    
    # Format the values in axisY using prefix 'R$'
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('R${x:,.2f}'))

    plt.legend()
    plt.show()

    return analisisByGroup_df

def filtersMenu(toFilter, selectedFilters): #return index in filterMenu
    if selectedFilters == []:
        for index, value in enumerate(toFilter):
            print(f"\33[1m{index+1} \033[0;0m{value}")
        print(f"\33[1m{index+2}\033[0;0m selected all\n{exitMessange(0, "exit")}")
    else:
        for index, value in enumerate(toFilter):
            print(f"\33[1m{index+1} \033[0;0m{value}")
        print(f"\33[1m{index+2}\033[0;0m selected all\n{nextMessange(index+3, 'next')}{exitMessange(0, "exit")}")
    return index

def getUserFilters(df): #return array with all filters to use
    available_columns = df.columns.tolist()
    theSelectedFilters = []
    while True:
        index = filtersMenu(available_columns, theSelectedFilters)
        try:
            print(f"\33[0;0mFilters selected: {theSelectedFilters} \33[0;0m\nIf you want to change the selection, just press on an already selected item") #show what filters was select
            input_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m"))

            if input_value != 0 and input_value != index+2 and input_value != index+3: #when 0 abort all, i+2 select all, i+3 finish

                while input_value < 0 or input_value-1 > len(available_columns):
                    print(errorCodes("Invalid input"))
                    input_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m")) #request new input

                selection = available_columns[input_value-1] #the selecion is the input_value on index available_columns

                if selection not in theSelectedFilters: #if selection wasnt select after
                    theSelectedFilters.append(selection)
                else: #remove the term if was select after
                    theSelectedFilters.remove(selection)
                viewDataFrame(df[theSelectedFilters].drop_duplicates())

            elif input_value == index+2: #selected all filters
                while True:
                    allfilters_value = int(input(f"\nDo you want to select all filters?\n\033[1m1 \033[0;0mYes\n\033[1m2 \033[0;0mNo\nPress a number to select: "))
                    match allfilters_value:
                        case 1: #confirm selection all terms
                            theSelectedFilters = available_columns
                            print(f"\033[0;0mFilters selected: {theSelectedFilters} \033[0;0m\n")
                            break
                        case 2: #return to choice the filters
                            break  # Break out of the loop without changing theSelectedFilters
                        case _: #error code
                            print(errorCodes("Invalid input"))

                if allfilters_value == 1: #before confirmation about selection all filters
                    break
                else: #new selection filters
                    print("\n")
                    continue

            elif input_value == index+3:# to finish
                while True:
                    allfilters_value = int(input(f"\nDo you want to select filters {theSelectedFilters}?\n\033[1m1 \033[0;0mYes\n\033[1m2 \033[0;0mNo\nPress a number to select: "))
                    match allfilters_value:
                        case 1: #confirm selection all terms
                            print(f"\n\033[0;0mFilters selected: {theSelectedFilters} \033[0;0m\n")
                            break
                        case 2: #return to choice the filters
                            break  # Break out of the loop without changing theSelectedFilters
                        case _: #error code
                            print(errorCodes("Invalid input"))
                if allfilters_value == 1: #before confirmation about selection all filters
                    break
                else: #new selection filters
                    print("\n")
                    continue

            else: # if choice 0, abort all
                break
        except: #errorCodes
            print(errorCodes("invalid input"))
    return theSelectedFilters #return de array with all selected filters

def filterPerValue(df, userSelectedFilters): #return dataFrame filtred
    #df dataFrame to started, userSelectedFilters is the array with all selections to filter per value
    using_df = pd.DataFrame()
    for filter in userSelectedFilters: #filter per columns defined in userSelectedFilters
        print(f"\n\033[0;0mFilter to select by: \033[92m{filter} \033[0;0m\n")
        filter_value = df[filter].drop_duplicates().tolist()
        theSelectedFilters = [] #cleanup the selection array per filter
        while True:
            index = filtersMenu(filter_value, theSelectedFilters) #menu with options
            try:
                print(f"\33[0;0mFilters selected: {theSelectedFilters} \33[0;0m\nIf you want to change the selection, just press on an already selected item") #show what filters was select
                input_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m"))

                if input_value != 0 and input_value != index+2 and input_value != index+3: #when 0 abort all, i+2 select all, i+3 finish

                    while input_value < 0 or input_value-1 > len(filter_value):
                        print(errorCodes("Invalid input"))
                        input_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m")) #request new input

                    selection = filter_value[input_value-1] #the selecion is the input_value on index input_values

                    if selection not in theSelectedFilters: #if selection wasnt select after
                        theSelectedFilters.append(selection)
                        
                        add_to_df = df[df[f'{filter}']==f'{selection}']
                        using_df = pd.concat([using_df, add_to_df])
                    
                    else: #remove the term if was select after
                        theSelectedFilters.remove(selection)
                        using_df = using_df.query(f"{filter} != '{selection}'")

                    viewDataFrame(using_df)

                elif input_value == index+2: #selected all filters
                    while True:
                        allfilters_value = int(input(f"\nDo you want to select all filters?\n\033[1m1 \033[0;0mYes\n\033[1m2 \033[0;0mNo\nPress a number to select: "))
                        match allfilters_value:
                            case 1: #confirm selection all terms
                                theSelectedFilters = filter_value
                                print(f"\033[0;0mFilters selected: {theSelectedFilters} \033[0;0m\n")
                                break
                            case 2: #return to choice the filters
                                break  # Break out of the loop without changing theSelectedFilters
                            case _: #error code
                                print(errorCodes("Invalid input"))

                    if allfilters_value == 1: #before confirmation about selection all filters
                        break
                    else: #new selection filters
                        print("\n")
                        continue

                elif input_value == index+3:# to finish

                    while True:
                        allfilters_value = int(input(f"\nDo you want to select filters {theSelectedFilters}?\n\033[1m1 \033[0;0mYes\n\033[1m2 \033[0;0mNo\nPress a number to select: "))

                        match allfilters_value:
                            case 1: #confirm selection all terms
                                print(f'\n\033[0;0mThe spreadsheet filtred with filters \033[92m{theSelectedFilters}\033[0;0m by \033[92m{filter}\033[0;0m\n')
                                viewDataFrame(using_df)
                                df = using_df #next filter use the dataFrame filtred
                                using_df = pd.DataFrame() #clean the dataFrame using_df
                                break
                            case 2: #return to choice the filters
                                break  # Break out of the loop without changing theSelectedFilters
                            case _: #error code
                                print(errorCodes("Invalid input"))
                                
                    if allfilters_value == 1: #before confirmation about selection all filters
                        break
                    else: #new selection filters
                        print("\n")
                        continue

                else: # if choice 0, abort all
                    break
            except: #errorCodes
                print(errorCodes("invalid input"))
    return df #return de array with all selected filters

sales_df = pd.read_csv('salesBase.csv')
sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce', format='%m/%d/%Y')
sales_df[['price','cost','revenue','profit']] = sales_df[['price','cost','revenue','profit']].applymap(lambda x: f'R$ {x}')

plot_sales_analysis(sales_df, axisX='day', axisY='profit', groupBy='store')