"""Pong Joystick Agent."""
import pygame
import numpy as np
import time

#####################################
# Change these to match your joystick
UP_AXIS = 4
SIDE_AXIS = 3
#####################################


class PongJoystickActor(object):
    """Joystick Controller for Pong."""

    def __init__(self, env, fps=50):
        """Init."""
        # if env.num_envs > 1:
        #     raise ValueError("Only one env can be controlled with the joystick.")
        self.env = env
        self.human_agent_action = np.array([0], dtype=np.int32)  # noop
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        # if len(joysticks) != 1:
        #     raise ValueError("There must be exactly 1 joystick connected."
        #                      f"Found {len(joysticks)}")
        # print(joysticks)
        self.joy = joysticks[0]
        self.joy.init()
        pygame.init()
        self.t = None
        self.fps = fps

    def _get_human_action(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == UP_AXIS:
                    if event.value < -0.5:
                        self.human_agent_action[0] = 2  # up
                    elif event.value > 0.5:
                        self.human_agent_action[0] = 3  # down
                    else:
                        self.human_agent_action[0] = 0  # noop
        # self.human_agent_action[0]=np.random.choice([0, 2, 3])
        return self.human_agent_action[0]

    def __call__(self, ob):
        """Act."""
        # self.env.render()
        # action = self._get_human_action()
        if self.t and (time.time() - self.t) < 1. / self.fps:
            st = 1. / self.fps - (time.time() - self.t)
            if st > 0.:
                time.sleep(st)
        self.t = time.time()
        self.env.render()
        action = self._get_human_action()
        print(action)
        return action

    def reset(self):
        # self.human_agent_action[:] = 0.
        pass


if __name__ == '__main__':
    import gym
    import residual_shared_autonomy.pong
    from dl.rl import ensure_vec_env

    env = gym.make("Pong-v4", render_mode="human")
    # env = gym.make("ALE/Pong-v4", render_mode="human")
    env.metadata['render_fps'] = 50

    actor = PongJoystickActor(env)

    for _ in range(10):
        ob = env.reset()
        # actor.reset()
        env.render()
        done = False
        reward = 0.0

        while not done:
            # print(actor(ob)[0])
            ob, r, done,info, _= env.step(actor(ob))
            reward += r
        print(reward)
#     # env.close()