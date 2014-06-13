
from numpy import random
import pdb

def transition(s, a, r_set, transitions):
	probs = [transitions[(s,a,'s_1')], transitions[(s,a,'s_2')], transitions[(s,a,'s_3')]]
	random_num = random.random()
	if 0 <= random_num < probs[0]:
		return 's_1', r_set['s_1']
	elif probs[0] <= random_num < probs[0]+probs[1]:
		return 's_2', r_set['s_2']
	else:
		return 's_3', r_set['s_3']


def run_simulation(s, a, policy, transitions):
	r_set = {'s_1':-1, 's_2':1, 's_3':2}
	v_pi = r_set[s]
	gamma = .5
	for i in range(1,1000):
		if i == 1:
			s, r = transition(s, a, r_set, transitions)
		else:
			s, r = transition(s, policy[s], r_set, transitions)
		v_pi += r*gamma**i
	return v_pi 

def main():
	v_pi_s = list()
	q_pi_s = list()

	states = ['s_1','s_2','s_3']
	actions = ['a_1','a_2']
	transitions = {(states[0],actions[0],states[0]) : .3,
					(states[0],actions[0],states[1]) : .5,
					(states[0],actions[0],states[2]) : .2, 
					(states[0],actions[1],states[0]) : .1, 
					(states[0],actions[1],states[1]) : .4, 
					(states[0],actions[1],states[2]) : .5, 
					(states[1],actions[0],states[0]) : .3, 
					(states[1],actions[0],states[1]) : .5, 
					(states[1],actions[0],states[2]) : .2, 
					(states[1],actions[1],states[0]) : .1, 
					(states[1],actions[1],states[1]) : .4, 
					(states[1],actions[1],states[2]) : .5, 
					(states[2],actions[0],states[0]) : .3, 
					(states[2],actions[0],states[1]) : .5, 
					(states[2],actions[0],states[2]) : .2,
				 	(states[2],actions[1],states[0]) : .1,
					(states[2],actions[1],states[1]) : .4, 
					(states[2],actions[1],states[2]) : .5}
	policy = {'s_1':'a_1', 's_2':'a_1', 's_3':'a_1'}
	#policy = (.3, .5, .2)


	q = dict()
	q_s = list()
	for y in range(3):
		for start_state in range(3):
			#test_policy = (transistions[(states[start_state], actions[action], states[end_state])]
			# for i in range(len(actions)):
			# 	for j in range(1000):
			# 		q_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[i], policy, transitions))
			# 	q[('s_%d'%(start_state+1), 'a_%d'%(i+1))] = sum(q_pi_s)/len(q_pi_s)
			# 	q_s.append(q[('s_%d'%(start_state+1), 'a_%d'%(i+1))])
			#print start_state, q_s
			##policy[states[start_state]] = actions[q_s.index(max(q_s))]
			#q_s=list()

			if policy[states[start_state]] == actions[0]:
				q_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[1], policy, transitions))
				v_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[0], policy, transitions))
			else:
				q_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[0], policy, transitions))
				v_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[0], policy, transitions))
			#v_pi_s.append(run_simulation('s_%d' %(start_state+1), policy[states[start_state]], policy, transitions))					
			#q_pi_s.append(run_simulation('s_%d' %(start_state+1), actions[1], policy, transitions))
		v = sum(v_pi_s)/len(v_pi_s)
		q = sum(q_pi_s)/len(q_pi_s)


		print v, q
		print policy
		if q > v:
			if policy[states[start_state]] == actions[0]:
				policy[states[start_state]] = actions[1]
			else:
				policy[states[start_state]] = actions[0]
			print q
		#print policy
		else:
			print v


		v_pi_s = list()
		q_pi_s = list()

	# for key in q:
	# 	print key,q[key]
	# print policy


main()