class Snake {
    constructor() {
        this.body = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        this.direction = 'right';
        this.nextDirection = 'right';
    }

    move(food) {
        const head = { ...this.body[0] };

        this.direction = this.nextDirection;

        switch (this.direction) {
            case 'up': head.y--; break;
            case 'down': head.y++; break;
            case 'left': head.x--; break;
            case 'right': head.x++; break;
        }

        // 边界穿越处理
        if (head.x < 0) head.x = 19;
        if (head.x >= 20) head.x = 0;
        if (head.y < 0) head.y = 19;
        if (head.y >= 20) head.y = 0;

        this.body.unshift(head);

        if (head.x === food.x && head.y === food.y) {
            return true;
        }

        this.body.pop();
        return false;
    }

    checkCollision(gridSize) {
        const head = this.body[0];
        
        // 只检查是否撞到自己
        for (let i = 1; i < this.body.length; i++) {
            if (head.x === this.body[i].x && head.y === this.body[i].y) {
                return true;
            }
        }

        return false;
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = 20; // 20x20的网格
        this.tileSize = this.canvas.width / this.gridSize;
        this.snake = new Snake();
        this.food = this.generateFood();
        this.score = 0;
        this.gameOver = false;
        this.speed = 150;

        this.setupEventListeners();
        this.gameLoop();
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowUp':
                    if (this.snake.direction !== 'down') this.snake.nextDirection = 'up';
                    break;
                case 'ArrowDown':
                    if (this.snake.direction !== 'up') this.snake.nextDirection = 'down';
                    break;
                case 'ArrowLeft':
                    if (this.snake.direction !== 'right') this.snake.nextDirection = 'left';
                    break;
                case 'ArrowRight':
                    if (this.snake.direction !== 'left') this.snake.nextDirection = 'right';
                    break;
            }
        });
    }

    generateFood() {
        let food;
        do {
            food = {
                x: Math.floor(Math.random() * this.gridSize),
                y: Math.floor(Math.random() * this.gridSize)
            };
        } while (this.snake.body.some(segment => 
            segment.x === food.x && segment.y === food.y));
        return food;
    }

    draw() {
        // 清空画布
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // 绘制蛇
        this.snake.body.forEach((segment, index) => {
            this.ctx.fillStyle = index === 0 ? '#4CAF50' : '#81C784';
            this.ctx.fillRect(
                segment.x * this.tileSize,
                segment.y * this.tileSize,
                this.tileSize - 1,
                this.tileSize - 1
            );
        });

        // 绘制食物
        this.ctx.fillStyle = '#FF5252';
        this.ctx.fillRect(
            this.food.x * this.tileSize,
            this.food.y * this.tileSize,
            this.tileSize - 1,
            this.tileSize - 1
        );

        // 更新分数
        document.getElementById('score').textContent = `分数: ${this.score}`;

        // 如果游戏结束，显示游戏结束信息
        if (this.gameOver) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.fillStyle = '#fff';
            this.ctx.font = '30px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('游戏结束!', this.canvas.width / 2, this.canvas.height / 2);
            this.ctx.font = '20px Arial';
            this.ctx.fillText(
                `最终分数: ${this.score}`,
                this.canvas.width / 2,
                this.canvas.height / 2 + 40
            );
            this.ctx.fillText(
                '按空格键重新开始',
                this.canvas.width / 2,
                this.canvas.height / 2 + 80
            );
        }
    }

    gameLoop() {
        if (!this.gameOver) {
            if (this.snake.move(this.food)) {
                this.score += 10;
                this.food = this.generateFood();
                // 每得100分加快速度
                if (this.score % 100 === 0) {
                    this.speed = Math.max(50, this.speed - 10);
                }
            }

            if (this.snake.checkCollision(this.gridSize)) {
                this.gameOver = true;
            }

            this.draw();
            setTimeout(() => this.gameLoop(), this.speed);
        }
    }

    reset() {
        this.snake = new Snake();
        this.food = this.generateFood();
        this.score = 0;
        this.gameOver = false;
        this.speed = 150;
        this.gameLoop();
    }
}

// 添加空格键重新开始游戏的功能
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        const game = window.game;
        if (game.gameOver) {
            game.reset();
        }
    }
});

// 启动游戏
window.onload = () => {
    window.game = new Game();
};