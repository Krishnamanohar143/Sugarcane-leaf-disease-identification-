let mediaRecorder;
let recordedChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            recordedChunks = [];

            mediaRecorder.addEventListener('dataavailable', event => {
                recordedChunks.push(event.data);
            });

            toggleRecordingControls(true);
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
}

function stopRecording() {
    mediaRecorder.stop();

    mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(recordedChunks);
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recording.wav');

        fetch('/process_audio', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Audio processed successfully');
            // Handle the response if needed
        })
        .catch(error => {
            console.error('Error processing audio:', error);
        });

        toggleRecordingControls(false);
    });
}

function toggleRecordingControls(isRecording) {
    const startButton = document.getElementById('start-button');
    const stopButton = document.getElementById('stop-button');
    startButton.disabled = isRecording;
    stopButton.disabled = !isRecording;
}
