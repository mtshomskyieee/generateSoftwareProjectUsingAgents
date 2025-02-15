// Data Structures  
struct Spaceship {  
    coord_x: int;  
    coord_y: int;  
    angle: float;  
    thrust: float;  
    shieldActive: bool;  
    bulletFired: bool;  
    }  

struct Bullet {  
    coord_x: int;  
    coord_y: int;  
    direction: float;  
    }  

struct Asteroid {  
    coord_x: int;  
    coord_y: int;  
    size: string; // "big" or "small"  
    }  

// Interface Definitions  
interface GameInterface {  
    void initializeCanvas();  
    void startGame();  
    void handleKeyPress(KeyCode key);  
    void updateGame();  
    void render();  
    void fireBullet();  
    void activateShield();  
    void deactivateShield();  
    void handleCollision(Bullet bullet, Asteroid asteroid);  
    void wrapAround(Spaceship ship);  
    }  

// Type Definitions  
typedef KeyCode int;  

// Error Specifications  
exception GameError {  
    string message;  
    int errorCode;  
    }