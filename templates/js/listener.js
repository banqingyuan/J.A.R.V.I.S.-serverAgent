document.addEventListener("DOMContentLoaded", function () {
    var audioContext = new AudioContext();
    var audioInput = null,
        realAudioInput = null,
        inputPoint = null,
        audioRecorder = null;
    var rafID = null;
    var analyserContext = null;
    var canvasWidth, canvasHeight;
    var recIndex = 0;
    /* TODO:
    - offer mono option
    - "Monitor input" switch
    */
    var isRecording = false; // 增加记录是否正在录音的变量
    var startTime = 0; // 记录开始录音时间

    // 获取该button元素
    let btn = document.querySelector('#myBtn');

    // 为该button添加点击事件
    btn.addEventListener('click', function () {
        toggleRecording(this);
    });
    function saveAudio() {
        audioRecorder.exportWAV(doneEncoding);
        console.log("save recording successed!")
        // could get mono instead by saying
        // audioRecorder.exportMonoWAV( doneEncoding );
    }
    function gotBuffers(buffers) {
        var canvas = document.getElementById("wavedisplay");
        drawBuffer(canvas.width, canvas.height, canvas.getContext('2d'), buffers[0]);
        // the ONLY time gotBuffers is called is right after a new recording is completed - 
        // so here's where we should set up the download.
        audioRecorder.exportWAV(doneEncoding);
    }
    function doneEncoding(blob) {
        // 将blob转换为url
        //var url = URL.createObjectURL(blob);
        var name = "myRecording" + ((recIndex < 10) ? "0" : "") + recIndex + ".wav";
        // 创建a标签，实现下载
        // var link = document.createElement('a');
        // link.href = url;
        // link.download = "myRecording" + ((recIndex < 10) ? "0" : "") + recIndex + ".wav";
        // recIndex++;
        // link.innerHTML = '<i class="icon icon-download"></i>';
        // 添加到页面
        //document.body.appendChild(link);
        // 执行下载
        //link.click();
        // 删除a标签
        //document.body.removeChild(link);
        sendToWishper(blob, name);
        
    }
    function sendToWishper(blob, name) {
            console.log(name)
            var formData = new FormData();
            formData.append("file", blob, name);
            formData.append("model", "whisper-1");


            const xhr = new XMLHttpRequest();
            const startTime = Date.now(); // 记录代码开始耗时

            xhr.open('POST', 'https://api.openai.com/v1/audio/transcriptions');
            xhr.setRequestHeader('Authorization', `Bearer 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`);
            xhr.onload = () => {
                if (xhr.status === 200) {
                    console.log(xhr.responseText);
                    const endTime = Date.now(); 
                    const totalTime = endTime - startTime; // 计算总耗时
                    console.log(`${totalTime}ms`); 
                }
            };
            xhr.send(formData);
    }
    function toggleRecording(e) {
        if (e.classList.contains("recording")) {
            console.log("stop recording")
            // stop recording
            audioRecorder.stop();
            e.classList.remove("recording");
            // audioRecorder.getBuffer(function(data) {
            //     console.log(data);
            //     gotBuffers
            //   });
            isRecording = false; // 停止录音
            startTime = 0; // 重置开始录音时间
        } else {
            // start recording
            if (!audioRecorder)
                return;
            console.log("start recording")

            e.classList.add("recording");
            audioRecorder.clear();
            audioRecorder.record();
            isRecording = true; // 开始录音
            startTime = new Date().getTime(); // 记录开始录音时间
            // 增加每隔10秒生成一个音频切片并保存在临时文件中的逻辑
            setInterval(() => {
                if (isRecording) {
                    var currentTime = new Date().getTime();
                    if (currentTime - startTime > 3000) {
                        console.log("saving recording")
                        saveAudio();
                        audioRecorder.clear();
                        startTime = currentTime;

                    }
                }
            }, 1000);
        }
    }

    // function convertToMono(input) {
    //     var splitter = audioContext.createChannelSplitter(2);
    //     var merger = audioContext.createChannelMerger(2);
    //     input.connect(splitter);
    //     splitter.connect(merger, 0, 0);
    //     splitter.connect(merger, 0, 1);
    //     return merger;
    // }
    function cancelAnalyserUpdates() {
        window.cancelAnimationFrame(rafID);
        rafID = null;
    }
    function updateAnalysers(time) {
        if (!analyserContext) {
            var canvas = document.getElementById("analyser");
            canvasWidth = canvas.width;
            canvasHeight = canvas.height;
            analyserContext = canvas.getContext('2d');
        }
        // analyzer draw code here
        {
            var SPACING = 3;
            var BAR_WIDTH = 1;
            var numBars = Math.round(canvasWidth / SPACING);
            var freqByteData = new Uint8Array(analyserNode.frequencyBinCount);
            analyserNode.getByteFrequencyData(freqByteData);
            analyserContext.clearRect(0, 0, canvasWidth, canvasHeight);
            analyserContext.fillStyle = '#F6D565';
            analyserContext.lineCap = 'round';
            var multiplier = analyserNode.frequencyBinCount / numBars;
            // Draw rectangle for each frequency bin.
            for (var i = 0; i < numBars; ++i) {
                var magnitude = 0;
                var offset = Math.floor(i * multiplier);
                // gotta sum/average the block, or we miss narrow-bandwidth spikes
                for (var j = 0; j < multiplier; j++)
                    magnitude += freqByteData[offset + j];
                magnitude = magnitude / multiplier;
                var magnitude2 = freqByteData[i * multiplier];
                analyserContext.fillStyle = "hsl( " + Math.round((i * 360) / numBars) + ", 100%, 50%)";
                analyserContext.fillRect(i * SPACING, canvasHeight, BAR_WIDTH, -magnitude);
            }
        }
        rafID = window.requestAnimationFrame(updateAnalysers);
    }
    // function toggleMono() {
    //     if (audioInput != realAudioInput) {
    //         audioInput.disconnect();
    //         realAudioInput.disconnect();
    //         audioInput = realAudioInput;
    //     } else {
    //         realAudioInput.disconnect();
    //         audioInput = convertToMono(realAudioInput);
    //     }
    //     audioInput.connect(inputPoint);
    // }
    function gotStream(stream) {
        audioContext.resume()
        inputPoint = audioContext.createGain();
        // Create an AudioNode from the stream.
        realAudioInput = audioContext.createMediaStreamSource(stream);
        audioInput = realAudioInput;
        audioInput.connect(inputPoint);
        //    audioInput = convertToMono( input );
        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 2048;
        inputPoint.connect(analyserNode);
        audioRecorder = new Recorder(inputPoint);
        zeroGain = audioContext.createGain();
        zeroGain.gain.value = 0.0;
        inputPoint.connect(zeroGain);
        zeroGain.connect(audioContext.destination);
        updateAnalysers();
    }
    function initAudio() {
        if (!navigator.getUserMedia)
            navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        if (!navigator.cancelAnimationFrame)
            navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
        navigator.getUserMedia(
            {
                "audio": {
                    "mandatory": {
                        "googEchoCancellation": "false",
                        "googAutoGainControl": "false",
                        "googNoiseSuppression": "false",
                        "googHighpassFilter": "false"
                    },
                    "optional": []
                },
            }, gotStream, function (e) {
                alert('Error getting audio');
                console.log(e);
            });
    }
    window.addEventListener('load', initAudio);
});