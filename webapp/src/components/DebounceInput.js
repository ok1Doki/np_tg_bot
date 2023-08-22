import React, {useState, useEffect, useCallback} from "react";
import {PaperAirplaneIcon} from "@heroicons/react/24/outline";

const DebouncedInput = ({
                            value: initialValue,
                            onChange,
                            debounce = 500,
                            ...props
                        }) => {
    const [value, setValue] = useState(initialValue);

    useEffect(() => {
        setValue(initialValue);
    }, [initialValue]);

    const debouncedOnChange = useCallback(
        (newValue) => {
            const timeout = setTimeout(() => {
                onChange(newValue);
            }, debounce);

            return () => clearTimeout(timeout);
        },
        [onChange, debounce]
    );

    return (
        <>
            <div className="relative w-full">
                <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <PaperAirplaneIcon className="w-4 h-4" />
                </div>
                <input
                    type="text"
                    className="w-full block p-1.5 pl-10 text-sm text-gray-900 border-gray-300 rounded-lg bg-white ring-0 focus:ring-0 outline-0 focus:outline-none"
                    id="message-box"
                    {...props}
                    value={value}
                    onChange={(e) => {
                        setValue(e.target.value);
                        debouncedOnChange(e.target.value);
                    }}
                />
            </div>
        </>
    );
};

export default DebouncedInput;
