create database tcl;
use tcl;

create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_name varchar(255) not null,
	member_age int default 0
);

select * from tbl_member;

insert into tbl_member(member_name, member_age)
values('한동석', 20);

rollback;
commit;

drop table tbl_member;




