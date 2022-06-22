import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"])
df = df.set_index('date')
## Column(s) to use as the row labels of the DataFrame, either given as string name or column index. If a sequence of int / str is given, a MultiIndex is used.

# Clean data
df = df.loc[(df["value"] <= df["value"].quantile(0.975)) & (df["value"] >= df["value"].quantile(0.025)) ]


def draw_line_plot():
    # Draw line plot
  
    fig, ax= plt.subplots()
    ax.plot(df["value"], color='r')
    # sns.lineplot(data=df, legend=False)
    ax.set(xlabel=r"Date",
           ylabel=r"Page Views",
           title=r"Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    print("df_bar",df_bar)
    # Filter by the years    
    df_bar["Years"]=df_bar.index.year
    # print(r"df_bar[Years]", df_bar["Years"])

    ## Filter by the months
    df_bar["Months"]=df_bar.index.month_name()
    # print(r"df_bar[Months name]", df_bar["Months"])  
    ## now use groupby method to make a new data fram and put the data based on Year and month in each year separately
    df_bar_gb = pd.DataFrame(df_bar.groupby(["Years", "Months"], sort= False)["value"].mean().round().astype(int))

  
    # it seems that there are some empty values. 
    # print(r"df_bar_gb" ,df_bar_gb)


    df_bar_gb = df_bar_gb.rename(columns={"value": "Average Page Views"})
    df_bar_gb = df_bar_gb.reset_index()
  
    ## so we want to make zero arrays and concatenated it to the dataframe. 
    ## after printing seems that "January" , "February" , "March", "April" are missing. Lets make a dictionary and input manually zero
    zero_val  = {
      "Years" : [2016 , 2016, 2016, 2016],
      "Months" : ["January" , "February" , "March", "April"],
      "Average Page Views"  : [0,0,0,0]}
    df_zero_val = pd.DataFrame(zero_val)

    ## concatenate the two dataframs.
    df_bar_con = pd.concat([df_zero_val , df_bar_gb])
    # print(df_bar_con)
  
    # Draw bar plot
    fig, ax = plt.subplots()
    ax = sns.barplot(data= df_bar_con, x=r"Years", y=r"Average Page Views",palette="Blues_d", hue="Months")
    # Note that "hue="Months" is crucial, since w/o it it will be average of the veiwvers
    
    ax.set(title=r"Daily freeCodeCamp Forum Average Page Views per Month")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()

    # print(r"df_box",df_box)
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    print(r"df_box",df_box)
  
    # Draw box plots (using Seaborn)

    fig, ax = plt.subplots(1, 2, )

    sns.boxplot(data=df_box, x="year", y="value", ax=ax[0])
    ax[0].set(title=r"Year-wise Box Plot (Trend)", xlabel=r"Year", ylabel=r"Page Views")


    # for the boxplot based on Month page view, first make a list and put the month in order
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    sns.boxplot(data=df_box, x="month", y="value", order=order, ax=ax[1])
    ax[1].set(title=r"Month-wise Box Plot (Seasonality)", xlabel=r"Month", ylabel=r"Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
