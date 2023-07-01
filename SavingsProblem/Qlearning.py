import numpy as np
import copy

class Qlearning():
    def __init__(self, n_states, n_actions, alpha = 1, gamma = 0.9, epsilon = 0.9, epsilon_decay = 0.99977, epsilon_min = 0.1): #learning rate should be 1 because deterministic code now. 
        # number of actions
        self.n_actions = n_actions

        # number of states
        self.n_states = n_states

        # setup the environment
        self.q_table = np.full([self.n_states, self.n_actions], fill_value= -10000.0)
        self.q_table1  = np.full([self.n_states, self.n_actions], fill_value= 0.0)
        print(self.q_table)
        self.number_of_times_state_action_pair_visited = np.zeros([self.n_states, self.n_actions])

        # discount factor
        self.gamma = gamma
        #self.alpha = alpha
        self.t = 1

        # 90% exploration, 10% exploitation
        self.epsilon = epsilon
        # exploration decays by this factor every episode
        self.epsilon_decay = epsilon_decay
        # in the long run, 10% exploration, 90% exploitation
        self.epsilon_min = epsilon_min

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


    # Q-Learning - update the Q Table using Q(s, a), but this is a full update for alpha is 1 (alpha is the learning rate) now alpha is added
    def update_q_table(self, state, action, reward, next_state):
        # Q(s, a) = reward + gamma * max_a' Q(s', a')
        #print(state, action, reward, next_state)
        if next_state == self.n_states:
            new_q_value = reward
        else:
            if np.amax(self.q_table[next_state]) == -10000.0:
                new_q_value = 0
            else:
                new_q_value = self.gamma * np.amax(self.q_table[next_state])

            #print(new_q_value)
            #print(reward)
            new_q_value += reward
            #print(new_q_value)
        #print(self.alpha * new_q_value)
        #print(((1 - self.alpha) * self.q_table[state, action]) + self.alpha * new_q_value)
        # compute alpha for this state action pair
        self.number_of_times_state_action_pair_visited[state, action] += 1
        alpha = 1 / (np.power((self.number_of_times_state_action_pair_visited[state, action]), 0.85))

        self.q_table[state, action] = ((1 - alpha) * self.q_table1[state, action]) + alpha * new_q_value
        self.q_table1[state, action] = ((1 - alpha) * self.q_table1[state, action]) + alpha * new_q_value
        
        #print('here', self.q_table[state, action])

    # UI to dump Q Table contents
    def print_q_table(self):
        print("Q-Table (Epsilon: %0.2f)" % self.epsilon)
        print(self.q_table)


    # update Exploration-Exploitation mix
    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        #if self.t < 10000:
        #    self.epsilon *= self.epsilon_decay
        #else:
        #    self.epsilon = np.power(1/copy.deepcopy(self.t), 0.1)
        #self.t += 1

