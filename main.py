import hashlib
import time
import random
from threading import Thread
import matplotlib.pyplot as plt
from datetime import datetime

class BitcoinMiningSimulator:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty # Nombre de zero requis qu debut du hash
        self.nonce = 0
        self.hash_rate = 0
        self.running = False
        self.hashes_computed = 0
        self.start_time = 0
        self.found_blocks = 0
        self.hash_rate_history = []
        self.timestamps = []

    def calculate_hash(self, data):
        """Calcule le hash SHA-256 des données données"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def mine_block(self, data):
        """Tente de miner un bloc avec les données données"""
        target = '0' * self.difficulty
        self.nonce = 0
        
        while self.running:
            self.nonce += 1
            self.hashes_computed += 1
            input_data = data + str(self.nonce)
            current_hash = self.calculate_hash(input_data)
            
            if current_hash.startswith(target):
                self.found_blocks += 1
                print(f"\nBloc trouvé! Nonce: {self.nonce}")
                print(f"Hash: {current_hash}")
                return current_hash
        
        return None
    
    def start_mining(self, data="Block data"):
        """Démarre le minage"""
        self.running = True
        self.start_time = time.time()
        print(f"Démarrage du minage avec difficulté {self.difficulty}...")
        
        # Thread pour mettre à jour le taux de hash
        Thread(target=self.update_hash_rate, daemon=True).start()
        
        # Thread pour le minage principal
        Thread(target=self.mine_block, args=(data,), daemon=True).start()
    
    def stop_mining(self):
        """Arrête le minage"""
        self.running = False
        elapsed = time.time() - self.start_time
        print(f"\nMinage arrêté après {elapsed:.2f} secondes")
        print(f"Hashes calculés: {self.hashes_computed}")
        print(f"Taux de hash moyen: {self.hashes_computed/elapsed:.2f} H/s")
        print(f"Blocs trouvés: {self.found_blocks}")
    
    def update_hash_rate(self):
        """Met à jour le taux de hash chaque seconde"""
        while self.running:
            time.sleep(1)
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                current_hash_rate = self.hashes_computed / elapsed
                self.hash_rate = current_hash_rate
                self.hash_rates_history.append(current_hash_rate)
                self.timestamps.append(datetime.now())
                print(f"\rHash rate: {current_hash_rate:.2f} H/s | Hashes: {self.hashes_computed} | Blocs: {self.found_blocks}", end="")
    
    def plot_hash_rate(self):
        """Affiche un graphique du taux de hash au fil du temps"""
        if not self.hash_rates_history:
            print("Aucune donnée à afficher")
            return
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.timestamps, self.hash_rates_history)
        plt.title("Évolution du taux de hash")
        plt.xlabel("Temps")
        plt.ylabel("Hash rate (H/s)")
        plt.grid(True)
        plt.show()

def main():
    simulator = BitcoinMiningSimulator(difficulty=4)
    
    try:
        print("Simulateur de minage Bitcoin")
        print("--------------------------")
        print("Options:")
        print("1. Démarrer le minage")
        print("2. Afficher le graphique du taux de hash")
        print("3. Quitter")
        
        while True:
            choice = input("\nVotre choix: ")
            
            if choice == "1":
                if simulator.running:
                    print("Le minage est déjà en cours")
                    continue
                
                data = input("Entrez les données du bloc (ou laissez vide pour la valeur par défaut): ")
                if not data:
                    data = f"Bloc #{random.randint(1000, 9999)}"
                
                simulator.start_mining(data)
                input("Appuyez sur Entrée pour arrêter le minage...")
                simulator.stop_mining()
            
            elif choice == "2":
                simulator.plot_hash_rate()
            
            elif choice == "3":
                if simulator.running:
                    simulator.stop_mining()
                print("Au revoir!")
                break
            
            else:
                print("Choix invalide")
    
    except KeyboardInterrupt:
        if simulator.running:
            simulator.stop_mining()
        print("\nProgramme terminé")

if __name__ == "__main__":
    main()