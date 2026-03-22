create database dml;
use dml;

drop table tbl_zoo;
create table tbl_zoo(
	id bigint unsigned auto_increment primary key,
	zoo_name varchar(255) not null,
	zoo_address varchar(255) not null,
	zoo_address_detail varchar(255) not null,
	zoo_max_animal int check(zoo_max_animal > 0)
);

drop table tbl_animal;
create table tbl_animal(
	id bigint unsigned auto_increment primary key,
	animal_name varchar(255) not null,
	animal_type varchar(255) not null,
	animal_age int default 0,
	animal_height decimal(5, 2) check(animal_height > 0),
	animal_weight decimal(5, 2) check(animal_weight > 0),
	zoo_id bigint unsigned not null,
	constraint fk_animal_zoo foreign key(zoo_id)
	references tbl_zoo(id)
);

/*insert into tbl_zoo(id, zoo_name, zoo_address, zoo_address_detail)
values(1, '서울랜드', '과천', '123');

insert into tbl_zoo
values(2, '애버랜드', '용인', '321', 10);*/

insert into tbl_zoo(zoo_name, zoo_address, zoo_address_detail, zoo_max_animal)
values('애버랜드', '경기도 용인시', '12345', 10);
insert into tbl_zoo(zoo_name, zoo_address, zoo_address_detail, zoo_max_animal)
values('서울랜드', '경기도 과천시', '55555', 5);

select id, zoo_name, zoo_address, zoo_address_detail, zoo_max_animal
from tbl_zoo;

select * from tbl_zoo;

insert into tbl_animal(animal_name, animal_type, animal_height, animal_weight, zoo_id)
values('호돌이', '호랑이', 123.25, 120.2, 1);

select * from tbl_animal;

update tbl_animal
set zoo_id = 2
where id = 1;

delete from tbl_animal
where id = 1;

/*insert 실습*/
/*첫 번째 동물원에 두 마리의 동물*/
insert into tbl_animal (animal_name, animal_type, animal_height, animal_weight, zoo_id)
values('코붕이', '코끼리', 300.42, 999.25, 1);
insert into tbl_animal (animal_name, animal_type, animal_height, animal_weight, zoo_id)
values('장대', '기린', 800.42, 500.25, 1);

/*두 번째 동물원에 한 마리의 동물*/
insert into tbl_animal (animal_name, animal_type, animal_height, animal_weight, zoo_id)
values('꼬꼬', '독수리', 88.42, 44.25, 2);

select * from tbl_animal;

/*동물원 중에서 최대 수용 동물 수가 5보다 큰 동물원 조회*/
select * from tbl_zoo
where zoo_max_animal > 5;

/*동물원 중 1번 동물원의 동물 나이를 모두 1씩 증가*/
update tbl_animal
set animal_age = animal_age + 1
where zoo_id = 1;

select * from tbl_animal;

/*동물 중에서 1번 동물원에 지내고 있는 동물 모두 삭제*/
delete from tbl_animal
where zoo_id = 1;

select * from tbl_animal;
/******************************************************************************/
drop table tbl_company;
create table tbl_company(
	id bigint unsigned auto_increment primary key,
	company_name varchar(255),
	company_address varchar(255)
);

drop table tbl_employee;
create table tbl_employee(
	id bigint unsigned auto_increment primary key,
	employee_name varchar(255),
	company_id bigint unsigned not null,
	constraint fk_employee_company foreign key(company_id)
	references tbl_company(id)
);

/*회사 2군데 추가*/
insert into tbl_company(company_name, company_address)
values('코리아', '역삼');
insert into tbl_company(company_name, company_address)
values('삼성', '논현');

select * from tbl_company;

/*각 회사별 직원 2명씩 추가*/
insert into tbl_employee(employee_name, company_id)
values('홍길동', 1), ('이순신', 1), ('둘리', 2), ('또치', 2);

select * from tbl_employee;

/*'홍길동'직원의 전체 정보 조회*/
select * from tbl_employee
where employee_name = '홍길동';

/*'코리아'회사의 전체 정보 조회*/
select * from tbl_company
where company_name = '코리아';

/*'코리아'회사에 다니는 직원의 이름을 모두 '둘리'로 수정*/
update tbl_employee
set employee_name = '둘리'
where company_id = 1;

select * from tbl_employee;

/*'홍길동'직원 삭제*/
delete from tbl_employee
where employee_name = '홍길동';
/******************************************************************************/
drop table tbl_member;
create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_email varchar(255) unique not null,
	member_name varchar(255)
);

