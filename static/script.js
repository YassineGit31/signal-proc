document.addEventListener("DOMContentLoaded", function () {
    const inputElement = document.getElementById("formulaInput");
    const submitButton = document.getElementById("submitButton");
    const canvas = document.getElementById("signalCanvas");
    let chartInstance = null;

    if (!inputElement || !submitButton || !canvas) {
        console.error("Error: Missing input field, button, or canvas!");
        return;
    }

    submitButton.addEventListener("click", function () {
        processSignal();
    });

    function processSignal() {
        const formula = inputElement.value.trim();

        if (formula === "") {
            console.error("Error: Formula input is empty!");
            return;
        }

        fetch("http://127.0.0.1:5000/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ formula: formula })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error:", data.error);
            } else {
                console.log("Signal Data:", data);

                // Plot the signal
                drawSignal(data.t, data.y);

                // Display energy output if available
                if (data.energy) {
                    document.getElementById("energyOutput").innerText = `Signal Energy: ${data.energy}`;
                }
            }
        })
        .catch(error => console.error("Error processing signal:", error));
    }

    function drawSignal(t, y) {
        if (chartInstance) {
            chartInstance.destroy(); // Destroy previous chart
        }

        const ctx = canvas.getContext("2d");
        chartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: t,
                datasets: [{
                    label: "Signal Amplitude",
                    data: y,
                    borderColor: "red",
                    backgroundColor: "rgba(255, 0, 0, 0.2)",
                    borderWidth: 2,
                    pointRadius: 0, // Remove points for a smooth curve
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Time (t)" } },
                    y: { title: { display: true, text: "Amplitude" } }
                }
            }
        });
    }
});



