// static, 클래스로만 접근 가능
// User.count = 2;

// prototype, 해당 타입의 객체로만 접근 가능
// User.prototype.introduce = function () {
//     console.log(this.name, this.age, this.gender);
// };

// function User(name, age, gender = "선택안함") {
//     this.name = name;
//     this.age = age;
//     this.gender = gender;
// }

// const lee = new User("이순신", 50);
// const hong = new User("홍길동", 95);

// console.log(User.count);
// lee.introduce();
// hong.introduce();

// 회사 객체에 직원의 정보가 있다.
// 직원의 수익이 회사의 수익에 더해져야한다.
Company.income = 0;

Company.prototype.setTotal = function () {
    Company.income += this.income;
};

function Company(name, age, income = 0) {
    this.name = name;
    this.age = age;
    this.income = income;
}

const lee = new Company("이순신", 54);
const hong = new Company("홍길동", 23);

lee.income = 3000;
hong.income = 5500;

// Company.income += lee.income;
// Company.income += hong.income;
lee.setTotal();
hong.setTotal();

console.log(Company.income);
