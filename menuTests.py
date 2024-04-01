import pandas as pd

sales_df = pd.read_csv("salesBase.csv")

def errorCodes(typeError):
    return f"\33[91mWARNING: {typeError}\33[0;0m\n"

def exitMessange(index_value,typeMessange):
    return f"\033[93m{index_value} {typeMessange}\033[0m\n"

def nextMessange(index_value, typeMessange):
    return f"\033[94m{index_value} {typeMessange}\033[0m\n"

def filterMenu(df, toFilter):
    theSelectedFilters = [] #list with selected filters
    while True:
        if theSelectedFilters == []:
            for index, value in enumerate(toFilter):
                print(f"\33[1m{index+1} \033[0;0m{value}")
            print(f"\33[1m{index+2} \033[0;0mselected all\n{exitMessange(0, "exit")}")
        else:
            for index, value in enumerate(toFilter):
                print(f"\33[1m{index+1} \033[0;0m{value}")
            print(f"\33[1m{index+2}\033[0;0mselected all\n{nextMessange(index+3, 'next')}{exitMessange(0, "exit")}")
        
        try:
            print(f"\33[0;0mFilters selected: {theSelectedFilters} \33[0;0m\nIf you want to change the selection, just press on an already selected item") #show what filters was select
            filter_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m"))

            if filter_value != 0 and filter_value != index+2 and filter_value != index+3: #when 0 abort all, i+2 select all, i+3 finish

                while filter_value < 0 or filter_value-1 > len(toFilter):
                    print(errorCodes("Invalid input"))
                    filter_value = int(input("\33[0;0mPress a number to select filter: \33[0;0m")) #request new input

                selection = toFilter[filter_value-1] #the selecion is the filter_value on index toFilter

                if selection not in theSelectedFilters: #if selection wasnt select after
                    theSelectedFilters.append(selection)
                else: #remove the term if was select after
                    theSelectedFilters.remove(selection)
                #print(df[theSelectedFilters].drop_duplicates().to_markdown(index=False), "\n")

            elif filter_value == index+2: #selected all filters
                while True:
                    allfilters_value = int(input(f"\nDo you want to select all filters?\n\033[1m1 \033[0;0mYes\n\033[1m2 \033[0;0mNo\nPress a number to select: "))
                    match allfilters_value:
                        case 1: #confirm selection all terms
                            theSelectedFilters = toFilter
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

            elif filter_value == index+3:# to finish
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

        
def apllyFilters(df): 
    #user_selected_filters = filterMenu(df, df.columns.tolist())
    user_selected_filters = ['brand', 'store']
    print(df[user_selected_filters].drop_duplicates().to_markdown(index=False))

    selected_array = []
    for filter in user_selected_filters:
        print(f"\n\033[0;0mFilter to select by: \033[92m{filter} \033[0;0m\n")
        elements_filter = df[f'{filter}'].drop_duplicates().tolist()
        selected_array.extend(filterMenu(df, elements_filter))

    print(f"\n\033[0;0mFilters selected: {selected_array} \033[0;0m\n")

    return selected_array
            
apllyFilters(sales_df)