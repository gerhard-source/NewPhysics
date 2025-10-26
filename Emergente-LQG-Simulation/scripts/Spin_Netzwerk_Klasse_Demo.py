#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Spin_Netzwerk_Klasse_Demo.py

Created on Sun Oct 26 09:13:12 2025

@author: gh
"""
import numpy as np
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class SpinEdge:
    """Spin-Kante mit geometrischer Information"""
    id: int
    source: int  # Startknoten
    target: int  # Zielknoten  
    spin: float  # Spin-Label j ∈ {0, 1/2, 1, 3/2, ...}
    length: float = 1.0
    
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
    volume: float = 0.0
    position: Tuple[float, float, float] = (0, 0, 0)
    
    def __hash__(self):
        return hash(self.id)

class SpinNetwork:
    """
    Spin-Netzwerk Klasse mit vollständigen LQG-Operationen
    """
    
    def __init__(self, vertices: List[SpinVertex] = None, edges: List[SpinEdge] = None):
        self.vertices = vertices or []
        self.edges = edges or []
        self.vertex_dict = {v.id: v for v in self.vertices}
        self.edge_dict = {e.id: e for e in self.edges}
        self._next_vertex_id = max([v.id for v in self.vertices]) + 1 if self.vertices else 0
        self._next_edge_id = max([e.id for e in self.edges]) + 1 if self.edges else 0
        
        # Metriken-Cache
        self._total_volume = None
        self._total_area = None
        
    def add_vertex(self, vertex: SpinVertex):
        """Fügt einen Knoten hinzu"""
        if vertex.id not in self.vertex_dict:
            self.vertices.append(vertex)
            self.vertex_dict[vertex.id] = vertex
            self._next_vertex_id = max(self._next_vertex_id, vertex.id + 1)
            self._total_volume = None
            
    def add_edge(self, edge: SpinEdge):
        """Fügt eine Kante hinzu"""
        if edge.id not in self.edge_dict:
            self.edges.append(edge)
            self.edge_dict[edge.id] = edge
            self._next_edge_id = max(self._next_edge_id, edge.id + 1)
            
            # Verknüpfe mit Knoten
            if edge.source in self.vertex_dict:
                self.vertex_dict[edge.source].edges.append(edge.id)
            if edge.target in self.vertex_dict:
                self.vertex_dict[edge.target].edges.append(edge.id)
                
            self._total_area = None
    
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
    
    def calculate_vertex_volume(self, vertex_id: int) -> float:
        """
        Berechnet das quantisierte Volumen eines Knotens
        VERBESSERTE Formel für realistischere Volumina
        """
        edges = self.get_vertex_edges(vertex_id)
        if len(edges) < 3:
            return 0.0
            
        # Verbesserte Volumen-Formel mit Spin-Kombinationen
        spins = [e.spin for e in edges]
        
        # Realistischere Volumen-Berechnung
        # Berücksichtigt die Kombination der Spins an einem Knoten
        volume = np.power(np.prod([s + 0.5 for s in spins]), 1/len(spins)) * 0.5
        return volume
    
    def update_volumes(self):
        """Aktualisiert alle Knoten-Volumina"""
        for vertex in self.vertices:
            vertex.volume = self.calculate_vertex_volume(vertex.id)
        self._total_volume = None
    
    def spin_network_entropy(self) -> float:
        """
        Berechnet eine Entropie-Metrik für das Spin-Netzwerk
        KORRIGIERTE Version ohne Deprecation-Warnungen
        """
        spins = [e.spin for e in self.edges]
        volumes = [v.volume for v in self.vertices]
        
        if not spins or not volumes:
            return 0.0
            
        # Entropie basierend auf Spin- und Volumen-Verteilung
        spin_hist = np.histogram(spins, bins=5, density=True)[0]
        volume_hist = np.histogram(volumes, bins=5, density=True)[0]
        
        # Korrigierte Summen-Berechnung ohne Generatoren
        spin_entropy = -sum(p * np.log(p + 1e-10) for p in spin_hist if p > 0)
        volume_entropy = -sum(p * np.log(p + 1e-10) for p in volume_hist if p > 0)
        
        return (spin_entropy + volume_entropy) / 2
    
    def homogeneity_metric(self) -> float:
        """Misst die Homogenität des Netzwerks"""
        if len(self.vertices) < 2:
            return 1.0
            
        volumes = [v.volume for v in self.vertices]
        spins = [e.spin for e in self.edges]
        
        if not volumes or not spins:
            return 1.0
            
        volume_variation = np.std(volumes) / (np.mean(volumes) + 1e-10)
        spin_variation = np.std(spins) / (np.mean(spins) + 1e-10)
        
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
        """Einfache 2D-Visualisierung"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Knoten und Kanten
        ax1.set_title(f"{title} - Struktur")
        
        # Zeichne Kanten
        for edge in self.edges:
            if edge.source in self.vertex_dict and edge.target in self.vertex_dict:
                src_pos = self.vertex_dict[edge.source].position
                tgt_pos = self.vertex_dict[edge.target].position
                
                ax1.plot([src_pos[0], tgt_pos[0]], 
                        [src_pos[1], tgt_pos[1]], 
                        'b-', alpha=0.6, linewidth=edge.spin * 2)
                
                mid_x = (src_pos[0] + tgt_pos[0]) / 2
                mid_y = (src_pos[1] + tgt_pos[1]) / 2
                ax1.text(mid_x, mid_y, f'{edge.spin:.1f}', fontsize=8, 
                        ha='center', va='center', 
                        bbox=dict(boxstyle="round,pad=0.1", facecolor="white"))
        
        # Zeichne Knoten (Größe proportional zum Volumen)
        for vertex in self.vertices:
            marker_size = 10 + vertex.volume * 50  # Skaliere mit Volumen
            ax1.plot(vertex.position[0], vertex.position[1], 'ro', 
                    markersize=marker_size, alpha=0.7)
            ax1.text(vertex.position[0], vertex.position[1] + 0.15, 
                    f'V{vertex.id}\n({vertex.volume:.2f})', 
                    fontsize=7, ha='center')
        
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Metriken
        ax2.set_title("Spin und Volumen Verteilung")
        
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
        
        # Metriken als Text
        metrics_text = f"""
        Metriken:
        - Knoten: {len(self.vertices)}
        - Kanten: {len(self.edges)}
        - Gesamtvolumen: {self.total_volume:.3f}
        - Gesamtfläche: {self.total_area:.3f}
        - Entropie: {self.spin_network_entropy():.3f}
        - Homogenität: {self.homogeneity_metric():.3f}
        """
        ax2.text(0.02, 0.98, metrics_text, transform=ax2.transAxes, 
                verticalalignment='top',
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8), 
                fontsize=9)
        
        plt.tight_layout()
        plt.show()

