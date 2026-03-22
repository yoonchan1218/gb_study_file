const input = document.getElementById("input");
const trList = document.querySelectorAll("tbody tr");

let tempTr = null;
let tempText = null;

const send = () => {
    let check = false;

    if (tempTr) {
        tempTr.style.background = "#fff";
        tempTr.firstElementChild.textContent = tempText;
    }

    trList.forEach((tr) => {
        const td = tr.firstElementChild;
        if (td.textContent === input.value) {
            check = true;

            tempTr = tr;
            tempText = input.value;

            tr.style.background = "#ef5350";
            td.textContent = "★" + input.value;
        }
    });

    if (!check) {
        input.value = "";
    }
};
