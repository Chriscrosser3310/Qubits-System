from qubits_system import Qubits_System

for i in range(3):
    file_str =  ''
    for j in range(2**3):
        q = Qubits_System(3, j)
        file_str += f'{str(q)}\n'
        q.QFT(all)
        q.H(i)
        q.IQFT(all)
        file_str += f'{str(q)}\n\n'
    with open(f'QFT_Hi_IQFT/QFT_H{i}_IQFT.txt', 'w') as file:
        file.write(file_str)