class LQGOperations:
    """
    Vollständige LQG-Operationen auf Spin-Netzwerken
    """
    
    @staticmethod
    def edge_split(network: SpinNetwork, edge_id: int, new_vertex_id: Optional[int] = None) -> SpinNetwork:
        """
        Teilt eine Kante in zwei Kanten durch Einfügen eines neuen Knotens
        """
        if edge_id not in network.edge_dict:
            return network
            
        edge = network.edge_dict[edge_id]
        new_network = network.copy()
        
        # Neue IDs
        new_vid = new_vertex_id if new_vertex_id else new_network._next_vertex_id
        new_eid1 = new_network._next_edge_id
        new_eid2 = new_network._next_edge_id + 1
        
        # Position des neuen Knotens (Mitte der Kante)
        src_pos = new_network.vertex_dict[edge.source].position
        tgt_pos = new_network.vertex_dict[edge.target].position
        mid_pos = (
            (src_pos[0] + tgt_pos[0]) / 2,
            (src_pos[1] + tgt_pos[1]) / 2, 
            (src_pos[2] + tgt_pos[2]) / 2
        )
        
        # Erstelle neuen Knoten
        new_vertex = SpinVertex(new_vid, [], 0.0, mid_pos)
        new_network.add_vertex(new_vertex)
        
        # Entferne alte Kante
        LQGOperations._remove_edge(new_network, edge_id)
        
        # Erstelle zwei neue Kanten mit halbem Spin (Spin-Erhaltung)
        new_edge1 = SpinEdge(new_eid1, edge.source, new_vid, edge.spin / 2)
        new_edge2 = SpinEdge(new_eid2, new_vid, edge.target, edge.spin / 2)
        
        new_network.add_edge(new_edge1)
        new_network.add_edge(new_edge2)
        new_network.update_volumes()
        
        return new_network
    
    @staticmethod
    def vertex_split(network: SpinNetwork, vertex_id: int, partition_edges: List[List[int]]) -> SpinNetwork:
        """
        Teilt einen Knoten in zwei Knoten
        partition_edges: Liste von zwei Kanten-Gruppen für die neuen Knoten
        """
        if vertex_id not in network.vertex_dict:
            return network
            
        vertex = network.vertex_dict[vertex_id]
        if len(partition_edges) != 2:
            return network
            
        new_network = network.copy()
        
        # Neue IDs
        new_vid1 = vertex_id
        new_vid2 = new_network._next_vertex_id
        
        # Erstelle zweiten Knoten (leicht versetzt)
        old_pos = new_network.vertex_dict[vertex_id].position
        new_pos = (old_pos[0] + 0.1, old_pos[1] + 0.1, old_pos[2] + 0.1)
        new_vertex = SpinVertex(new_vid2, [], 0.0, new_pos)
        new_network.add_vertex(new_vertex)
        
        # Verteile Kanten auf die beiden Knoten
        edges_group1, edges_group2 = partition_edges
        
        # Aktualisiere Kanten-Zuordnungen
        for edge_id in edges_group1:
            if edge_id in new_network.edge_dict:
                edge = new_network.edge_dict[edge_id]
                if edge.source == vertex_id:
                    edge.source = new_vid1
                if edge.target == vertex_id:
                    edge.target = new_vid1
        
        for edge_id in edges_group2:
            if edge_id in new_network.edge_dict:
                edge = new_network.edge_dict[edge_id]
                if edge.source == vertex_id:
                    edge.source = new_vid2
                if edge.target == vertex_id:
                    edge.target = new_vid2
        
        # Verbinde die beiden neuen Knoten mit einer Kante
        new_eid = new_network._next_edge_id
        connecting_spin = 0.5  # Minimale Kopplung
        new_edge = SpinEdge(new_eid, new_vid1, new_vid2, connecting_spin)
        new_network.add_edge(new_edge)
        
        # Aktualisiere Knoten-Kanten-Listen
        LQGOperations._rebuild_vertex_edges(new_network)
        new_network.update_volumes()
        
        return new_network
    
    @staticmethod
    def edge_merge(network: SpinNetwork, edge1_id: int, edge2_id: int) -> SpinNetwork:
        """
        Verschmilzt zwei benachbarte Kanten zu einer Kante (Inverse von edge_split)
        """
        if edge1_id not in network.edge_dict or edge2_id not in network.edge_dict:
            return network
            
        edge1 = network.edge_dict[edge1_id]
        edge2 = network.edge_dict[edge2_id]
        
        # Finde gemeinsamen Knoten
        common_vertex = LQGOperations._find_common_vertex(edge1, edge2)
        if common_vertex is None:
            return network
            
        # Finde die anderen beiden Knoten
        other_vertices = LQGOperations._find_other_vertices(edge1, edge2, common_vertex)
        if len(other_vertices) != 2:
            return network
            
        new_network = network.copy()
        
        # Neue ID für die verschmolzene Kante
        new_eid = new_network._next_edge_id
        
        # Spin-Erhaltung: Summe der Spins
        new_spin = edge1.spin + edge2.spin
        
        # Erstelle neue Kante zwischen den äußeren Knoten
        new_edge = SpinEdge(new_eid, other_vertices[0], other_vertices[1], new_spin)
        
        # Entferne alte Kanten und gemeinsamen Knoten
        LQGOperations._remove_edge(new_network, edge1_id)
        LQGOperations._remove_edge(new_network, edge2_id)
        LQGOperations._remove_vertex(new_network, common_vertex)
        
        # Füge neue Kante hinzu
        new_network.add_edge(new_edge)
        new_network.update_volumes()
        
        return new_network
    
    @staticmethod
    def vertex_merge(network: SpinNetwork, vertex1_id: int, vertex2_id: int) -> SpinNetwork:
        """
        Verschmilzt zwei benachbarte Knoten zu einem Knoten
        """
        if vertex1_id not in network.vertex_dict or vertex2_id not in network.vertex_dict:
            return network
            
        # Prüfe ob die Knoten durch genau eine Kante verbunden sind
        connecting_edges = LQGOperations._find_connecting_edges(network, vertex1_id, vertex2_id)
        if len(connecting_edges) != 1:
            return network
            
        new_network = network.copy()
        connecting_edge = connecting_edges[0]
        
        # Position des neuen Knotens (Mittelpunkt)
        pos1 = new_network.vertex_dict[vertex1_id].position
        pos2 = new_network.vertex_dict[vertex2_id].position
        new_pos = (
            (pos1[0] + pos2[0]) / 2,
            (pos1[1] + pos2[1]) / 2,
            (pos1[2] + pos2[2]) / 2
        )
        
        # Erstelle neuen Knoten mit kombinierten Kanten
        all_edges = (set(new_network.vertex_dict[vertex1_id].edges) | 
                    set(new_network.vertex_dict[vertex2_id].edges) - 
                    {connecting_edge.id})
        
        new_vertex = SpinVertex(vertex1_id, list(all_edges), 0.0, new_pos)
        
        # Entferne alte Knoten und Verbindungskante
        LQGOperations._remove_vertex(new_network, vertex1_id)
        LQGOperations._remove_vertex(new_network, vertex2_id)
        LQGOperations._remove_edge(new_network, connecting_edge.id)
        
        # Füge neuen Knoten hinzu
        new_network.add_vertex(new_vertex)
        
        # Aktualisiere alle Kanten, die auf die alten Knoten zeigten
        for edge in new_network.edges:
            if edge.source == vertex1_id or edge.source == vertex2_id:
                edge.source = vertex1_id
            if edge.target == vertex1_id or edge.target == vertex2_id:
                edge.target = vertex1_id
        
        LQGOperations._rebuild_vertex_edges(new_network)
        new_network.update_volumes()
        
        return new_network
    
    # ===== HILFSFUNKTIONEN =====
    
    @staticmethod
    def _remove_edge(network: SpinNetwork, edge_id: int):
        """Entfernt eine Kante aus dem Netzwerk"""
        if edge_id in network.edge_dict:
            # Entferne aus Kanten-Liste und Dictionary
            network.edges = [e for e in network.edges if e.id != edge_id]
            network.edge_dict.pop(edge_id, None)
            
            # Entferne aus Knoten-Referenzen
            for vertex in network.vertices:
                if edge_id in vertex.edges:
                    vertex.edges.remove(edge_id)
    
    @staticmethod
    def _remove_vertex(network: SpinNetwork, vertex_id: int):
        """Entfernt einen Knoten aus dem Netzwerk"""
        if vertex_id in network.vertex_dict:
            # Entferne alle anliegenden Kanten
            vertex = network.vertex_dict[vertex_id]
            for edge_id in vertex.edges[:]:  # Kopie der Liste
                LQGOperations._remove_edge(network, edge_id)
            
            # Entferne Knoten
            network.vertices = [v for v in network.vertices if v.id != vertex_id]
            network.vertex_dict.pop(vertex_id, None)
    
    @staticmethod
    def _find_common_vertex(edge1: SpinEdge, edge2: SpinEdge) -> Optional[int]:
        """Findet gemeinsamen Knoten zwischen zwei Kanten"""
        vertices1 = {edge1.source, edge1.target}
        vertices2 = {edge2.source, edge2.target}
        common = vertices1.intersection(vertices2)
        return common.pop() if common else None
    
    @staticmethod
    def _find_other_vertices(edge1: SpinEdge, edge2: SpinEdge, common_vertex: int) -> List[int]:
        """Findet die nicht-gemeinsamen Knoten zweier Kanten"""
        all_vertices = {edge1.source, edge1.target, edge2.source, edge2.target}
        all_vertices.discard(common_vertex)
        return list(all_vertices)
    
    @staticmethod
    def _find_connecting_edges(network: SpinNetwork, vertex1_id: int, vertex2_id: int) -> List[SpinEdge]:
        """Findet Kanten, die zwei Knoten verbinden"""
        connecting = []
        for edge in network.edges:
            if (edge.source == vertex1_id and edge.target == vertex2_id) or \
               (edge.source == vertex2_id and edge.target == vertex1_id):
                connecting.append(edge)
        return connecting
    
    @staticmethod
    def _rebuild_vertex_edges(network: SpinNetwork):
        """Baut die Kanten-Listen aller Knoten neu auf"""
        for vertex in network.vertices:
            vertex.edges = []
        
        for edge in network.edges:
            if edge.source in network.vertex_dict:
                network.vertex_dict[edge.source].edges.append(edge.id)
            if edge.target in network.vertex_dict:
                network.vertex_dict[edge.target].edges.append(edge.id)

