import numpy as np

class Qlearning():
    def __init__(self, n_states, n_actions, gamma = 0.9, epsilon = 0.9, epsilon_decay = 0.9, epsilon_min = 0.1):
        # number of actions
        self.n_actions = n_actions

        # number of states
        self.n_states = n_states

        # setup the environment
        self.q_table = np.zeros([self.n_states, self.n_actions])

        # discount factor
        self.gamma = gamma

        # 90% exploration, 10% exploitation
        self.epsilon = 0.9
        # exploration decays by this factor every episode
        self.epsilon_decay = 0.9
        # in the long run, 10% exploration, 90% exploitation
        self.epsilon_min = 0.1

        self.is_explore = True
    
    # determine the next action
    def get_action(self, state):
        # action is from exploration
        if np.random.rand() <= self.epsilon:
            # explore - do random action
            self.is_explore = True
            return np.random.choice(self.n_actions,1)[0] ### @TODO change hardcoded numbers: chooses from [0, 1, 2, ..., self.n_actions-1]

        # or action is from exploitation
        # exploit - choose action with max Q-value
        self.is_explore = False
        return np.argmax(self.q_table[state]) # returns the number of the action with the highest Q-value, so actions need to be identified by numbers for this to work


    # Q-Learning - update the Q Table using Q(s, a)
    def update_q_table(self, state, action, reward, next_state):
        # Q(s, a) = reward + gamma * max_a' Q(s', a')
        q_value = self.gamma * np.amax(self.q_table[next_state])
        q_value += reward
        self.q_table[state, action] = q_value


    # UI to dump Q Table contents
    def print_q_table(self):
        print("Q-Table (Epsilon: %0.2f)" % self.epsilon)
        print(self.q_table)


    # update Exploration-Exploitation mix
    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

