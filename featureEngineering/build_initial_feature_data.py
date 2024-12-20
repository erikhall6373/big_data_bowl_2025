import pandas as pd

class FeatureDataBuilder:

    def __init__(self, tracking_week_numbers):

        self.tracking_week_numbers = tracking_week_numbers
        self.pass_play_df = self._get_pass_plays()
        self.route_runner_df = self._get_route_runners_on_pass_plays()
        self.feature_data_df = self._build_feature_data()

    def _get_pass_plays(self):

        result_cols = ["gameId", "playId", "quarter", "down", "yardsToGo", "possessionTeam", "playNullifiedByPenalty", 
                       "offenseFormation", "receiverAlignment", "passResult", "playAction",
                       "timeToThrow"]

        play_df = pd.read_parquet("data\plays.parquet")

        pass_play_df = play_df[~play_df["passResult"].isin(['R'])]
        pass_play_df = play_df[play_df["passResult"].notnull()]

        return pass_play_df[result_cols]
    
    
    def _get_primary_defenders_on_pass_plays(self):

        result_cols = ["gameId", "playId", "nflId", "pff_primaryDefensiveCoverageMatchupNflId"]

        player_play_df = pd.read_parquet("data\player_play.parquet")

        pass_play_id_df = self.pass_play_df[["gameId", "playId"]]

        route_defender_df = pd.merge(player_play_df, pass_play_id_df, on = ["gameId", "playId"], how = "inner")

        route_defender_df = route_defender_df[result_cols]

        route_defender_df = route_defender_df.rename(columns = {"nflId" : "defender_nflId",
                                                                "pff_primaryDefensiveCoverageMatchupNflId" : "nflId"})
        
        return route_defender_df
    
    def _get_route_runners_on_pass_plays(self):

        result_cols = ["gameId", "playId", "nflId", "teamAbbr", "inMotionAtBallSnap",
                       "shiftSinceLineset", "motionSinceLineset", "wasRunningRoute",
                       "routeRan", "defender_nflId"]

        player_play_df = pd.read_parquet("data\player_play.parquet")

        pass_play_id_df = self.pass_play_df[["gameId", "playId"]]

        route_runner_df = pd.merge(player_play_df, pass_play_id_df, on = ["gameId", "playId"], how = "inner")
        route_runner_df = route_runner_df[route_runner_df["wasRunningRoute"] == 1]

        route_defender_df = self._get_primary_defenders_on_pass_plays()

        route_runner_df = pd.merge(route_runner_df, route_defender_df, on = ["gameId", "playId", "nflId"], how = "inner")

        return route_runner_df[result_cols]
    
    def _get_passing_tracking_plays(self):
        
        for index, week in enumerate(self.tracking_week_numbers):

            if index == 0:

                tracking_df = pd.read_parquet(f"data\\tracking_week_{week}.parquet")
            
            elif index > 0:

                current_df = pd.read_parquet(f"data\\tracking_week_{week}.parquet")

                tracking_df = pd.concat([tracking_df, current_df])
        
        pass_play_id_df = self.pass_play_df[["gameId", "playId"]]

        tracking_pass_play_df = pd.merge(tracking_df, pass_play_id_df, on = ["gameId", "playId"], how = "inner")

        return tracking_pass_play_df
    
    def _create_3_secs_post_snap_event(self, passing_tracking_plays):

        ball_snap_df = passing_tracking_plays[passing_tracking_plays['event'].isin(['ball_snap'])].copy()
        three_secs_post_ball_snap_df = ball_snap_df[['gameId', 'playId', 'frameId']].copy().drop_duplicates()

        three_secs_post_ball_snap_df['frameId'] = three_secs_post_ball_snap_df['frameId'] + 30

        three_secs_post_ball_snap_df['three_secs_post_snap_event'] = 'three_secs_post_snap'

        result_df = passing_tracking_plays.merge(three_secs_post_ball_snap_df, on = ['gameId', 'playId', 'frameId'], how = 'left')

        result_df['event'] = result_df['event'].combine_first(result_df['three_secs_post_snap_event'])
        result_df = result_df.drop(columns = ['three_secs_post_snap_event'])

        return result_df
    
    def _get_tracking_data_on_routes_at_time_of_throw(self):

        result_cols = ['gameId', 'playId', 'nflId', 'event', 'frameId', 'receiver_x', 'receiver_y', 'defender_x', 'defender_y',
                       "receiver_s", "defender_s", "receiver_dir", "defender_dir"]

        tracking_pass_play_df = self._get_passing_tracking_plays()
        tracking_pass_play_df = self._create_3_secs_post_snap_event(tracking_pass_play_df)
        tracking_pass_play_df = tracking_pass_play_df[tracking_pass_play_df['event'].isin(['line_set', 'pass_forward', 'qb_sack', 'ball_snap', 'three_secs_post_snap'])]

        tracking_pass_play_df = tracking_pass_play_df[["gameId", "playId", "nflId", "x", "y", "s", "dir", "event", "frameId"]]

        route_runner_tracking_df = pd.merge(self.route_runner_df, tracking_pass_play_df, 
                                            on = ["gameId", "playId", "nflId"], how = "inner")
        
        route_runner_tracking_df = route_runner_tracking_df.rename(columns = {"x" : "receiver_x",
                                                                              "y" : "receiver_y",
                                                                              "s" : "receiver_s",
                                                                              "dir" : "receiver_dir"})
        
        tracking_pass_play_df = tracking_pass_play_df.rename(columns = {"nflId" : "defender_nflId"})

        route_runner_tracking_df = pd.merge(route_runner_tracking_df, tracking_pass_play_df, 
                                            on = ["gameId", "playId", "defender_nflId", "event", "frameId"], how = "inner")
        
        route_runner_tracking_df = route_runner_tracking_df.rename(columns = {"x" : "defender_x",
                                                                              "y" : "defender_y",
                                                                              "s" : "defender_s",
                                                                              "dir" : "defender_dir"})
        
        return route_runner_tracking_df[result_cols]
    
    def _calculate_distance(self):

        self.route_runner_with_tracking_df["x_separation_yardage"] = self.route_runner_with_tracking_df['receiver_x'] - self.route_runner_with_tracking_df['defender_x']
        self.route_runner_with_tracking_df["y_separation_yardage"] = self.route_runner_with_tracking_df['receiver_y'] - self.route_runner_with_tracking_df['defender_y']

        self.route_runner_with_tracking_df["separation_yardage"] = self.route_runner_with_tracking_df["x_separation_yardage"]**2 + self.route_runner_with_tracking_df["y_separation_yardage"]**2

        self.route_runner_with_tracking_df["separation_yardage"] = self.route_runner_with_tracking_df["separation_yardage"]**.5

    
    def _build_feature_data(self):

        result_cols = ["gameId", "playId", 'event', 'frameId', "quarter", "down", "yardsToGo", "possessionTeam", "playNullifiedByPenalty", 
                       "offenseFormation", "receiverAlignment", "passResult", "playAction",
                       "timeToThrow", "nflId", "teamAbbr", "inMotionAtBallSnap",
                       "shiftSinceLineset", "motionSinceLineset", "wasRunningRoute",
                       "routeRan", "defender_nflId", "separation_yardage", "receiver_x", "receiver_y", "receiver_s", "receiver_dir",
                       "defender_x", "defender_y", "defender_s", "defender_dir"]
        
        result_df = pd.merge(self.pass_play_df, self.route_runner_df, on = ["gameId", "playId"], how = 'left')

        self.route_runner_with_tracking_df = self._get_tracking_data_on_routes_at_time_of_throw()
        self._calculate_distance()

        result_df = pd.merge(result_df, self.route_runner_with_tracking_df, on = ["gameId", "playId", "nflId"], how = "left")
        result_df = result_df[~result_df["defender_nflId"].isnull()]
        result_df = result_df[~result_df["event"].isnull()]

        return result_df[result_cols]
    
    def write_feature_data(self):

        self.feature_data_df.to_parquet("data\initial_separation_yardage_feature_data.parquet")


FeatureData = FeatureDataBuilder(list(range(1, 9)))
FeatureData.write_feature_data()