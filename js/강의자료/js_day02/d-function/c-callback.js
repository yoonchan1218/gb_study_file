// JS에서 false로 취급되는 값
// 0, "", null, undefined

// 두 정수의 덧셈, 결과 출력
// const add = (number1, number2, callback) => {
//     if (callback) {
//         callback(number1 + number2);
//         return;
//     }
//     return number1 + number2;
// };

// add(1, 3, console.log);
// const result = add(1, 3);

// 두 정수의 곱셈, 결과에 2를 곱해서 출력
// const multiply = (number1, number2, callback) => {
//     if (callback) {
//         // callback(number1 * number2);
//         return callback(number1 * number2);
//     }
//     return number1 * number2;
// };

// const result = multiply(5, 2);
// console.log(result);

// multiply(5, 2, (result) => {
//     console.log(result * 2);
// });

// const result = multiply(5, 2, (result) => {
//     return result * 2;
// });

// console.log(result);

// 성씨와 이름을 전달받아서 전체 이름을 만든 뒤 "000님" 출력
// const getFullName = (firstName, lastName, callback) => {
//     if (callback) {
//         // callback(lastName + firstName);
//         return callback(lastName + firstName);
//     }

//     return lastName + firstName;
// };

// const fullName = getFullName("동석", "한");
// getFullName("동석", "한", (fullName) => {
//     console.log(fullName + "님");
// });
// const fullName = getFullName("동석", "한", (fullName) => {
//     return fullName + "님";
// });

// console.log(fullName);

// 상품 1개 가격과 총 가격을 입력받고 개수를 알아낸 뒤
// 개수가 5개 이하라면 true 아니면 false 리턴
// const getCount = (price, total, callback) => {
//     let count = total / price;

//     if (callback) {
//         return callback(count);
//     }

//     return count;
// };

// const result = getCount(3000, 54000, (count) => {
//     return count <= 5;
// });

// console.log(result);

// 농장에서 축사 대청소를 하려고 한다.
// 소와 돼지의 총 마리 수를 각각 비교해 가축 중 수가 적은 쪽의 동물 이름을 리턴
// 두 수는 절대 같지 않다.
// const compareCowWithPig = (cowCount, pigCount, callback) => {
//     let result = cowCount > pigCount;
//     if (callback) {
//         return callback(result);
//     }
//     return result;
// };

// const resultName = compareCowWithPig(100, 400, (result) =>
//     result ? "돼지" : "소"
// );
// console.log(resultName);

// 학생의 국어, 영어, 수학 점수를 전달받아서 평균을 구한 뒤
// 정확히 60점일 경우 합격, 아니면 불합격

// ※ 무분별한 callback 사용은 지옥을 불러온다.
// const getTotal = (kor, eng, math, callback1, callback2) => {
//     let total = kor + eng + math;
//     if (callback1) {
//         return callback1(total, 3, callback2);
//     }
//     return total;
// };

// const getAverage = (total, count, callback) => {
//     let average = Math.round(total / count);
//     if (callback) {
//         return callback(average);
//     }

//     return average;
// };

// const isEqaulTo60 = (average) => {
//     return average === 60 ? "합격" : "불합격";
// };

// const message = getTotal(60, 30, 90, getAverage, isEqaulTo60);
// console.log(message);

// const getAverage = (kor, eng, math, callback) => {
//     let total = kor + eng + math;
//     let average = total / 3;

//     if (callback) {
//         return callback(average);
//     }

//     return average;
// };

// const message = getAverage(100, 90, 80, (average) =>
//     average === 60 ? "합격" : "불합격"
// );
// console.log(message);

// 1 ~ n까지 합을 구한 뒤 5000이상이면 5000을 빼고 출력
// const count = (end, callback) => {
//     let total = 0;
//     for (let i = 0; i < end; i++) {
//         total += i + 1;
//     }

//     if (callback) {
//         return callback(total);
//     }

//     return total;
// };

// const result = count(10, (total) => {
//     return total - (total >= 5000 && 5000);
// });

// console.log(result);

// n ~ m에서 첫 번째로 짝수인 숫자를 찾고, 그 숫자가 10 이상이면 true 아니면 false
// const checkFirstEven = (start, end, callback) => {
//     let target = 0;
//     for (let i = start; i <= end; i++) {
//         if (i % 2 == 0) {
//             target = i;
//             break;
//         }
//     }

//     if (callback) {
//         return callback(target);
//     }

//     return target;
// };

// let condition = checkFirstEven(13, 50, (target) => target >= 10);
// console.log(condition);

// const checkFirstEven = (start, callback) => {
//     let target = start + (start % 2 != 0 && 1);
//     if (callback) {
//         return callback(target);
//     }

//     return target;
// };

// let condition = checkFirstEven(14, (target) => target >= 10);
// console.log(condition);

// 두 정수의 뺄셈 결과와 두 정수의 곱셈 결과가 각각 5이상 50이상이면 true
// const isGreaterEqaulsThan5 = (result) => result >= 5;
// const isGreaterEqaulsThan50 = (result) => result > 50;

// const subtract = (number1, number2) => {
//     return number1 - number2;
// };

// const multiply = (number1, number2) => {
//     return number1 * number2;
// };

// const check = (number1, number2, callback) => {
//     let condition =
//         isGreaterEqaulsThan5(subtract(number1, number2)) &&
//         isGreaterEqaulsThan50(multiply(number1, number2));

//     if (callback) {
//         callback(condition);
//     }

//     return condition;
// };

// check(20, 6, console.log);
