
from numpy import random
import pdb
#from scipy import stats
# transitions = {('s_1','a_1','s_1'):.3,
# 				('s_1','a_1','s_2'):.7,

# 				('s_1','a_2','s_1'):.4,
# 				('s_1','a_2','s_2'):.6,

# 				('s_2','a_1','s_1'):.5,
# 				('s_2','a_1','s_2'):.5,

# 				('s_2','a_2','s_1'):.2,
# 				('s_2','a_2','s_2'):.8}

def select_based_on_probabilities(probs):
	random_num = random.random()
	already_covered = 0
	for j in range(1,len(probs) + 1):
		if random_num <= probs[j - 1] + already_covered:
			return j		
		already_covered += probs[j - 1]

def transition(s, a, r_set, transitions):
	'''transitions to a new state, given a probability distribution for a given action
	returns a reward and the new state'''
	probs = list()
	for i in range(1,len(r_set) + 1):
		#pdb.set_trace()
		probs.append(transitions[s,a,'s_%d'%i])
		#print i, a, s

	j = select_based_on_probabilities(probs)
	return 's_%d'%j, r_set['s_%d'%j]
	# random_num = random.random()
	# already_covered = 0
	# #print 'hello'
	# for j in range(1,len(probs) + 1):
	# 	#print j
	# 	#print s
	# 	#pdb.set_trace()
	# 	if random_num <= probs[j - 1] + already_covered:
	# 		#print 'whoosh'
	# 		return 's_%d'%j, r_set['s_%d'%j]
	# 	already_covered += probs[j-1]
		#print j
		#if j == len(probs) + 1:
		#	pdb.set_trace()


def choose_action(s, actions, r_set, q, transitions):
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

	 	#pdb.set_trace()
		s_prime, r = transition(s, actions[q_s.index(max(q_s))], r_set, transitions)

		#q values for s_prime
		q_sp = list()
		for h in range(len(actions)-1):
			q_sp.append(q[(s_prime,actions[h])])


		#update q_sa
		q_sa = q_sa + alpha*(r + gamma*max(q_sp) - q_sa)
		return q_sa, s_prime, actions[q_s.index(max(q_s))]#put q_sa into q array

	else:
		# q_sp = list()
		# chance_action = random.random()
		# #q_s.remove(q_sa)
		# #actions_new = list(actions)
		# #actions_new.remove(actions[q_s.index(max(q_s))])
		# probs = list()
		# for j in range(len(actions)):
		# 	probs.append(1.0/len(actions))

		# a = actions[select_based_on_probabilities(probs) - 1]
		# s_prime, r = transition(s, a, r_set, transitions) 
		# q_sa = q[(s, a)]

		# for h in range(len(actions)):
		# 	q_sp.append(q[(s_prime,actions[h])])

		# q_sa = q_sa + alpha*(r + gamma*max(q_sp) - q_sa)
		# return q_sa, s_prime, actions[j-1]

		#next task: make it choose randomly rather than choose the non-greedy action
		q_sp = list()
		chance_action = random.random()
		#q_s.remove(q_sa)
		# print 'mew'
		# print actions
		# print len(actions)
		u = [.5, .5]
		g = select_based_on_probabilities(u)
		q_sa = q[(s, actions[g-1])]
		s_prime, r = transition(s, actions[g-1], r_set, transitions)
		#pdb.set_trace()
		for u in range(len(actions)):
			q_sp.append(q[s_prime,actions[u]])
		q_sa = q_sa + alpha*(r+gamma*max(q_sp) - q_sa)
		return q_sa, s_prime, actions[g-1]



		# for j in range(1,len(actions)+1):
		# 	print 'l'
		# 	if chance_action <= j*1/(len(actions)):
		# 		#chance_action less than chance
		# 		#call transition to change the state given action probabilities
		# 		print 'wa'
		# 		s_prime, r = transition(s, actions[j-1], r_set, transitions)
		# 		q_sa = q[(s, actions[j-1])]
		# 		for h in (len(actions)-1):
		# 			q_sp.append(q[(s_prime,actions[h])])

		# 		print 'hello'
		# 		q_sa = q[(s,actions[j-1])] + alpha*(r + gamma*max(q_sp) - q_sa)
		# #measure q
		# #update state
		# 		return q_sa, s_prime, actions[j-1]


		# q_sp = list()
		# chance_action = random.random()
		# #q_s.remove(q_sa)
		# actions_new = list(actions)
		# actions_new.remove(actions[q_s.index(max(q_s))])
		# for j in range(1,len(actions_new)+1):
		# 	if chance_action <= 1/(j*len(actions_new)):
		# 		#call transition to change the state given action probabilities
		# 		s_prime, r = transition(s, actions_new[j-1], r_set, transitions)
		# 		q_sa = q[(s, actions_new[j-1])]
		# 		for h in (len(actions)-1):
		# 			q_sp.append(q[(s_prime,actions[h])])

		# 		q_sa = q[(s,actions_new[j-1])] + alpha*(r + gamma*max(q_sp) - q_sa)
		# #measure q
		# #update state
		# 		return q_sa, s_prime, actions_new[j-1]


		# for j in range(1,len(actions_new)+1):

		# 	if chance_action <= 1/(j*len(actions_new)):
		# 		#call transition to change the state given action probabilities
		# 		#print s
		# 		s_prime, r = transition(s, actions_new[j-1], r_set, transitions)
		# 		q_sa = q[(s, actions_new[j-1])]
		# 		for h in range(len(actions)-1):
		# 			q_sp.append(q[(s_prime,actions[h])])

		# 		q_sa = q[(s,actions_new[j-1])] + alpha*(r + gamma*max(q_sp) - q_sa)
		# 		#measure q
		# 		#update state
		# 		return q_sa, s_prime, actions_new[j-1]

	#max(q_sa)


