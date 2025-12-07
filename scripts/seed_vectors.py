"""
Script to seed Qdrant with book content embeddings
Run this after setting up Qdrant and OpenAI API key
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.qdrant_client import get_qdrant_client, add_vector
from app.openai_client import get_embeddings
import uuid

# Book content chunks
BOOK_CHUNKS = [
    {
        "text": "ROS 2 (Robot Operating System 2) is the middleware that enables communication between different components of a robot system. Think of it as the nervous system that allows the robot's brain (AI algorithms) to communicate with its body (sensors and actuators).",
        "module": "module1",
        "section": "introduction"
    },
    {
        "text": "ROS 2 follows a distributed architecture where different processes (nodes) communicate through topics, services, and actions. Nodes are individual processes that perform specific tasks. Topics are asynchronous communication channels for streaming data.",
        "module": "module1",
        "section": "architecture"
    },
    {
        "text": "Gazebo is a powerful physics simulation environment that allows you to test robot behaviors in realistic virtual environments. It simulates physics, gravity, collisions, and various sensors including LiDAR, cameras, and IMUs.",
        "module": "module2",
        "section": "gazebo"
    },
    {
        "text": "NVIDIA Isaac Sim is a photorealistic simulation environment built on NVIDIA Omniverse. It provides high-fidelity physics simulation, realistic rendering with ray tracing, synthetic data generation for training, and domain randomization for sim-to-real transfer.",
        "module": "module3",
        "section": "isaac-sim"
    },
    {
        "text": "Vision-Language-Action (VLA) represents the convergence of Large Language Models (LLMs) and Robotics. OpenAI Whisper converts spoken language into text, enabling voice commands for robot control. LLMs can translate high-level natural language commands into sequences of robot actions.",
        "module": "module4",
        "section": "vla"
    },
    {
        "text": "The capstone project involves building a simulated humanoid robot that receives voice commands, plans paths, navigates obstacles, identifies objects using computer vision, and manipulates objects to complete tasks.",
        "module": "capstone",
        "section": "overview"
    },
]

async def seed_vectors():
    """Seed Qdrant with book content"""
    print("Starting vector seeding...")
    
    qdrant_client = await get_qdrant_client()
    
    for chunk in BOOK_CHUNKS:
        print(f"Processing chunk from {chunk['module']}...")
        
        # Get embedding
        embedding = await get_embeddings(chunk["text"])
        if not embedding:
            print(f"Failed to get embedding for chunk: {chunk['module']}")
            continue
        
        # Add to Qdrant
        vector_id = str(uuid.uuid4())
        await add_vector(
            qdrant_client,
            vector_id,
            embedding,
            {
                "text": chunk["text"],
                "module": chunk["module"],
                "section": chunk["section"]
            }
        )
        
        print(f"✓ Added vector for {chunk['module']}")
    
    print("Vector seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_vectors())

