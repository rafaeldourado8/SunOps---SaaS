"""Gerenciador de conexões WebSocket."""
from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    """Gerencia conexões WebSocket ativas."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]
    
    def join_room(self, user_id: str, room_id: str):
        if user_id in self.user_rooms:
            self.user_rooms[user_id].add(room_id)
    
    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
    
    async def broadcast_to_room(self, message: dict, room_id: str):
        for user_id, rooms in self.user_rooms.items():
            if room_id in rooms and user_id in self.active_connections:
                await self.send_personal_message(message, user_id)


manager = ConnectionManager()
