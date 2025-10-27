#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spin-Netzwerk-Klasse.py

Created on Sat Oct 25 18:09:02 2025

@author: gh
"""

import numpy as np
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
import matplotlib.pyplot as plt
from collections import defaultdict

@dataclass
class SpinEdge:
    """Spin-Kante mit geometrischer Information"""
    id: int
    source: int  # Startknoten
    target: int  # Zielknoten  
    spin: float  # Spin-Label j ∈ {0, 1/2, 1, 3/2, ...}
    length: float = 1.0  # Relative Länge für Visualisierung
    
    @property
    def area(self) -> float:
        """Quantisierte Fläche gemäß LQG: A = 8πγℓₚ² √[j(j+1)]"""
        return np.sqrt(self.spin * (self.spin + 1))
    
    def __hash__(self):
        return hash(self.id)

@dataclass  
class SpinVertex:
    """Spin-Knoten mit Intertwiner-Information"""
    id: int
    edges: List[int]  # IDs der angeschlossenen Kanten
    volume: float = 0.0  # Quantisiertes Volumen
    position: Tuple[float, float, float] = (0, 0, 0)  # 3D-Position
    
    def __hash__(self):
        return hash(self.id)

class SpinNetwork:
    """
    Spin-Netzwerk Klasse für LQG-Simulationen
    Repräsentiert einen quanten-geometrischen Zustand
    """
    
    def __init__(self, vertices: List[SpinVertex] = None, edges: List[SpinEdge] = None):
        self.vertices = vertices or []
        self.edges = edges or []
        self.vertex_dict = {v.id: v for v in self.vertices}
        self.edge_dict = {e.id: e for e in self.edges}
        
        # Metriken
        self._total_volume = None
        self._total_area = None
        
    def add_vertex(self, vertex: SpinVertex):
        """Fügt einen Knoten hinzu"""
        if vertex.id not in self.vertex_dict:
            self.vertices.append(vertex)
            self.vertex_dict[vertex.id] = vertex
            self._total_volume = None  # Cache invalidieren
            
    def add_edge(self, edge: SpinEdge):
        """Fügt eine Kante hinzu und verknüpft sie mit Knoten"""
        if edge.id not in self.edge_dict:
            self.edges.append(edge)
            self.edge_dict[edge.id] = edge
            
            # Verknüpfe mit Quellknoten
            if edge.source in self.vertex_dict:
                self.vertex_dict[edge.source].edges.append(edge.id)
                
            # Verknüpfe mit Zielknoten  
            if edge.target in self.vertex_dict:
                self.vertex_dict[edge.target].edges.append(edge.id)
                
            self._total_area = None  # Cache invalidieren
    
    @property
    def total_volume(self) -> float:
        """Gesamtvolumen des Spin-Netzwerks"""
        if self._total_volume is None:
            self._total_volume = sum(v.volume for v in self.vertices)
        return self._total_volume
    
    @property 
    def total_area(self) -> float:
        """Gesamtfläche des Spin-Netzwerks"""
        if self._total_area is None:
            self._total_area = sum(e.area for e in self.edges)
        return self._total_area
    
    def get_vertex_edges(self, vertex_id: int) -> List[SpinEdge]:
        """Gibt alle mit einem Knoten verbundenen Kanten zurück"""
        if vertex_id not in self.vertex_dict:
            return []
        return [self.edge_dict[eid] for eid in self.vertex_dict[vertex_id].edges 
                if eid in self.edge_dict]
    
    def get_adjacent_vertices(self, vertex_id: int) -> List[SpinVertex]:
        """Gibt alle benachbarten Knoten zurück"""
        adjacent = set()
        for edge in self.get_vertex_edges(vertex_id):
            if edge.source == vertex_id:
                adjacent.add(edge.target)
            else:
                adjacent.add(edge.source)
        return [self.vertex_dict[vid] for vid in adjacent if vid in self.vertex_dict]
    
    def calculate_vertex_volume(self, vertex_id: int) -> float:
        """
        Berechnet das quantisierte Volumen eines Knotens
        Vereinfachte Formel basierend auf angeschlossenen Spins
        """
        edges = self.get_vertex_edges(vertex_id)
        if len(edges) < 3:
            return 0.0
            
        # Vereinfachte Volumen-Formel (Ashtekar-Lewandowski)
        spins = [e.spin for e in edges]
        # Hier könnte die eigentliche LQG-Volumen-Formel implementiert werden
        return np.sqrt(np.abs(np.prod(spins))) * 0.1
    
    def update_volumes(self):
        """Aktualisiert alle Knoten-Volumina"""
        for vertex in self.vertices:
            vertex.volume = self.calculate_vertex_volume(vertex.id)
        self._total_volume = None
    
    def spin_network_entropy(self) -> float:
        """
        Berechnet eine Entropie-Metrik für das Spin-Netzwerk
        Höhere Entropie = mehr Unordnung/Struktur
        """
        spins = [e.spin for e in self.edges]
        volumes = [v.volume for v in self.vertices]
        
        if not spins or not volumes:
            return 0.0
            
        # Entropie basierend auf Spin- und Volumen-Verteilung
        spin_hist = np.histogram(spins, bins=5, density=True)[0]
        volume_hist = np.histogram(volumes, bins=5, density=True)[0]
        
        spin_entropy = -np.sum(p * np.log(p) for p in spin_hist if p > 0)
        volume_entropy = -np.sum(p * np.log(p) for p in volume_hist if p > 0)
        
        return (spin_entropy + volume_entropy) / 2
    
    def homogeneity_metric(self) -> float:
        """
        Misst die Homogenität des Netzwerks
        1.0 = perfekt homogen, 0.0 = hochgradig strukturiert
        """
        if len(self.vertices) < 2:
            return 1.0
            
        volumes = [v.volume for v in self.vertices]
        spins = [e.spin for e in self.edges]
        
        volume_variation = np.std(volumes) / (np.mean(volumes) + 1e-10)
        spin_variation = np.std(spins) / (np.mean(spins) + 1e-10)
        
        # Homogenität ist invers zur Variation
        homogeneity = 1.0 / (1.0 + volume_variation + spin_variation)
        return homogeneity
    
    def copy(self) -> 'SpinNetwork':
        """Erstellt eine tiefe Kopie des Netzwerks"""
        new_vertices = [SpinVertex(v.id, v.edges.copy(), v.volume, v.position) 
                       for v in self.vertices]
        new_edges = [SpinEdge(e.id, e.source, e.target, e.spin, e.length) 
                    for e in self.edges]
        return SpinNetwork(new_vertices, new_edges)
    
    def visualize_2d(self, title="Spin Network"):
        """
        Einfache 2D-Visualisierung ohne networkx
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Knoten und Kanten
        ax1.set_title(f"{title} - Struktur")
        
        # Zeichne Kanten
        for edge in self.edges:
            if edge.source in self.vertex_dict and edge.target in self.vertex_dict:
                src_pos = self.vertex_dict[edge.source].position
                tgt_pos = self.vertex_dict[edge.target].position
                
                # 2D-Projektion (ignoriere z-Koordinate)
                ax1.plot([src_pos[0], tgt_pos[0]], 
                        [src_pos[1], tgt_pos[1]], 
                        'b-', alpha=0.6, linewidth=edge.spin)
                
                # Kanten-Label (Spin)
                mid_x = (src_pos[0] + tgt_pos[0]) / 2
                mid_y = (src_pos[1] + tgt_pos[1]) / 2
                ax1.text(mid_x, mid_y, f'{edge.spin}', fontsize=8, 
                        ha='center', va='center', bbox=dict(boxstyle="round,pad=0.1", facecolor="white"))
        
        # Zeichne Knoten
        for vertex in self.vertices:
            ax1.plot(vertex.position[0], vertex.position[1], 'ro', markersize=10)
            ax1.text(vertex.position[0], vertex.position[1] + 0.1, f'V{vertex.id}', 
                    fontsize=8, ha='center')
        
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Metriken
        ax2.set_title("Spin und Volumen Verteilung")
        
        # Spin-Verteilung
        spins = [e.spin for e in self.edges]
        volumes = [v.volume for v in self.vertices]
        
        if spins:
            ax2.hist(spins, bins=10, alpha=0.7, label=f'Spins (Avg: {np.mean(spins):.2f})')
        if volumes:
            ax2.hist(volumes, bins=10, alpha=0.7, label=f'Volumes (Avg: {np.mean(volumes):.2f})')
        
        ax2.legend()
        ax2.set_xlabel("Wert")
        ax2.set_ylabel("Häufigkeit")
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Beispiel für LQG-Operationen auf Spin-Netzwerken
class LQGOperations:
    """Sammlung von LQG-Operationen auf Spin-Netzwerken"""
    
    @staticmethod
    def vertex_creation(network: SpinNetwork, vertex_id: int, position: Tuple[float, float, float]) -> SpinNetwork:
        """Erzeugt einen neuen Knoten (vereinfacht)"""
        new_vertex = SpinVertex(vertex_id, [], 0.0, position)
        new_network = network.copy()
        new_network.add_vertex(new_vertex)
        return new_network
    
    @staticmethod
    def edge_split(network: SpinNetwork, edge_id: int, new_vertex_id: int) -> SpinNetwork:
        """Teilt eine Kante durch Einfügen eines neuen Knotens"""
        if edge_id not in network.edge_dict:
            return network
            
        edge = network.edge_dict[edge_id]
        new_network = network.copy()
        
        # Entferne alte Kante
        new_network.edges = [e for e in new_network.edges if e.id != edge_id]
        new_network.edge_dict.pop(edge_id, None)
        
        # Erstelle neuen Knoten in der Mitte
        if edge.source in network.vertex_dict and edge.target in network.vertex_dict:
            src_pos = network.vertex_dict[edge.source].position
            tgt_pos = network.vertex_dict[edge.target].position
            mid_pos = (
                (src_pos[0] + tgt_pos[0]) / 2,
                (src_pos[1] + tgt_pos[1]) / 2,
                (src_pos[2] + tgt_pos[2]) / 2
            )
        else:
            mid_pos = (0, 0, 0)
            
        new_vertex = SpinVertex(new_vertex_id, [], 0.0, mid_pos)
        new_network.add_vertex(new_vertex)
        
        # Erstelle zwei neue Kanten
        new_edge1 = SpinEdge(edge_id * 10, edge.source, new_vertex_id, edge.spin / 2)
        new_edge2 = SpinEdge(edge_id * 10 + 1, new_vertex_id, edge.target, edge.spin / 2)
        
        new_network.add_edge(new_edge1)
        new_network.add_edge(new_edge2)
        new_network.update_volumes()
        
        return new_network
    
    @staticmethod
    def spin_fluctuation(network: SpinNetwork, edge_id: int, delta_spin: float) -> SpinNetwork:
        """Ändert den Spin einer Kante (Quanten-Fluktuation)"""
        if edge_id not in network.edge_dict:
            return network
            
        new_network = network.copy()
        edge = new_network.edge_dict[edge_id]
        
        # Ändere Spin (bleibt in halbzahligen Werten)
        new_spin = max(0.5, edge.spin + delta_spin)
        new_spin = round(new_spin * 2) / 2  # Auf halbe Zahlen runden
        
        edge.spin = new_spin
        new_network.update_volumes()
        new_network._total_area = None
        
        return new_network

