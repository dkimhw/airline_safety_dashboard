import pandas as pd
import numpy as np
import sqlite3


# Returns the data from sqlite table & calculates new metrics
def get_data():
    conn = sqlite3.connect("data/airline")
    cur = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM airline_safety;", conn)
    conn.close()

    cols = list(df.columns)
    cols.remove('airline')
    for col in cols:
        df[col] = df[col].astype(int)

    # New Metrics
    df['avail_seat_km'] = (df.avail_seat_km_per_week * 52 * 15)
    df['incident_rate_85_99'] = 1000000000000 *  df.incidents_85_99 / (df.avail_seat_km)
    df['fatal_accidents_rate_85_99'] = 1000000000000 *  df.fatal_accidents_85_99 / (df.avail_seat_km)
    df['fatalities_rate_85_99'] = 1000000000000 *  df.fatalities_85_99 / (df.avail_seat_km)                                  
    df['incident_rate_00_14'] = 1000000000000 *  df.incidents_00_14 / (df.avail_seat_km)
    df['fatal_accidents_rate_00_14'] = 1000000000000 *  df.fatal_accidents_00_14 / (df.avail_seat_km)
    df['fatalities_rate_00_14'] = 1000000000000 *  df.fatalities_00_14 / (df.avail_seat_km)         

    return df

def period_map(time_period):
    if time_period == '85_99':
        return '1985-1999'
    else:
        return '2000-2014'

# Returns long data format where periods get their own rows
def get_long_data():
    df = get_data()

    cols = list(df.columns)
    cols.remove("airline")
    cols.remove("avail_seat_km_per_week")
    cols.remove("avail_seat_km")
    df_melt = pd.melt(df, id_vars=['airline', 'avail_seat_km'], value_vars=cols)

    # Extract period from the variable col
    df_melt['period'] = df_melt.variable.str.extract(r'_([0-9_]+)')

    # Clean up the variable column
    df_melt['period'] = df_melt.period.apply(lambda x : period_map(x))
    df_melt['variable'] = df_melt.variable.str.extract(r'([a-zA-Z_]+)')
    df_melt['variable'] = df_melt['variable'].apply(lambda x : x[0:len(x)-1])

    # Extract 1985 data
    df_melt_1985 = df_melt.loc[df_melt.period == '1985-1999']
    variable_types = df_melt.variable.unique()
    df1985 = df.loc[:, ['airline', 'avail_seat_km']]
    df1985['period'] = '1985-1999'

    for t in variable_types:
        sub_df = df_melt_1985.loc[df_melt_1985['variable'] == t,  ['airline', 'value']]
        sub_df.columns = ['airline', t]
        df1985 = df1985.merge(sub_df, how='left', on='airline')

    # Extract 2000 data
    df_melt_2000 = df_melt.loc[df_melt.period == '2000-2014']
    variable_types = df_melt.variable.unique()
    df2000 = df.loc[:, ['airline', 'avail_seat_km']]
    df2000['period'] = '2000-2014'

    for t in variable_types:
        sub_df = df_melt_2000.loc[df_melt_2000 ['variable'] == t,  ['airline', 'value']]
        sub_df.columns = ['airline', t]
        df2000 = df2000.merge(sub_df, how='left', on='airline')

    # combine 1985 and 2000
    df_clean = pd.concat([df2000, df1985])

    return df_clean

