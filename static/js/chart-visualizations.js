// ===================================
// CHART VISUALIZATIONS
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    initAnalysisCharts();
    initComparisonCharts();
});

// ===================================
// ANALYSIS PAGE CHARTS
// ===================================
function initAnalysisCharts() {
    const dataElement = document.getElementById('analysisData');
    if (!dataElement) return;
    
    const statsChurned = parseInt(dataElement.getAttribute('data-churned'));
    const statsRetained = parseInt(dataElement.getAttribute('data-retained'));
    const rechargeDataStr = dataElement.getAttribute('data-recharge');
    const rechargeData = rechargeDataStr ? JSON.parse(rechargeDataStr) : {};
    
    // Churn Distribution Chart
    const churnCtx = document.getElementById('churnChart');
    if (churnCtx) {
        new Chart(churnCtx, {
            type: 'doughnut',
            data: {
                labels: ['Retained', 'Churned'],
                datasets: [{
                    data: [statsRetained, statsChurned],
                    backgroundColor: [
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(244, 67, 54, 0.8)'
                    ],
                    borderColor: [
                        'rgba(76, 175, 80, 1)',
                        'rgba(244, 67, 54, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            font: { size: 14 }
                        }
                    }
                }
            }
        });
    }
    
    // Recharge Type Chart
    const rechargeCtx = document.getElementById('rechargeChart');
    if (rechargeCtx && Object.keys(rechargeData).length > 0) {
        const labels = Object.keys(rechargeData);
        const data = Object.values(rechargeData);
        
        new Chart(rechargeCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Churned Customers',
                    data: data,
                    backgroundColor: 'rgba(139, 127, 217, 0.8)',
                    borderColor: 'rgba(139, 127, 217, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            stepSize: 1
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            maxRotation: 45,
                            minRotation: 45
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            font: { size: 14 }
                        }
                    }
                }
            }
        });
    }
}

// ===================================
// COMPARISON PAGE CHARTS
// ===================================
function initComparisonCharts() {
    const dataElement = document.getElementById('comparisonData');
    if (!dataElement) return;
    
    const dtAccuracy = parseFloat(dataElement.getAttribute('data-dt-accuracy'));
    const dtPrecision = parseFloat(dataElement.getAttribute('data-dt-precision'));
    const dtRecall = parseFloat(dataElement.getAttribute('data-dt-recall'));
    const dtF1 = parseFloat(dataElement.getAttribute('data-dt-f1'));
    
    const knnAccuracy = parseFloat(dataElement.getAttribute('data-knn-accuracy'));
    const knnPrecision = parseFloat(dataElement.getAttribute('data-knn-precision'));
    const knnRecall = parseFloat(dataElement.getAttribute('data-knn-recall'));
    const knnF1 = parseFloat(dataElement.getAttribute('data-knn-f1'));
    
    const comparisonCtx = document.getElementById('comparisonChart');
    if (comparisonCtx) {
        new Chart(comparisonCtx, {
            type: 'bar',
            data: {
                labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                datasets: [
                    {
                        label: 'Decision Tree',
                        data: [dtAccuracy, dtPrecision, dtRecall, dtF1],
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2
                    },
                    {
                        label: 'KNN',
                        data: [knnAccuracy, knnPrecision, knnRecall, knnF1],
                        backgroundColor: 'rgba(196, 167, 231, 0.8)',
                        borderColor: 'rgba(196, 167, 231, 1)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            callback: function(value) {
                                return value.toFixed(2);
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: 'rgba(232, 230, 240, 0.95)'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(232, 230, 240, 0.95)',
                            font: { size: 14 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(4);
                            }
                        }
                    }
                }
            }
        });
    }
}

console.log('✅ Chart visualizations loaded successfully');
