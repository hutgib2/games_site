---
# This is where we write the variables for our game
title: 'Chess Reboot'
description: 'A fun, interactive variation of classic Chess!'
image: './thumbnails/chess_preview.png'
type: 'Strategy'
---
<!-- This is where we write the long-form content in .md syntax -->
<article class="prose">

## Description
This is my unique varation of Chess, I've replaced all the pieces with new ones to make the game more fun! ***(add a little more here)***

## How to Play
<!-- explain how to win, etc -->


## Pieces

**Legionary** *(replaces pawn)*
- Can move forward one tile at a time
- Can attack only one tile in front
- A legionary's shield blocks **all** attacks from the front
- A Legionary cannot be attacked diagonally if an ally Legionary is adjacent to it (Turtle formation)
  
**Archer** *(replaces queen)*
- Can move one tile in all directions
- Has a ranged attack in all directions up to 3 tiles away, cannot attack a 1-tile radius
- Can shoot over enemy and ally pieces 1 tile away from it

**Dragon** *(replaces knight)*
- Can move exactly like a knight
- Dragons fire breath does area damage to all tiles in front and to the sides
- Can kill multiple pieces with one attack

**Wizard** *(replaces bishop)*
- Can move and kill diagonally up to 2 tiles
- Can swap places with any ally or enemy Legionary, as long as it doesn't result in a promotion or a checkmate
- Cannot swap tile positions with Legionaries that are in attacking range

**Catapult** *(replaces rook)*
- Can move up to two tiles in all non-diagonal directions
- Can fire boulder in all non-diagonal directions with unlimited range
- Boulder kills the first enemy piece, then stuns all pieces behind 
- Boulder is stopped by Legionary shield or ally piece

**Emperor** *(replaces king)*
- Can move and kill like a queen on its first move but moves and kills like a regular king afterwards
</article>