
from numpy import random
import pdb

# transitions = {('s_1','a_1','s_1'):.3,
# 				('s_1','a_1','s_2'):.7,

# 				('s_1','a_2','s_1'):.4,
# 				('s_1','a_2','s_2'):.6,

# 				('s_2','a_1','s_1'):.5,
# 				('s_2','a_1','s_2'):.5,

# 				('s_2','a_2','s_1'):.2,
# 				('s_2','a_2','s_2'):.8}

def transition(s, a, r_set, transitions):
	'''transitions to a new state, given a probability distribution for a given action
	returns a reward and the new state'''
	probs = list()
	for i in range(1,len(r_set)+1):
		#pdb.set_trace()
		probs.append(transitions[s,a,'s_%d'%i])
	random_num = random.random()
	already_covered = 0
	for j in range(1,len(probs)+1):
		if random_num <= probs[j-1]+already_covered:
			return 's_%d'%j, r_set['s_%d'%j]
		already_covered+=probs[j-1]


def choose_action(s, actions, r_set, q, transitions):
	chance_greedy = random.random()
	epsilon = .1
	alpha = .05
	gamma = .5
	q_s = list()

	#define q values for all actions from state s
	for i in range(len(s)-1):
	  	q_s.append(q[(s,actions[i])])

	if chance_greedy > epsilon/len(actions):
		#take the greedy option
		#define current q(s,a)
	 	q_sa = max(q_s)

	 	#pdb.set_trace()
		s_prime, r = transition(s, actions[q_s.index(max(q_s))], r_set, transitions)

		q_sp = list()
		for h in range(len(actions)-1):
			q_sp.append(q[(s_prime,actions[h])])

		#update q_sa
		q_sa = q_sa + alpha*(r + gamma*max(q_sp) - q_sa)
		return q_sa, s_prime, actions[q_s.index(max(q_s))]#put q_sa into q array



		#measure Q
		#update state
	else:
		q_sp = list()
		chance_action = random.random()
		#q_s.remove(q_sa)
		actions_new = list(actions)
		actions_new.remove(actions[q_s.index(max(q_s))])
		for j in range(1,len(actions_new)+1):
			if chance_action <= 1/(j*len(actions_new)):
				#call transition to change the state given action probabilities
				s_prime, r = transition(s, actions_new[j-1], r_set, transitions)
				q_sa = q[(s, actions_new[j-1])]
				for h in range(len(actions)-1):
					q_sp.append(q[(s_prime,actions[h])])

				q_sa = q[(s,actions_new[j-1])] + alpha*(r + gamma*max(q_sp) - q_sa)
				#measure q
				#update state
				return q_sa, s_prime, actions_new[j-1]

	#max(q_sa)

def set_values():
	transitions = {('s_1','a_1','s_1'):.3,
				('s_1','a_1','s_2'):.7,

				('s_1','a_2','s_1'):.4,
				('s_1','a_2','s_2'):.6,

				('s_2','a_1','s_1'):.5,
				('s_2','a_1','s_2'):.5,

				('s_2','a_2','s_1'):.2,
				('s_2','a_2','s_2'):.8}
	q =  {('s_1','a_1'):.5, ('s_1','a_2'):.5,('s_2','a_1'):.5,('s_2','a_2'):.5}
	r_set = {'s_1':-1, 's_2':0}
	states = ['s_1','s_2']
	actions = ['a_1','a_2']
	return q, r_set, states, actions, transitions

def set_test_values():
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
	#policy = {'s_1':'a_1', 's_2':'a_1', 's_3':'a_1'}

	q =  {('s_1','a_1'):0, ('s_1','a_2'):0,
		('s_2','a_1'):0,('s_2','a_2'):0,
		('s_3','a_1'):0,('s_3','a_2'):0}

	r_set = {'s_1':-1, 's_2':1, 's_3':2}

	return q, r_set, states, actions, transitions


def main():
	q, r_set, states, actions, transitions = set_test_values()

	for episode in range(10000):
		state_num = random.randint(0,len(states))
		#repeat for greatest accuracy		
		for key in q:
			tiny_rand = random.uniform(.0000001,.000001)
			q[key] = q[key] + tiny_rand
		#calculate q at the starting state
		q_sa, s_prime, a = choose_action(states[state_num], actions, r_set, q, transitions)
		q[(states[state_num], a)] = q_sa

		for step in range(1000):
			#calculate Q values at each time step
			#adjust q values so that they have tiny differences to guarantee no tie
			for key in q:
				tiny_rand = random.uniform(.0000001,.000001)
				q[key] = q[key] + tiny_rand

			q_sa, s_prime, a = choose_action(s_prime, actions, r_set, q, transitions)
			q[(s_prime, a)] = q_sa
			# if s_prime == 's_1':
			# 	if a == 'a_1':
			# 		for key in q:
			# 			print key,q[key], episode, step
	for key in q:
	 	print key,q[key]
	print state_num
	return q


main()

