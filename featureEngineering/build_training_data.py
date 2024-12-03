import pandas as pd

class TrainingDataBuilder:

    def __init__(self, tracking_week_numbers):

        self.tracking_week_numbers = tracking_week_numbers
        self.pass_play_df = self._get_pass_plays()
        self.route_runner_df = self._get_route_runners_on_pass_plays()
        self.route_runner_with_tracking_df = self._get_tracking_data_on_routes_at_time_of_throw()
        self._calculate_distance()

    def _get_pass_plays(self):

        result_cols = ["gameId", "playId", "quarter", "down", "yardsToGo", "possessionTeam", "playNullifiedByPenalty", 
                       "offenseFormation", "receiverAlignment", "passResult", "playAction",
                       "timeToThrow"]

        play_df = pd.read_parquet("data\plays.parquet")

        pass_play_df = play_df[~play_df["passResult"].isin(['S','R'])]
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
                tracking_df['week'] = week
            
            elif index > 0:

                current_df = pd.read_parquet(f"data\\tracking_week_{week}.parquet")
                current_df['week'] = week

                tracking_df = pd.concat([tracking_df, current_df])
        
        pass_play_id_df = self.pass_play_df[["gameId", "playId"]]

        tracking_pass_play_df = pd.merge(tracking_df, pass_play_id_df, on = ["gameId", "playId"], how = "inner")

        return tracking_pass_play_df
    
    def _get_tracking_data_on_routes_at_time_of_throw(self):

        tracking_pass_play_df = self._get_passing_tracking_plays()
        tracking_pass_play_df = tracking_pass_play_df[tracking_pass_play_df['event'] == 'pass_forward']

        tracking_pass_play_df = tracking_pass_play_df[["gameId", "playId", "nflId", "week", "x", "y"]]

        route_runner_tracking_df = pd.merge(self.route_runner_df, tracking_pass_play_df, 
                                            on = ["gameId", "playId", "nflId"], how = "left")
        
        route_runner_tracking_df = route_runner_tracking_df.rename(columns = {"x" : "receiver_x",
                                                                              "y" : "receiver_y"})
        
        tracking_pass_play_df = tracking_pass_play_df.rename(columns = {"nflId" : "defender_nflId"})

        route_runner_tracking_df = pd.merge(route_runner_tracking_df, tracking_pass_play_df, 
                                            on = ["gameId", "playId", "defender_nflId", "week"], how = "left")
        
        route_runner_tracking_df = route_runner_tracking_df.rename(columns = {"x" : "defender_x",
                                                                              "y" : "defender_y"})
        
        return route_runner_tracking_df
    
    def _calculate_distance(self):

        self.route_runner_with_tracking_df["defensive_x_distance_from_target"] = self.route_runner_with_tracking_df['receiver_x'] - self.route_runner_with_tracking_df['defender_x']
        self.route_runner_with_tracking_df["defensive_y_distance_from_target"] = self.route_runner_with_tracking_df['receiver_y'] - self.route_runner_with_tracking_df['defender_y']

        self.route_runner_with_tracking_df["defensive_distance_from_target"] = self.route_runner_with_tracking_df["defensive_x_distance_from_target"]**2 + self.route_runner_with_tracking_df["defensive_y_distance_from_target"]**2

        self.route_runner_with_tracking_df["defensive_distance_from_target"] = self.route_runner_with_tracking_df["defensive_distance_from_target"]**.5


        




test = TrainingDataBuilder([1, 2])

#test_df = test._get_passing_tracking_plays()

#print(test_df['event'].unique())

print(test.route_runner_with_tracking_df.shape)