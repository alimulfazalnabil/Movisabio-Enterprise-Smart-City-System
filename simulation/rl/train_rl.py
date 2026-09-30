import time
import random
import json
import os

def train_agent(agent_type: str, episodes: int):
    """
    Simulates training a DQN or PPO agent in the SUMO environment.
    """
    print(f"--- Initializing {agent_type.upper()} Training Pipeline ---")
    print("Environment: MoviSabio SUMO Gym Wrapper")
    print("Action Space: Discrete(3) [MAINTAIN, SWITCH_NS, SWITCH_EW]")
    print("State Space: Box(4) [NS_Queue, EW_Queue, Phase_Enc, Elapsed]")
    print("Safety Filter: ENABLED\n")
    
    # Mocking convergence
    results = []
    current_reward = -500.0
    
    for ep in range(1, episodes + 1):
        # Simulate an episode
        time.sleep(0.05)
        
        # Agent learns and reward improves
        if agent_type == "dqn":
            current_reward += random.uniform(5, 15)
        elif agent_type == "ppo":
            current_reward += random.uniform(8, 20) # PPO might converge slightly faster
            
        current_reward = min(current_reward, -50.0 + random.uniform(-10, 10))
        
        if ep % 10 == 0:
            print(f"Episode {ep}/{episodes} | Avg Reward: {current_reward:.2f}")
            results.append({"episode": ep, "reward": current_reward})
            
    print(f"\n{agent_type.upper()} Training Complete. Final Reward: {current_reward:.2f}")
    
    # Save training curve
    os.makedirs("experiments/rl_models", exist_ok=True)
    with open(f"experiments/rl_models/{agent_type}_learning_curve.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    train_agent("dqn", 50)
    train_agent("ppo", 50)