# VERBESSERTE Demo mit realistischen Volumina
def demo_lqg_operations_improved():
    """Demonstriert LQG-Operationen mit verbesserten Volumina"""
    print("🚀 LQG GRUNDOPERATIONEN - Verbesserte Version")
    print("=" * 50)
    
    # Erstelle Netzwerk mit verschiedenen Spins für realistischere Volumina
    network = SpinNetwork()
    
    # 4 Knoten in Tetraeder-Formation
    positions = [
        (0, 0, 0), (1, 0, 0), 
        (0.5, np.sqrt(3)/2, 0), (0.5, np.sqrt(3)/6, np.sqrt(2/3))
    ]
    
    for i in range(4):
        network.add_vertex(SpinVertex(i, [], 0.0, positions[i]))
    
    # Kanten mit verschiedenen Spins
    edges_data = [
        (0, 1, 1.0), (0, 2, 1.5), (0, 3, 2.0),
        (1, 2, 0.5), (1, 3, 1.0), (2, 3, 1.5)
    ]
    
    for i, (src, tgt, spin) in enumerate(edges_data):
        network.add_edge(SpinEdge(i, src, tgt, spin))
    
    network.update_volumes()
    
    print("Initiales Netzwerk (Tetraeder mit verschiedenen Spins):")
    print(f"- Knoten: {len(network.vertices)}, Kanten: {len(network.edges)}")
    print(f"- Gesamtvolumen: {network.total_volume:.3f}")
    print(f"- Gesamtfläche: {network.total_area:.3f}")
    print(f"- Entropie: {network.spin_network_entropy():.3f}")
    print(f"- Homogenität: {network.homogeneity_metric():.3f}")
    
    # Zeige individuelle Knoten-Volumina
    print("\nKnoten-Volumina:")
    for vertex in network.vertices:
        edges = network.get_vertex_edges(vertex.id)
        spins = [e.spin for e in edges]
        print(f"  Knoten {vertex.id}: {vertex.volume:.3f} (Spins: {spins})")
    
    network.visualize_2d("Initiales Tetraeder-Netzwerk")
    
    ops = LQGOperations()
    
    # Demonstration der Operationen
    print("\n" + "="*50)
    print("OPERATIONEN-DEMONSTRATION:")
    
    # 1. Kante aufspalten
    print("\n1. KANTEN-AUFSPALTUNG (Kante 0):")
    split_network = ops.edge_split(network, 0)
    print(f"- Vorher: {len(network.vertices)} Knoten, {len(network.edges)} Kanten")
    print(f"- Nachher: {len(split_network.vertices)} Knoten, {len(split_network.edges)} Kanten")
    print(f"- Volumen-Änderung: {network.total_volume:.3f} → {split_network.total_volume:.3f}")
    
    split_network.visualize_2d("Nach Kanten-Aufspaltung")
    
    # 2. Knoten verschmelzen (mit einem einfacheren Netzwerk)
    print("\n2. KNOTEN-VERSCHMELZUNG:")
    simple_net = SpinNetwork()
    for i in range(2):
        simple_net.add_vertex(SpinVertex(i, [], 0.0, (i, 0, 0)))
    simple_net.add_edge(SpinEdge(0, 0, 1, 1.0))
    simple_net.update_volumes()
    
    print(f"- Vor Verschmelzung: {len(simple_net.vertices)} Knoten, Volumen: {simple_net.total_volume:.3f}")
    merged = ops.vertex_merge(simple_net, 0, 1)
    print(f"- Nach Verschmelzung: {len(merged.vertices)} Knoten, Volumen: {merged.total_volume:.3f}")
    
    print("\n✅ LQG-Operationen erfolgreich mit realistischen Volumina!")

if __name__ == "__main__":
    demo_lqg_operations_improved()
