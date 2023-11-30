import pandas as pd

def create_timeline_df(df):
    """
    Create a timeline DataFrame from a given DataFrame with date ranges.

    This function takes a DataFrame containing experience data with start and 
    end dates, and expands it into a continuous timeline format with each row 
    representing a day.

    Args:
        df (pandas.DataFrame): A DataFrame containing columns 'organization', 
                               'position', 'experience_type', 'location', 
                               'begin_date', and 'end_date'.

    Returns:
        pandas.DataFrame: An expanded DataFrame where each row corresponds to 
                          a day in the range from 'begin_date' to 'end_date' 
                          for each entry in the input DataFrame.
    """
    df_list = []
    for row in df.itertuples(index=False):
        df_tmp = pd.DataFrame({
            'organization': row.organization,
            'position': row.position,
            'experience_type': row.experience_type,
            'location': row.location,
            'date': pd.date_range(row.begin_date, row.end_date, freq='D')
        })
        df_list.append(df_tmp)

    timeline_df = pd.concat(df_list)
    timeline_df.sort_values('date', inplace=True)

    return timeline_df


def transform_skills_data(csv_path, num_steps=13):
    """
    Transform and interpolate a DataFrame of skills data over time.

    This function reads a CSV file containing skills data, reshapes it,
    and performs interpolation to fill in data points between years.

    Args:
        csv_path (str): Path to the CSV file to read.
        num_steps (int): Number of steps for interpolation between years.

    Returns:
        pandas.DataFrame: Transformed DataFrame with interpolated values.
    """

    df_skills = pd.read_csv(csv_path)
    df_skills = df_skills.melt(id_vars='Year', var_name='Skill', value_name='Rating')

    def interpolate_rows(row1, row2):
        """
        Interpolate data points between two rows.

        Args:
            row1, row2 (dict): Rows between which to interpolate.

        Returns:
            list: List of interpolated dictionaries.
        """
        delta = (row2['Rating'] - row1['Rating']) / (num_steps + 1)
        return [
            {'Year': row1['Year'] + (i / (num_steps + 1)),
             'Skill': row1['Skill'],
             'Rating': row1['Rating'] + i * delta}
            for i in range(1, num_steps + 1)
        ]

    new_rows = []
    for i in range(len(df_skills) - 1):
        current_row = df_skills.iloc[i]
        next_row = df_skills.iloc[i + 1]

        if current_row['Year'] + 1 == next_row['Year'] and current_row['Skill'] == next_row['Skill']:
            new_rows.extend(interpolate_rows(current_row, next_row))

    df_interpolated = pd.DataFrame(new_rows)
    df_skills = pd.concat([df_skills, df_interpolated]).sort_values(by=['Year', 'Skill'])

    return df_skills