def set_walk_values():
	states = ['s_1','s_2','s_3','s_4','s_5']
	actions = ['a_1','a_2']
	transitions = {(states[0],actions[0],states[0]) : 0,
					(states[0],actions[0],states[1]) : 0,
					(states[0],actions[0],states[2]) : 0, 
					(states[0],actions[0],states[3]) : 0, 
					(states[0],actions[0],states[4]) : 0, 

					(states[0],actions[1],states[0]) : 0, 
					(states[0],actions[1],states[1]) : 0, 
					(states[0],actions[1],states[2]) : 0, 
					(states[0],actions[1],states[3]) : 0, 
					(states[0],actions[1],states[4]) : 0, 


					(states[1],actions[0],states[0]) : 1, 
					(states[1],actions[0],states[1]) : 0, 
					(states[1],actions[0],states[2]) : 0,
					(states[1],actions[0],states[3]) : 0, 
					(states[1],actions[0],states[4]) : 0, 

					(states[1],actions[1],states[0]) : 0, 
					(states[1],actions[1],states[1]) : 0, 
					(states[1],actions[1],states[2]) : 1,
					(states[1],actions[1],states[3]) : 0, 
					(states[1],actions[1],states[4]) : 0, 

	
					(states[2],actions[0],states[0]) : 0, 
					(states[2],actions[0],states[1]) : 1, 
					(states[2],actions[0],states[2]) : 0, 
					(states[2],actions[0],states[3]) : 0, 
					(states[2],actions[0],states[4]) : 0,  

					(states[2],actions[1],states[0]) : 0, 
					(states[2],actions[1],states[1]) : 0, 
					(states[2],actions[1],states[2]) : 0, 
					(states[2],actions[1],states[3]) : 1, 
					(states[2],actions[1],states[4]) : 0, 


					(states[3],actions[0],states[0]) : 0, 
					(states[3],actions[0],states[1]) : 0, 
					(states[3],actions[0],states[2]) : 1,
					(states[3],actions[0],states[3]) : 0, 
					(states[3],actions[0],states[4]) : 0, 

					(states[3],actions[1],states[0]) : 0, 
					(states[3],actions[1],states[1]) : 0, 
					(states[3],actions[1],states[2]) : 0,
					(states[3],actions[1],states[3]) : 0, 
					(states[3],actions[1],states[4]) : 1,  

					
					(states[4],actions[0],states[0]) : 0, 
					(states[4],actions[0],states[1]) : 0, 
					(states[4],actions[0],states[2]) : 0,
					(states[4],actions[0],states[3]) : 0, 
					(states[4],actions[0],states[4]) : 0, 

					(states[4],actions[1],states[0]) : 0, 
					(states[4],actions[1],states[1]) : 0, 
					(states[4],actions[1],states[2]) : 0,
					(states[4],actions[1],states[3]) : 0, 
					(states[4],actions[1],states[4]) : 0}
	#policy = {'s_1':'a_1', 's_2':'a_1', 's_3':'a_1'}

	q =  {('s_1','a_1'):0, ('s_1','a_2'):0,
		('s_2','a_1'):0,('s_2','a_2'):0,
		('s_3','a_1'):0,('s_3','a_2'):0,
		('s_4','a_1'):0,('s_4','a_2'):0,
		('s_5','a_1'):0,('s_5','a_2'):0}

	r_set = {'s_1':0, 's_2':0, 's_3':0, 's_4':0, 's_5':1}

	return q, r_set, states, actions, transitions


def main():
	q, r_set, states, actions, transitions = set_walk_values()
	print transitions[('s_2', 'a_2', 's_3')]

	for episode in range(15000):
		state_num = 2
		#repeat for greatest accuracy		
		for key in q:
			tiny_rand = random.uniform(.0000001,.000001)
			tiny_rand = 0
			q[key] = q[key] + tiny_rand
		#calculate q at the starting state
	#	q_sa, s_prime, a = choose_action(states[state_num], actions, r_set, q, transitions)
	#	q[(states[state_num], a)] = q_sa
		s = 's_3'

		while((s != 's_1') and (s != 's_5')):
			#calculate Q values at each time step
			#adjust q values so that they have tiny differences to guarantee no tie
			for key in q:
				tiny_rand = random.uniform(.0000001,.000001)
				#q[key] = q[key] + tiny_rand
			q_sa, s_prime, a = choose_action(s, actions, r_set, q, transitions)
			q[(s, a)] = q_sa
			s = s_prime
			# if s_prime == 's_1':
			# 	if a == 'a_1':
			# 		for key in q:
			# 			print key,q[key], episode, step

	for key in q:
	 	print key,q[key]
	print state_num
	return q


main()

