import pygame
from game.menu import Menu
import asyncio

async def main():
    menu = Menu()
    await menu.run()

asyncio.run(main())