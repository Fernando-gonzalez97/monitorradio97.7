const ctx = document.getElementById('audioChart').getContext('2d');
const { audioLevel, isSilent } = window.radioData;

let animationFrame = 0;

const generateWaveform = (level, silent, frame) => {
    const data = [];
    const points = 100;
    const amplitude = silent ? 0.5 : Math.abs(level) / 3;
    
    for (let i = 0; i < points; i++) {
        if (silent) {
            data.push((Math.random() - 0.5) * 0.3);
        } else {
            const x = ((i / points) * Math.PI * 4) + (frame * 0.1);
            const noise = (Math.random() - 0.5) * amplitude * 0.3;
            const wave = Math.sin(x) * amplitude + Math.cos(x * 0.5) * (amplitude * 0.5) + noise;
            data.push(wave);
        }
    }
    return data;
};

const audioChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array(100).fill(''),
        datasets: [{
            label: 'Señal de Audio',
            data: generateWaveform(audioLevel, isSilent, 0),
            borderColor: isSilent ? 'rgba(239, 68, 68, 0.8)' : 'rgba(34, 197, 94, 0.8)',
            backgroundColor: isSilent ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
        },
        scales: {
            x: { display: false },
            y: {
                display: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                    drawBorder: false
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.5)',
                    font: { size: 10 }
                }
            }
        },
        animation: false
    }
});

// Efectos visuales según silencio
const visualizer = document.querySelector('.visualizer-container');
if (isSilent) {
    visualizer.style.opacity = '0.5';
    visualizer.style.filter = 'grayscale(50%)';
} else {
    visualizer.style.opacity = '1';
    visualizer.style.filter = 'none';
}

// Animar solo si NO hay silencio
function animate() {
    if (!isSilent) {
        animationFrame++;
        audioChart.data.datasets[0].data = generateWaveform(audioLevel, isSilent, animationFrame);
        audioChart.update('none');
    }
    requestAnimationFrame(animate);
}

animate();