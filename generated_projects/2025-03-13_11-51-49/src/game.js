// Data Structures  
struct Spaceship {  
    var positionX; // float  
    var positionY; // float  
    var angle; // float  
    var isShieldActive; // boolean  
    var bulletActive; // boolean  
}  
  
struct Bullet {  
    var positionX; // float  
    var positionY; // float  
    var direction; // float  
}  
  
struct Asteroid {  
    var positionX; // float  
    var positionY; // float  
    var size; // enum { BIG, SMALL }  
}  
  
// Interface Definitions  
interface GameInterface {  
    void initializeGame();  
    void updateGame();  
    void handleKeyPress(var key);  
    void fireBullet();  
    void activateShield();  
    void deactivateShield();  
}  
  
interface AsteroidManager {  
    void createAsteroid(var positionX, var positionY, var size);  
    void updateAsteroids();  
    void checkCollisions(Bullet bullet, Asteroid asteroid);  
}  
  
interface BulletManager {  
    void updateBullet(Bullet bullet);  
    void destroyBullet(Bullet bullet);  
}  
  
// Type Definitions  
typedef var Point;  
typedef var Angle;  
typedef var Velocity;  
  
// Error Specifications  
exception GameError {  
    var errorCode; // int  
    var errorMessage; // string  
}  
  
exception CollisionError {  
    var asteroid; // Asteroid  
    var bullet; // Bullet  
}