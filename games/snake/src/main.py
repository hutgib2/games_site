import pygame
import asyncio

from game.snake import Snake

async def main():
    game = Snake()
    await game.show_menu()
    
asyncio.run(main())