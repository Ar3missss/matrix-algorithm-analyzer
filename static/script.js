document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('timeChart').getContext('2d');
    let chart = null;

    document.getElementById('matrixForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const size = document.getElementById('size').value;
        
        try {
            const response = await fetch('/multiply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `size=${size}`
            });
            
            const data = await response.json();
            
            // Display matrices
            document.getElementById('matrix1').textContent = 
                data.matrix1.map(row => row.join('\t')).join('\n');
            document.getElementById('matrix2').textContent = 
                data.matrix2.map(row => row.join('\t')).join('\n');
            
            // Update chart
            if (chart) chart.destroy();
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Standard', 'Strassen'],
                    datasets: [{
                        label: 'Execution Time (seconds)',
                        data: [data.standard_time, data.strassen_time],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Time (seconds)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Algorithm Performance Comparison'
                        }
                    }
                }
            });

            // Show results section
            document.getElementById('results').style.display = 'block';
            const correctnessElem = document.getElementById('correctness');
            correctnessElem.className = data.is_correct ? 'correct' : 'incorrect';
            correctnessElem.innerHTML = data.is_correct 
                ? '✅ Results validated against NumPy' 
                : '❌ Result mismatch detected';
            
        } catch (error) {
            console.error('Error:', error);
            alert('Analysis failed. Please check console for details.');
        }
    });
});