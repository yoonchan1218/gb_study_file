// function add(number1, number2) {
//     return number1 + number2;
// }

// let plus = add;

// const result = plus(1, 3);
// console.log(result);

// const add = (number1, number2) => {
//     return number1 + number2;
// };

// console.log(add(3, 5));

// const printInfo = (age, address, name = "익명") => {
//     console.log(age, address, name);
// };

// printInfo(20, "경기도", "한동석");
// printInfo(100, "서울");

// 두 정수를 전달받고 두 수를 곱한다.
// 이 때, 만약 apply라는 매개변수가 true라면 결과값에서 10을 뺀다.
// apply는 기본값이 false이다.
// const multiply = (number1, number2, apply = false) => {
//     // return number1 * number2 - (apply ? 10 : 0);
//     return number1 * number2 - (apply && 10);
// };

// const result = multiply(2, 5);
// console.log(result);
