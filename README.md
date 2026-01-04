# arcade_receipt_task_system

## Summary

This project is a receipt-based productivity and motivation system that turns real-world tasks into arcade-style score runs printed on a 80mm thermal receipt printer.

Instead of managing traditional todo lists, users play sessions, earn points, trigger combos, and track high scores using physical receipts as tangible proof of progress.

The goal is to reduce friction, guilt, and overplanning while increasing momentum, consistency, and enjoyment of work.

## Motivation

Traditional productivity tools often:
- Create guilt when tasks are missed.
- Encourage perfectionism and over-planning.
- Remain abstract and easy to ignore.

Arcade machines do the opposite:
- Reward action immediately.
- Provide clear numeric feedback.
- Make progress tangible and memorable.

This project serves two purposes:
- Practical: Make tasks easier to start and more satisfying to complete.
- Educational: Explore systems design, automation, printing, formatting constraints, and future AI-driven task orchestration.

## High Level Architecture

- User (player)
  - Defines tasks and point values
  - Initiates play sessions
- Task Engine
  - Groups tasks into score runs
  - Calculates points, combos, and totals
- Receipt Generator
  - Formats output for 80mm thermal printers
  - Produces SCORE RUN, SCORE RESULT, and SUMMARY receipts
- Thermal Receipt Printer
  - Prints physical records of play sessions
- AI Agent (Future Improvements)
  - Auto-breaks assignments into tasks
  - Balances point values
  - Generates daily score runs

## Flow

1. User defines a set of tasks with point values.
2. A SCORE RUN receipt is generated and printed before starting.
3. The user completes tasks during a work session.
4. A SCORE RESULT receipt is generated after the session:
   1. Completed tasks earn points.
   2. Missed tasks score zero.
   3. Combos and final score are calculated.
5. Receipts are physically crumbled and tossed into a jar.
6. Weekly or project-level summaries can be printed as HIGH SCORE receipts.

## Features

- Arcade-style point system (no priorities, no penalties).
- Multiple task categories (arcade lanes).
- Combo multipliers for momentum.
- Streak tracking based on score days.
- Receipt formats optimized for 80mm printers.
- Physical output for tangible motivation

## Prerequisites

### Software 

- Python 3.x
- Terminal or CLI environment
- ESC/POS compatible receipt printer drivers

### Python Dependencies

- subprocess
- 

### Hardware

- 80mm thermal receipt printer
- USB, or Network connection

## Configuration 



## Status

This project is currently in active development and primarily intended as a learning and experimentation tool. Stability and edge cases are still being refined.


## Future Improvements

- TODO
