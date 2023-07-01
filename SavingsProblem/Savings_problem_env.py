import gymnasium as gym
import numpy as np
import copy 
import math

class Savings_problem_env(gym.Env):
    metadata = {"render_modes": []} #only allow not rendering (= None) for optimal cloud compatibility

    def __init__(self, number_of_epochs) -> None:
        self.render_mode = None
        self.current_assets = 0
        self.interest = 0.07 # 7% interest rate
        self.number_of_retired_years = 2
        self.number_of_epochs = number_of_epochs
        self.get_income(epoch = 0)

        self.number_of_state_buckets = 10
        self.asset_upper = 2
        self.asset_lower = 0 # 0 because no borrowing allowed so the interval is [0, 2) divided into 24 buckets + 1 bucket [2, inf)

        #                    0       1     2    3     4    5    6   7    8   9   10  11   12  13   14  15   16   17  18  19
        self.action_space = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, 1] # 20 actions, each action is a percentage of assets to consume

        self.state_space = np.reshape(a = np.arange(self.number_of_state_buckets * number_of_epochs), newshape = (self.number_of_state_buckets, number_of_epochs)) 
        print(self.state_space)

        #self.state_space = np.arange(number_of_epochs) # (x,y) of the boxes that make up the states. FIRST STATE SHOULD BE INITIAL STATE
        self.current_epoch = 0
        
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
    
        # reset should return the initial state and some information
        info = {}

        self.current_assets = 0
        self.current_epoch = 0
        self.get_income(epoch = 0)
        state = self.get_state_index(self.current_assets)

        return state, info
    
    def step(self, action, epoch):
        # take action
        #print(self.current_state)
        amount_consumed = self.current_assets * action # since action is consuming a percentage of assets
        
        # get reward
        reward = self.get_reward(amount_consumed)
        
        #reward = self.get_robust_reward(action)

        # get info
        info = {'amount consumed': amount_consumed}

        # set new current assets
        self.current_assets = self.current_assets - amount_consumed

        # update current epoch this is before calculating the next state because the next state is (next_assets, next_epoch)
        self.current_epoch += 1 

        # get income and interest to determine next state
        self.update_before_epoch(epoch)

        if self.current_epoch == self.number_of_epochs:
            next_state = None
        else:    
            #print(self.current_epoch)
            # set next state
            next_state = self.get_state_index(self.current_assets)

        return next_state, reward, False, False, info # actually the first one should be a number 
    
    def get_reward(self, amount_consumed):
        utility = -math.exp(-amount_consumed)

        return utility
    
    def get_robust_reward(self, action):
        robust_amound_consumed = 0

        upperbounds = np.linspace(self.asset_lower, self.asset_upper, num=self.number_of_state_buckets)

        if self.current_assets >= self.asset_upper: 
            robust_amound_consumed = 2
        elif self.current_assets < self.asset_lower:
            robust_amound_consumed = 0 
        else:
            for i, upperbound in enumerate(upperbounds): # Theoratically i is 0 should be passed but the if statement does that for us
                if self.current_assets < upperbound:
                    robust_amound_consumed = upperbounds[i-1]
                    break
        
        
        robust_amound_consumed = action * robust_amound_consumed

        robust_utility = -math.exp(-robust_amound_consumed)
        return robust_utility
    
    def get_state_index(self, current_assets):
        upperbounds = np.linspace(self.asset_lower, self.asset_upper, num=self.number_of_state_buckets)
        #print(buckets)

        if current_assets >= self.asset_upper: 
            return self.state_space[-1, self.current_epoch]
        elif current_assets < self.asset_lower:
            return self.state_space[0, self.current_epoch]
        else:
            for i, upperbound in enumerate(upperbounds): # Theoratically i is 0 should be passed but the if statement does that for us
                if current_assets < upperbound:
                    #print(i-1)
                    #print('current_assets',current_assets, ' to', i-1)
                    #print(upperbound)
                    return self.state_space[i-1, self.current_epoch]
    
    def get_income(self, epoch):
        if epoch >= self.number_of_epochs - self.number_of_retired_years:
            income = 0
        else:
            income = math.pow(1.05, epoch)  # 5% increase in income every year. epoch starts at 0 so is t-1

        self.current_assets += income

    def get_interest(self):
        self.current_assets = self.current_assets * (1 + self.interest)

    def update_before_epoch(self, epoch):
        self.get_interest() # update interest before getting income
        self.get_income(epoch) # update income 