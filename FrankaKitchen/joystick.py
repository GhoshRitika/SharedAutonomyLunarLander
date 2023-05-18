"""FrankaKitchen Joystick Agent."""
import pygame
import numpy as np
import time
import gymnasium as gym

#####################################
# Change these to match your joystick
LEFT_UP_AXIS = 1 #LINEAR X
LEFT_SIDE_AXIS = 0 #LINEAR Y
RIGHT_UP_AXIS = 4 # LINEAR Z
RIGHT_SIDE_AXIS = 3 # ANGULAR Z
LEFT_TRIGGER = 2 #EE OPEN
RIGHT_TRIGGER = 5 #EE CLOSED
A_BUTTON = 0 
B_BUTTON = 1 #ANGULAR Y
X_BUTTON = 2 
Y_BUTTON = 3 #ANGULAR X
# D_UP = 11 
# D_DOWN = 12 
# D_LEFT = 13 
# D_RIGHT = 14 
#####################################


class FrankaKitchenJoystickActor(object):
    """Joystick Controller for Lunar Lander."""

    def __init__(self, env, fps=50):
        """Init."""
        # if env.num_envs > 1:
        #     raise ValueError("Only one env can be controlled with the joystick.")
        self.env = env
        self.human_agent_action = np.array([0., 0., 0., 0., 0., 0., 0.], dtype=np.float32)  # noop
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        if len(joysticks) != 1:
            raise ValueError("There must be exactly 1 joystick connected."
                             f"Found {len(joysticks)}")
        self.joy = joysticks[0]
        self.joy.init()
        pygame.init()
        self.t = None
        self.fps = fps
        self.ang_x=0.0
        self.ang_y=0.0

    def _get_human_action(self):
        for event in pygame.event.get():
            print("actuon")
            if event.type == pygame.JOYAXISMOTION:
                self.ang_x=0.0
                self.ang_y=0.0
                if event.axis == LEFT_UP_AXIS: #x lin displacement
                    self.human_agent_action[1] = event.value
                elif event.axis == LEFT_SIDE_AXIS: #y lin displacement
                    self.human_agent_action[0] = event.value
                elif event.axis == RIGHT_UP_AXIS : #z lin displacement
                    self.human_agent_action[2] = event.value
                elif event.axis == RIGHT_SIDE_AXIS:# self.ang displacement about z
                    self.human_agent_action[5] = event.value
                elif event.axis == LEFT_TRIGGER: #EE OPEN
                    self.human_agent_action[6] = 1.0
                elif event.axis == RIGHT_TRIGGER: #EE CLOSE
                    self.human_agent_action[6] = -1.0
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == Y_BUTTON:
                    self.ang_x+=0.25
                    if self.ang_x>=1:
                        self.ang_x=1.0
                    print("x", self.ang_x)
                    self.human_agent_action[4] = self.ang_x
                # elif event.button == A_BUTTON:
                #     self.ang_x-=0.25
                #     if self.ang_x<=-1:
                #         self.ang_x=-1.0
                #     print("x", self.ang_x)
                #     self.human_agent_action[4] = self.ang_x
                if event.button == B_BUTTON:
                    self.ang_y+=0.25
                    if self.ang_y>=1:
                        self.ang_y=1.0
                    print("y", self.ang_y)
                    self.human_agent_action[3] = self.ang_y
                # elif event.button == X_BUTTON:
                #     self.ang_y-=0.25
                #     if self.ang_y<=-1:
                #         self.ang_y=-1.0
                #     print("y", self.ang_y)
                #     self.human_agent_action[3] = self.ang_y
            if event.type == pygame.JOYBUTTONUP:
                # if event.button == Y_BUTTON:
                #     self.ang_x+=0.25
                #     if self.ang_x>=1:
                #         self.ang_x=1.0
                #     print("x", self.ang_x)
                #     self.human_agent_action[4] = self.ang_x
                if event.button == Y_BUTTON:
                    self.ang_x-=0.25
                    if self.ang_x<=-1:
                        self.ang_x=-1.0
                    print("x", self.ang_x)
                    self.human_agent_action[4] = self.ang_x
                # if event.button == B_BUTTON:
                #     self.ang_y+=0.25
                #     if self.ang_y>=1:
                #         self.ang_y=1.0
                #     print("y", self.ang_y)
                #     self.human_agent_action[3] = self.ang_y
                if event.button == B_BUTTON:
                    self.ang_y-=0.25
                    if self.ang_y<=-1:
                        self.ang_y=-1.0
                    print("y", self.ang_y)
                    self.human_agent_action[3] = self.ang_y
        if abs(self.human_agent_action[0]) < 0.1:
            self.human_agent_action[0] = 0.0
        return self.human_agent_action

    def __call__(self, ob):
        """Act."""
        self.env.render()
        action = self._get_human_action()
        if self.t and (time.time() - self.t) < 1. / self.fps:
            st = 1. / self.fps - (time.time() - self.t)
            if st > 0.:
                time.sleep(st)
        self.t = time.time()
        return action

    def reset(self):
        self.human_agent_action[:] = 0.


if __name__ == '__main__':
    # import gym

    env = gym.make('FrankaKitchen-v1', ik_controller=True, render_mode='human') #tasks_to_complete=['microwave', 'kettle', 'bottom_left_burner'],
    actor = FrankaKitchenJoystickActor(env)

    for _ in range(10):
        ob = env.reset()
        env.render()
        done = False
        reward = 0.0

        while not done:
            action=actor(ob)
            # print(action[:3])
            bs, r, terminated, truncated, info = env.step(action)
            reward += r
        print(reward)
        if terminated:
            break
    env.close()


# for i in range(10):
#     state=env.reset()
#     while(True):
#         env.render()
#         action = env.action_space.sample()
#         print(action)
#         bs, reward, terminated, truncated, info = env.step(action)
#         if terminated:
#                 break
# env.close()
