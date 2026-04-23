import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import product

class ModularSpiral:
    """
    A moduláris térben haladó spirálpálya.
    Equivalent: Φ_k(n) = (n mod p_1, ..., n mod p_k)
    """
    def __init__(self, moduli):
        self.moduli = np.array(moduli)
        self.k = len(moduli)
        self.period = np.prod(moduli)
        
    def map_number(self, n):
        """Φ(n) = (n mod m_1, ..., n mod m_k)"""
        return np.array([n % m for m in self.moduli])
    
    def trajectory(self, n_start=0, n_steps=None):
        """A pálya a moduláris térben"""
        if n_steps is None:
            n_steps = self.period * 2
        points = []
        for n in range(n_start, n_start + n_steps):
            points.append(self.map_number(n))
        return np.array(points)
    
    def to_2d_projection(self, points, dim1=0, dim2=1):
        """Kivetítés 2D-re vizualizációhoz"""
        return points[:, dim1], points[:, dim2]


class PrimeDetector:
    """Prím detektálás a moduláris pályában"""
    def __init__(self, primes_up_to=100):
        self.primes = self._sieve(primes_up_to)
        
    def _sieve(self, n):
        """Egyszerű Eratoszthenész szita"""
        sieve = np.ones(n+1, dtype=bool)
        sieve[:2] = False
        for i in range(2, int(n**0.5)+1):
            if sieve[i]:
                sieve[i*i:n+1:i] = False
        return np.where(sieve)[0].tolist()
    
    def is_prime(self, n):
        return n in self.primes if n <= max(self.primes) else None
    
    def classify(self, n):
        """Osztályozás: prime, composite, 1, or unknown"""
        if n == 1:
            return 'unit'
        if self.is_prime(n):
            return 'prime'
        if n <= max(self.primes):
            return 'composite'
        return 'unknown'
    
class SingularityField:
    """
    A diszkrét vektormező, ahol a prímek szingularitásként jelennek meg.
    DVFM V.1: V(s) = 0  ->  szingularitás
    """
    def __init__(self, moduli):
        self.spiral = ModularSpiral(moduli)
        self.detector = PrimeDetector(primes_up_to=500)
        
    def vector_field(self, n):
        """
        V(n) = Φ(n+1) - Φ(n) = (1 mod m_1, ..., 1 mod m_k)
        Ez konstans! A szingularitás NEM a vektormezőben van,
        hanem a pálya geometriájában.
        """
        phi_n = self.spiral.map_number(n)
        phi_n1 = self.spiral.map_number(n+1)
        # modulo különbség (ciklikus)
        diff = (phi_n1 - phi_n) % self.spiral.moduli
        return diff
    
    def is_singularity(self, n):
        """
        DVFM V.1 definíció: V(s) = 0
        De itt V(n) konstans (1,1,...,1) mod m_i,
        ami soha nem 0 a nem-triviális modulusoknál.
        
        A VALÓDI szingularitás: amikor a pálya "megszakad" a térben.
        Ez a prímeknél történik: nincs előző pálya, ami betöltené.
        """
        # Alternatív: a pálya "új" irányt vesz
        # Ezt a szomszédos pontok moduláris távolságával mérjük
        phi_n = self.spiral.map_number(n)
        phi_n_minus_1 = self.spiral.map_number(n-1) if n > 0 else phi_n
        
        # A "szakadás" mértéke: a pálya görbülete a moduláris térben
        # Egyszerűsítve: ha n prím, a moduláris távolság nagyobb
        modular_distance = np.sum((phi_n - phi_n_minus_1) % self.spiral.moduli)
        
        return modular_distance > np.mean(self.spiral.moduli) * 0.7