drop table tbl_like;
create table tbl_like(
	id bigint unsigned auto_increment primary key,
	sender_id bigint unsigned not null,
	receiver_id bigint unsigned not null,
	constraint fk_like_sender_member foreign key(sender_id)
	references tbl_member(id),
	constraint fk_like_receiver_member foreign key(receiver_id)
	references tbl_member(id)
);

/*회원 3명 추가*/
insert into tbl_member
(member_email, member_name)
values
('test1234@gmail.com', '홍길동'), 
('test5555@naver.com', '이순신'), 
('test7777@test.com', '장보고');

select * from tbl_member;

/*1번 -> 2번 좋아요*/
/*1번 -> 3번 좋아요*/
/*2번 -> 1번 좋아요*/
insert into tbl_like(sender_id, receiver_id)
values(1, 2), (1, 3), (2, 1);

/*1번을 좋아요한 전체 회원 번호 조회*/
select * from tbl_like
where receiver_id = 1;

/*이름이 '홍길동'인 회원을 좋아요한 회원의 이름 조회*/
select * from tbl_member
where member_name = '홍길동';

select * from tbl_like
where receiver_id = 1;

select member_name from tbl_member
where id = 2;

/*2번 -> 1번 좋아요 취소, 2번 -> 3번 좋아요*/
select * from tbl_like;

update tbl_like
set receiver_id = 3
where id = 3;

/*1번 -> 2번 좋아요 취소*/
delete from tbl_like
where id = 1;

delete from tbl_like
where sender_id = 1 and receiver_id = 2;

select * from tbl_like;
/******************************************************************************/
/*join*/
/*from -> join -> on -> where -> select*/
drop table tbl_member;
create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_email varchar(255) unique not null,
	member_name varchar(255)
);

drop table tbl_like;
create table tbl_like(
	id bigint unsigned auto_increment primary key,
	sender_id bigint unsigned not null,
	receiver_id bigint unsigned not null,
	constraint fk_like_sender_member foreign key(sender_id)
	references tbl_member(id),
	constraint fk_like_receiver_member foreign key(receiver_id)
	references tbl_member(id)
);

insert into tbl_member
(member_email, member_name)
values
('test1234@gmail.com', '홍길동'), 
('test5555@naver.com', '이순신'), 
('test7777@test.com', '장보고');

insert into tbl_like(sender_id, receiver_id)
values(1, 2), (1, 3), (2, 1);

select 
l.id, l.sender_id, m2.member_name sender_name, 
l.receiver_id, m1.member_name receiver_name
from tbl_like l join tbl_member m1
on l.receiver_id  = m1.id
join tbl_member m2
on l.sender_id = m2.id
where m2.member_name = '홍길동';
/******************************************************************************/
drop table tbl_car;
create table tbl_car(
	id bigint unsigned auto_increment primary key,
	car_brand varchar(255) not null,
	car_model varchar(255) not null,
	car_price bigint unsigned default 0,
	car_release_date date
);

insert into tbl_car(car_brand, car_model, car_price, car_release_date)
values('Benz', 'E-class', 15000, '2024-12-04');
insert into tbl_car(car_brand, car_model, car_price, car_release_date)
values('BMW', 'M4', 10000, '2025-03-24');

select * from tbl_car;

create table tbl_owner(
	id bigint unsigned auto_increment primary key,
	owner_name varchar(255) not null,
	owner_phone varchar(255) not null,
	owner_address varchar(255) not null,
	owner_address_detail varchar(255) not null
);

insert into tbl_owner(owner_name, owner_phone, owner_address, owner_address_detail)
values('홍길동', '01012341234', '서울시 강남구', '12345');
insert into tbl_owner(owner_name, owner_phone, owner_address, owner_address_detail)
values('이순신', '01088887777', '경기도 하남시', '78784');
insert into tbl_owner(owner_name, owner_phone, owner_address, owner_address_detail)
values('장보고', '01085555111', '경기도 남양주시', '54212');

select * from tbl_owner;

create table tbl_registration(
	id bigint unsigned auto_increment primary key,
	car_id bigint unsigned not null,
	owner_id bigint unsigned not null,
	constraint fk_registration_car foreign key(car_id)
	references tbl_car(id),
	constraint fk_registration_owner foreign key(owner_id)
	references tbl_owner(id)
);

insert into tbl_registration(car_id, owner_id)
values(1, 2), (2, 2), (1, 3), (1, 1);

select c.car_brand, c.car_model, o.owner_name, o.owner_phone
from tbl_registration r join tbl_car c
on r.car_id = c.id
join tbl_owner o
on o.id = r.owner_id;
/******************************************************************************/
create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_email varchar(255) unique not null,
	member_name varchar(255) default '익명'
);

