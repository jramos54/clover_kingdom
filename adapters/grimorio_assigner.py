import random
from engine.entities import Grimorio, Solicitud
from engine.interfaces import GrimorioAssignerInterface

class GrimorioAssigner(GrimorioAssignerInterface):
    def assign_grimorio(self, solicitud: Solicitud) -> Grimorio:
        grimorios = [
            {"tipo": "Trébol de una hoja", "rareza": 1},
            {"tipo": "Trébol de dos hojas", "rareza": 1},
            {"tipo": "Trébol de tres hojas", "rareza": 2},
            {"tipo": "Trébol de cuatro hojas", "rareza": 3},
            {"tipo": "Trébol de cinco hojas", "rareza": 5},
        ]
        
        # Ponderación según la rareza
        ponderaciones = [g["rareza"] for g in grimorios]
        grimorio_seleccionado = random.choices(grimorios, weights=ponderaciones, k=1)[0]
        
        return Grimorio(tipo=grimorio_seleccionado["tipo"], rareza=grimorio_seleccionado["rareza"])