# Beispiel für die Verwendung
def create_example_spin_network() -> SpinNetwork:
    """Erstellt ein Beispiel-Spin-Netzwerk"""
    network = SpinNetwork()
    
    # Erstelle 4 Knoten (Tetraeder)
    positions = [
        (0, 0, 0), (1, 0, 0), (0.5, np.sqrt(3)/2, 0), (0.5, np.sqrt(3)/6, np.sqrt(2/3))
    ]
    
    for i in range(4):
        network.add_vertex(SpinVertex(i, [], 0.0, positions[i]))
    
    # Erstelle Kanten zwischen allen Knotenpaaren
    edge_id = 0
    for i in range(4):
        for j in range(i+1, 4):
            spin = np.random.choice([0.5, 1.0, 1.5, 2.0])
            network.add_edge(SpinEdge(edge_id, i, j, spin))
            edge_id += 1
    
    network.update_volumes()
    return network

# Test der Implementation
if __name__ == "__main__":
    # Erstelle Beispiel-Netzwerk
    network = create_example_spin_network()
    
    print("Spin-Netzwerk erstellt:")
    print(f"- {len(network.vertices)} Knoten")
    print(f"- {len(network.edges)} Kanten") 
    print(f"- Gesamtvolumen: {network.total_volume:.3f}")
    print(f"- Gesamtfläche: {network.total_area:.3f}")
    print(f"- Entropie: {network.spin_network_entropy():.3f}")
    print(f"- Homogenität: {network.homogeneity_metric():.3f}")
    
    # Visualisiere das Netzwerk
    network.visualize_2d("Initiales Spin-Netzwerk")
    
    # Teste LQG-Operationen
    ops = LQGOperations()
    new_network = ops.edge_split(network, 0, 100)
    print(f"\nNach Kantenteilung:")
    print(f"- {len(new_network.vertices)} Knoten")
    print(f"- {len(new_network.edges)} Kanten")
    print(f"- Homogenität: {new_network.homogeneity_metric():.3f}")
    
    # Visualisiere das modifizierte Netzwerk
    new_network.visualize_2d("Nach Kantenteilung")
    
    # Teste Spin-Fluktuation
    fluctuated_network = ops.spin_fluctuation(network, 1, 0.5)
    print(f"\nNach Spin-Fluktuation:")
    print(f"- Homogenität: {fluctuated_network.homogeneity_metric():.3f}")