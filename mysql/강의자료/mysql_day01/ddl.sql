create database ddl;
use ddl;

/*
 * 회원 테이블
 * 
 * 회원 번호
 * 회원 이메일
 * 회원 비밀번호
 * 회원 나이
 * 
 * */

create table tbl_member(
	id bigint primary key,
	member_email varchar(255),
	member_password varchar(255),
	member_age int
);

/*
 * 동물원 테이블
 * 
 * 고유 번호
 * 동물원 이름
 * 동물원 주소
 * 동물원 상세 주소
 * 동물 최대 수용치
 * */

create table tbl_zoo(
	id bigint primary key,
	zoo_name varchar(255) not null,
	zoo_address varchar(255) not null,
	zoo_address_detail varchar(255) not null,
	zoo_max_animal int check(zoo_max_animal > 0)
);

/*
 * 동물 테이블
 * 
 * 고유 번호
 * 동물 이름
 * 동물 종류
 * 동물 나이
 * 동물 키
 * 동물 몸무게
 * 
 * */
create table tbl_animal(
	id bigint primary key,
	animal_name varchar(255) not null,
	animal_type varchar(255) not null,
	animal_age int default 0,
	animal_height decimal(3, 2) check(animal_height > 0),
	animal_weight decimal(3, 2) check(animal_weight > 0),
	zoo_id bigint not null,
	constraint fk_animal_zoo foreign key(zoo_id)
	references tbl_zoo(id)
);

/*
 * 회사
 * 번호
 * 회사 이름
 * 회사 주소
 * */
create table tbl_company(
	id bigint primary key,
	company_name varchar(255),
	company_address varchar(255)
);

/*
 * 직원
 * 번호
 * 이름
 * */
create table tbl_employee(
	id bigint primary key,
	employee_name varchar(255),
	company_id bigint not null,
	constraint fk_employee_company foreign key(company_id)
	references tbl_company(id)
);

/*tbl_member
-------------------------------------------------
id: bigint unsigned primary key
-------------------------------------------------
member_email: varchar(255) unique not null
member_password varchar(255) not null*/

create table tbl_member(
	id bigint unsigned primary key,
	member_email varchar(255) unique not null,
	member_password varchar(255) not null
);

create table tbl_product(
	id bigint unsigned primary key,
	product_name varchar(255) not null,
	product_price int default 0,
	product_stock int default 0
);

create table tbl_order(
	id bigint unsigned primary key,
	order_date datetime default current_timestamp(),
	member_id bigint unsigned not null,
	product_id bigint unsigned not null,
	constraint fk_order_member foreign key(member_id)
	references tbl_member(id),
	constraint fk_order_product foreign key(product_id)
	references tbl_product(id)
);

/*
 * 1. 요구사항 분석
 * 		꽃 테이블과 화분 테이블 2개가 필요하고,
 *  	꽃을 구매할 때 화분도 같이 구매합니다.
 *  	꽃은 이름과 색상, 가격이 있고
 *  	화분은 제품번호, 색상, 모양이 있습니다.
 * 		화분은 모든 꽃을 담을 수 없고 정해진 꽃을 담아야 합니다.
 */

/*create table tbl_flower(
	id bigint unsigned primary key,
	flower_name varchar(255) not null,
	flower_color varchar(255) not null,
	flower_price int default 0
);

create table tbl_pot(
	id bigint unsigned primary key,
	pot_color varchar(255) not null,
	pot_shape varchar(255) not null,
	flower_id bigint unsigned not null,
	constraint fk_pot_flower foreign key(flower_id)
	references tbl_flower(id)
);*/


create table tbl_flower(
	id bigint unsigned primary key,
	flower_name varchar(255) not null,
	flower_color varchar(255) not null,
	flower_price int default 0
);

create table tbl_pot(
	id bigint unsigned primary key,
	pot_color varchar(255) not null,
	pot_shape varchar(255) not null
);

create table tbl_flower_pot(
	id bigint unsigned primary key,
	flower_id bigint unsigned not null,
	pot_id bigint unsigned not null,
	constraint fk_flower_pot_flower foreign key(flower_id)
	references tbl_flower(id),
	constraint fk_flower_pot_pot foreign key(pot_id)
	references tbl_pot(id)
);

/*
 * 1. 요구사항 분석
 * 	안녕하세요, 동물병원을 곧 개원하는 원장입니다.
 * 	동물은 보호자랑 항상 같이 옵니다. 가끔 보호소에서 오는 동물도 있습니다.
 * 	보호자가 여러 마리의 동물을 데리고 올 수 있습니다.
 * 	보호자는 이름, 나이, 전화번호, 주소 정보를 알려줘야 하고
 * 	동물은 병명, 이름, 나이, 몸무게 정보가 필요합니다.
 * 
 */

create table tbl_owner(
	id bigint unsigned primary key,
	owner_name varchar(255) not null,
	owner_age int,
	owner_phone varchar(255) not null,
	owner_address varchar(255) not null,
	owner_address_detail varchar(255) not null
);

create table tbl_pet(
	id bigint unsigned primary key,
	pet_ill_name varchar(255) not null,
	pet_name varchar(255) not null,
	pet_age int,
	pet_weight decimal(3, 2) not null,
	owner_id bigint unsigned,
	constraint fk_pet_owner foreign key(owner_id)
	references tbl_owner(id)
);

/*
1. 요구 사항
    커뮤니티 게시판을 만들고 싶어요.
    게시판에는 게시글 제목과 게시글 내용, 작성한 시간, 작성자가 있고,
    게시글에는 댓글이 있어서 댓글 내용들이 나와야 해요.
    작성자는 번호, 이메일, 이름이 있다.
    댓글에도 작성자가 필요해요.
*/


















