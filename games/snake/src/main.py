import pygame
import asyncio

from game.menu import Menu

async def main():
    menu = Menu()
    await menu.run()
    
asyncio.run(main())