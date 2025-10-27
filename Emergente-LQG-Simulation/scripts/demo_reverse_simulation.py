#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nächster Schritt: Reverse-LQG-Simulation

Jetzt können wir die komplette Reverse-Simulation implementieren:
    
    demo_reverse_simulation.py
    
Created on Sun Oct 26 09:31:21 2025

@author: gh
"""
from typing import List
from Spin_Netzwerk_Klasse_Demo import SpinNetwork, LQGOperations, SpinVertex, SpinEdge

class ReverseLQGSimulation:
    """
    Reverse-Simulation für LQG: Vom heutigen Zustand zum Urzustand
    """
    
    def __init__(self, observed_network: SpinNetwork):
        self.initial_network = observed_network
        self.ops = LQGOperations()
        self.history = []
        
    def reverse_evolution_step(self, network: SpinNetwork) -> List[SpinNetwork]:
        """
        Ein Reverse-Schritt: Erzeugt mögliche Vorgänger-Zustände
        """
        candidate_networks = []
        
        # 1. Kanten-Verschmelzung (Reduktion der Komplexität)
        for edge1 in network.edges:
            for edge2 in network.edges:
                if edge1.id >= edge2.id:
                    continue
                    
                # Prüfe ob Kanten verschmelzbar sind
                common_vertex = self.ops._find_common_vertex(edge1, edge2)
                if common_vertex is not None:
                    merged = self.ops.edge_merge(network, edge1.id, edge2.id)
                    if self._is_physically_valid(merged):
                        candidate_networks.append(merged)
        
        # 2. Knoten-Verschmelzung (weitere Reduktion)
        for vertex1 in network.vertices:
            for vertex2 in network.vertices:
                if vertex1.id >= vertex2.id:
                    continue
                    
                connecting_edges = self.ops._find_connecting_edges(network, vertex1.id, vertex2.id)
                if len(connecting_edges) == 1:  # Genau eine Verbindung
                    merged = self.ops.vertex_merge(network, vertex1.id, vertex2.id)
                    if self._is_physically_valid(merged):
                        candidate_networks.append(merged)
        
        return candidate_networks
    
    def _is_physically_valid(self, network: SpinNetwork) -> bool:
        """
        Prüft physikalische Konsistenz eines Netzwerks
        """
        # Mindest-Anforderungen
        if len(network.vertices) < 2:
            return False
            
        if len(network.edges) < 3:
            return False
            
        # Homogenitäts-Check (für Reverse: sollte zunehmen)
        homogeneity = network.homogeneity_metric()
        if homogeneity < 0.3:  # Zu inhomogen
            return False
            
        return True
    
    def find_primordial_state(self, max_steps: int = 10) -> List[SpinNetwork]:
        """
        Findet primordialen Zustand durch iterative Reverse-Simulation
        """
        print("🔬 Starte Reverse-LQG-Simulation...")
        current_candidates = [self.initial_network]
        self.history = [current_candidates]
        
        for step in range(max_steps):
            print(f"⏳ Reverse-Schritt {step + 1}/{max_steps}")
            
            next_candidates = []
            for candidate in current_candidates:
                predecessors = self.reverse_evolution_step(candidate)
                next_candidates.extend(predecessors)
            
            if not next_candidates:
                print("❌ Keine weiteren physikalisch validen Zustände gefunden")
                break
                
            # Zustandsauswahl basierend auf Homogenität
            next_candidates.sort(key=lambda n: n.homogeneity_metric(), reverse=True)
            current_candidates = next_candidates[:5]  # Behalte Top 5
            
            self.history.append(current_candidates)
            
            # Fortschrittsausgabe
            best_candidate = current_candidates[0]
            print(f"   - Beste Homogenität: {best_candidate.homogeneity_metric():.3f}")
            print(f"   - Knoten: {len(best_candidate.vertices)}, Kanten: {len(best_candidate.edges)}")
            
            # Abbruchkriterium: Hohe Homogenität erreicht
            if best_candidate.homogeneity_metric() > 0.95:
                print("🎯 Primordialzustand erreicht!")
                break
        
        return current_candidates

# Demo der Reverse-Simulation
def demo_reverse_simulation():
    """Demonstriert die komplette Reverse-LQG-Simulation"""
    print("🚀 REVERSE-LQG-SIMULATION - Vom Heute zum Urzustand")
    print("=" * 60)
    
    # Erstelle komplexeres "heutiges" Netzwerk
    today_network = SpinNetwork()
    
    # 6 Knoten (komplexere Struktur)
    positions = [
        (0, 0, 0), (1, 0, 0), (0.5, 0.866, 0),
        (0.5, 0.289, 0.816), (0, 0.577, 0.816), (1, 0.577, 0.816)
    ]
    
    for i in range(6):
        today_network.add_vertex(SpinVertex(i, [], 0.0, positions[i]))
    
    # Komplexeres Kanten-Netzwerk
    edges_data = [
        (0, 1, 1.0), (0, 2, 1.5), (0, 3, 2.0), (0, 4, 1.0),
        (1, 2, 0.5), (1, 3, 1.0), (1, 5, 1.5),
        (2, 4, 1.0), (2, 5, 2.0),
        (3, 4, 1.5), (3, 5, 1.0),
        (4, 5, 0.5)
    ]
    
    for i, (src, tgt, spin) in enumerate(edges_data):
        today_network.add_edge(SpinEdge(i, src, tgt, spin))
    
    today_network.update_volumes()
    
    print("Heutiger Zustand (komplexes Netzwerk):")
    print(f"- Knoten: {len(today_network.vertices)}, Kanten: {len(today_network.edges)}")
    print(f"- Homogenität: {today_network.homogeneity_metric():.3f}")
    
    today_network.visualize_2d("Heutiger Zustand - Komplex")
    
    # Starte Reverse-Simulation
    simulator = ReverseLQGSimulation(today_network)
    primordial_candidates = simulator.find_primordial_state(max_steps=8)
    
    # Ergebnisse analysieren
    if primordial_candidates:
        best_primordial = primordial_candidates[0]
        print(f"\n🎉 BESTER PRIMORDIALZUSTAND GEFUNDEN:")
        print(f"- Knoten: {len(best_primordial.vertices)}")
        print(f"- Kanten: {len(best_primordial.edges)}") 
        print(f"- Homogenität: {best_primordial.homogeneity_metric():.3f}")
        print(f"- Gesamtvolumen: {best_primordial.total_volume:.3f}")
        
        best_primordial.visualize_2d("Bester Primordialzustand")
        
        # Zeige Entwicklung
        print(f"\n📈 ENTWICKLUNG der Homogenität:")
        for i, candidates in enumerate(simulator.history):
            if candidates:
                best = candidates[0]
                print(f"  Schritt {i}: Homogenität = {best.homogeneity_metric():.3f}")
    
    print("\n✅ Reverse-LQG-Simulation abgeschlossen!")

if __name__ == "__main__":
    demo_reverse_simulation()