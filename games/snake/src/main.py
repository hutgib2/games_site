import pygame
import asyncio

from game.snake import Snake

async def main():
    game = Snake()
    await game.run()
    
asyncio.run(main())