create table tbl_post(
	id bigint unsigned auto_increment primary key,
	post_title varchar(255) not null,
	post_content text not null,
	created_datetime datetime default current_timestamp(),
	member_id bigint unsigned not null,
	constraint fk_post_member foreign key(member_id)
	references tbl_member(id)
);

create table tbl_reply(
	id bigint unsigned auto_increment primary key,
	reply_content text not null,
	member_id bigint unsigned not null,
	post_id bigint unsigned not null,
	constraint fk_reply_member foreign key(member_id)
	references tbl_member(id),
	constraint fk_reply_post foreign key(post_id)
	references tbl_post(id)
);

insert into tbl_member
(member_email, member_name)
values
('test1234@naver.com', '홍길동'), 
('test5555@gmail.com', '이순신'),
('test7777@test.com', '장보고');

insert into tbl_post(post_title, post_content, member_id)
values
('테스트 제목1', '테스트 내용1', 1),
('테스트 제목2', '테스트 내용2', 1),
('테스트 제목3', '테스트 내용3', 2),
('테스트 제목4', '테스트 내용4', 2),
('테스트 제목5', '테스트 내용5', 3),
('테스트 제목6', '테스트 내용6', 2),
('테스트 제목7', '테스트 내용7', 1),
('테스트 제목8', '테스트 내용8', 1),
('테스트 제목9', '테스트 내용9', 1);

insert into tbl_reply(reply_content, member_id, post_id)
values
('댓글 테스트1', 1, 3),
('댓글 테스트1', 1, 2),
('댓글 테스트1', 1, 9),
('댓글 테스트1', 1, 8),
('댓글 테스트1', 3, 1),
('댓글 테스트1', 3, 2),
('댓글 테스트1', 3, 1),
('댓글 테스트1', 2, 6),
('댓글 테스트1', 2, 5),
('댓글 테스트1', 2, 5),
('댓글 테스트1', 1, 7),
('댓글 테스트1', 1, 7),
('댓글 테스트1', 3, 8),
('댓글 테스트1', 3, 8),
('댓글 테스트1', 2, 4);

/*댓글 정보와 작성자 이름 조회*/
select m.member_name, r.reply_content
from tbl_member m join tbl_reply r
on m.id = r.member_id;

/*댓글이 달린 게시글 제목 조회*/
select distinct p.id, p.post_title 
from tbl_post p join tbl_reply r
on p.id = r.post_id;

/*이메일이 test5555@gmail.com인 회원이 작성한 게시글 정보와 회원의 이름 조회*/
select * 
from tbl_member m join tbl_post p
on m.id = p.member_id
where m.member_email = 'test5555@gmail.com'

/*댓글 작성자 이름이 '이순신'인 회원 정보와 댓글 정보 조회*/
select m.*, r.* 
from tbl_member m join tbl_reply r
on m.id = r.member_id
where m.member_name = '이순신';

/*like: 포함된 문자열 값을 찾고, 문자의 개수도 제한을 줄 수 있다.*/
/*%: 모든 것*/
/*_: 글자 수*/

/*
 * '%A'	:A로 끝나는 모든 값
 * 'A%'	:A로 시작하는 모든 값
 * '%A%':A가 포함된 모든 값
 * 'A_'	:A로 시작하면서 2글자인 값
 * '__A':A로 끝나면서 3글자인 값
 * */
select concat(member_name, '님') 이름 from tbl_member
where member_name like concat('%', '순', '%');

/***************************************************************/
/*
 * 집계 함수
 * 
 * 평균 avg()
 * 최대값 max()
 * 최소값 min()
 * 총합 sum()
 * 개수 count()
 * */
create table tbl_owner(
	id bigint unsigned auto_increment primary key,
	owner_name varchar(255) not null,
	owner_age int,
	owner_phone varchar(255) not null,
	owner_address varchar(255) not null,
	owner_address_detail varchar(255) not null
);

create table tbl_pet(
	id bigint unsigned auto_increment primary key,
	pet_ill_name varchar(255) not null,
	pet_name varchar(255) not null,
	pet_age int,
	pet_weight decimal(4, 2) not null,
	owner_id bigint unsigned,
	constraint fk_pet_owner foreign key(owner_id)
	references tbl_owner(id)
);

insert into tbl_owner
(owner_name, owner_age, owner_phone, owner_address, owner_address_detail)
values
('한동석', 20, '01012341234', '경기도', '12345'),
('홍길동', 37, '01078784585', '서울', '33322'),
('이순신', 50, '01041812318', '대구', '54322');

