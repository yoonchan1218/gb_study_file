use jsp;
create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_email varchar(255) unique not null,
	member_password varchar(255) not null,
	member_name varchar(255) not null,
	member_age int default 0,
	member_gender varchar(255) default '선택안함',
	created_datetime datetime default current_timestamp(),
	updated_datetime datetime default current_timestamp()
);

select * from tbl_member;