
from numpy import random
import pdb
import pickle
import csv
#run frozen_dict.py
from frozen_dict import *


w = csv.writer(open("output.csv", "w"))

#from scipy import stats

def select_based_on_probabilities(probs):
	random_num = random.random()
	already_covered = 0
	for j in range(1,len(probs) + 1):
		if random_num <= probs[j - 1] + already_covered:
			return j		
		already_covered += probs[j - 1]

def transition(s, a, r_set, transitions, states):
	'''transitions to a new state, given a probability distribution for a given action
	returns a reward and the new state'''
	probs = list()



	for i in range(1,len(states)+1):
		#pdb.set_trace()
		probs.append(transitions[s,a,states[i-1]])
		#print i, a, s

	j = select_based_on_probabilities(probs)
	#print states
	#print j
	#print probs
	#print s
	#print a
	#print #pdb.set_trace()
	return states[j-1], r_set[states[j-1]]



def choose_action(s, actions, r_set, q, transitions, states):
	'''chooses an action based on e-greedy policy.  Then calls to transitions to switch the values and returns the new q-value and state'''
	chance_greedy = random.random()
	epsilon = .8
	alpha = .05
	gamma = .9
	q_s = list()

	#define q values for all actions from state s
	for i in range(len(s)-1):
	  	q_s.append(q[(s,actions[i])])

	if chance_greedy > epsilon/len(actions):
		#take the greedy option
		#define current q(s,a)
	 	q_sa = max(q_s)
	 	greedy_action = actions[q_s.index(max(q_s))]

	 	#pdb.set_trace()
		s_prime, r = transition(s, greedy_action, r_set, transitions, states)

		#q values for s_prime
		q_sp = list()
		for h in range(len(actions)):
			q_sp.append(q[(s_prime,actions[h])])

		#update q_sa
		q_sa = q_sa + alpha*(r + gamma*max(q_sp) - q_sa)
		#print s_prime
		return q_sa, s_prime, greedy_action#put q_sa into q array

	else:

		q_sp = list()
		chance_action = random.random()
		#q_s.remove(q_sa)
		# print 'mew'
		# print actions
		# print len(actions)
		u = [.5, .5]
		g = select_based_on_probabilities(u)
		q_sa = q[(s, actions[g-1])]
		s_prime, r = transition(s, actions[g-1], r_set, transitions, states)
		#print 'non-greedy'
		#print s_prime
		#pdb.set_trace()
		for u in range(len(actions)):
			q_sp.append(q[s_prime,actions[u]])
		q_sa = q_sa + alpha*(r+gamma*max(q_sp) - q_sa)
		#print s_prime
		return q_sa, s_prime, actions[g-1]





