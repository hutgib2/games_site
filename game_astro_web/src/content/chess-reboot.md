---
# This is where we write the variables for our game
title: 'Chess Reboot'
description: 'A fun, interactive variation of classic Chess!'
image: './thumbnails/chess_preview.png'
video: './previews/chess_reboot_preview.mp4'
type: 'Strategy'
---
<!-- This is where we write the long-form content in .md syntax -->
<article class="prose">

## Description
This is a unique variation of Chess, all the pieces have been replaced with new ones to make the game more fun!

## How to Play
The way to win is the same as regular chess, by putting the Emporer in a checkmate.

## Pieces
**Legionary** *(replaces pawn)*
- Can move and attack forward one tile at a time
- A legionary's shield blocks **all** attacks from the front
- A Legionary cannot be attacked diagonally if an ally Legionary is adjacent to it (Turtle formation)
  
**Archer** *(replaces queen)*
- Can move one tile in all directions
- Has a ranged attack in all directions up to 3 tiles away, but cannot attack a 1-tile radius
- Can shoot over enemy and ally pieces 1 tile away from it

**Dragon** *(replaces knight)*
- Can move exactly like a knight
- Dragons fire breath does area damage to all tiles in front and to the sides
- Can kill multiple pieces with one attack

**Wizard** *(replaces bishop)*
- Can move and kill diagonally up to 2 tiles
- Can swap places with any ally or enemy Legionary, as long as it doesn't result in a promotion or a checkmate
- Cannot swap tile positions with Legionaries that are in the wizard's attacking range

**Catapult** *(replaces rook)*
- Can move up to two tiles in all non-diagonal directions
- Can fire boulder in all non-diagonal directions with unlimited range
- Boulder kills the first enemy piece, then stuns all pieces behind for 2 turns
- Boulder is stopped by Legionary shield or ally piece

**Emperor** *(replaces king)*
- Can move and kill like a queen on its first move only, then kills and moves like a regular king afterwards
</article>