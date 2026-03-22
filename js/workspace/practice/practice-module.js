// 모듈화란 합쳐져있는 기능들을 하나하나 분리한다.
// 하나의 함수는 한가지 기능만 실행한다.
// 기능이 여러가지라면 callback 함수를 사용하여
// callback 함수 안에서 나머지 기능을 실행하게 만들어준다.
// ex) getList같은 경우 리스트를 가져오는 함수를 만들고
// 그 리스트를 조회하는 것은 callback 함수에 맡긴다.

// 선언과 동시에 사용
// (function() {})();
// (() => {})();

// const add = function (number1, number2) {
//     return number1 + number2;
// };
// console.log(add(3, 2));

// 이렇게 사용할 수도 있지만

// console.log(
//     (function (number1, number2) {
//         return number1 + number2;
//     })(3, 2)
// );

// 위와 같이 함수를 선언함과 동시에 사용할 수 있고, 이 형태에 익숙해져야함.
// (function(){})();

// 서버와 통신(CRUD)
// const postService = (() => {
// 이 내부에 있는 것들은 private 데이터(외부에서 접근 불가)
//     const write = (post) => {};

//     const getList = (callback, page = 1) => {
//         if (callback) {
//             callback();
//         }
//     };

//     const read = (id, callback) => {
//         if (callback) {
//             callback();
//         }
//     };

//     const update = (post) => {};

//     const remove = (id) => {};

//     return {
//         write: write,
//         getList: getList,
//         read: read,
//         update: update,
//         remove: remove,
//     }; return한 것만 외부에서 사용한다.
// })();
