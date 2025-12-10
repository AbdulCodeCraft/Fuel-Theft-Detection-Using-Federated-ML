import numpy as np

class FederatedServer:
    """
    Simulates the Global Server in a Federated Learning Architecture.
    Responsibility: Aggregates model weights from edge nodes.
    """
    def __init__(self):
        self.global_weights = None
        self.round_number = 0

    def fed_avg(self, local_weights):
        """
        Implementation of the Federated Averaging (FedAvg) algorithm.
        Takes local model updates and averages them to update the global model.
        """
        self.round_number += 1
        print(f"[FML SYSTEM] Starting Round {self.round_number} Aggregation...")
        
        # Mathematically averaging the weights 
        # Here we average the statistical variance of the sensor data.
        aggregated_weight = np.mean(local_weights)
        
        self.global_weights = aggregated_weight
        
        print(f"[FML SYSTEM] Round {self.round_number} Complete. Global Model Updated.")
        print(f"[FML SYSTEM] Broadcasting new parameters to Edge Nodes...\n")
        return self.global_weights