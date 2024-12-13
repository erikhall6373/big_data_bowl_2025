import pandas as pd




def get_players_in_motion_from_feature_set():

    feature_set_df = pd.read_parquet("data\separation_yardage_feature_data.parquet")
    feature_set_df = feature_set_df[feature_set_df['motionSinceLineset'] == True]

    result_df = feature_set_df[['gameId', 'playId', 'nflId']]

    return result_df.drop_duplicates()

def get_tracking_data():
        
    weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
    for index, week in enumerate(weeks):

        if index == 0:

            tracking_df = pd.read_parquet(f"data\\tracking_week_{week}.parquet")
            
        elif index > 0:

            current_df = pd.read_parquet(f"data\\tracking_week_{week}.parquet")

            tracking_df = pd.concat([tracking_df, current_df])

    return tracking_df


def get_motion_tracking_data():

    player_motion_df = get_players_in_motion_from_feature_set()

    tracking_df = get_tracking_data()

    result_df = pd.merge(tracking_df, player_motion_df, on = ['gameId', 'playId', 'nflId'])

    return result_df

motion_tracking_df = get_motion_tracking_data()

motion_tracking_df.to_parquet("data\motion_tracking.parquet")

