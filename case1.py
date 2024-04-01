import pandas as pd
from collections import OrderedDict

sales_df = pd.read_csv('salesBase.csv')
sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce', format='%d/%m/%Y')

# create list of all elements of given category used to create menu
def category_list(category, table):
    try:
        print(sorted((list(table.loc[:, category].drop_duplicates()))))
        return sorted((list(table.loc[:, category].drop_duplicates())))
    except:
        print("erro")
        return

# retrieve the songs with a given filter
def filterSongs(theFilter, table, filterArray):
    selection = 0
    selectionArray = []

    # present the same menu while input is invalid
    while selection == 0:

        # select multiple elements of a column
        while(selection in range(len(filterArray))):
            filter_menu(theFilter, filterArray)
            if(selectionArray == []):
                print("\033[1m", "0", "\033[0;0m ", "(select all)")
            else:
                print("\033[1m", "0", "\033[0;0m ", "(next)")
            print(" current selection", selectionArray)
            try:
                selection = int(input("\033[5m press a number(toggle selection) => "))-1
                if selection in range(len(filterArray)):
                    if filterArray[selection] in selectionArray:
                        selectionArray.remove(filterArray[selection])
                    else:
                        selectionArray.append(filterArray[selection])
                else:
                    break
            except:
                break
        if(selection == -1):
            table.set_index(theFilter, inplace = True)
            if selectionArray != []:
                table = table.loc[selectionArray]
                print("this print \n", table)
                return table
            else:
                print(table)
                return table
        else:
            selection = 0
            print(" Invalid choice.\n")

# output menu for given filter
def filter_menu(theFilter, theArray):
    print("\n" + "\033[1m" + " FILTER " + theFilter.upper() + "\033[0;0m")
    for i in range(0, len(theArray), 1):
        print("\033[1m", str(i+1), "\033[0;0m ", str(theArray[i]))
    return len(theArray)

#Get the user parameters
def getUsersFilters(df): #df = tableMusic_df
    available_columns = df.columns.tolist()
    filterList = []

    while True:
        print(" Filter songs\nAvailable filters:")
        for i, column in enumerate(available_columns, start=1): #menu starts in 1
            print("\033[1m", i, "\033[0;0m ", column)
        print("\033[1m", "0", "\033[0;0m ", "(next)")

        try:
            print(f" current selection: {filterList}\n")
            choice = int(input(" Choose a filter: "))

            if choice == 0: #next
                if filterList == []:
                    print(df) # present the whole unfiltered table
                break
            elif 1 <= choice <= len(available_columns):
                selected_column = available_columns[choice - 1] #array index, value - 1
                filterList.append(selected_column) #list with parameters
                filterList = list(OrderedDict.fromkeys(filterList))
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

    print(" selected filters:", filterList)
    return filterList #return array with filters, used on apllyFilters

user_filters = getUsersFilters(sales_df)