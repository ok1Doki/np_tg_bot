import React, {useState} from "react";
import DebouncedInput from "./DebounceInput";

const ChatInputBox = ({sendANewMessage}) => {
    const [newMessage, setNewMessage] = useState("");

    const doSendMessage = () => {
        if (newMessage && newMessage.length > 0) {
            const newMessagePayload = {
                sentAt: new Date(),
                sentBy: "devlazar",
                isChatOwner: true,
                text: newMessage
            };
            sendANewMessage(newMessagePayload);
            setNewMessage("");
        }
    };

    return (
        <div className="px-6 py-3 bg-red-600 overflow-hidden w-100 rounded-bl-xl rounded-br-xl">
            <div className="flex flex-row items-center space-x-5">
                <DebouncedInput
                    value={newMessage ?? ""}
                    debounce={100}
                    onChange={(value) => setNewMessage(String(value))}
                />
                <button
                    type="button"
                    disabled={!newMessage || newMessage.length === 0}
                    className="px-3 py-2 text-xs font-medium text-center text-red-600 bg-white rounded-lg hover:bg-red-200 focus:ring-1 focus:outline-none focus:bg-red-200 disabled:opacity-50"
                    onClick={() => doSendMessage()}
                > Send
                </button>
            </div>
        </div>
    );
};

export default ChatInputBox;
