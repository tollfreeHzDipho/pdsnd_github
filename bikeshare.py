#code written by Turyamuhaki Diphas (tdiphas@gmail.com)
import time
import pandas as pd
import numpy as np
import click as cl
import json
#Check whether the matplotlib module is installed
try:
    import matplotlib.pyplot as plt
    import_checker=True
except ModuleNotFoundError:
    print("__"*14+"xx"*10+" NOTICE!! "+"xx"*10+("__"*14))
    print("Module \'{}\' as \'{}\' is not installed."\
        " Without this module, you won\'t have a rich experience with tha app".format('matplotlib','plt'))
    print("__"*14+"xx"*14+"xx"*11+("__"*14))
    import_checker=False
#city files dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Month list
days= ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']
#Days list
months = ['january', 'february', 'march', 'april', 'may', 'june']

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
    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
       if city in CITY_DATA:
           break

    if cl.confirm("WANT SOME CUSTOM FILTERS FOR "+city.upper()+"?"):
        while True:
            # get user input for month (all, january, february, ... , june)
            month=input('Alright then, enter a month to explore. eg. \"january,february,march, april,may,june\"\n>')
            #validating the month
            if month.isalpha():
                month=month.lower()
                #makeing sure the user typed in a month
                month_set = frozenset(months)
                if month not in month_set:
                    month='all'
                break            
        while True:
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day=input('Enter a day. eg. \"monday, tuesday, ... sunday\"\n>')
            #validating the day for non letters 
            if day.isalpha():
                day=day.lower()
                #making sure the user typed in a day
                day_set = frozenset(days)
                if day not in day_set:           
                    day='all'
                break
           
    else:  month, day='all','all'

    print('-'*40)
    return city, month.lower(), day


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
    #Loading city data 
    df = pd.read_csv(CITY_DATA[city]) 
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
  
    if month != 'all':
        # use the index of the months list to get the corresponding int       
        #month +1 to match the indices om months
        month = months.index(month)+1     
        # filter by month to create the new dataframe
        df = df[df['month']==month]  #set the month to arg 'month'

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month=df['month'].value_counts().idxmax()
    print("The most common month is :{}".format(months[most_common_month-1]))

    # display the most common day of week
    most_common_day=df['day_of_week'].value_counts().idxmax()
    print('The most common day is: {}'.format(most_common_day))
      
    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is : {}".format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used End station is :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_freq_start_end_station =df[['Start Station','End Station']].mode().loc[0]
    print("The most frequently used start and end station combination is:\n\
    ({0} - {1})".format(most_freq_start_end_station[0], most_freq_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is:", total_travel_time)
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if check_column_exists('User Type',df):
        user_type_counts = df['User Type'].value_counts()
        print("Total number of user type counts is :\n{}".format(user_type_counts))
    # Display counts of gender
    if check_column_exists('Gender',df):
        user_gender_counts = df['Gender'].value_counts()
        print("Total number of users based on gender counts is :\n{}".format(user_gender_counts))

    # Display earliest, most recent, and most common year of birth  
    if check_column_exists('Birth Year', df):
        print('\tThe Earliest of birth is :{0[0]} \n'\
            'The most recent year of birth is :{0[1]}\n'\
            'The Most common year of birth is: {0[2]}'\
                .format(display_year_of_birth_stats(df)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_year_of_birth_stats(df):
    """Function to return the earliest, most recent, and most common year of birth;
       INPUT: DataFrame
       OUTPUT:  Earliest year of birth
                Most recent year of birth
                Most common year of birth
    """
    #display earliest year of birth exluding the NaN values 
    min_year_of_b = df['Birth Year'].dropna().min()
    #display the most recent
    max_year_of_b = df['Birth Year'].dropna().max()
    #sisplay the most common year of birth
    most_common_year_of_b = df['Birth Year'].dropna().value_counts().idxmax()
    return min_year_of_b, max_year_of_b, most_common_year_of_b

def check_column_exists(column,df):
    """ check in a column exists in the data frame
        INPUT:  -column name(str) to test if exist
                -df dataframe(DataFrame) to provide the test data
        OUTPUT: Return the True if exists in dataframe or False otherwise
    """
    value=False
    if column in df.columns:
        value=True
    return value

def Show_genderbased_trip_duration(df):
    """Display a graph of the total trip duration based on gender eg. female 1200, etc """
    #check if colimn exists in dataframe
    if check_column_exists('Gender',df):
        n=df.groupby(['Gender'])['Trip Duration'].sum().reset_index(name="Trip Duration")
        #check if matplot has been imported successfully
        if import_checker:
            #PLot the graph
            plt.ticklabel_format(style='plain')
            plt.bar(n.loc[:,'Gender'],n.loc[:,'Trip Duration'],label="Total Trip Duration") 
            plt.title("Total trip duration based on gender ")
            plt.legend()
            plt.ylabel("Trip duration")
            plt.xlabel("Gender")
            plt.show()
        else:
            print("List showing the gender against Total trip duration\n") 
            print(n)

def Show_according_to_gender_and_the_type(df,gender):
    """ #Display the number of users according to gender and the type of user they are  """
    #check if colimn exists in dataframe
    if check_column_exists('Gender',df) and  check_column_exists('User Type',df):
        group_user_and_gender =  df.groupby(['Gender','User Type']).size().reset_index(name="Counter")
        gendertype=group_user_and_gender.loc[group_user_and_gender["Gender"] ==gender.title(), :]
        #check if matplot has been imported successfully
        if import_checker:
            #PLot the graph
            plt.ticklabel_format(style='plain')
            plt.plot(gendertype.loc[:,"User Type"],gendertype.loc[:,"Counter"],'go',label=gender)
            plt.plot(gendertype.loc[:,"User Type"],gendertype.loc[:,"Counter"],color="orange")
            plt.title("Number of {} users against User type ".format(gender))
            plt.legend()
            plt.ylabel("Number of users")
            plt.xlabel("USER TYPES")
            plt.show()
            plt.rc('axes', axisbelow=True)
        else:
            print("List showing the number of users grouped by gender and type\n") 
            print(group_user_and_gender)

def display_raw_data_to_user(df):
    """ This function displays the list of 5 consecutive rows of raw data as requested by the user"""
    data_length = df.shape[0]
    row = 0
    while  row<data_length-1:
        if cl.confirm("\nWould you like to see the raw data? Type 'Yes' or 'No'.\n"):      
        #print(df.iloc[row:row+5,:])
            #lets parse the dataframe to json format using records 
            # Sanitise my columns first           
            df.columns = df.columns.str.replace('[#,@,:,&]', '')
           
            result = df.iloc[row:row+5,:].fillna(0).to_json(orient="records", lines=True).split('\n')
            for i in range(len(result)-1):
                    # Lets beautify the print out of our rows
                    parsed_row = json.loads(result[i])
                    json_row = json.dumps(parsed_row, indent=2)
                    print(json_row)
            row += 5
        else:
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('**'*40)
        print('\t\t\tSELECTED CITY:{city}\n\
            \t\tSELECTED MONTH:{month}\n\
            \t\tSELECTED DAY:{day}'.format(city=city,month=month,day=day))
        print('**'*40)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        if import_checker:
            Show_genderbased_trip_duration(df)
            genders=['Female','Male']
            for value in enumerate(genders):
                Show_according_to_gender_and_the_type(df,value[1])              
        else:
            Show_genderbased_trip_duration(df)
            Show_according_to_gender_and_the_type(df,'Female')
        display_raw_data_to_user(df)    
        if cl.confirm("\nWould you like to restart? Enter yes or no.\n"):       
            break
        

if __name__ == "__main__":
	main()
