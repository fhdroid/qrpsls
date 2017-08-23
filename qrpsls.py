# Rock Paper Scissors Lizard Spock, the Quantum Way

import sys
if sys.version_info < (3,0):
    raise Exception('Please use Python version 3 or greater.')

import sys
sys.path.append('../')
# importing the QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

config = {
   "url": 'https://quantumexperience.ng.bluemix.net/api'
}

# note that device should be 'ibmqx_qasm_simulator', 'ibmqx2' or 'local_qasm_simulator'
device = 'local_qasm_simulator'
# uncomment below for the real thing
#device = 'ibmqx2'
        
# we are going to build a superpositon over 3 qubits 
qp = QuantumProgram()
qp.set_api(Qconfig.APItoken, Qconfig.config["url"], verify=True) # set the APIToken and API url
# test to see what's available
#print(qp.available_backends())


n = 3  # number of qubits 
q = qp.create_quantum_register('q', n)
c = qp.create_classical_register('c', n)

# will be set to false when the game is over
play_game = True

the_list = ['rock', 'paper', 'scissors', 'spock', 'lizard'];
player_total = 0
qc_total = 0

# function to convert number to name
def number_to_name(number):
    return the_list[number]


# function to convert name to number
def name_to_number(name):
    if name in the_list:
        return the_list.index(name)
    else:
        print (name + " is not a character in RPSLS\n")
        return -1

# get max value and its dictonary mapping and return the name
def get_comp_choice():
    # quantum circuit to make a superpostion state 
    superposition = qp.create_circuit('superposition', [q], [c])
    superposition.h(q)
    superposition.s(q[0])
    superposition.measure(q[0], c[0])
    superposition.measure(q[1], c[1])
    superposition.measure(q[2], c[2])

    circuit_name = 'superposition'

    # execute the quantum circuit 
    result = qp.execute([circuit_name], device, shots=1000, max_credits=5, wait=10, timeout=240, silent = False)
    value = result.get_counts('superposition')
    choosen = max(value, key=value.get)
	# we must map the result to the list, but we have more items in result, so after index 4 we start again form [0]
    if (device == 'ibmqx2'):
        list_map = {'00101': the_list[0], '00010': the_list[1], '00110': the_list[2], '00001': the_list[3], '00011': the_list[4], '00111': the_list[0], '00100': the_list[1], '00000': the_list[2]}
    else: #want local_qasm_simulator has only 3 qubits
        list_map = {'101': the_list[0], '010': the_list[1], '110': the_list[2], '001': the_list[3], '011': the_list[4], '111': the_list[0], '100': the_list[1], '000': the_list[2]}
    return list_map[choosen]


# function that selects the winner
def rpsls(guess): 
    global player_total, qc_total
	
    # convert name to player_number using name_to_number
    player_number = name_to_number(guess)
    
    # compute random guess for comp_number 
    comp_number = name_to_number(get_comp_choice())

    # compute difference between player_number and comp_number modulo five
    winner = (5 + player_number - comp_number) % 5
    
    # convert comp_number to name
    comp_name = number_to_name(comp_number)
    print ("Player chooses: " + guess)
    print ("Computer chooses: " + comp_name)
	
    if player_number == -1:
        print ("Quantum Computer wins!\n")
        qc_total += 1
    elif winner == 0:
       print ("Player and quantum computer tie!\n")
    elif winner == 1 or winner == 3:
        print ("You win!\n")
        player_total += 1
    elif winner == 2 or winner == 4:
        print ("Quantum Computer wins!\n")
        qc_total += 1
        
    print("Score >>> You: "+str(player_total)+" vs. Quantum Computer: " + str(qc_total) )

print("Welcome to Rock, Paper, Scissors, Lizard, Spock, the Quantum Way!\n\n");
print("Try to beat the Quantum Computer!\n\n")
print("FYI:")
print("Scissors cuts Paper")
print("Paper covers Rock")
print("Rock crushes Lizard")
print("Lizard poisons Spock")
print("Spock smashes Scissors")
print("Scissors decapitates Lizard")
print("Lizard eats Paper")
print("Paper disproves Spock")
print("Spock vaporizes Rock")
print("(and as it always has) Rock crushes Scissors\n")
input("Press enter to begin")


while (play_game):
    player_guess = input('Enter your choice..\nOptions: rock, paper, scissors, lizard, spock or quit to quit\n')
    if str(player_guess) == "quit":
        play_game = False
        print("Game over\n")
    else:
        rpsls(str(player_guess))