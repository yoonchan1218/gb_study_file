// const datas = [10, 4, 20, 3, 2];
// console.log(datas);

// 값 추가
// push(): 가장 마지막에 값 추가
// datas.push(3);
// console.log(datas);

// 값 연결
// join(): 전달한 값으로 각 요소를 구분하여 모두 연결해준다.
// console.log(datas.join(","));
// console.log([10, 30, 15].join(":"));

// 값 추출
// slice(begin, end): 원하는 부분을 추출하기 위해 시작(포함)과 끝(제외) 인덱스를 전달한다.
// console.log(datas.slice(0, 3));

// slice(begin): 원하는 부분을 추출하기 위해 시작(포함) 인덱스만 전달하면, 끝까지 추출한다.
// console.log(datas.slice(1));

// 값 삭제
// splice(index, count): index부터 count개 삭제, 삭제된 값을 Array객체로 리턴
// console.log(datas.splice(2, 2));
// console.log(datas);

// 값 교체
// splice(index, count, ...args): index부터 count개 삭제, 삭제된 위치에 args에 전달된 값으로 대체
// console.log(datas.splice(2, 2, 100, 200));
// console.log(datas);

// 가변 인자
// const getTotal = (...numbers) => {
//     let total = 0;
//     for (let i = 0; i < numbers.length; i++) {
//         total += numbers[i];
//     }

//     return total;
// };

// let result = getTotal(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
// console.log(result);

// pop(): 마지막 요소 삭제
// let result = datas.pop();
// console.log(result);
// console.log(datas);

// shift(): 첫 번째 요소 삭제
// let result = datas.shift();
// console.log(result, datas);

// 값 조회
// indexOf(), lastIndexOf();
// datas.push(10);
// console.log(datas.indexOf(10));
// console.log(datas.lastIndexOf(10));

// 몇 칸인지 아는데, 무슨 값이 들어갈지 모를 때
// const datas = new Array(10).fill(0);
// console.log(datas.length);
// console.log(datas);

// 반복
// const datas = [10, 4, 20, 3, 2];

// // 값 가져오기
// for (let data of datas) {
//     console.log(data);
// }

// // 인덱스 가져오기
// for (let i in datas) {
//     console.log(i);
// }

// array.forEach((data, index, array) => {});
// 접근한 array객체로부터 각 요소를 data에 담고
// 각 인덱스를 index에 담는다.
// 접근한 array객체를 array에 담는다.
// const datas = [10, 4, 20, 3, 2];

// 매개변수 중 필요 없는 부분은 _(언더바)로 작성한다.
// 뒤에 있는 매개변수는 굳이 _(언더바)를 작성할 필요 없이 그냥 안쓰면 된다.
// datas.forEach((_, i) => {
//     console.log(i);
// });

// 2 ~ 10까지 중 2의 배수만 Array 객체에 담기
// const datas = new Array(5).fill(0);

// datas.forEach((_, i, datas) => {
//     datas[i] = (i + 1) * 2;
// });

// console.log(datas);

// 1 ~ 10까지 담은 후 각 값의 제곱을 출력한다.
// const datas = new Array(10).fill(0);

// datas.forEach((_, i, datas) => {
//     datas[i] = i + 1;
// });

// datas.forEach((data) => {
//     console.log(data * data);
// });

// map((data, index, array) => {});
// 전달한 callback 함수의 리턴값으로 변경
// let datas = new Array(10, 6, 4, 8, 2);
// datas = datas.map((data) => data - 1);
// console.log(datas);

// 기존 값을 두 배 증가시키기
// let datas = new Array(10, 6, 4, 8, 2);
// datas = datas.map((data) => data * 2);
// console.log(datas);

// filter((data, index, array) => {});
// callback 함수의 리턴값이 true인 것만 추출
// let datas = new Array(10).fill(0).map((_, i) => i + 1);
// datas = datas.filter((data) => data > 4);
// console.log(datas);

// 1 ~ 100까지 담고 4의 배수만 추출
const datas = new Array(100)
    .fill(0)
    .map((_, i) => i + 1)
    .filter((data) => data % 4 == 0);
console.log(datas);
