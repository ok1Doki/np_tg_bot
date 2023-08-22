import React, {useRef, useState} from 'react';
import ImageButton from "./components/ImageButton";
import ChatContent from "./components/ChatContent";
// import ChatInputBox from "./components/ChatInputBox";
import {useGetMessages} from "./hooks/useGetMassages";

function MyApp() {
    const {messages: {data}} = useGetMessages();
    // const [isInputShown, setIsInputShown] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [chatMessages, setChatMessages] = useState(data);
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    const handleStartRecording = async () => {
        if (!isRecording) {
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
            }

            const stream = await navigator.mediaDevices.getUserMedia({audio: true});
            mediaRecorderRef.current = new MediaRecorder(stream);

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    chunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(chunksRef.current);
                transcribe(audioBlob);
                chunksRef.current = [];
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        }
    };

    const handleStopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            setIsProcessing(true)
        }
    };

    const transcribe = (audioData) => {
        if (audioData) {
            const socket = new WebSocket("ws://localhost:8008/voice-assistant/ws");
            socket.onopen = (event) => {
                console.log("WebSocket connection established");
                socket.send(audioData);
            };

            socket.onmessage = (event) => {
                const message = JSON.parse(event.data);

                if (message.type === "audio") {
                    const audioBlob = base64ToBlob(message.data, "audio/mpeg");
                    const audioUrl = URL.createObjectURL(audioBlob);

                    const audioElement = new Audio(audioUrl);
                    audioElement.play().catch(error => {
                        console.error("Error playing audio:", error);
                    });
                    setIsProcessing(false)
                }

                if (message.type === "text") {
                    if (message.role === "assistant" || message.role === "user") {
                        sendANewMessage({
                            text: message.data,
                            sentAt: new Date(),
                            isChatOwner: message.role === "user"
                        })
                    }
                }
            }

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
            };

            socket.onclose = (event) => {
                console.log("WebSocket connection closed:", event);
            };
        }

    }

    function base64ToBlob(base64Data, contentType) {
        const sliceSize = 1024;
        const byteCharacters = atob(base64Data);
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);

            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }

        return new Blob(byteArrays, {type: contentType});
    }

    const sendANewMessage = (message) => {
        setChatMessages((prevMessages) => [...prevMessages, message]);
    };

    // const toggleInput = () => {
    //     setIsInputShown((prevState) => !prevState);
    // };
    return (
        <div className="app-container">
            <br/>
            <div className="max-w-2xl w-full mx-auto mt-8 ">
                <div className="w-full bg-white border border-gray-200 rounded-lg shadow relative">
                    <ChatContent messages={chatMessages}/>
                </div>
                {/*{isInputShown ? (*/}
                {/*    <div className="w-full mt-8 border border-gray-200 rounded-lg shadow relative">*/}
                {/*        <ChatInputBox sendANewMessage={sendANewMessage}/>*/}
                {/*    </div>) : null}*/}
            </div>
            {isRecording ? (
                <ImageButton
                    onClick={handleStopRecording}
                    imageSrc={require('./assets/voiceLoading.gif')}
                />
            ) : isProcessing ? (
                    <ImageButton
                        imageSrc={require('./assets/loading.gif')}
                    />
                )
                : (
                    <ImageButton
                        onClick={handleStartRecording}
                        imageSrc={require('./assets/recordingIcon.png')}
                    />
                )}
        </div>
    );
}

export default MyApp;
