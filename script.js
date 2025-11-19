const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const player = {
  x: canvas.width / 2 - 15,
  y: canvas.height - 40,
  width: 30,
  height: 30,
  speed: 5,
};

let keys = {};
let enemies = [];
let score = 0;
let gameOver = false;

document.addEventListener("keydown", (e) => {
  keys[e.key] = true;
});

document.addEventListener("keyup", (e) => {
  keys[e.key] = false;
});

function spawnEnemy() {
  const width = 30;
  const height = 30;
  const x = Math.random() * (canvas.width - width);
  const y = -height;

  enemies.push({ x, y, width, height, speed: 2 + Math.random() * 3 });
}

function updatePlayer() {
  if (keys["ArrowLeft"] && player.x > 0) {
    player.x -= player.speed;
  }
  if (keys["ArrowRight"] && player.x + player.width < canvas.width) {
    player.x += player.speed;
  }
}

function updateEnemies() {
  enemies.forEach((enemy) => {
    enemy.y += enemy.speed;
  });

  enemies = enemies.filter((enemy) => enemy.y < canvas.height + enemy.height);
}

function checkCollisions() {
  for (const enemy of enemies) {
    if (
      player.x < enemy.x + enemy.width &&
      player.x + player.width > enemy.x &&
      player.y < enemy.y + enemy.height &&
      player.y + player.height > enemy.y
    ) {
      gameOver = true;
    }
  }
}

function drawPlayer() {
  ctx.fillStyle = "white";
  ctx.fillRect(player.x, player.y, player.width, player.height);
}

function drawEnemies() {
  ctx.fillStyle = "red";
  enemies.forEach((enemy) => {
    ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
  });
}

function drawScore() {
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";
  ctx.fillText(`Score: ${score}`, 10, 25);
}

let lastSpawn = 0;

function gameLoop(timestamp) {
  if (gameOver) {
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.font = "40px Arial";
    ctx.fillText("Game Over!", canvas.width / 2 - 110, canvas.height / 2);
    ctx.font = "20px Arial";
    ctx.fillText(
      `Final Score: ${score}`,
      canvas.width / 2 - 70,
      canvas.height / 2 + 40
    );
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  updatePlayer();
  updateEnemies();
  checkCollisions();

  drawPlayer();
  drawEnemies();
  drawScore();

  // spawn enemies every ~700ms
  if (timestamp - lastSpawn > 700) {
    spawnEnemy();
    lastSpawn = timestamp;
    score++;
  }

  requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
