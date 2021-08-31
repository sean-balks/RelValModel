import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import companyClass
import windowClass

from matplotlib.ticker import MaxNLocator

stats = [] #List of financials, balance sheet, and cashflow data to retrieve
companies = [] #List of company objects
legend_names = [] #List of company names to show on legend
colors = ['yellow', 'black', 'orange', 'purple', 'cyan', 'blue', 'green', 'red'] #Base colors to differentiate company lines
color_set = {} #Dictionary for setting colors

#Gather input on companies
num_companies = int(input("How many companies would you like to evaluate? \n"))
for i in range(num_companies):
    curr = (input("Enter a ticker for company " + str((i+1)) + " (ex: MSFT): \n"))
    legend_names.append(curr.upper())
    companies.append(companyClass.Company(curr))
print()

#Find which statistics are available for all companies and inform user
print("Here is a list of the available statistics: ")
if(len(companies) > 0):
    available_financials = set(companies[0].financials.index)
    available_cashflow = set(companies[0].cashflow.index)
    available_balancesheet = set(companies[0].balancesheet)
    for company in companies:
        available_financials = available_financials.intersection(company.financials.index)
        available_cashflow = available_cashflow.intersection(company.cashflow.index)
        available_balancesheet = available_balancesheet.intersection(company.balancesheet.index)
    for item in available_financials:
        print(item)
    for item in available_cashflow:
        print(item)
    for item in available_balancesheet:
        print(item)
print()
    
#Gather input on stats
num_stats = int(input("How many statistics would you like to view? \n"))
for i in range(num_stats):
    stats.append(input("Enter statistic " + str((i+1)) + " of " + str(num_stats)  + " : \n"))

#Retrieve data and organize color dictionary
for company in companies:
    for stat in stats:
        company.add_data(stat)
    color_set[company.name] = colors[len(colors)-1]
    colors.pop()

    

#Size subplots
if(len(stats) == 1):
    fig, axs = plt.subplots(1, 2)
    for i in range(len(companies)):
        companies[i].generate_raw_dataframe(companies[i].raw_data, 'Year', stats[0])
        companies[i].generate_percent_dataframe(companies[i].percent_data, 'Year', stats[0])
        axs[0].plot(companies[i].raw_dataframes[0]['Year'], companies[i].raw_dataframes[0][stats[0]], color=color_set[companies[i].name], marker='o')
        axs[1].plot(companies[i].percent_dataframes[0]['Year'], companies[i].percent_dataframes[0][stats[0]], color=color_set[companies[i].name], marker='o')

    axs[0].set_title(stats[0] + " (in millions)")
    axs[0].legend(legend_names, loc="upper left")
    axs[1].set_title(stats[0] + " (%)")
    axs[1].legend(legend_names, loc="upper left")

    axs[1].yaxis.set_major_locator(MaxNLocator(5))
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=5))

    plt.setp(axs[0].get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(axs[1].get_xticklabels(), rotation=30, horizontalalignment='right')
else:

    fig, axs = plt.subplots(len(stats), 2)
    for i in range(len(stats)):
        
        for j in range(len(companies)):
            companies[j].generate_raw_dataframe(companies[j].raw_data, 'Year', stats[i])
            companies[j].generate_percent_dataframe(companies[j].percent_data, 'Year', stats[i])
            axs[i, 0].plot(companies[j].raw_dataframes[0]['Year'], companies[j].raw_dataframes[i][stats[i]], color=color_set[companies[j].name], marker='o')
            axs[i, 1].plot(companies[j].percent_dataframes[0]['Year'], companies[j].percent_dataframes[i][stats[i]], color=color_set[companies[j].name], marker='o')
        
        axs[i, 0].set_title(stats[i] + " (in millions)")
        axs[i, 0].legend(legend_names, loc="upper left")
        axs[i, 1].set_title(stats[i] + " (%)")
        axs[i, 1].legend(legend_names, loc="upper left")

        axs[i,1].yaxis.set_major_locator(MaxNLocator(5))
        axs[i,1].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=5))

        plt.setp(axs[i, 0].get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.setp(axs[i, 1].get_xticklabels(), rotation=30, horizontalalignment='right')


plt.tight_layout()
#a = windowClass.ScrollableWindow(plt)
plt.show()


#Future
#% on Y axis
# - 100 %, 0%, 100% or something like that 
#Fix 0's on X axis
#Basically make it aesthetic