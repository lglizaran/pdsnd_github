import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city != 'all' and city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input('Enter a city (chicago, new york city, washington or all):').lower()
        #city = 'chicago'
    # get user input for month (all, january, february, ... , june)
    month = ''
    while month != 'all' and  month != 'january' and  month != 'february' and  month != 'march' and  month != 'april' and  month != 'may' and \
    month != 'june' and  month != 'july' and  month != 'august' and  month != 'september' and  month != 'october' and  month != 'november' and  month != 'december':
        month = input('Enter a month (all, january, february, ... , june):').lower()
        #month = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day != 'all' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
        day = input('Enter a day (all, monday, tuesday, .... , sunday):').lower()
        #day = 'all'
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

    if city == 'all':
        df = pd.read_csv(CITY_DATA['chicago'])
        df['city'] = 'chicago'
        ny = pd.read_csv(CITY_DATA['new york city'])
        ny['city'] = 'new york city'
        df = df.append(ny,sort = True)
        wa = pd.read_csv(CITY_DATA['washington'])
        wa['city'] = 'washington'
        df = df.append(wa,sort = True)
    else:
        df = pd.read_csv(CITY_DATA[city])
        df['city'] = CITY_DATA[city]

    df['Start Time'] = pd.to_datetime(df['Start Time']) #converts Start Time to datetime
    df['End Time'] = pd.to_datetime(df['End Time']) #converts End Time to datetime
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    #print(df) #DataFrame

    #filter by month
    if month != 'all':
        month_name = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
        month_num = month_name.index(month) + 1
        df = df[df['month'] == month_num]
    #filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    recs = df['Start Time'].count()

    return df, recs


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(str(most_common_month)))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(str(most_common_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most start station is: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' and ' + df['End Station']
    most_common_start_end_station = df['start_end_station'].mode()[0]
    print('The most common combination of start and end station is: {}'.format(most_common_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['trip_duration'] = (df['End Time'] - df['Start Time'])

    # display total travel time
    total_travel_time = df['trip_duration'].sum()
    print('The total travel time is: {}'.format(str(total_travel_time)))

    # display mean travel time
    avg_travel_time = df['trip_duration'].mean()
    print('The average travel time is: {}'.format(str(avg_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of User Types:')
    print(df.groupby(['User Type'])['User Type'].count())

    # Display counts of gender
    if city != 'washington':
        print('Count of genders:')
        print(df.groupby(['Gender'])['Gender'].count())
    else:
        print('Washington dataset data does not include Gender')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('Earliest year of birth: {}'.format(str(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(str(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(str(df['Birth Year'].mode()[0])))
    else:
        print('Washington dataset data does not include Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    more = ''
    n = 1
    while more == 'yes' or more == '':
        more = ''
        df_ = df[['Start Time', 'End Time','city','month','day_of_week','hour','Birth Year','Gender','User Type']]
        print(df_[0:5*n])
        while more != 'yes' and more != 'no':
            more = input('Want to see 5 more lines? Enter yes or no: \n').lower()
        n += 1

def main():
    while True:
        city, month, day = get_filters()
        df,recs = load_data(city, month, day)
        if recs == 0:
            print('No data selected, reduce the filters')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)

            raw = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
            if raw == 'yes':
                raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break




if __name__ == "__main__":
	main()
