# Space Invaders (Toy Jet Shooter)

One of my oldest projects, recently given a fresh update! 🚀 A Python implementation of the classic Space Invaders arcade game using Pygame.

## Game Features

### Core Gameplay
- Player-controlled jet that moves horizontally
- Multiple enemy types with different behaviors
- Shooting mechanics with visual and sound effects
- Score tracking and high score system
- Lives system with heart indicators
- Progressive difficulty levels (Easy, Medium, Hard)

### Technical Implementation
- **Game Engine**: Pygame
- **Object-Oriented Design**: Clean separation of game objects and logic
- **Asset Management**: Handles missing assets gracefully with fallbacks
- **Sound Effects**: Custom sound effects for shooting and explosions
- **Visual Feedback**: Particle effects and animations

### Controls
- **Left/Right Arrow Keys**: Move player
- **Space**: Shoot
- **R**: Restart game (when game over)
- **L**: Toggle bullet visualization (if bullet image is available)

## Getting Started

### Prerequisites
- Python 3.x
- Pygame library

### Installation
1. Clone the repository
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python gun.py
   ```

## 🛠️ Technical Details

### Game Architecture
- **Main Game Loop**: Handles events, updates game state, and renders graphics
- **Entity System**: Manages player, enemies, and projectiles
- **Collision Detection**: Pixel-perfect collision detection for all game objects
- **State Management**: Handles game states (menu, playing, game over)

### Assets Used
- Custom sprites for player, enemies, and projectiles
- Sound effects for shooting and explosions
- Custom font with fallback options

## 📝 Notes
- This was one of my earliest game development projects
- Recently refactored to improve code quality and performance

---
*Created with ❤️ as a nostalgic look back at my programming journey*