insert into tbl_pet
(pet_ill_name, pet_name, pet_age, pet_weight, owner_id)
values
('장염', '뽀삐', 4, 10.45, 1),
('감기', '달구', 12, 14.25, 2),
('탈골', '댕댕', 7, 8.46, 2),
('염좌', '쿠키', 11, 5.81, 3),
('충치', '바둑', 1, 3.47, 1);

select round(avg(pet_weight), 2) average_weight from tbl_pet;
select max(pet_weight) from tbl_pet;
select min(pet_weight) from tbl_pet;
select sum(pet_weight) from tbl_pet;
select count(*) from tbl_pet;

/*group by: ~ 별*/
insert into tbl_pet
(pet_ill_name, pet_name, pet_age, pet_weight, owner_id)
values
('장염', '방울', 4, 10.45, 1),
('장염', '초롱', 7, 8.46, 2),
('장염', '까미', 11, 5.81, 3);

select pet_ill_name, count(*) from tbl_pet
group by pet_ill_name;

select pet_ill_name, max(pet_weight) from tbl_pet
group by pet_ill_name;
/******************************************************************************/
/*서브 쿼리*/
/*메인 쿼리 안에 또 다른 쿼리를 작성하는 문법*/
/*
 * from: 인라인 뷰
 * where: 서브 쿼리
 * select: 스칼라 서브 쿼리
 * 
 * */

drop table tbl_member;
create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_email varchar(255) unique not null,
	member_name varchar(255)
);

drop table tbl_like;
create table tbl_like(
	id bigint unsigned auto_increment primary key,
	sender_id bigint unsigned not null,
	receiver_id bigint unsigned not null,
	constraint fk_like_sender_member foreign key(sender_id)
	references tbl_member(id),
	constraint fk_like_receiver_member foreign key(receiver_id)
	references tbl_member(id)
);

/*회원 3명 추가*/
insert into tbl_member
(member_email, member_name)
values
('test1234@gmail.com', '홍길동'), 
('test5555@naver.com', '이순신'), 
('test7777@test.com', '장보고');

/*1번 -> 2번 좋아요*/
/*1번 -> 3번 좋아요*/
/*2번 -> 1번 좋아요*/
insert into tbl_like(sender_id, receiver_id)
values(1, 2), (1, 3), (2, 1);

/*이름이 '홍길동'인 회원을 좋아요한 회원의 이름 조회*/
select m1.member_name sender_name
from tbl_member m1 join tbl_like l
on m1.id = l.sender_id
join tbl_member m2
on m2.id = l.receiver_id
where m2.member_name = '홍길동';

select member_name from tbl_member
where id = (
	select sender_id from tbl_like
	where receiver_id = 
	(
		select id from tbl_member
		where member_name = '홍길동'
	)
);
/******************************************************************************/
create table tbl_owner(
	id bigint unsigned auto_increment primary key,
	owner_name varchar(255) not null,
	owner_age int,
	owner_phone varchar(255) not null,
	owner_address varchar(255) not null,
	owner_address_detail varchar(255) not null
);

create table tbl_pet(
	id bigint unsigned auto_increment primary key,
	pet_ill_name varchar(255) not null,
	pet_name varchar(255) not null,
	pet_age int,
	pet_weight decimal(4, 2) not null,
	owner_id bigint unsigned,
	constraint fk_pet_owner foreign key(owner_id)
	references tbl_owner(id)
);
select * from tbl_owner;

insert into tbl_owner
(owner_name, owner_age, owner_phone, owner_address, owner_address_detail)
values
('한동석', 20, '01012341234', '경기도', '12345'),
('홍길동', 37, '01078784585', '서울', '33322'),
('이순신', 50, '01041812318', '대구', '54322'),
('정보성', 10, '01077745558', '서울', '74512');

insert into tbl_pet
(pet_ill_name, pet_name, pet_age, pet_weight, owner_id)
values
('장염', '뽀삐', 4, 10.45, 8),
('감기', '달구', 12, 14.25, 9),
('탈골', '댕댕', 7, 8.46, 10),
('염좌', '쿠키', 11, 5.81, 10),
('충치', '바둑', 1, 3.47, 8);

select * from tbl_pet p1
join 
(
	select pet_ill_name, max(pet_weight) max_weight 
	from tbl_pet
	group by pet_ill_name 
) p2
on p1.pet_weight = p2.max_weight
join tbl_owner o
on o.id = p1.owner_id;


/*외부 조인*/
select o.owner_name, p.pet_name
from tbl_owner o left outer join tbl_pet p
on o.id = p.owner_id
order by owner_name desc;








