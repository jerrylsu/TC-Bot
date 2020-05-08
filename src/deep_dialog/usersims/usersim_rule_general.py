# -*- coding: utf-8 -*-
"""
# 通用的用户模拟器模块，通过读取配置文件来设定不同场景的参数
"""
import logging
import argparse
import json
import random
import copy
from .usersim import UserSimulator
from deep_dialog import dialog_config

_logger = logging.getLogger(__name__)


class CustomRuleSimulator(UserSimulator):
    """ A custom rule-based user simulator for testing dialog policy """
    def __init__(self, movie_dict=None, act_set=None, slot_set=None, start_set=None, params=None):
        """ Constructor shared by all user simulators """

        self.movie_dict = movie_dict
        self.act_set = act_set
        self.slot_set = slot_set
        self.start_set = start_set

        self.max_turn = params['max_turn']
        self.slot_err_probability = params['slot_err_probability']
        self.slot_err_mode = params['slot_err_mode']
        self.intent_err_probability = params['intent_err_probability']

        self.simulator_run_mode = params['simulator_run_mode']
        self.simulator_act_level = params['simulator_act_level']

        self.learning_phase = params['learning_phase']

    def initialize_episode(self):
        """ Initialize a new episode (dialog)
        state['history_slots']: keeps all the informed_slots
        state['rest_slots']: keep all the slots (which is still in the stack yet)
        """

        self.state = {}
        self.state['history_slots'] = {}
        self.state['inform_slots'] = {}
        self.state['request_slots'] = {}
        self.state['rest_slots'] = []
        # first turn is agent, so user start dialogue is second turn
        # but turn initialize value is -1(-1+2=1)
        self.state['turn'] = -1

        self.episode_over = False
        self.dialog_status = dialog_config.NO_OUTCOME_YET

        # get goal
        self.goal = self._sample_goal()
        # add new dict key for the request_slots dict,
        # for example:(dialogue task is book ticket)
        # self.goal['request_slots']['ticket'] = 'UNK'

        self.constraint_check = dialog_config.CONSTRAINT_CHECK_FAILURE

        # 获取agent的观测内容，例如系统通过摄像头获取头像信息
        # （此种信息可以直接生成为user action，因此user initialize获取）
        user_sample_action = self.get_initialize_info()

        return user_sample_action

    def _sample_goal(self):
        """sample a user goal"""
        sample_goal = random.choice(self.start_set[self.learning_phase])

        return sample_goal

    def get_initialize_info(self):
        """get the user is initialize input inform, for example face inform
        :return:{"request_slots": {}, "inform_slots": {}}
        """
        # 包含一个对人脸输入信息的解析过程
        user_initialize_sample_action = {}

        return user_initialize_sample_action

    def corrupt(self, user_action):
        """Randomly corrupt an action with error probs
         (slot_err_probability and slot_err_mode) on Slot and
         Intent (intent_err_probability).
        :param user_action:
        :return:
        """
        pass

    def debug_fake_goal(self):
        """Debug function: build a fake goal mannually (Can be moved in future)
        :return:
        """
        pass

    def next(self, system_action):
        """Generate next User Action based on Last System Action.
        :param system_action:
        :return:
        """
        self.state['turn'] += 2
        self.episode_over = False
        self.dialog_status = dialog_config.NO_OUTCOME_YET

        sys_act = system_action.get('diaact')

        if self.max_turn > 0 and self.state.get('turn') > self.max_turn:
            self.dialog_status = dialog_config.FAILED_DIALOG
            self.episode_over = True
            self.state['diaact'] = 'closing'
        else:
            self.state['history_slots'].update(self.state.get('inform_slots'))
            self.state['inform_slots'].clear()

            if sys_act == "request":
                self.response_request(system_action)
            elif sys_act in ["welcomestaff", "welcomevisitor", "staffmeet"]:
                self.response_end()
            elif sys_act == "closing":
                self.episode_over = True
                self.state['diaact'] = "manualservice"

        response_action = {}
        response_action['diaact'] = self.state['diaact']
        response_action['inform_slots'] = self.state['inform_slots']
        response_action['request_slots'] = self.state['request_slots']
        response_action['turn'] = self.state['turn']
        response_action['nl'] = ""

        # add NL to dia_act
        # self.add_nl_to_action(response_action)
        return response_action, self.episode_over, self.dialog_status

    def response_request(self, system_action):
        """ Response for Request (System Action)
        Replay agent's request: speaker -> agent, diaact -> request"""
        if len(system_action['request_slots'].keys()) > 0:
            slot = system_action['request_slots'].keys()[0]  # only one slot
            if slot in self.goal['inform_slots'].keys():  # request slot in user's constraints  #and slot not in self.state['request_slots'].keys():
                self.state['inform_slots'][slot] = self.goal['inform_slots'][slot]
                self.state['diaact'] = "inform"
                if slot in self.state['rest_slots']: self.state['rest_slots'].remove(slot)
                if slot in self.state['request_slots'].keys(): del self.state['request_slots'][slot]
                self.state['request_slots'].clear()  # 之前累加的问题全部删除，不在提问，回答当前轮agent的问题。
            elif slot in self.goal['request_slots'].keys() and slot not in self.state['rest_slots'] and slot in self.state['history_slots'].keys(): # the requested slot has been answered
                self.state['inform_slots'][slot] = self.state['history_slots'][slot]
                self.state['request_slots'].clear()
                self.state['diaact'] = "inform"
            elif slot in self.goal['request_slots'].keys() and slot in self.state['rest_slots']: # request slot in user's goal's request slots, and not answered yet
                self.state['diaact'] = "request" # "confirm_question"
                self.state['request_slots'][slot] = "UNK"

                ########################################################################
                # Inform the rest of informable slots
                ########################################################################
                for info_slot in self.state['rest_slots']:
                    if info_slot in self.goal['inform_slots'].keys():
                        self.state['inform_slots'][info_slot] = self.goal['inform_slots'][info_slot]

                for info_slot in self.state['inform_slots'].keys():
                    if info_slot in self.state['rest_slots']:
                        self.state['rest_slots'].remove(info_slot)
            else:
                if len(self.state['request_slots']) == 0 and len(self.state['rest_slots']) == 0:
                    self.state['diaact'] = "thanks"
                else:
                    self.state['diaact'] = "inform"
                self.state['inform_slots'][slot] = dialog_config.I_DO_NOT_CARE
        else: # this case should not appear
            if len(self.state['rest_slots']) > 0:
                random_slot = random.choice(self.state['rest_slots'])
                if random_slot in self.goal['inform_slots'].keys():
                    self.state['inform_slots'][random_slot] = self.goal['inform_slots'][random_slot]
                    self.state['rest_slots'].remove(random_slot)
                    self.state['diaact'] = "inform"
                elif random_slot in self.goal['request_slots'].keys():
                    self.state['request_slots'][random_slot] = self.goal['request_slots'][random_slot]
                    self.state['diaact'] = "request"

    def response_end(self):
        self.episode_over = True
        self.dialog_status = dialog_config.SUCCESS_DIALOG
        self.state["diaact"] = "thanks"

        request_slot_set = copy.deepcopy(self.state['request_slots'].keys())
        rest_slot_set = copy.deepcopy(self.state['rest_slots'])
        if len(request_slot_set) > 0 or len(rest_slot_set) > 0:
            self.dialog_status = dialog_config.FAILED_DIALOG

        for info_slot in self.state['history_slots'].keys():
            if self.state['history_slots'][info_slot] == dialog_config.NO_VALUE_MATCH:
                self.dialog_status = dialog_config.FAILED_DIALOG
            if info_slot in self.goal['inform_slots'].keys():
                if self.state['history_slots'][info_slot] != self.goal['inform_slots'][info_slot]:
                    self.dialog_status = dialog_config.FAILED_DIALOG

        # if self.constraint_check == dialog_config.CONSTRAINT_CHECK_FAILURE:
        #    self.dialog_status = dialog_config.FAILED_DIALOG

    def respone_welcomevisitor(self, system_action):
        pass

    def  respone_staffmeet(self, system_action):
        pass
