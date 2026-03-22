const lunch = new Object();

lunch.name = "김밥";
lunch.price = 3000;

// delete lunch.name;

console.log(lunch.name);

lunch.pay = function (user) {
    user.money -= this.price;
};

const user = {};

user.name = "홍길동";
user.money = 10000;

lunch.pay(user);
console.log(user);
