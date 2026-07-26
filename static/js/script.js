/* ========================================================
   ONLINE QUIZ APPLICATION - CLIENT JAVASCRIPT
   ======================================================== */

document.addEventListener('DOMContentLoaded', function () {
    // ----------------------------------------------------
    // 1. Quiz Timer & Auto Submit Logic
    // ----------------------------------------------------
    const timerElement = document.getElementById('quiz-timer');
    const quizForm = document.getElementById('quiz-form');

    if (timerElement && quizForm) {
        const timeLimitMinutes = parseInt(timerElement.getAttribute('data-time-limit')) || 10;
        let totalSeconds = timeLimitMinutes * 60;

        const timerDisplay = document.getElementById('timer-display');
        const progressBar = document.getElementById('timer-progress-bar');
        const initialSeconds = totalSeconds;

        const countdownInterval = setInterval(function () {
            if (totalSeconds <= 0) {
                clearInterval(countdownInterval);
                timerDisplay.textContent = "00:00 - Time's Up!";
                timerDisplay.classList.add('text-danger', 'fw-bold');
                
                // Show modal alert if available or submit immediately
                alert("Time is up! Your quiz will now be submitted automatically.");
                quizForm.submit();
            } else {
                totalSeconds--;

                const minutes = Math.floor(totalSeconds / 60);
                const seconds = totalSeconds % 60;
                const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                
                if (timerDisplay) {
                    timerDisplay.textContent = formattedTime;
                }

                if (progressBar) {
                    const percentageRemaining = (totalSeconds / initialSeconds) * 100;
                    progressBar.style.width = percentageRemaining + '%';
                    
                    if (percentageRemaining < 20) {
                        progressBar.className = 'progress-bar bg-danger';
                    } else if (percentageRemaining < 50) {
                        progressBar.className = 'progress-bar bg-warning';
                    }
                }
            }
        }, 1000);
    }

    // ----------------------------------------------------
    // 2. Answer Progress Counter
    // ----------------------------------------------------
    const totalQuestionsCount = document.querySelectorAll('.question-block').length;
    const answeredCountDisplay = document.getElementById('answered-count');

    if (totalQuestionsCount > 0 && answeredCountDisplay) {
        function updateAnsweredCount() {
            const answeredNames = new Set();
            document.querySelectorAll('.btn-check:checked').forEach(radio => {
                answeredNames.add(radio.name);
            });
            answeredCountDisplay.textContent = `${answeredNames.size} of ${totalQuestionsCount} Answered`;
        }

        document.querySelectorAll('.btn-check').forEach(radio => {
            radio.addEventListener('change', updateAnsweredCount);
        });

        updateAnsweredCount();
    }

    // ----------------------------------------------------
    // 3. Confirm Delete Prompts
    // ----------------------------------------------------
    document.querySelectorAll('.confirm-delete').forEach(button => {
        button.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // ----------------------------------------------------
    // 4. Auto-hide Flash Messages after 5 seconds
    // ----------------------------------------------------
    const flashAlerts = document.querySelectorAll('.alert-dismissible');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
