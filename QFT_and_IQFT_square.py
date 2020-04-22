from qubits_system import Qubits_System

q_num = 3

QFT_file = f'QFT{q_num}_square.txt'
QFT_str = ''

IQFT_file = f'IQFT{q_num}_square.txt'
IQFT_str = ''

for i in range(2**q_num):
    q = Qubits_System(q_num, i)
    
    temp_str = f'{str(q)}\n'
    q.QFT(all)
    q.QFT(all)
    temp_str += f'{str(q)}\n\n'
    print(temp_str,end='')
    QFT_str += temp_str
    
    q.IQFT(all)
    q.IQFT(all)
    
    temp_str = f'{str(q)}\n'
    q.IQFT(all)
    q.IQFT(all)
    temp_str += f'{str(q)}\n\n'
    print(temp_str,end='')
    IQFT_str += temp_str

with open(QFT_file, 'w') as file:
    file.write(QFT_str)

with open(IQFT_file, 'w') as file:
    file.write(IQFT_str)