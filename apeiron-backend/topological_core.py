import numpy as np

class ApeironV53TopologicalCore:
    """
    v53.1 Rigorous Quantum Error Correction & Pauli Stabilizer Recovery Core.
    Replaces ideal-state mixing with true Pauli correction operators (X, Z) 
    conditioned exclusively on measured error syndromes.
    """
    def __init__(self):
        # Ideal Bell state |Phi+> = (|00> + |11>) / sqrt(2)
        self.psi_bell = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], dtype=complex)
        self.rho_ideal = np.outer(self.psi_bell, self.psi_bell.conj())
        
        # Pauli operators
        self.I = np.array([[1, 0], [0, 1]], dtype=complex)
        self.X = np.array([[0, 1], [1, 0]], dtype=complex)
        self.Z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        # Two-qubit Pauli operators for correction
        self.IX = np.kron(self.I, self.X)
        self.ZI = np.kron(self.Z, self.I)
        self.XZ = np.kron(self.X, self.Z)

        # Stabilizer generators: S1 = X \otimes X, S2 = Z \otimes Z
        self.S_XX = np.kron(self.X, self.X)
        self.S_ZZ = np.kron(self.Z, self.Z)

    def apply_kraus_noise(self, gamma=0.25):
        """
        Applies rigorous Kraus amplitude damping operators to simulate physical decoherence.
        """
        K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]], dtype=complex)
        K1 = np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex)
        
        K0_2q = np.kron(K0, np.eye(2, dtype=complex))
        K1_2q = np.kron(K1, np.eye(2, dtype=complex))
        
        rho_noisy = np.dot(K0_2q, np.dot(self.rho_ideal, K0_2q.conj().T)) + \
                    np.dot(K1_2q, np.dot(self.rho_ideal, K1_2q.conj().T))
                    
        trace = np.real(np.trace(rho_noisy))
        if trace > 0:
            rho_noisy /= trace
        return rho_noisy

    def measure_stabilizers_and_extract_syndrome(self, rho_noisy):
        """
        Performs true expectation value measurements of S_XX and S_ZZ 
        to dynamically extract the error syndrome.
        """
        exp_xx = np.real(np.trace(np.dot(self.S_XX, rho_noisy)))
        exp_zz = np.real(np.trace(np.dot(self.S_ZZ, rho_noisy)))
        
        s_bit1 = 0 if exp_xx >= 0.75 else 1
        s_bit2 = 0 if exp_zz >= 0.75 else 1
        syndrome_flag = f"{s_bit1}{s_bit2}"
        
        fidelity = np.real(np.trace(np.dot(self.rho_ideal, rho_noisy)))
        return syndrome_flag, exp_xx, exp_zz, fidelity

    def apply_pauli_recovery(self, rho_noisy, syndrome_flag):
        """
        Applies discrete Pauli correction operators (X, Z) based ONLY on the 
        extracted syndrome, without peeking at the ideal state.
        """
        correction_operator = np.eye(4, dtype=complex)
        
        if syndrome_flag == "10":
            # Phase flip detected by XX stabilizer violation
            correction_operator = self.ZI
        elif syndrome_flag == "01":
            # Bit flip detected by ZZ stabilizer violation
            correction_operator = self.IX
        elif syndrome_flag == "11":
            # Combined phase & bit flip
            correction_operator = self.XZ
            
        # Apply correction channel: rho_recovered = U_corr * rho_noisy * U_corr^dagger
        rho_recovered = np.dot(correction_operator, np.dot(rho_noisy, correction_operator.conj().T))
        
        trace = np.real(np.trace(rho_recovered))
        if trace > 0:
            rho_recovered /= trace
            
        return rho_recovered
