
from numpy import random
import pdb
import pickle
import csv
#run frozen_dict.py
from frozen_dict import *
import itertools


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
		#print i, a, s, states[i-1]

	j = select_based_on_probabilities(probs)
	#print states
	#print j
	print probs
	print s, a, states[j-1]
	if int(sum(probs)) != 1:
		raise Exception('uh-oh, better check out those transition probabilities.')
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

	alpha = float(alpha)
	actions = ['replace_0','replace_1', 'replace_2', 'replace_3', 'ignore']
	stim_list = []
	num_stim = 6
	wm_capacity = 4
	prob_forget = .25
	transitions = dict()
	for i in range(1,num_stim+1):
		stim_list.append('stim%d'%i)
	#stim_list.append(0)

	#state_init = frozendict({'stimulus':'stim%d'%random.randint(1,num_stim), 'wm':[]})
	wm_set=set()
	wm_list=list()
	states = list()
	new_wm_list = list()

	#define all possible contents of working memory
	for elm1 in stim_list:
		for elm2 in stim_list:
			for elm3 in stim_list:
				for elm4 in stim_list:
					wm_set.add(frozenset({elm1,elm2,elm3,elm4}))
	wm_list = list(wm_set)
	num_set = len(wm_set)
	for i in range(num_set):
		new_wm_list.extend(list(itertools.permutations(wm_list[i])))



	for presented_stim in stim_list:
		for content in wm_set:
			states.append(frozendict({'stimulus':presented_stim, 'wm':content}))

	#pdb.set_trace()



	#define initial states
	empty_states = list()
	for init_stim in stim_list:
		empty_states.append(frozendict({'stimulus':init_stim,'wm':frozenset([])}))
	q = dict()

	states.extend(empty_states)


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
	 		for act in actions:
				if act == 'ignore':
					transitions[origin, 'ignore', frozendict({'stimulus': newstim, 'wm': frozenset({})})] = float(1.0/num_stim)
				else:
					if start['stimulus'] == newstim:
						transitions[origin, act, frozendict({'stimulus': newstim, 'wm': frozenset({start['stimulus']})})] = 1 - alpha
						#if origin['stimulus'] == 'stim5' and act == 'replace_0':
							#print transitions[origin, act, frozendict({'stimulus': newstim, 'wm': frozenset({start['stimulus']})})]
					else:
						transitions[origin, act, frozendict({'stimulus': newstim, 'wm': frozenset({start['stimulus']})})] = float(alpha)/(num_stim - 1)
						#if origin['stimulus'] == 'stim5' and act == 'replace_0':
							#print transitions[origin, act, frozendict({'stimulus': newstim, 'wm': frozenset({start['stimulus']})})]
							#print alpha
							#print float(alpha)/(num_stim - 1))
	#pdb.set_trace()





	#define transition values
	for start_state in states:#excluse initial states
		if start_state == states[-1*len(stim_list)]:
			break
		for action in actions:
			if action == 'replace_1':
				if start_state == frozendict({'stimulus':'stim5','wm':frozenset({'stim1'})}):
					print 'okey'
					#pdb.set_trace()
			if action == 'replace_0' or action == 'replace_1' or action == 'replace_2' or action == 'replace_3':
				for new_stim in stim_list:
					#print start_state['wm']
					#print action, new_stim, start_state
					#print start_state,action, frozendict({'stimulus': new_stim, 'wm': [start_state['stimulus']]})
					#print start_state
					new_mem = list(start_state['wm'])
					#print new_mem, action
					if len(new_mem) < (int(action[-1]) + 1):
						new_mem.append(start_state['stimulus'])
					else:
						new_mem[int(action[-1])] = start_state['stimulus']#i can't index
					if start_state['stimulus'] == new_stim:
					#stimulus stays the same
						#new_mem = list(start_state['wm'])
						#new_mem[action[-1]] = start_state['stimulus']#i can't index
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(new_mem)})] = float(1.0 - alpha)/(len(new_mem))
						if action == 'replace_1':
							print 'debugs', transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(new_mem)})]
						#forgetting
						for forgotten_stim_ind in range(len(new_mem)-1):
							mem_forget = list(new_mem)

							if forgotten_stim_ind != int(action[-1]):
								mem_forget.pop(forgotten_stim_ind)
								#pdb.set_trace()
								transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(mem_forget)})] = float(1.0 - alpha)/(len(new_mem))#you can't forget the stimulus you just learned
								if action == 'replace_1':
									print '2x', transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(mem_forget)})]
									#pdb.set_trace()
							



					else:

						#print transitions
						#print start_state, action, frozendict({'stimulus': new_stim, 'wm':start_state['stimulus']})
						#pdb.set_trace()
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm':frozenset(new_mem)})] = float(alpha)/((num_stim-1)*(len(new_mem)))
						if action == 'replace_1':
							#pdb.set_trace()
							print 'hallohh', transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm':frozenset(new_mem)})]
						for forgotten_stim_ind in range(len(new_mem) - 1):
							mem_forget = list(new_mem)

							if forgotten_stim_ind != int(action[-1]):
								mem_forget.pop(forgotten_stim_ind)
								transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(mem_forget)})] = (alpha)/((num_stim-1)*(len(new_mem)))#you can't forget the stimulus you just learned
								if action == 'replace_1':
									print 'meark', transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': frozenset(mem_forget)})]
					#right now all of the states with new wm:start_state[wm] have been covered

					#transitions[state_init, action, frozendict({'stimulus':new_stim, 'wm': [start_state['stimulus']]})] = 1 #the agent HAS to learn when wm is empty
			else:
				for new_stim in stim_list:
					#print action, new_stim, start_state
					#print start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})
					if start_state['stimulus'] == new_stim:
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})] = float(1 - alpha)/(len(start_state['wm'])+1)
						for forgotten_stim_ind in range(len(start_state['wm'])):
							mem_forget = list(start_state['wm'])
							mem_forget.pop(forgotten_stim_ind)
							transitions[start_state, action, frozenset(mem_forget)] = float(1 - alpha)/(len(start_state['wm'])+1)
					else:
						transitions[start_state, action, frozendict({'stimulus': new_stim, 'wm': start_state['wm']})] = float(alpha)/(num_stim - 1)
						for forgotten_stim_ind in range(len(start_state['wm'])):
							mem_forget = list(start_state['wm'])
							mem_forget.pop(forgotten_stim_ind)
							transitions[start_state, action, frozenset(mem_forget)] = float(1 - alpha)/(len(start_state['wm'])+1)
			q[start_state, action] = 0
	#q[state_init,'replace'] = 0
	#q[state_init, 'ignore'] = 0

	#pdb.set_trace()

	for s in states:
		for a in actions:
			q[s,a] = 0


	#define r_state
	r_set = dict()
	for state in states:
		if state['stimulus'] in state['wm']:
			r_set[state] = 1
		else:
			r_set[state] = 0
	#pdb.set_trace()

	return q, r_set, states, actions, transitions, num_stim#, state_init


def main(alpha):
	q, r_set, states, actions, transitions, num_stim = set_values(alpha)
	q_table = dict()
	time = 0
	state_order = list()



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
		state_init = frozendict({'stimulus':'stim%d'%random.randint(1,num_stim+1), 'wm':frozenset({})})
		s = state_init
		state_order = [state_init]
		#print s
		#print episode
		step = 1
		for step in range(20):
			#calculate Q values at each time step
			#adjust q values so that they have tiny differences to guarantee no tie
			for key in q:
				tiny_rand = random.uniform(.0000001,.000001)
				q[key] = q[key] + tiny_rand
			print episode, step
			q_sa, s_prime, a = choose_action(s, actions, r_set, q, transitions, states)
			state_order.append(s_prime)
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
	return q,q_table, state_order


count_transition = 0
main(1)

