import math
from random import choices, randrange

class Qubits_System():
    def __init__(self, q_num, init = 0):
        self.q_num = q_num
        #self.state = [[Qubits_System.generate_bin(self.q_num, i), 0] for i in range(2**self.q_num)]
        #self.state[init][1] = 1
        if isinstance(init, int):
            assert 0 <= init < 2*q_num, 'initial state(int) must be in range [0, 2^q_num-1]'
            self.state = [[Qubits_System.generate_bin(self.q_num, init), 1]]
        elif isinstance(init, str):
            assert all(s in {'0', '1'} for s in init), 'initial state(str) must be a binary string'
            assert len(init) == self.q_num, 'initial state does not match qubit number'
            self.state = [[init, 1]]
        elif isinstance(init, list):
            assert all(type(l)==list and len(l) == 2 for l in init), 'initial state(list) must be list of 2-lists'
            init.sort(key = lambda t:t[0])
            assert all(init[i][0] != init[i+1][0] for i in range(len(init)-1)), 'cannot have two identical state'
            self.state = init
            self.normalize()
        else:
            raise AssertionError('illegal type of initial state')
    
    @staticmethod
    def generate_bin(q_num, i):
        return '0'*(q_num-len(bin(i)[2:]))+bin(i)[2:]
    
    def __str__(self):
        returned_str = ''
        for s, a in self.state:
            if isinstance(a, complex):
                if abs(a.imag) <= 0.0001:
                    if abs(a.real) <= 0.0001:
                        pass
                    elif a.real > 0:
                        returned_str += f' + {a.real:.2f}|{s}>'
                    elif a.real < 0:
                        returned_str += f' - {-a.real:.2f}|{s}>'
                else:
                    if a.imag > 0:
                        returned_str += f' + ({a.real:.2f}+{a.imag:.2f}i)|{s}>'
                    elif a.imag < 0:
                        returned_str += f' + ({a.real:.2f}-{-a.imag:.2f}i)|{s}>'
            elif a > 0:
                returned_str += f' + {a:.2f}|{s}>'
            elif a < 0:
                returned_str += f' - {-a:.2f}|{s}>'
        if len(returned_str) > 0 and returned_str[1] == '+':
            return returned_str[3:]
        else:
            return returned_str[1:]
    
    def __repr__(self):
        return f'Qubits_System({self.q_num}, init = {self.state})'
    
    def __getitem__(self, key):
        for i in range(len(self.state)):
            if self.state[i][0] == key:
                return self.state[i][1]
    
    def __setitem__(self, key, value):
        for i in range(len(self.state)):
            if self.state[i][0] == key:
                self.state[i][1] = value
                
    def normalize(self):
        L2_norm = math.sqrt(sum(abs(i)**2 for _, i in self.state))
        if L2_norm != 1:
            for i in range(len(self.state)):
                self.state[i][1] /= L2_norm
    
    def merge_sorted_state(self):
        temp_s = ['0'*self.q_num]
        temp_a = [0]
        for s, a in self.state:
            if s == temp_s[-1]:
                temp_a[-1] += a
            else:
                temp_s.append(s)
                temp_a.append(a)
        self.state = [[s, a] for s, a in zip(temp_s, temp_a)]
                
    
    def X(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.X(*(x for x in range(self.q_num)))
        else:
            pos_l = [self.q_num-1-x for x in args_set]
            if any(i<0 for i in pos_l):
                raise ValueError('qubit number doesn\'t match')
            for pos in pos_l:
                for i in range(len(self.state)):
                    if self.state[i][0][pos] == '0':
                        self.state[i][0] = self.state[i][0][:pos] + '1' + self.state[i][0][pos+1:]
                    else:
                        self.state[i][0] = self.state[i][0][:pos] + '0' + self.state[i][0][pos+1:]
            self.state.sort(key = lambda t:t[0])
        
    def Y(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.Y(*(x for x in range(self.q_num)))
        else:
            pos_l = [self.q_num-1-x for x in args_set]
            if any(i<0 for i in pos_l):
                raise ValueError('qubit number doesn\'t match')
            for pos in pos_l:
                for i in range(len(self.state)):
                    if self.state[i][0][pos] == '0':
                        self.state[i][0] = self.state[i][0][:pos] + '1' + self.state[i][0][pos+1:]
                        if self.state[i][1] != 0:
                            self.state[i][1] *= 1j
                    else:
                        self.state[i][0] = self.state[i][0][:pos] + '0' + self.state[i][0][pos+1:]
                        if self.state[i][1] != 0:
                            self.state[i][1] *= -1j
            self.state.sort(key = lambda t:t[0])
    
    def Z(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.Z(*(x for x in range(self.q_num)))
        else:
            pos_l = [self.q_num-1-x for x in args_set]
            for pos in pos_l:
                if pos < 0:
                    raise ValueError('qubit number doesn\'t match')
                for i in range(len(self.state)):
                    if self.state[i][0][pos] == '1':
                        self.state[i][1] *= -1
        
    def H(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.H(*(x for x in range(self.q_num)))
        else:
            pos_l = [self.q_num-1-x for x in args_set]
            for pos in pos_l:
                if pos < 0:
                    raise ValueError('qubit number doesn\'t match')
                c = 1/math.sqrt(2)
                for i in range(len(self.state)):
                    if self.state[i][0][pos] == '0':
                        s1 = self.state[i][0]
                        s2 = self.state[i][0][:pos] + '1' + self.state[i][0][pos+1:]
                        amp = c*self.state[i][1]
                        self.state[i][1] = 0
                        self.state.append([s1, amp])
                        self.state.append([s2, amp])
                    else:
                        s1 = self.state[i][0][:pos] + '0' + self.state[i][0][pos+1:]
                        s2 = self.state[i][0]
                        amp = c*self.state[i][1]
                        self.state[i][1] = 0
                        self.state.append([s1, amp])
                        self.state.append([s2, -amp])
                self.state.sort(key = lambda t:t[0])
                self.merge_sorted_state()
                #self.normalize()
    
    def SWAP(self, x, y):
        pos_x = self.q_num-1-x
        pos_y = self.q_num-1-y
        if pos_x < 0 or pos_y < 0:
            raise ValueError('qubit number doesn\'t match')
        for i in range(len(self.state)):
            temp_x = self.state[i][0][pos_x]
            temp_y = self.state[i][0][pos_y]
            self.state[i][0] = self.state[i][0][:pos_y] + temp_x + self.state[i][0][pos_y+1:]
            self.state[i][0] = self.state[i][0][:pos_x] + temp_y + self.state[i][0][pos_x+1:]
        self.state.sort(key = lambda t:t[0])
        
    def CNOT(self, x, y):
        pos_x = self.q_num-1-x
        pos_y = self.q_num-1-y
        if pos_x < 0 or pos_y < 0:
            raise ValueError('qubit number doesn\'t match')
        for i in range(len(self.state)):
            if self.state[i][0][pos_x] == '1':
                if self.state[i][0][pos_y] == '0':
                    self.state[i][0] = self.state[i][0][:pos_y] + '1' + self.state[i][0][pos_y+1:]
                else:
                    self.state[i][0] = self.state[i][0][:pos_y] + '0' + self.state[i][0][pos_y+1:]
        self.state.sort(key = lambda t:t[0])
        self.merge_sorted_state()
        self.normalize()
    
    def QFT(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.QFT(*(x for x in range(self.q_num)))
        else:
            operated_q = sorted(args_set)
            if operated_q[-1] >= self.q_num:
                raise ValueError('qubit number doesn\'t match')
            q_n = len(operated_q)
            N = 2**q_n
            omega = math.cos(2*math.pi/N) + 1j*math.sin(2*math.pi/N)
            matrix_T = [[omega**(i*j) for i in range(N)] for j in range(N)]
            pos_l = sorted([self.q_num-1-x for x in operated_q])
            for i in range(len(self.state)):
                q_bin_str = ''
                for p in pos_l:
                    q_bin_str += self.state[i][0][p]
                q_int = int(q_bin_str, 2)
                count = 0
                
                for element in matrix_T[q_int]:
                                    
                    #current state
                    cur_s = self.state[i][0]
                    
                    #qubits that are substituded with new qubits
                    sub_q = Qubits_System.generate_bin(len(operated_q), count)
                    for p,q in zip(pos_l, sub_q):
                        cur_s = cur_s[:p] + q + cur_s[(p+1):]
                    
                    self.state.append([cur_s, element*self.state[i][1]])
                    count += 1
                self.state[i][1] = 0
            self.state.sort(key = lambda t:t[0])
            self.merge_sorted_state()
            self.normalize()
    
    def IQFT(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.IQFT(*(x for x in range(self.q_num)))
        else:
            operated_q = sorted(args_set)
            if operated_q[-1] >= self.q_num:
                raise ValueError('qubit number doesn\'t match')
            q_n = len(operated_q)
            N = 2**q_n
            omega = math.cos(2*math.pi/N) - 1j*math.sin(2*math.pi/N)
            matrix_T = [[omega**(i*j) for i in range(N)] for j in range(N)]
            pos_l = sorted([self.q_num-1-x for x in operated_q])
            for i in range(len(self.state)):
                q_bin_str = ''
                for p in pos_l:
                    q_bin_str += self.state[i][0][p]
                q_int = int(q_bin_str, 2)
                count = 0
                
                for element in matrix_T[q_int]:
                                    
                    #current state
                    cur_s = self.state[i][0]
                    
                    #qubits that are substituded with new qubits
                    sub_q = Qubits_System.generate_bin(len(operated_q), count)
                    for p,q in zip(pos_l, sub_q):
                        cur_s = cur_s[:p] + q + cur_s[(p+1):]
                    
                    self.state.append([cur_s, element*self.state[i][1]])
                    count += 1
                self.state[i][1] = 0
            self.state.sort(key = lambda t:t[0])
            self.merge_sorted_state()
            self.normalize()
    
    def C(self, o, c, t):
        if not callable(o):
            raise ValueError('first arg must be an operation')
        
        if type(c) == int:
            c = [c]
        if type(t) == int:
            t = [t]
        
        assert len(c) > 0 and len(t) > 0, 'must have at least one control and target qubit'
        assert all(cq not in t for cq in c), 'cannot have the same cq and tq'
        
        pos_c = [self.q_num-1-cq for cq in c]
        assert all(p >= 0 for p in pos_c), 'qubit number doesn\'t match'
        assert all(0 <= tq < 2**self.q_num for tq in t), 'qubit number doesn\'t match'
        
        for i in range(len(self.state)):
            if all(self.state[i][0][pos] == '1' for pos in pos_c):
                amp = self.state[i][1]
                _q_new = Qubits_System(self.q_num, init = self.state[i][0])
                eval(f'_q_new.{o.__name__}(*t)')
                self.state[i][1] = 0
                for s in _q_new.state:
                    s[1] *= amp
                    q.state.append(s)

        self.state.sort(key = lambda t:t[0])
        self.merge_sorted_state()
        self.normalize()
    
    ''' #One-controll version
    def C(self, *args):
        if not callable(type(args[0])):
            raise ValueError('first arg must be an operation')
        args_set = set(args[1:])
        if len(args_set) < 2:
            raise ValueError('must operate on at least 2 qubits')
        
        operation = args[0]
        C_q = args[1]
        pos_C_q = self.q_num-1-C_q
        operated_q_set = set(args[2:])
        o_pos_l = [self.q_num-1-x for x in operated_q_set]
        if pos_C_q <0 or any(x<0 for x in o_pos_l):
            raise ValueError('qubit number doesn\'t match')
        for i in range(len(self.state)):
            if self.state[i][0][pos_C_q] == '1':
                amp = self.state[i][1]
                _q_new = Qubits_System(self.q_num, int(self.state[i][0], 2))
                eval(f'_q_new.{operation.__name__}(*operated_q_set)')
                self.state[i][1] = 0
                for s in _q_new.state:
                    s[1] *= amp
                    q.state.append(s)

        self.state.sort(key = lambda t:t[0])
        self.merge_sorted_state()
        self.normalize()
    '''
    
    def M(self, *args):
        args_set = set(args)
        if any(i is not all and type(i) != int for i in args):
            raise ValueError('must be int or all')
        elif all in args_set:
            self.M(*(x for x in range(self.q_num)))
        else:
            sorted_arg = sorted(args_set)
            c = choices([t[0] for t in self.state], [abs(t[1])**2 for t in self.state], k=1)[0]
            c_q = ''
            
            for q in sorted_arg:
                pos_q = self.q_num-1-q
                c_q += c[pos_q]
            
            temp_s = []
            for s in self.state:
                s_q = ''
                for q in sorted_arg:
                    pos_q = self.q_num-1-q
                    s_q += s[0][pos_q]
                if s_q == c_q:
                    temp_s.append(s)
            
            self.state = temp_s
            self.state.sort(key = lambda t:t[0])
            self.normalize()
    
    def mod(self, g, N):
        assert self.q_num % 2 == 0, 'must be even number of qubits'
        assert N**2 < 2**(self.q_num/2) <= 2*(N**2), 'unsuitable number of qubits'
        for s in self.state:
            
            i_init = s[0][:self.q_num//2]
            
            int_i = int(i_init, 2)
            int_a = pow(g, int_i, N)
            bin_a = Qubits_System.generate_bin(self.q_num//2, int_a)
            
            o_init = s[0][self.q_num//2:]
            o_fin = ''
            for b, o in zip(bin_a, o_init):
                if b == o:
                    o_fin += '0'
                else:
                    o_fin += '1'
            
            s[0] = i_init + o_fin
        
        self.state.sort(key = lambda t:t[0])
    
    def init_oracle(self, o='r', n=None):
        assert isinstance(o, str), 'must be "r" or binary str'
        if n == None:
            n = self.q_num
        if o == 'r':
            self.o = Qubits_System.generate_bin(n-1, randrange(0, 2**(n-1)-1))
        else:
            self.o = o
    
    def oracle(self, *args):
        assert 'o' in self.__dict__, 'must initalize oracle first'
        if len(args) == 0 or args == (all,):
            args = list(range(0, self.q_num))
        assert len(self.o)+1 == len(args), "qubit number doesn't match"
        
        sorted_args = sorted(set(args), key = lambda x:-x)
        posl = [self.q_num-1-q for q in sorted_args]
        for s in self.state:
            if ''.join(s[0][a] for a in posl[:-1]) == self.o:
                s[0] = s[0][:-1] + str(int(not int(s[0][posl[-1]])))
        
        self.state.sort(key = lambda t:t[0])
                                    
        
    def reduce_phase(self):
        assert len(self.state) == 1, 'Not very meaningful to reduce phases of superposition state'
        self.state[0][1] = 1
    
    def reset(self):
        self.state = [[Qubits_System.generate_bin(self.q_num, 0), 1]]
            
if __name__ == '__main__':
    
    done = False
    q_num_set = False
    while True:
        if not q_num_set:
            while True:
                q_num = input('Number of qubits: ')
                try:
                    q_num = int(q_num)
                    print()
                    break
                except Exception as exc:
                    print(exc)
                    print()
            q_num_set = True
            q = Qubits_System(int(q_num))
            file_str = f'{q.q_num}-qubit system\nInitial State:\n{str(q)}\n\n'
            print(file_str,end='')
        
        answer = input("Operation: ")
        if answer == 'done':
            file_name = input("File name: ")
            if file_name != '':
                with open(file_name, 'w') as file:
                    file.write(file_str)
                print('\n==========Saved==========\n')
            else:
                print('\n==========Not saved==========\n')
            while True:
                answer = input("Y to continue/N to quit: ")
                if answer == 'Y':
                    q_num_set = False
                    print('\n=============================\n')
                    break
                elif answer == 'N':
                    done = True
                    break
                else:
                    print('illegal answer')
                    print()
            if done:
                break
        
        elif answer == 'seq':
            sub_a = input('Operations: ')
            for s in sub_a.split(' '):
                try:
                    eval(f'q.{s}')
                    file_str += f'{s}\n'
                except Exception as exc:
                    print(f'{str(exc)}\n{str(q)}\n\n', end='')   
                    break     
            file_str += f'{str(q)}\n\n'
            print(f'{str(q)}\n\n', end='')   
                    
        else:
            try:
                eval(f'q.{answer}')
                temp_str = f'{str(q)}\n\n'
                file_str += f'{answer}\n' + temp_str
                print(temp_str, end='')
            except Exception as exc:
                temp_str = f'{str(exc)}\n{str(q)}\n\n'
                #file_str += temp_str
                print(temp_str, end='')
        