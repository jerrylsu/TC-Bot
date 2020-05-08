# -*- coding: utf-8 -*-
"""
# PRD 场景的一些配置文件，例如所有可使用的agent action
"""


sys_request_slots = ['is_staff', 'is_reserve_visitor', 'self_name', 'host_name', 'digits_key', 'phone_key']
sys_inform_slots = []

# # only first turn dialogue is user utter used
# start_dia_acts = {
#     'request': ['is_staff', 'is_reserve_visitor', 'self_name', 'host_name']
# }

# Dialogue status
FAILED_DIALOG = -1
SUCCESS_DIALOG = 1
NO_OUTCOME_YET = 0

# Rewards
SUCCESS_REWARD = 50
FAILURE_REWARD = 0
PER_TURN_REWARD = 0

# Special Slot Values
I_DO_NOT_CARE = "I do not care"
NO_VALUE_MATCH = "NO VALUE MATCHES!!!"

# Constraint Check
CONSTRAINT_CHECK_FAILURE = 0
CONSTRAINT_CHECK_SUCCESS = 1

# NLG Beam Search
nlg_beam_size = 10

# run_mode: 0 for dia-act; 1 for NL; 2 for no output
run_mode = 0
auto_suggest = 0

# A Basic Set of Feasible actions to be Considered By an RL agent
feasible_actions = [
    {'diaact': "request", 'inform_slots': {}, 'request_slots': {sys_request_slots[0]: "UNK"}},
    {'diaact': "thanks", 'inform_slots': {}, 'request_slots': {}},
    {'diaact': "goodbye", 'inform_slots': {}, 'request_slots': {}},
    # 欢迎员工上班
    {'diaact': "welcomestaff", 'inform_slots': {}, 'request_slots': {}},
    # 欢迎访客访问
    {'diaact': "welcomevisitor", 'inform_slots': {}, 'request_slots': {}},
    # 呼叫被访员工前来迎接
    {'diaact': "staffmeet", 'inform_slots': {}, 'request_slots': {}},
    # 呼叫前台
    {'diaact': "manualservice", 'inform_slots': {}, 'request_slots': {}},
]

# Adding the inform actions
for slot in sys_request_slots[1:]:
    # sys_request_slots first value has been filled in the feasible_actions first element
    feasible_actions.append({'diaact': "request", 'inform_slots': {}, 'request_slots': {slot: "UNK"}})