# Returns the top three closest airlines based on ASK based on the argument
def get_comp_airline(airline):
    # Recursive Query
    query = """
    SELECT
        airline 
        , comp_airline
    FROM
    (
        SELECT
            a.airline
            , a.avail_seat_km
            , a.comp_avail_seat_km
            , a.comp_airline
            , a.comp_percentage
            , ROW_NUMBER() OVER(PARTITION BY a.airline ORDER BY a.comp_percentage ASC) AS comp_rank
        FROM
        (
            SELECT
                a.airline
                , (a.avail_seat_km_per_week * 52 * 15) AS avail_seat_km
                , b.airline AS comp_airline
                , (b.avail_seat_km_per_week * 52 * 15) AS comp_avail_seat_km
                , ABS(CAST(((a.avail_seat_km_per_week * 52 * 15) - (b.avail_seat_km_per_week * 52 * 15)) AS float)) / (b.avail_seat_km_per_week * 52 * 15) AS comp_percentage
            FROM
                airline_safety AS a
                LEFT JOIN airline_safety AS b
                    ON a.airline != b.airline
        ) AS a
    )
    WHERE
        comp_rank IN (1, 2, 3)
    ;
    """
    conn = sqlite3.connect("data/airline")
    cur = conn.cursor()
    airline_comp = pd.read_sql_query(query, conn)
    conn.close()
    airline_comparison_list = list(airline_comp.loc[airline_comp['airline'] == airline , 'comp_airline'])


    return airline_comparison_list

# Returns the mean incident/fatal accidents rate by the two time periods
def get_period_mean_data():
    df_long = get_long_data()
    
    return df_long.groupby('period', as_index=False).agg({
        'incident_rate': 'mean',
        'fatal_accidents_rate': 'mean'
    }) 

# Returns an aggregated dataset by the two time periods & contains % of total information by the two major accident types (regular incident, fatal incidents)
def get_period_total_perc_data():
    df_long = get_long_data()
    period_total_perc = df_long.groupby('period', as_index=False).agg({
        'incidents': 'sum',
        'fatal_accidents': 'sum'
    })
    period_total_perc['total'] = period_total_perc.incidents + period_total_perc.fatal_accidents
    period_total_perc['perc_of_incidents'] = (period_total_perc.incidents / period_total_perc.total) * 100
    period_total_perc['perc_of_fatal_accidents'] = (period_total_perc.fatal_accidents / period_total_perc.total) * 100
    period_total_perc['display_incidents'] = period_total_perc.incidents.astype(str) + " - " + period_total_perc.perc_of_incidents.round(0).astype(str) + "%"
    period_total_perc['display_fatal_accidents'] = period_total_perc.fatal_accidents.astype(str) + " - " + period_total_perc.perc_of_fatal_accidents.round(0).astype(str) + "%"

    return period_total_perc

# For each airline get formatted % change data that can be displayed in a nice tabular manner
def get_formatted_fatal_rate_perc_changed_by_airline_data():
    df_fatal = get_data()
    df_fatal['Fatal Accidents Rate % Change'] = ((df_fatal.fatal_accidents_rate_00_14 - df_fatal.fatal_accidents_rate_85_99) \
                                                / df_fatal.fatal_accidents_rate_85_99 * 100)

    df_fatal = df_fatal.replace([np.inf, -np.inf], np.nan)    
    df_fatal.dropna(subset=["Fatal Accidents Rate % Change"], how = 'all', inplace = True)
    df_fatal['Fatal Accidents Rate % Change'] = df_fatal['Fatal Accidents Rate % Change'].apply(lambda i : "{0:.2f}%".format(i))
    df_fatal.sort_values(by='Fatal Accidents Rate % Change', ascending = False, inplace = True)

    return df_fatal

def get_formatted_incident_rate_perc_changed_by_airline_data():
    df_incidents = get_data()
    df_incidents['Incident Rate % Change'] = ((df_incidents.incident_rate_00_14 - df_incidents.incident_rate_85_99) \
                                        / df_incidents.incident_rate_85_99 * 100)

    df_incidents = df_incidents.replace([np.inf, -np.inf], np.nan)    
    df_incidents.dropna(subset=["Incident Rate % Change"], how = 'all', inplace = True)
    df_incidents['Incident Rate % Change'] = df_incidents['Incident Rate % Change'].apply(lambda i : "{0:.2f}%".format(i))
    df_incidents.sort_values(by='Incident Rate % Change', ascending = False, inplace = True)

    return df_incidents    