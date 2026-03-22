// function change(img) {
//     // img.src = "images/icon4.png";
//     img.src = "images/" + 
//         (img.src.includes("icon5.png") ? "icon4.png" : "icon5.png")
// }

const module = (() => {

    const change = (img) => {
        img.src = "images/" + 
            (img.src.includes("icon5.png") ? "icon4.png" : "icon5.png")
    }

    return {change: change};
})();