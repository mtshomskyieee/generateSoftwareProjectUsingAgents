class GameInterfaceTest {
    constructor() {
        this.game = new GameInterface();
    }

    testSpawnAsteroids() {
        const initialAsteroidCount = this.game.asteroids.length;
        this.game.spawnAsteroids();
        console.assert(this.game.asteroids.length === initialAsteroidCount + 5, "Asteroids spawn test failed");
    }

    testUpdateAsteroidsBoundaryConditions() {
        this.game.asteroids = [new Asteroid('BIG', -10, -10)];
        this.game.updateAsteroids();
        console.assert(this.game.asteroids[0].positionX > 0, "Asteroid wrap failed on X");
        console.assert(this.game.asteroids[0].positionY > 0, "Asteroid wrap failed on Y");
    }

    testClearCanvas() {
        this.game.clearCanvas();
        console.assert(this.game.ctx.clearRect.called, "Clear canvas did not work");
    }

    testDrawSpaceship() {
        this.game.drawSpaceship();
        // Verify if drawing functions are called by checking the ctx methods. 
        console.assert(this.game.ctx.fill.called, "Spaceship draw failed");
    }

    testDrawAsteroids() {
        this.game.asteroids = [new Asteroid('SMALL', 50, 50)];
        this.game.drawAsteroids();
        console.assert(this.game.ctx.fill.called, "Asteroid draw failed");
    }

    testFireBullet() {
        const initialBulletCount = this.game.bullets.length;
        this.game.fireBullet();
        console.assert(this.game.bullets.length === initialBulletCount + 1, "Bullet firing failed");
    }

    testCollisionHandling() {
        this.game.bullets = [new Bullet()];
        this.game.asteroids = [new Asteroid('BIG', 0, 0)];
        this.game.bullets[0].positionX = 0;
        this.game.bullets[0].positionY = 0;
        this.game.checkBulletCollisions(this.game.bullets[0], 0);
        console.assert(this.game.asteroids.length === 2, "Collision handling failed for BIG asteroid");
    }

    testEdgeCaseShield() {
        this.game.spaceship.isShieldActive = true;
        this.game.drawShield();
        // Some way to verify shield drawing. 
    }

    testKeyHandlingMovement() {
        this.game.spaceship.angle = Math.PI / 2; // Facing up
        const initialPositionX = this.game.spaceship.positionX;
        const initialPositionY = this.game.spaceship.positionY;
        this.game.handleKeyPress();
        // Simulate the ArrowUp key press
        window.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowUp'}));
        console.assert(this.game.spaceship.positionY < initialPositionY, "Ship movement upwards failed");
    }

    testKeyPressFire() {
        const initialBulletCount = this.game.bullets.length;
        this.game.handleKeyPress();
        window.dispatchEvent(new KeyboardEvent('keydown', {key: ' '}));
        console.assert(this.game.bullets.length === initialBulletCount + 1, "Fire bullet failed");
    }

    testKeyPressDeactivateShield() {
        this.game.spaceship.isShieldActive = true;
        this.game.handleKeyPress();
        window.dispatchEvent(new KeyboardEvent('keyup', {key: 's'}));
        console.assert(this.game.spaceship.isShieldActive === false, "Shield deactivation failed");
    }
}

// Run tests
const tests = new GameInterfaceTest();
tests.testSpawnAsteroids();
tests.testUpdateAsteroidsBoundaryConditions();
tests.testClearCanvas();
tests.testDrawSpaceship();
tests.testDrawAsteroids();
tests.testFireBullet();
tests.testCollisionHandling();
tests.testEdgeCaseShield();
tests.testKeyHandlingMovement();
tests.testKeyPressFire();
tests.testKeyPressDeactivateShield();