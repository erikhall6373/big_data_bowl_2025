
import pandas as pd
import numpy as np
from pandasql import sqldf



def get_frame_Id_for_lineset_and_snap(motion_tracking_df):

    lineset_df = motion_tracking_df[motion_tracking_df['event'].isin(['line_set'])].copy()
    ball_snap_df = motion_tracking_df[motion_tracking_df['event'].isin(['ball_snap'])].copy()


    lineset_df = lineset_df[['gameId', 'playId', 'nflId', 'frameId']].rename(columns = {'frameId' : 'lineSetFrameId'})
    ball_snap_df = ball_snap_df[['gameId', 'playId', 'nflId', 'frameId']].rename(columns = {'frameId' : 'ballsnapFrameId'})

    result_df = pd.merge(lineset_df, ball_snap_df, on = ['gameId', 'playId', 'nflId'], how = 'inner')

    return result_df

def filter_and_sort_motion_tracking(motion_tracking_df):

    lineset_and_snap_frames = get_frame_Id_for_lineset_and_snap(motion_tracking_df)

    result_df = pd.merge(motion_tracking_df, lineset_and_snap_frames, on = ['gameId', 'playId', 'nflId'], how = 'inner')

    result_df = result_df[result_df['frameId'] >= result_df['lineSetFrameId']]
    result_df = result_df[result_df['frameId'] <= result_df['ballsnapFrameId']]

    result_df['dis'] = np.where(result_df['frameId'] == result_df['lineSetFrameId'], 0, result_df['dis'])

    return result_df

def calculate_cumulative_distance_before_snap(motion_tracking_df):

    frame_filtered_df = filter_and_sort_motion_tracking(motion_tracking_df)

    result_df = sqldf("""
    SELECT *,
    SUM(dis) OVER (PARTITION BY gameId, playId, nflId ORDER BY frameId) AS running_distance
    FROM frame_filtered_df
    """)

    result_df = sqldf("""
    SELECT *,
    LAST_VALUE(running_distance) OVER (PARTITION BY gameId, playId, nflId) AS cumulative_motion_distance
    FROM result_df
    """)

    return result_df[["gameId", "playId", "nflId", "cumulative_motion_distance"]].drop_duplicates()


motion_tracking_df = pd.read_parquet(("data\motion_tracking.parquet"))
cumulative_distance_df = calculate_cumulative_distance_before_snap(motion_tracking_df)
feature_set_df = pd.read_parquet("data\initial_separation_yardage_feature_data.parquet")

feature_set_with_cumulative_motion_df = pd.merge(feature_set_df, cumulative_distance_df, on = ["gameId", "playId", "nflId"], how = 'left')

feature_set_with_cumulative_motion_df.to_parquet("data\\updated_separation_yardage_feature_data.parquet")