def set_values(alpha):

	actions = ['replace','ignore']
	stim_list = []
	num_stim = 2
	transitions = dict()
	for i in range(1,num_stim+1):
		stim_list.append('stim%d'%i)

	#state_init = frozendict({'stimulus':'stim%d'%random.randint(1,num_stim), 'wm':[]})

	states = [frozendict({'stimulus':'stim1', 'wm':['stim1']}),frozendict({'stimulus':'stim1', 'wm':['stim2']}),frozendict({'stimulus':'stim2','wm':['stim1']}),frozendict({'stimulus':'stim2','wm':['stim2']}), frozendict({'stimulus':'stim1','wm':[]}),frozendict({'stimulus':'stim2','wm':[]}),]

	empty_states = [frozendict({'stimulus':'stim1','wm':[]}),frozendict({'stimulus':'stim2','wm':[]})]
	q = dict()



	#alpha = 1

	#initialize transition values as zeros
	for end in states:
		for a in actions:
			for start in states:
					transitions[start, a, end] = 0;
					q[start, a] = 0
			#transitions[state_init, a, end] = 0

	#define transition values for initial state
	for origin in empty_states:
		for newstim in stim_list:
			transitions[origin, 'ignore', frozendict({'stimulus': newstim, 'wm': []})] = float(1.0/num_stim)
			if start['stimulus'] == newstim:
				transitions[origin, 'replace', frozendict({'stimulus': newstim, 'wm': [start['stimulus']]})] = 1 - alpha
			else:
				transitions[origin, 'replace', frozendict({'stimulus': newstim, 'wm': [start['stimulus']]})] = float(alpha/(num_stim - 1))
	#pdb.set_trace()




	#define transition values
	for start_state in states:#[:-1]:
		for action in actions:
			if action == 'replace':
				for new_stim in stim_list:
					#print action, new_stim, start_state
					#print start_state,action, frozendict({'stimulus': new_stim, 'wm': [start_state['stimulus']]})
					if start_state['stimulus'] == new_stim:
					#stimulus stays the same
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': [start_state['stimulus']]})] = 1 - alpha

					else:
						#print transitions
						#print start_state, action, frozendict({'stimulus': new_stim, 'wm':start_state['stimulus']})
						#pdb.set_trace()
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm':[start_state['stimulus']]})] = float(alpha/(num_stim - 1))
					#right now all of the states with new wm:start_state[wm] have been covered
					#transitions[state_init, action, frozendict({'stimulus':new_stim, 'wm': [start_state['stimulus']]})] = 1 #the agent HAS to learn when wm is empty
			else:
				for new_stim in stim_list:
					#print action, new_stim, start_state
					#print start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})
					if start_state['stimulus'] == new_stim:
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})] = 1 - alpha
					else:
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})] = float(alpha/(num_stim - 1))
			q[start_state, action] = 0
	#q[state_init,'replace'] = 0
	#q[state_init, 'ignore'] = 0



	#pdb.set_trace()


	# transitions = {(states[0],actions[0],states[0]) : (1-alpha),
	# 				(states[0],actions[0],states[1]) : 0,
	# 				(states[0],actions[0],states[2]) : alpha, 
	# 				(states[0],actions[0],states[3]) : 0, 

	# 				(states[0],actions[1],states[0]) : (1-alpha), 
	# 				(states[0],actions[1],states[1]) : 0, 
	# 				(states[0],actions[1],states[2]) : alpha, 
	# 				(states[0],actions[1],states[3]) : 0, 


	# 				(states[1],actions[0],states[0]) : (1-alpha), 
	# 				(states[1],actions[0],states[1]) : 0, 
	# 				(states[1],actions[0],states[2]) : alpha,
	# 				(states[1],actions[0],states[3]) : 0, 

	# 				(states[1],actions[1],states[0]) : 0, 
	# 				(states[1],actions[1],states[1]) : (1-alpha), 
	# 				(states[1],actions[1],states[2]) : 0,
	# 				(states[1],actions[1],states[3]) : alpha, 

	
	# 				(states[2],actions[0],states[0]) : 0, 
	# 				(states[2],actions[0],states[1]) : alpha, 
	# 				(states[2],actions[0],states[2]) : 0, 
	# 				(states[2],actions[0],states[3]) : (1-alpha), 

	# 				(states[2],actions[1],states[0]) : alpha, 
	# 				(states[2],actions[1],states[1]) : 0, 
	# 				(states[2],actions[1],states[2]) : (1-alpha), 
	# 				(states[2],actions[1],states[3]) : 0, 


	# 				(states[3],actions[0],states[0]) : 0, 
	# 				(states[3],actions[0],states[1]) : alpha, 
	# 				(states[3],actions[0],states[2]) : 0,
	# 				(states[3],actions[0],states[3]) : 1-alpha, 

	# 				(states[3],actions[1],states[0]) : 0, 
	# 				(states[3],actions[1],states[1]) : alpha, 
	# 				(states[3],actions[1],states[2]) : 0,
	# 				(states[3],actions[1],states[3]) : 1-alpha,}

					
	#policy = {'s_1':'a_1', 's_2':'a_1', 's_3':'a_1'}

	for s in states:
		for a in actions:
			q[s,a] = 0


	r_set = {states[0]:1, states[1]:0, states[2]:0, states[3]:1, states[4]:0, states[5]:0}

	return q, r_set, states, actions, transitions, num_stim#, state_init


def main(alpha):
	q, r_set, states, actions, transitions, num_stim = set_values(alpha)
	q_table = dict()
	time = 0



	for episode in range(800):
		#state_num = 2#fix this ?
		#repeat for greatest accuracy		
		for key in q:
			tiny_rand = random.uniform(.0000001,.000001)
			tiny_rand = 0
			q[key] = q[key] + tiny_rand
		#calculate q at the starting state
	#	q_sa, s_prime, a = choose_action(states[state_num], actions, r_set, q, transitions)
	#	q[(states[state_num], a)] = q_sa
		state_init = frozendict({'stimulus':'stim%d'%random.randint(1,num_stim+1), 'wm':[]})
		s = state_init
		#print s
		#print episode
		step = 1
		for step in range(20):
			#calculate Q values at each time step
			#adjust q values so that they have tiny differences to guarantee no tie
			for key in q:
				tiny_rand = random.uniform(.0000001,.000001)
				q[key] = q[key] + tiny_rand
			q_sa, s_prime, a = choose_action(s, actions, r_set, q, transitions, states)
			#print s_prime
			#if a == 'a_2' and s == 's_4':
				#print q_sa
			q[(s, a)] = q_sa
			q_table[(s,a,time)] = q_sa

			s = s_prime
			# if s_prime == 's_1':
			# 	if a == 'a_1':
			# 		for key in q:
			# 			print key,q[key], episode, step			q_table[(s,a,episode,step)] = q_sa			q_table[(s,a,episode,step)] = q_sa			
			time += 1
		#print 'hello'
	for key, val in q_table.items():
    		w.writerow([key, val])

	#for key in q:
	 	#print key,q[key]
	return q,q_table



#main(alpha)

