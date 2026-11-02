import pygame
from game.roguelike import Roguelike
import asyncio

async def main():
    game = Roguelike()
    await game.run()

asyncio.run(main())