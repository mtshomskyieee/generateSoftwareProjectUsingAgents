// Test Suite for Asteroids Game

// Assuming we use a testing framework like Jasmine or Mocha for unit tests in JavaScript
describe('Asteroids Game', function() {

    let game;

    beforeEach(function() {
        game = new Game();
    });

    describe('Spaceship', function() {
        it('should initialize with correct default values', function() {
            expect(game.spaceship.coord_x).toBe(window.innerWidth / 2);
            expect(game.spaceship.coord_y).toBe(window.innerHeight / 2);
            expect(game.spaceship.angle).toBe(0);
            expect(game.spaceship.thrust).toBe(0);
            expect(game.spaceship.shieldActive).toBe(false);
            expect(game.spaceship.bulletFired).toBe(false);
        });
    });

    describe('Bullet', function() {
        it('should initialize with correct coordinates and direction', function() {
            let bullet = new Bullet(100, 200, Math.PI / 4);
            expect(bullet.coord_x).toBe(100);
            expect(bullet.coord_y).toBe(200);
            expect(bullet.direction).toBe(Math.PI / 4);
        });
    });

    describe('Asteroid', function() {
        it('should initialize with coordinates and size', function() {
            let asteroid = new Asteroid(300, 400, 'big');
            expect(asteroid.coord_x).toBe(300);
            expect(asteroid.coord_y).toBe(400);
            expect(asteroid.size).toBe('big');
        });
    });

    describe('Game', function() {
        it('should initialize canvas correctly', function() {
            expect(game.canvas.width).toBe(window.innerWidth);
            expect(game.canvas.height).toBe(window.innerHeight);
        });

        it('should start the game successfully', function() {
            game.startGame();
            expect(game.isRunning).toBe(true);
        });

        it('should handle key press for left arrow correctly', function() {
            game.handleKeyPress(37);
            expect(game.spaceship.angle).toBe(-0.1);
        });

        it('should handle key press for right arrow correctly', function() {
            game.handleKeyPress(39);
            expect(game.spaceship.angle).toBe(0.1);
        });

        it('should thrust when up arrow is pressed', function() {
            game.handleKeyPress(38);
            expect(game.spaceship.thrust).toBe(0.1);
        });

        it('should fire a bullet using space key', function() {
            game.fireBullet();
            expect(game.spaceship.bulletFired).toBe(true);
            expect(game.bullet.coord_x).toBe(game.spaceship.coord_x);
            expect(game.bullet.coord_y).toBe(game.spaceship.coord_y);
            expect(game.bullet.direction).toBe(game.spaceship.angle);
        });

        it('should stop thrust when key is released', function() {
            game.handleKeyPress(38);
            game.registerKeyEvents();
            game.handleKeyPress(38); // Key release
            expect(game.spaceship.thrust).toBe(0);
        });

        it('should activate shield when S key is pressed', function() {
            game.handleKeyPress(83);
            expect(game.spaceship.shieldActive).toBe(true);
        });

        it('should deactivate shield when S key is released', function() {
            game.handleKeyPress(83);
            game.registerKeyEvents();
            game.handleKeyPress(83); // Key release
            expect(game.spaceship.shieldActive).toBe(false);
        });

        it('should wrap spaceship around canvas edges correctly', function() {
            game.spaceship.coord_x = -10;
            game.wrapAround(game.spaceship);
            expect(game.spaceship.coord_x).toBe(game.canvas.width);
            
            game.spaceship.coord_x = game.canvas.width + 10;
            game.wrapAround(game.spaceship);
            expect(game.spaceship.coord_x).toBe(0);
            
            game.spaceship.coord_y = -10;
            game.wrapAround(game.spaceship);
            expect(game.spaceship.coord_y).toBe(game.canvas.height);
            
            game.spaceship.coord_y = game.canvas.height + 10;
            game.wrapAround(game.spaceship);
            expect(game.spaceship.coord_y).toBe(0);
        });

        it('should add asteroids to the game', function() {
            expect(game.asteroids.length).toBe(5);
        });

        it('should update bullet position correctly', function() {
            game.fireBullet();
            game.updateBullet();
            expect(game.bullet.coord_x).toBeGreaterThan(0);
            expect(game.bullet.coord_y).toBeGreaterThan(0);
        });

        it('should remove bullet when it goes off-screen', function() {
            game.fireBullet();
            game.bullet.coord_x = game.canvas.width + 10; // Off-screen
            game.updateBullet();
            expect(game.bullet).toBe(null);
            expect(game.spaceship.bulletFired).toBe(false);
        });

        it('should detect collisions between bullet and asteroid', function() {
            game.fireBullet();
            game.bullet.coord_x = game.asteroids[0].coord_x;
            game.bullet.coord_y = game.asteroids[0].coord_y;
            game.handleCollisions();
            expect(game.bullet).toBe(null);
            expect(game.spaceship.bulletFired).toBe(false);
            expect(game.asteroids.length).toBe(4); // One asteroid should be removed
        });
    });

    describe('Integration Test', function() {
        it('should support full game flow', function() {
            game.startGame();
            game.handleKeyPress(38); // Start thrusting
            game.fireBullet(); // Fire bullet
            expect(game.spaceship.bulletFired).toBe(true);
            game.updateGame(); // Trigger a game update
            expect(game.spaceship.coord_x).toBeGreaterThan(window.innerWidth / 2); // Verify movement
        });
    });
});