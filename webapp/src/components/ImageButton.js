import React from 'react';

function ImageButton({ onClick, imageSrc, altText }) {
    return (
        <button className="image-button mt-8" onClick={onClick}>
            <img className="rounded-full" src={imageSrc} alt={altText} />
        </button>
    );
}

export default ImageButton;
