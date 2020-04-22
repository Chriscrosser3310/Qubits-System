from qubits_system import Qubits_System

q_num = 4
q_list = []
file_str = ''
CNOT_str = '02'
file_name = f'QFT4_CNOT{CNOT_str}.txt'
for i in range(2**q_num):
    q = Qubits_System(q_num, i)
    temp_str = f'{repr(q)}\n'
    q.QFT(0, 1, 2, 3)
    q.CNOT(*(int(s) for s in CNOT_str))
    q.QFT(0, 1, 2, 3)
    temp_str += f'{repr(q)}\n\n'
    print(temp_str,end='')
    file_str += temp_str
with open(file_name, 'w') as file:
    file.write(file_str)