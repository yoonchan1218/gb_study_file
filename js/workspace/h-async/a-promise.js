const promise = new Promise((resolve, reject) => {
    let check = true;

    if (check) {
        resolve("resolve");
    } else {
        reject("reject");
    }
});

let data = null;

promise
    .then((result) => {
        data = result;
        console.log(result);
        return 10;
    })
    .then((data) => {
        console.log(data);
    })
    .catch((err) => {
        console.log(err);
    });

console.log(data);
