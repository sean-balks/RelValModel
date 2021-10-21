import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import companyClass
import windowClass
from PySimpleGUI.PySimpleGUI import InputText
from matplotlib.ticker import MaxNLocator
tickers_inputs = ['-INPUT1-','-INPUT2-','-INPUT3-','-INPUT4-','-INPUT5-','-INPUT6-','-INPUT7-','-INPUT8-','-INPUT9-',]
stats_inputs = ['-STAT1-','-STAT2-','-STAT3-','-STAT4-','-STAT5-'] 
all_stats = [] #List of all available statistics (intersection of statistic sets)
stats = [] #List of requested statistics
companies = [] #List of company objects
legend_names = [] #List of company names to show on legend
colors = ['brown', 'yellow', 'black', 'purple', 'cyan', 'orange', 'blue', 'green', 'red'] #Base colors to differentiate company graph lines
color_set = {} #Dictionary for setting colors

#Functions to prevent GUI blurring and theme setup
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()
sg.theme('Reddit')

#First layout - inputting tickers
layout_1 = [
    [sg.Text("Welcome to the Relative Valuation Model Generator", font=("Helvetica", 20))],
    [sg.Text("Enter up to 9 tickers to analyze:", font=("Helvetica", 20), pad=(0,10))],
    [[sg.Text("$", font=("Helvetica", 12, "italic"))] + [sg.InputText(key="-INPUT" + str(i)+"-", pad=(0,10), size=(15,200))] for i in range(1, 10)],
    [sg.Button("Next")]
    #-INPUT1- to -INPUT9-
]


window_1 = sg.Window('Relative Valuation Model Generator', layout_1, size=(1300, 800))

while True:
    event, values = window_1.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        window_1.close()
        del window_1
        quit()
    else:
        for input in tickers_inputs:
            if(values[input] != ''):
                companies.append(companyClass.Company(values[input]))
        break

window_1.close()

#Second layout - inputting stats
if(len(companies) > 0):
    available_financials = set(companies[0].financials.index)
    available_cashflow = set(companies[0].cashflow.index)
    available_balancesheet = set(companies[0].balancesheet)
    for i in range(len(companies)):
        available_financials = available_financials.intersection(companies[i].financials.index)
        available_cashflow = available_cashflow.intersection(companies[i].cashflow.index)
        available_balancesheet = available_balancesheet.intersection(companies[i].balancesheet.index)
    for item in available_financials:
        all_stats.append(item)
    for item in available_cashflow:
        all_stats.append(item)
    for item in available_balancesheet:
        all_stats.append(item)

layout_2 = [
    [sg.Text("Select up to 5 available statistics:", font=("Helvetica", 20))],
    [[sg.Combo(all_stats, default_value='Select Statistic',key='-STAT' + str(i)+"-")] for i in range(1, 6)],
    [sg.Button("Next")]
    #-STAT1- to -STAT5-
]

window_2 = sg.Window('Relative Valuation Model Generator', layout_2, size=(1300, 800))

while True:
    event, values = window_2.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        window_2.close()
        del window_1
        del window_2
        quit()
    else:
        for input in stats_inputs:
            if(values[input] != 'Select Statistic'):
                stats.append(values[input])
        break

for company in companies:
    for stat in stats:
        company.add_data(stat)
    color_set[company.name] = colors[len(colors)-1]
    legend_names.append(company.name)
    colors.pop()

window_2.close()

#Third layout - graphs - created using PyQt5 for scrollable window feature

layout_3 = [
    [sg.Canvas(key='-CANVAS-')],
    [sg.Button('Exit', font='Any 16')]
]

#Creating graphs
if(len(stats) == 1):
    fig, axs = plt.subplots(1, 2, figsize=(6.7,8))
    for i in range(len(companies)):
        companies[i].generate_raw_dataframe(companies[i].raw_data, 'Year', stats[0])
        companies[i].generate_percent_dataframe(companies[i].percent_data, 'Year', stats[0])
        axs[0].plot(companies[i].raw_dataframes[0]['Year'], companies[i].raw_dataframes[0][stats[0]], color=color_set[companies[i].name], marker='o')
        axs[1].plot(companies[i].percent_dataframes[0]['Year'], companies[i].percent_dataframes[0][stats[0]], color=color_set[companies[i].name], marker='o')

    axs[0].set_title(stats[0] + " (in millions)")
    axs[0].legend(legend_names, loc="upper left", prop={'size': 6})
    axs[1].set_title(stats[0] + " (%)")
    axs[1].legend(legend_names, loc="upper left", prop={'size': 6})

    axs[1].yaxis.set_major_locator(MaxNLocator(5))
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=5))

    plt.setp(axs[0].get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.setp(axs[1].get_xticklabels(), rotation=30, horizontalalignment='right')
else:

    fig, axs = plt.subplots(len(stats), 2, figsize=(6.7,9))
    for i in range(len(stats)):
        
        for j in range(len(companies)):
            companies[j].generate_raw_dataframe(companies[j].raw_data, 'Year', stats[i])
            companies[j].generate_percent_dataframe(companies[j].percent_data, 'Year', stats[i])
            axs[i, 0].plot(companies[j].raw_dataframes[0]['Year'], companies[j].raw_dataframes[i][stats[i]], color=color_set[companies[j].name], marker='o')
            axs[i, 1].plot(companies[j].percent_dataframes[0]['Year'], companies[j].percent_dataframes[i][stats[i]], color=color_set[companies[j].name], marker='o')
        
        axs[i, 0].set_title(stats[i] + " (in millions)")
        axs[i, 0].legend(legend_names, loc="upper left", prop={'size': 3})
        axs[i, 1].set_title(stats[i] + " (%)")
        axs[i, 1].legend(legend_names, loc="upper left", prop={'size': 3})

        axs[i,1].yaxis.set_major_locator(MaxNLocator(5))
        axs[i,1].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=5))

        plt.setp(axs[i, 0].get_xticklabels(), rotation=50, horizontalalignment='right')
        plt.setp(axs[i, 1].get_xticklabels(), rotation=50, horizontalalignment='right')

plt.tight_layout()
if(len(stats) > 1):
    plt.subplots_adjust(top=0.945, bottom=0.13, left=0.105, right=0.975, hspace=0.87, wspace=0.305)
else:
    plt.subplots_adjust(top=0.945, bottom=0.615, left=0.1, right=0.99, hspace=0.87, wspace=0.305)

a = windowClass.ScrollableWindow(fig)

del window_1
del window_2