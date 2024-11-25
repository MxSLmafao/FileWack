document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('gradient-canvas');
    const ctx = canvas.getContext('2d');
    let time = 0;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    function createWave(x, y, time) {
        const wave1 = Math.sin(x * 0.015 + time) * Math.cos(y * 0.015 + time * 0.8) * 25;
        const wave2 = Math.sin(x * 0.02 - time * 1.2) * Math.cos(y * 0.02 - time) * 15;
        return wave1 + wave2;
    }

    function draw() {
        // Clear canvas with a very dark background
        ctx.fillStyle = 'rgba(33, 37, 41, 0.98)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Create gradient waves
        const imageData = ctx.createImageData(canvas.width, canvas.height);
        const data = imageData.data;

        for (let x = 0; x < canvas.width; x += 2) {
            for (let y = 0; y < canvas.height; y += 2) {
                const wave = createWave(x, y, time);
                const index = (y * canvas.width + x) * 4;
                
                // Primary color (blue) wave
                data[index] = 13 + wave;      // R
                data[index + 1] = 110 + wave; // G
                data[index + 2] = 253 + wave; // B
                data[index + 3] = 35;         // A (slightly higher opacity)

                // Apply the same color to adjacent pixels for performance
                if (x + 1 < canvas.width && y + 1 < canvas.height) {
                    const idx2 = ((y + 1) * canvas.width + x) * 4;
                    const idx3 = (y * canvas.width + (x + 1)) * 4;
                    const idx4 = ((y + 1) * canvas.width + (x + 1)) * 4;
                    
                    [idx2, idx3, idx4].forEach(idx => {
                        data[idx] = data[index];
                        data[idx + 1] = data[index + 1];
                        data[idx + 2] = data[index + 2];
                        data[idx + 3] = data[index + 3];
                    });
                }
            }
        }

        ctx.putImageData(imageData, 0, 0);

        time += 0.01; // Slightly slower animation for smoother effect
        requestAnimationFrame(draw);
    }

    draw();
});
