import time
import pandas as pd
import numpy as np
import datetime
import collections

CITY_DATA = {'chicago': 'chicago.csv',
             'new_york_city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ["january", "february", "march", "april", "may", "june"]
days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
filters = ["month", "day", "both", "no"]
# ----------------------------------------------------------------------------------------------------
months_list = []
days_list = []
hours_list = []


# ----------------------------------------------------------------------------------------------------
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs4

    month = ""
    day = ""
    filter = ""
    city = ""
    ls = []
    for i in list(CITY_DATA.keys()):
        ls.append(i.lower())

    city = input("would you like to see data for  chicago, new_york_city, washington : ").strip().lower()
    while city not in ls:
        city = input("please enter a name of theses cities chicago, new_york_city, washington  : ").strip().lower()

    filter = input("would you like to filter data by month, day, both, or no filter : ").strip().lower()
    while filter not in filters:
        filter = input("please enter \"month\" or \"day\" or \"both\" or \"no\" for no filter   : ").strip().lower()

    if filter == "no" or filter == "day":  # month filter
        pass
    else:
        month = input("please enter one of the first six months e.g. march : ").strip().lower()
        while month not in months:
            month = input("please enter a valid month e.g. march  : ").strip().lower()

    if filter == "no" or filter == "month":  # dayfilter
        pass
    else:
        day = input("please enter one of the week days e.g. sunday : ").strip().lower()
        while day not in days:
            day = input("please enter a valid day e.g. sunday  ").strip().lower()

    print('-' * 40)
    return city.lower(), month.lower(), day.lower(), filter.lower()


def seperateDate(df):
    '''
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset=["Start Time"], inplace=True)
    '''

    for i in list(df["Start Time"]):
        months_list.append(datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').month)
        days_list.append(datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').strftime("%A"))
        hours_list.append(datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').hour)


# ----------------------------------------------------------------------------------------------------
def load_data(city, month, day, filter):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city + ".csv")

    seperateDate(df)

    df["months"] = months_list
    df["days"] = days_list
    df["hours"] = hours_list

    if (filter == "month"):
        df = df[(df.months == months.index(month) + 1)]

    if (filter == "day"):
        df = df[(df.days == day.capitalize())]

    if (filter == "both"):
        df = df[(df.months == months.index(month) + 1)]
        df = df[(df.days == day.capitalize())]

    print("please wait for seconds :) \n ")
    return df


# ----------------------------------------------------------------------------------------------------

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months_list.clear()
    days_list.clear()
    hours_list.clear()

    seperateDate(df)

    Month_occurrences = collections.Counter(months_list)
    Days_occurrences = collections.Counter(days_list)
    Hours_occurrences = collections.Counter(hours_list)
    '''
    print(Month_occurrences, "\n", Days_occurrences, "\n", Hours_occurrences, "\n",
          )

          max(Month_occurrences.items(), key=lambda x: x[1])[0],"\n",max(Days_occurrences.items(), key=lambda x: x[1])[0],"\n",
          max(Hours_occurrences.items(), key=lambda x: x[1])[0]
          )
    '''

    most_common_month = max(Month_occurrences.items(), key=lambda x: x[1])[0]
    most_common_day = max(Days_occurrences.items(), key=lambda x: x[1])[0]
    most_common_hour = max(Hours_occurrences.items(), key=lambda x: x[1])[0]
    # display the most common month
    print("the most common month", months[most_common_month - 1])
    # display the most common day of week
    print("the most common day of week", most_common_day)
    # display the most common start hour
    print("the most common hour", most_common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    res = []

    # display most commonly used start station
    res = df["Start Station"].value_counts()
    print("Most Commonly used Start Station : ", res.keys()[0], "- Count:", max(res))
    # display most commonly used end station
    print("Most Commonly used Etart Station : ", df["End Station"].value_counts().keys()[0], "- Count:",
          max(df["End Station"].value_counts()))
    # display most frequent combination of start station and end station trip

    print("Most Frequent Trip :",
          df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False).head(1)
          )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Trip_Dur = int(df["Trip Duration"].sum())
    ave=Trip_Dur / (df["Trip Duration"].count())
    print(" total travel time : ", Trip_Dur, "  Duration in days H-M-S : ", datetime.timedelta(seconds=Trip_Dur))
    # display mean travel time
    print(" mean travel time : ",ave,"  average in days H-M-S : ",datetime.timedelta(seconds=ave) )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city == "washington":
        print("NO Gender Data Or Birth Year Data to share")
    else:
        # Display counts of gender
        print("Gender: ", df["Gender"].value_counts().keys()[0], "- Count:", df["Gender"].value_counts()[0], "  ",
              df["Gender"].value_counts().keys()[1], "- Count:", df["Gender"].value_counts()[1]
              )
        # Display earliest, most recent, and most common year of birth
        print(" oldest, youngest, most popular year of birth respectively :", min(df["Birth Year"]), "-",
              max(df["Birth Year"]), "-", df["Birth Year"].value_counts().keys()[0]
              )

    # Display counts of user types
    print("User Type: ", df["User Type"].value_counts().keys()[0], "- Count:", df["User Type"].value_counts()[0], "  ",
          df["User Type"].value_counts().keys()[1], "- Count:", df["User Type"].value_counts()[1]
          )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    ans = ""
    ans = input("would You like to see raw data? ").strip().lower()
    pd.set_option('display.max_columns', None)
    while ans == "yes":
        print(df.sample(n=5))
        ans = input("would You like to see 5 more rows of the data? ").strip().lower()


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day, filter)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)
        months_list.clear()
        days_list.clear()
        hours_list.clear()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


