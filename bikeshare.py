import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_DATA = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello There! Let\'s see what the US bikeshare data as to show you!')

    # asks to choose a city name
    print('Choose a city: Chicago, New York City or Washington')
    city = input('Enter the city name: ').lower()
    while city not in CITY_DATA:
        city = input('Enter the city name: ').lower()

    # asks to choose a month
    print('Choose a month: January, February, March, April, May, June or All')
    month = input('Enter a month: ').lower()
    while month not in MONTH_DATA:
        month = input('Enter a month: ').lower()

    # asks to choose a day of the week
    print('Choose a day: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All')
    day = input('Enter the day : ').capitalize()
    while day not in DAY_DATA:
        day = input('Enter a Day: ').capitalize()

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day of Week'] = pd.to_datetime(df['Start Time']).dt.day_name()


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'All':
        df = df[df['day of Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Arg:
        Dataframe
    Returns:
        Display statistics for time travels.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Month'] = df['Start Time'].dt.month_name()
    most_common_month = df['Month'].mode()[0]
    most_common_month_value = df.groupby(['Month']).size()
    most_common_month_value = most_common_month_value.sort_values(ascending=False)
    most_common_month_value = most_common_month_value.reset_index(drop=True)[0]
    print('most common month: {} count: {}'.format(most_common_month, most_common_month_value))

    # display the most common day of week
    df['day of Week'] = df['Start Time'].dt.day_name()
    most_common_day_week = df['day of Week'].mode()[0]
    most_common_day_week_value = df.groupby(['day of Week']).size()
    most_common_day_week_value = most_common_day_week_value.sort_values(ascending=False)
    most_common_day_week_value = most_common_day_week_value.reset_index(drop=True)[0]
    print('most common day of week: {} count: {}'.format(most_common_day_week, most_common_day_week_value))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    most_common_start_hour_value = df.groupby(['hour']).size()
    most_common_start_hour_value = most_common_start_hour_value.sort_values(ascending=False)
    most_common_start_hour_value = most_common_start_hour_value.reset_index(drop=True)[0]
    print('most common start hour: {} count: {}'.format(most_common_start_hour, most_common_start_hour_value))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Arg:
        Dataframe
    Returns:
        Display statistics for most popular stations ans trips.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    most_common_start_station_value = df.groupby(['Start Station']).size()
    most_common_start_station_value = most_common_start_station_value.sort_values(ascending=False)[0]
    print('most common start station : {} count: {}'.format(most_common_start_station, most_common_start_station_value))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    most_common_end_station_value = df.groupby(['End Station']).size()
    most_common_end_station_value = most_common_end_station_value.sort_values(ascending=False)[0]
    print('most common end station : {} count: {}'.format(most_common_end_station, most_common_end_station_value))

    # display most frequent combination of start station and end station trip
    most_freq_comb_stations_value = df.groupby(['Start Station', 'End Station'])['Unnamed: 0'].count()
    most_freq_comb_stations_value = most_freq_comb_stations_value.sort_values(axis=0, ascending=False).head(1)
    print('most frequent combinations stations :\n', most_freq_comb_stations_value)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Arg:
        Dataframe
    Returns:
        Display statistics for total and average trip durations.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = datetime.timedelta(seconds = int(total_travel_time))
    print('total travel time : ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print('mean travel time : ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    Arg:
        Dataframe
        (str) city: name of the city chosen by the user to filter statistics for new york city and chicago only.
    Returns:
        Display statistics for bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    df['User Type'] = df['User Type'].fillna('Unknown')
    counts_user_types = df.groupby(['User Type']).size()
    print('Counts User Types : ', counts_user_types)


    if city != 'washington':

        # Display counts of gender

        df['Gender'] = df['Gender'].fillna('Unknown')
        counts_gender = df.groupby(['Gender']).size()
        print('Counts Gender : \n', counts_gender)

        # Display earliest, most recent, and most common year of birth

        df = df.dropna(axis=0)
        earliest_birth = df.sort_values(by=['Start Time'], ascending=True)
        earliest_birth = earliest_birth.reset_index(drop=True)
        print('Earliest Year of Birth : ', int(earliest_birth['Birth Year'][0]))

        most_birth = df.sort_values(by=['Start Time'], ascending=False)
        most_birth = most_birth.reset_index(drop=True)
        print('Most Recent Year of Birth : ', int(most_birth['Birth Year'][0]))

        common_birth = df['Birth Year'].mode()[0]
        common_birth_value = df.groupby(['Birth Year']).size()
        common_birth_value = common_birth_value.sort_values(ascending=False)
        common_birth_value = common_birth_value.reset_index(drop=True)[1]
        print('Common Year of Birth : {} count: {}'.format(int(common_birth), common_birth_value))

    else:
        print('No Gender and Birth Year data avalilable for Washington!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':

            while True:
                print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
                i += 5
                more_rows = input('\nDisplay 5 more rows? Enter yes or no: \n')
                if more_rows.lower() != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
