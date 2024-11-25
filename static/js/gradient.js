document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('gradient-canvas');
    const ctx = canvas.getContext('2d');
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let targetX = mouseX;
    let targetY = mouseY;
    let time = 0;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    document.addEventListener('mousemove', (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
    });

    function lerp(start, end, factor) {
        return start * (1 - factor) + end * factor;
    }

    function createWave(x, y, time) {
        return Math.sin(x * 0.02 + time) * Math.cos(y * 0.02 + time) * 20;
    }

    function drawWaves(time) {
        const imageData = ctx.createImageData(canvas.width, canvas.height);
        const data = imageData.data;

        for (let x = 0; x < canvas.width; x++) {
            for (let y = 0; y < canvas.height; y++) {
                const wave = createWave(x, y, time);
                const index = (y * canvas.width + x) * 4;
                
                // Dark theme colors with wave effect
                data[index] = 13 + wave;     // R (primary blue)
                data[index + 1] = 110 + wave; // G
                data[index + 2] = 253 + wave; // B
                data[index + 3] = 25;         // A (low opacity)
            }
        }

        return imageData;
    }

    function draw() {
        // Smooth mouse movement
        mouseX = lerp(mouseX, targetX, 0.1);
        mouseY = lerp(mouseY, targetY, 0.1);

        // Clear canvas with very dark background
        ctx.fillStyle = 'rgba(33, 37, 41, 0.95)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw waves
        const waveImage = drawWaves(time);
        ctx.putImageData(waveImage, 0, 0);

        // Create blackhole effect
        const gradient = ctx.createRadialGradient(
            mouseX, mouseY, 0,
            mouseX, mouseY, 300
        );

        // Dark theme colors for blackhole
        gradient.addColorStop(0, 'rgba(13, 110, 253, 0.3)');   // Primary
        gradient.addColorStop(0.2, 'rgba(32, 201, 151, 0.2)'); // Success
        gradient.addColorStop(0.4, 'rgba(13, 202, 240, 0.15)'); // Info
        gradient.addColorStop(1, 'rgba(33, 37, 41, 0)');       // Background

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        time += 0.02;
        requestAnimationFrame(draw);
    }

    draw();
});
