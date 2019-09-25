import random
import pandas as pd
import numpy as np


class Environment:
    def __init__(self):
        self.data = pd.read_csv('data/stock_data_features.csv', encoding='utf-8')
        self.steps_left = len(self.data)
        self.position = 0
        self.active_data = self.data.iloc[0:]
        self.total_reward = 0.0

    def get_observation(self):
        rsi = self.active_data.iloc[self.position]['RSI']
        open_close = self.active_data.iloc[self.position]['open_close']
        open_high = self.active_data.iloc[self.position]['open_high']
        open_low = self.active_data.iloc[self.position]['open_low']
        obs = [rsi, open_close, open_high, open_low]
        print(obs)
        return obs

    def get_obs_space(self):
        return len(self.data.columns) - 1

    def reset(self):
        start = random.randint(0, len(self.data) - 10)
        self.active_data = self.data.iloc[start:]
        self.position = 0
        self.total_reward = 0.0
        self.steps_left = len(self.active_data) - 1
        return self.get_observation()

    def get_actions(self):
        return [0, 1]

    def get_action_space(self):
        return len(self.get_actions())

    def is_done(self):
        return self.steps_left == 0

    def action(self, action):
        if self.is_done():
            raise Exception("Game is over")
        self.steps_left -= 1
        return random.random()

    def step(self, action):
        self.position += 1
        next_obs = self.get_observation()
        reward = 0
        if action == self.active_data.iloc[self.position]['color']:
            reward = 1
        self.steps_left -= 1
        is_done = self.is_done()
        return next_obs, reward, is_done, ''



class Agent:
    def __init__(self):
        self.total_reward = 0.0

    def step(self, env):
        current_obs = env.get_observation()
        actions = env.get_actions()
        reward = env.action(random.choice(actions))
        self.total_reward += reward


if __name__ == "__main__":
    env = Environment()
    agent = Agent()

    while not env.is_done():
        agent.step(env)

    print("Total reward got: %.4f" % agent.total_reward)
