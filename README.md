# PyGame-Shooter

## 🛠️ Update: Refactoring & Health Bar  

### 🔄 Refactoring  
- The `src` folder structure has been reorganized for better maintainability.  

### ❤️ New Feature: Health Bar System  
- Implemented a new `HealthBar` class.  
- Each soldier now has an associated health bar displayed above their head.  
- Added visual indicators showing the number of bullets and grenades the player has.  


classDiagram
    direction LR

    class A {
        +__init__(c: C)
        +method_A()
    }

    class B {
        +method_B()
    }

    class C {
        +method_C()
    }

    class A1 {
        +__init__()
        +method_A1()
    }

    class A2 {
        +__init__()
        +method_A2()
    }

    A1 "1" --|> A : inherits
    A2 "1" --|> A : inherits
    A1 "1" --|> B : inherits
    A2 "1" --|> B : inherits
    A "1" -- "1" C : uses
