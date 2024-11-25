document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('gradient-canvas');
    const ctx = canvas.getContext('2d');
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let targetX = mouseX;
    let targetY = mouseY;

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

    function draw() {
        // Smooth mouse movement
        mouseX = lerp(mouseX, targetX, 0.1);
        mouseY = lerp(mouseY, targetY, 0.1);

        // Clear canvas
        ctx.fillStyle = 'rgba(33, 37, 41, 0.1)'; // Bootstrap dark theme background
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Create gradient
        const gradient = ctx.createRadialGradient(
            mouseX, mouseY, 0,
            mouseX, mouseY, 300
        );

        // Use Bootstrap dark theme colors
        gradient.addColorStop(0, 'rgba(13, 110, 253, 0.2)'); // Primary color
        gradient.addColorStop(0.2, 'rgba(32, 201, 151, 0.15)'); // Success color
        gradient.addColorStop(0.4, 'rgba(13, 202, 240, 0.1)'); // Info color
        gradient.addColorStop(1, 'rgba(33, 37, 41, 0)'); // Background color

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        requestAnimationFrame(draw);
    }

    draw();
});
