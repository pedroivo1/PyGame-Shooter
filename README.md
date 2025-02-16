# PyGame-Shooter

## 🛠️ Update: Refactoring & Health Bar  

### 🔄 Refactoring  
- The `src` folder structure has been reorganized for better maintainability.  

### ❤️ New Feature: Health Bar System  
- Implemented a new `HealthBar` class.  
- Each soldier now has an associated health bar displayed above their head.  
- Added visual indicators showing the number of bullets and grenades the player has.  

classDiagram
Class01 <|-- AveryLongClass : Cool
<<Interface>> Class01
Class09 --> C2 : Where am I?
Class09 --* C3
Class09 --|> Class07
Class07 : equals()
Class07 : Object[] elementData
Class01 : size()
Class01 : int chimp
Class01 : int gorilla
class Class10 {
  <<service>>
  int id
  size()
}


```mermaid
graph TD;
    HealthBox --|> ItemBox;
    GrenadeBox --|> ItemBox;
    BulletBox --|> ItemBox;
```