def create_spiral_visualization(moduli=(2,3,5), n_max=100):
    """
    A központi vizualizáció: 
    - A moduláris pálya 2D vetülete
    - Prímek kiemelve
    - A "szakadások" (új irányok) jelölve
    """
    spiral = ModularSpiral(moduli)
    field = SingularityField(moduli)
    
    # Pálya kiszámítása
    points = spiral.trajectory(n_start=0, n_steps=n_max)
    
    # 2D vetítés (első két modulus használatával)
    x, y = spiral.to_2d_projection(points, dim1=0, dim2=1)
    
    # Minden pont osztályozása
    detector = PrimeDetector(n_max * 2)
    colors = []
    sizes = []
    for i, n in enumerate(range(n_max)):
        cls = detector.classify(n)
        if cls == 'prime':
            colors.append('red')
            sizes.append(50)
        elif cls == 'composite':
            colors.append('blue')
            sizes.append(20)
        else:
            colors.append('gray')
            sizes.append(15)
    
    # Ábra
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Bal oldal: a spirálpálya
    ax1.scatter(x, y, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=0.3)
    ax1.plot(x, y, 'k-', alpha=0.2, linewidth=0.5)
    ax1.set_title(f'Moduláris spirálpálya\nM = {moduli}\nPiros = prím, Kék = összetett')
    ax1.set_xlabel(f'$n \\mod {moduli[0]}$')
    ax1.set_ylabel(f'$n \\mod {moduli[1]}$')
    ax1.grid(True, alpha=0.3)
    
    # 2. Jobb oldal: a "szakadások" – ahol prím születik
    #    Ez a DVMF divergencia analógiája
    divergences = []
    n_values = list(range(1, n_max))
    for n in n_values:
        # Diszkrét divergencia a pályán
        phi_n = spiral.map_number(n)
        phi_n1 = spiral.map_number(n+1)
        phi_n_1 = spiral.map_number(n-1)
        
        # Egyszerűsített divergencia: |Φ(n+1)-Φ(n)| - |Φ(n)-Φ(n-1)|
        forward = np.sum(np.abs(phi_n1 - phi_n))
        backward = np.sum(np.abs(phi_n - phi_n_1))
        div = forward - backward
        divergences.append(div)
    
    prime_positions = [n for n in n_values if detector.is_prime(n)]
    prime_divs = [divergences[n-1] for n in prime_positions if n-1 < len(divergences)]
    
    ax2.plot(n_values, divergences, 'b-', alpha=0.5, label='Divergencia')
    ax2.scatter(prime_positions, prime_divs, c='red', s=30, zorder=5, label='Prímek')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('Diszkrét divergencia a pályán\nAhol a divergencia ugrik = "szakadás"')
    ax2.set_xlabel('n')
    ax2.set_ylabel('Divergencia')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def coarse_grain_primes(moduli, n_max=500, delta=0.3):
    """
    FRD hierarchikus réteg:
    A prímek körüli régiókat összevonjuk magasabb szintű csomópontokká.
    """
    spiral = ModularSpiral(moduli)
    detector = PrimeDetector(n_max * 2)
    
    # 1. szint: eredeti pontok
    points = spiral.trajectory(n_start=0, n_steps=n_max)
    x, y = spiral.to_2d_projection(points)
    
    # 2. Klaszterek azonosítása prímek körül
    clusters = []
    used = set()
    
    for n in range(n_max):
        if detector.is_prime(n) and n not in used:
            # Klaszter: a prím és a körülötte lévő delta távolságú pontok
            phi_p = spiral.map_number(n)
            cluster = [n]
            used.add(n)
            
            for m in range(max(0, n-5), min(n_max, n+6)):
                if m not in used:
                    phi_m = spiral.map_number(m)
                    # Távolság a moduláris térben
                    dist = np.sum((phi_m - phi_p) % spiral.moduli)
                    if dist < delta * np.sum(spiral.moduli):
                        cluster.append(m)
                        used.add(m)
            
            if len(cluster) > 1:  # csak ha van klaszter
                clusters.append(cluster)
    
    # 3. Vizualizáció: színezzük a klasztereket
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cluster_colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))
    
    # Először a nem klaszterezett pontok
    non_clustered = [n for n in range(n_max) if n not in used]
    for n in non_clustered:
        phi = spiral.map_number(n)
        ax.scatter(phi[0], phi[1], c='lightgray', s=15, alpha=0.5)
    
    # Aztán a klaszterek
    for idx, cluster in enumerate(clusters):
        for n in cluster:
            phi = spiral.map_number(n)
            color = cluster_colors[idx]
            ax.scatter(phi[0], phi[1], c=[color], s=30, edgecolors='black')
            
            # A prím (klaszter középpontja) kiemelve
            if detector.is_prime(n):
                ax.scatter(phi[0], phi[1], c='red', s=80, marker='*', zorder=10)
    
    ax.set_title(f'Koarsz-grainelés: prímek körüli klaszterek\nM = {moduli}')
    ax.set_xlabel(f'n mod {moduli[0]}')
    ax.set_ylabel(f'n mod {moduli[1]}')
    ax.grid(True, alpha=0.3)
    
    return fig


# Futtatás
if __name__ == "__main__":
    fig = create_spiral_visualization(moduli=(2,3,5), n_max=200)
    plt.show()