import pandas as pd

def create_timeline_df(df):
    df_list = []
    for row in df.itertuples(index=False):
        organization = row.organization
        position = row.position
        experience_type = row.experience_type
        location = row.location
        begin_date = row.begin_date
        end_date = row.end_date

        df_tmp = pd.DataFrame({'organization':organization,
                   'position':position,
                    'experience_type':experience_type,
                    'location':location,
                   'date':pd.date_range(begin_date, end_date,freq='D')})
        df_list.append(df_tmp)

    df = pd.concat(df_list)
    df.sort_values('date',inplace=True)

    return(df)
