import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# Global Variables
NUM_PLAYERS = 100 # Total players in the simulation
ODDS_WIN = 0.50 # Base chance for each player to win
OUTCOMES = ['W', 'L'] # Possible outcomes of each match
ROUNDS = 100 # Number of round one player will play every other player
WIN_WEIGHT = 0.01 # How much a win increase the chance for the player to win in the future

# Have each player play against every other player once per round
def play_games(player_odds, rounds):
    for k in range(rounds):
        for i in range(len(player_odds)):
            for j in range(len(player_odds)):
                if (i != j): # Ensure each player does not play themselves
                    p1_win = matches(player_odds[i][0], player_odds[j][0], player_odds[i][1], player_odds[j][1])

                    # Update Games Won and Games Lost for each player in the round
                    if p1_win: 
                        player_odds[i][2] += 1
                        player_odds[j][3] += 1
                    else:
                        player_odds[i][3] += 1
                        player_odds[j][2] += 1
        
        # After each round, update the probability of winning for each player
        for u in range(len(player_odds)):
            player_odds[u][1] = win_chance(player_odds[u][2], player_odds[u][3])


    return player_odds

# Define the logic of how each match will decide a winner
def matches(p1, p2, prob1, prob2):
    p1_game_won = None
    if prob1 < prob2: # If probability 1 is less likely than probability 2, if a random number is less than or equal to probability 1, then player 1 wins 
        if random.randint(0, 1) <= prob1:
            p1_game_won = True
    elif prob1 > prob2:
        if random.randint(0, 1) <= prob2: # Same as above but for player 2
            p1_game_won = False
    else: # If the probabilites are the same, randomly choose which player wins
        winner = random.choice((p1, p2)) 
        if winner == p1:
            p1_game_won = True

    return p1_game_won

# Players who win more matchs are given a better chance at winning. Losing matches lowers the chance of winning future matches
def win_chance(games_won, games_lost):
    odds = ODDS_WIN + (((games_won - games_lost)) * WIN_WEIGHT) # Base odds are set at 50%, and is adjusted by the difference between matches won and lost, adjusted by a weight factor

    # if the odds are too high or too low, change the odds to a set number so that losses and wins are not 100% guarunteed for any player
    if odds <= 0:
        odds = 0.01
    elif odds >= 1:
        odds = 0.99
    
    return odds

# Calculates general statistical values of data
def calculate_stats(data):
    mean_val = round(data.mean(), 2)
    median_val = round(data.median(), 2)
    std_val = round(data.std(), 2)

    vals = [mean_val, median_val, std_val]

    return vals

# Run all functions and define parameters
def main():
    # Generate list of players
    players = np.arange(1, NUM_PLAYERS + 1).tolist()

    # Generate Odds of Winning per player
    odds = [ODDS_WIN] * len(players)

    # Generate games won/lost
    games_won = [0] * len(players)
    games_lost = [0] * len(players)

    # zip lists together
    player_odds = list(zip(players, odds, games_won, games_lost))
    player_odds = [list(i) for i in player_odds]
    #print(player_odds[0][0])

    # Sort dataframe in player order of who won the most matches
    final_score = play_games(player_odds, ROUNDS)
    final_df = pd.DataFrame(final_score, columns = ['Player ID', 'Chance to Win', 'Games Won', 'Games Lost'])
    final_df = final_df.sort_values('Games Won', ascending = False)
    print(final_df)

    # Calculate stats of the simulation
    chance_to_win_stats = calculate_stats(final_df['Chance to Win'])
    games_won_stats = calculate_stats(final_df['Games Won'])
    games_lost_stats = calculate_stats(final_df['Games Lost'])

    print(f'The mean chance to win for players was {chance_to_win_stats[0]}, with a median of {chance_to_win_stats[1]}, and a standard deviation of {chance_to_win_stats[2]}.')
    print(f'The mean games won for players was {games_won_stats[0]}, with a median of {games_won_stats[1]}, and a standard deviation of {games_won_stats[2]}.')
    print(f'The mean games lost for players was {games_lost_stats[0]}, with a median of {games_lost_stats[1]}, and a standard deviation of {games_lost_stats[2]}.')

main()