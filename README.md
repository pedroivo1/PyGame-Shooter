# PyGame-Shooter

# 🛠️ Update: Refactoring & Explosion Mechanics

## 🔄 Refactoring
We have refactored the `animation_import` method in the `Game` class, improving its structure and maintainability.

## 💥 New Feature: Explosion System
- Implemented an `Explosion` class that is triggered when a `Grenade` is destroyed.
- The `Grenade` now deals **area damage** to all soldiers within its proximity radius.
