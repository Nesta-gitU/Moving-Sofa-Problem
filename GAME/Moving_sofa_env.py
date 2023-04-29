import Board
import Shape
import gymnasium as gym


class Moving_sofa_env(gym.Env):
    metadata = {"render_modes": []} #only allow not rendering (= None) for optimal cloud compatibility

    def __init__(self) -> None:
        self.board = Board()
        self.shape = Shape()

        self.render_mode = None

        self.action_space = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        self.state_space = [(1,2), (1,3), (2,5)] # (x,y) of the boxes that make up the states. FIRST STATE SHOULD BE INITIAL STATE
        
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Reset the board and shape
        self.board = Board()
        self.shape = Shape()

        # reset should return the initial state and some information
        info = {}
        state = self.state_space[0]

        return state, info
    
    def step(self, action):
        previous_distance = self.board.get_distance_value(self.shape)

        # take action
        self.shape.rotate(self.board, degrees = action)
        self.shape.moveForward(self.board, distance = self.board.h)

        # get reward
        reward = self.board.get_distance_value(self.shape) - previous_distance
        
        # get state
        state = self.state_space[1] # @TODO: check in which state the new shape ends up return that state 

        # check if done
        done = self.board.is_finished(self.shape)

        # get info
        info = {}

        return state, reward, done, info