import gym
import numpy as np
from keras import layers
from keras.models import Model
from keras import backend as K
from keras import utils as np_utils
from keras import optimizers


class Agent(object):

    def __init__(self, input_dim, output_dim, hidden_dims=[32, 32]):
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.__build_network(input_dim, output_dim, hidden_dims)
        self.__build_train_fn()

    def __build_network(self, input_dim, output_dim, hidden_dims=[32, 32]):
        self.X = layers.Input(shape=(input_dim,))
        net = self.X

        for h_dim in hidden_dims:
            net = layers.Dense(h_dim)(net)
            net = layers.Activation("relu")(net)

        net = layers.Dense(output_dim)(net)
        net = layers.Activation("softmax")(net)

        self.model = Model(inputs=self.X, outputs=net)

    def __build_train_fn(self):
        action_prob_placeholder = self.model.output
        action_onehot_placeholder = K.placeholder(shape=(None, self.output_dim),
                                                  name="action_onehot")
        discount_reward_placeholder = K.placeholder(shape=(None,),
                                                    name="discount_reward")

        action_prob = K.sum(action_prob_placeholder * action_onehot_placeholder, axis=1)
        log_action_prob = K.log(action_prob)

        loss = - log_action_prob * discount_reward_placeholder
        loss = K.mean(loss)

        adam = optimizers.Adam()

        updates = adam.get_updates(params=self.model.trainable_weights,
                                   constraints=[],
                                   loss=loss)

        self.train_fn = K.function(inputs=[self.model.input,
                                           action_onehot_placeholder,
                                           discount_reward_placeholder],
                                   outputs=[],
                                   updates=updates)

    def get_action(self, state):
        shape = state.shape

        if len(shape) == 1:
            assert shape == (self.input_dim,), "{} != {}".format(shape, self.input_dim)
            state = np.expand_dims(state, axis=0)

        elif len(shape) == 2:
            assert shape[1] == (self.input_dim), "{} != {}".format(shape, self.input_dim)

        else:
            raise TypeError("Wrong state shape is given: {}".format(state.shape))

        action_prob = np.squeeze(self.model.predict(state))
        assert len(action_prob) == self.output_dim, "{} != {}".format(len(action_prob), self.output_dim)
        return np.random.choice(np.arange(self.output_dim), p=action_prob)

    def fit(self, S, A, R):
        action_onehot = np_utils.to_categorical(A, num_classes=self.output_dim)
        discount_reward = compute_discounted_R(R)

        assert S.shape[1] == self.input_dim, "{} != {}".format(S.shape[1], self.input_dim)
        assert action_onehot.shape[0] == S.shape[0], "{} != {}".format(action_onehot.shape[0], S.shape[0])
        assert action_onehot.shape[1] == self.output_dim, "{} != {}".format(action_onehot.shape[1], self.output_dim)
        assert len(discount_reward.shape) == 1, "{} != 1".format(len(discount_reward.shape))

        self.train_fn([S, action_onehot, discount_reward])


def compute_discounted_R(R, discount_rate=.99):
    discounted_r = np.zeros_like(R, dtype=np.float32)
    running_add = 0
    for t in reversed(range(len(R))):

        running_add = running_add * discount_rate + R[t]
        discounted_r[t] = running_add

    discounted_r -= discounted_r.mean() / discounted_r.std()

    return discounted_r


def run_episode(env, agent):
    done = False
    S = []
    A = []
    R = []

    s = env.reset()

    total_reward = 0

    while not done:

        a = agent.get_action(s)

        s2, r, done, info = env.step(a)
        total_reward += r

        S.append(s)
        A.append(a)
        R.append(r)

        s = s2

        if done:
            S = np.array(S)
            A = np.array(A)
            R = np.array(R)

            agent.fit(S, A, R)

    return total_reward


def main():
    try:
        env = gym.make("CartPole-v1")
        input_dim = env.observation_space.shape[0]
        output_dim = env.action_space.n
        agent = Agent(input_dim, output_dim, [16, 16])

        for episode in range(2000):
            reward = run_episode(env, agent)
            print(episode, reward)

    finally:
        env.close()


if __name__ == '__main__':
    main()